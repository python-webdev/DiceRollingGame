from ..api.schemas import DeleteHistoryResponse
from ..storage.roll_repository import clear_rolls_by_session
from ..storage.session_repository import (
    get_game_session,
    reset_game_session_points,
)
from .exceptions import GameSessionNotFoundError


def clear_session_history(game_session_id: str) -> DeleteHistoryResponse:
    session = get_game_session(game_session_id)
    if session is None:
        raise GameSessionNotFoundError("Game session not found")

    deleted = clear_rolls_by_session(game_session_id)
    reset_game_session_points(game_session_id)

    return DeleteHistoryResponse(
        deleted_records=deleted,
        player_points=0,
    )
