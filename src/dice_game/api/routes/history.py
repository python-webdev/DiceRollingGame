from fastapi import APIRouter, HTTPException

from ...storage.sqlite_storage import (
    clear_rolls,
    export_rolls_to_csv,
    paginated_rolls,
)

router = APIRouter()


@router.get("/history")
def get_history(limit: int = 10, offset: int = 0):
    rows = paginated_rolls(limit=limit, offset=offset)
    return rows


@router.delete("/history")
def delete_history():
    deleted = clear_rolls(reset_ids=True)
    return {"deleted_records": deleted}


@router.get("/history/export")
def export_history():
    exported = export_rolls_to_csv()

    if exported == 0:
        raise HTTPException(status_code=404, detail="No rolls to export")

    return {
        "message": f"Exported {exported} rolls to CSV file",
        "records": exported,
        "file": "roll_history.csv",
    }
