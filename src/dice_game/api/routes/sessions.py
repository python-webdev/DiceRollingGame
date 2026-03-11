from fastapi import APIRouter, HTTPException

from ...storage.sqlite_storage import (
    create_game_session,
    delete_game_session,
    get_game_session,
)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("")
def create_session():
    session = create_game_session()
    return {
        "game_session_id": session["id"],
        "player_points": session["player_points"],
        "status": session["status"],
        "created_at": session["created_at"],
        "updated_at": session["updated_at"],
    }


@router.get("/{game_session_id}")
def get_session(game_session_id: str):
    session = get_game_session(game_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found")

    return {
        "game_session_id": session["id"],
        "player_points": session["player_points"],
        "status": session["status"],
        "created_at": session["created_at"],
        "updated_at": session["updated_at"],
    }


@router.delete("/{game_session_id}")
def delete_session(game_session_id: str):
    deleted = delete_game_session(game_session_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Game session not found")

    return {"deleted": True}
