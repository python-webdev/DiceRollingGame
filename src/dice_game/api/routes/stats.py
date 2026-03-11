from fastapi import APIRouter, HTTPException

from ...storage.sqlite_storage import get_game_session, session_stats

router = APIRouter(prefix="/sessions", tags=["stats"])


@router.get("/{game_session_id}/stats")
def get_stats(game_session_id: str):
    session = get_game_session(game_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found")

    stats = session_stats(game_session_id)

    return {
        "game_session_id": game_session_id,
        "player_points": session["player_points"],
        **stats,
    }
