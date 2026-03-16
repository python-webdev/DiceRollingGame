from fastapi import APIRouter, HTTPException

from ...services.exceptions import GameSessionNotFoundError
from ...storage.roll_repository import session_stats
from ...storage.session_repository import get_game_session
from ..schemas import StatsResponse

router = APIRouter(prefix="/sessions", tags=["stats"])


@router.get("/{game_session_id}/stats", response_model=StatsResponse)
def get_stats(game_session_id: str):
    session = get_game_session(game_session_id)
    try:
        if session is None:
            raise GameSessionNotFoundError("Game session not found")
    except GameSessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    stats = session_stats(game_session_id)

    return StatsResponse(
        game_session_id=game_session_id,
        player_points=session["player_points"],
        **stats,
    )
