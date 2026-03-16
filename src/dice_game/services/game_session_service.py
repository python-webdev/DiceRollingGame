from dice_game.api.schemas import RollResponse
from dice_game.domain.config import GameConfig
from dice_game.domain.constants import DICE_TYPES
from dice_game.domain.models import RollContext, TurnState
from dice_game.domain.modes import GameMode
from dice_game.domain.stats import Stats
from dice_game.services.logic import (
    apply_turn_effects,
    build_temp_result,
    finalize_result,
    resolve_turn,
    roll_dice,
)
from dice_game.storage.roll_repository import save_roll
from dice_game.storage.session_repository import (
    get_game_session,
    update_game_session_points,
)

from .exceptions import (
    GameSessionNotFoundError,
    InvalidDiceTypeError,
    InvalidGameModeError,
)


def play_session_turn(
    *,
    game_session_id: str,
    mode_name: str,
    dice_type: str,
    num_dice: int,
) -> RollResponse:
    session = get_game_session(game_session_id)
    if session is None:
        raise GameSessionNotFoundError("Game session not found")

    if dice_type not in DICE_TYPES:
        raise InvalidDiceTypeError("Invalid dice type")

    try:
        mode = GameMode[mode_name.upper()]
    except KeyError as exc:
        raise InvalidGameModeError("Invalid game mode") from exc

    context = RollContext(
        game_session_id=game_session_id,
        mode=mode,
        dice_type=dice_type,
        num_dice=num_dice,
        sides=DICE_TYPES[dice_type],
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
