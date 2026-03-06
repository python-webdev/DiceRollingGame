from typing import TypedDict


class HistoryRecord(TypedDict, total=False):
    time: str
    mode: str
    dice: int
    dice_type: str
    sides: int
    rolls: object
    total: int
    match: bool | int
    outcome: str
    points_delta: int
    points_total: int
