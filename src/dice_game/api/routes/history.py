from fastapi import APIRouter, HTTPException, Query

from ...storage.roll_repository import (
    clear_rolls_by_session,
    export_rolls_to_csv_by_session,
    paginated_rolls_by_session,
)
from ...storage.session_repository import get_game_session, reset_game_session_points
from ..schemas import DeleteHistoryResponse, ExportHistoryResponse, HistoryItemResponse

router = APIRouter(prefix="/sessions", tags=["history"])


@router.get("/{game_session_id}/history", response_model=list[HistoryItemResponse])
def get_history(
    game_session_id: str,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    session = get_game_session(game_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found")

    return paginated_rolls_by_session(
        game_session_id,
        limit=limit,
        offset=offset,
    )


@router.delete("/{game_session_id}/history", response_model=DeleteHistoryResponse)
def delete_history(game_session_id: str):
    session = get_game_session(game_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found")

    deleted = clear_rolls_by_session(game_session_id)
    reset_game_session_points(game_session_id)

    return DeleteHistoryResponse(
        deleted_records=deleted,
        player_points=0,
    )


@router.get("/{game_session_id}/history/export", response_model=ExportHistoryResponse)
def export_history(game_session_id: str):
    session = get_game_session(game_session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found")

    exported = export_rolls_to_csv_by_session(game_session_id)

    if exported == 0:
        raise HTTPException(status_code=404, detail="No rolls to export")

    return ExportHistoryResponse(
        message=f"Exported {exported} rolls to CSV file",
        records=exported,
        file=f"roll_history_{game_session_id}.csv",
    )
