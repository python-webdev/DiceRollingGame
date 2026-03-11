from typing import TypedDict


class HistoryRecord(TypedDict):
    game_session_id: str
    time: str
    mode: str
    dice: int
    dice_type: str
    sides: int
    rolls: list[int]
    total: int
    has_match: int
    outcome: str
    points_delta: int
    points_total: int


class DatabaseRecord(HistoryRecord):
    id: int
