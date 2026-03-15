from fastapi import APIRouter, HTTPException

from ...domain.config import GameConfig
from ...domain.constants import DICE_TYPES
from ...domain.models import RollContext, TurnState
from ...domain.modes import GameMode
from ...domain.stats import Stats
from ...services.logic import (
    apply_turn_effects,
    build_temp_result,
    finalize_result,
    resolve_turn,
    roll_dice,
)
from ...storage.sqlite_storage import (
    get_game_session,
    save_roll,
    update_game_session_points,
)
from ..schemas import RollRequest, RollResponse

router = APIRouter(prefix="/sessions", tags=["roll"])


@router.post("/{game_session_id}/roll", response_model=RollResponse)
def roll(game_session_id: str, request: RollRequest):
    session = get_game_session(game_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found")

    if request.dice_type not in DICE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid dice type")

    try:
        mode = GameMode[request.mode.upper()]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Invalid game mode") from exc

    context = RollContext(
        game_session_id=game_session_id,
        mode=mode,
        dice_type=request.dice_type,
        num_dice=request.num_dice,
        sides=DICE_TYPES[request.dice_type],
    )

    state = TurnState(
        game_session_id=game_session_id,
        game_config=GameConfig(),
        stats=Stats(),
        player_points=session["player_points"],
    )

    rolls = roll_dice(context)
    temp_result = build_temp_result(context, rolls, state.player_points)
    outcome, delta = resolve_turn(state.game_config, temp_result)
    extra_turn = apply_turn_effects(state, temp_result, delta)
    result = finalize_result(temp_result, outcome, delta, state.player_points)

    update_game_session_points(game_session_id, result.points_total)
    save_roll(result)

    return RollResponse(
        game_session_id=game_session_id,
        rolls=result.rolls,
        total=result.total,
        outcome=result.outcome,
        points_delta=result.points_delta,
        points_total=result.points_total,
        extra_turn=extra_turn,
    )
