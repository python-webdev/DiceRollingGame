from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...storage.sqlite_storage import (
    create_game_session,
    delete_game_session,
    get_game_session,
)

router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionResponse(BaseModel):
    game_session_id: str
    player_points: int
    status: str
    created_at: str
    updated_at: str


@router.post("", response_model=SessionResponse)
def create_session():
    session = create_game_session()
    return SessionResponse(
        game_session_id=session["id"],
        player_points=session["player_points"],
        status=session["status"],
        created_at=session["created_at"],
        updated_at=session["updated_at"],
    )


@router.get("/{game_session_id}", response_model=SessionResponse)
def get_session(game_session_id: str):
    session = get_game_session(game_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found")

    return SessionResponse(
        game_session_id=session["id"],
        player_points=session["player_points"],
        status=session["status"],
        created_at=session["created_at"],
        updated_at=session["updated_at"],
    )


@router.delete("/{game_session_id}")
def delete_session(game_session_id: str):
    deleted = delete_game_session(game_session_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Game session not found")

    return {"deleted": True}
