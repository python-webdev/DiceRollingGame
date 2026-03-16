from fastapi import APIRouter, HTTPException, Query

from ...services.exceptions import (
    GameSessionNotFoundError,
    HistoryExportError,
)
from ...services.history_service import clear_session_history
from ...storage.roll_repository import (
    export_rolls_to_csv_by_session,
    paginated_rolls_by_session,
)
from ...storage.session_repository import get_game_session
from ..schemas import DeleteHistoryResponse, ExportHistoryResponse, HistoryItemResponse

router = APIRouter(prefix="/sessions", tags=["history"])


@router.get("/{game_session_id}/history", response_model=list[HistoryItemResponse])
def get_history(
    game_session_id: str,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    session = get_game_session(game_session_id)
    try:
        if session is None:
            raise GameSessionNotFoundError("Game session not found")
    except GameSessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return paginated_rolls_by_session(
        game_session_id,
        limit=limit,
        offset=offset,
    )


@router.delete("/{game_session_id}/history", response_model=DeleteHistoryResponse)
def delete_history(game_session_id: str):
    try:
        result = clear_session_history(game_session_id)
        return result
    except GameSessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/{game_session_id}/history/export", response_model=ExportHistoryResponse)
def export_history(game_session_id: str):
    session = get_game_session(game_session_id)
    try:
        if session is None:
            raise GameSessionNotFoundError("Game session not found")
    except GameSessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    exported = export_rolls_to_csv_by_session(game_session_id)

    try:
        if exported == 0:
            raise HistoryExportError("No rolls to export")
    except HistoryExportError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return ExportHistoryResponse(
        message=f"Exported {exported} rolls to CSV file",
        records=exported,
        file=f"roll_history_{game_session_id}.csv",
    )
