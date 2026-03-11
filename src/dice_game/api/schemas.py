from pydantic import BaseModel, Field


class RollRequest(BaseModel):
    mode: str
    dice_type: str
    num_dice: int = Field(ge=2)
