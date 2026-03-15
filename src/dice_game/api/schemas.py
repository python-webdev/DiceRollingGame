from pydantic import BaseModel, Field


class RollRequest(BaseModel):
    mode: str
    dice_type: str
    num_dice: int = Field(ge=2)


class SessionResponse(BaseModel):
    game_session_id: str
    player_points: int
    status: str
    created_at: str
    updated_at: str


class DeleteSessionResponse(BaseModel):
    deleted: bool


class RollResponse(BaseModel):
    game_session_id: str
    rolls: list[int]
    total: int
    outcome: str
    points_delta: int
    points_total: int
    extra_turn: bool


class HistoryItemResponse(BaseModel):
    id: int
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


class DeleteHistoryResponse(BaseModel):
    deleted_records: int
    player_points: int


class ExportHistoryResponse(BaseModel):
    message: str
    records: int
    file: str


class StatsResponse(BaseModel):
    game_session_id: str
    player_points: int
    total_rolls: int
    total_roll_value: int
    highest_roll: int | None
    lowest_roll: int | None
    average_roll: float | None
    total_matches: int
