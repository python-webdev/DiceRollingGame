from fastapi import APIRouter, HTTPException

from ...domain.constants import DICE_TYPES
from ...domain.models import RollContext
from ...domain.modes import GameMode
from ...services.logic import (
    apply_turn_effects,
    build_temp_result,
    finalize_result,
    resolve_turn,
    roll_dice,
)
from ...storage.sqlite_storage import save_roll
from ..schemas import RollRequest
from ..state import state

router = APIRouter()


@router.post("/roll")
def roll(request: RollRequest):
    if request.dice_type not in DICE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid dice type")

    try:
        mode = GameMode[request.mode.upper()]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Invalid game mode") from exc

    sides = DICE_TYPES[request.dice_type]

    context = RollContext(
        mode=mode,
        dice_type=request.dice_type,
        num_dice=request.num_dice,
        sides=sides,
    )

    rolls = roll_dice(context)
    temp_result = build_temp_result(context, rolls, state.player_points)
    outcome, delta = resolve_turn(state.game_config, temp_result)
    extra_turn = apply_turn_effects(state, temp_result, delta)
    result = finalize_result(temp_result, outcome, delta, state.player_points)

    save_roll(result)

    return {
        "rolls": result.rolls,
        "total": result.total,
        "outcome": result.outcome,
        "points_delta": result.points_delta,
        "points_total": result.points_total,
        "extra_turn": extra_turn,
    }
