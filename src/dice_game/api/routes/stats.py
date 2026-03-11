from fastapi import APIRouter

from ...storage.sqlite_storage import count_rolls

router = APIRouter()


@router.get("/stats")
def get_stats():
    total = count_rolls()
    return {"total_rolls": total}
