from pydantic import BaseModel


class RollRequest(BaseModel):
    mode: str
    dice_type: str
    num_dice: int
