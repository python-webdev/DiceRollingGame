import random
from dataclasses import dataclass, field

DICE_TYPES: dict[str, int] = {
    "D4": 4,
    "D6": 6,
    "D8": 8,
    "D10": 10,
    "D12": 12,
    "D20": 20,
}


@dataclass(frozen=True)
class Dice:
    type: str = "D6"
    sides: int = field(init=False)

    def __post_init__(self):
        if self.type not in DICE_TYPES:
            raise ValueError(f"Invalid dice type: {self.type}")
        object.__setattr__(self, "sides", DICE_TYPES[self.type])

    def roll_dice(self, num_dice: int) -> list[int]:
        return [random.randint(1, self.sides) for _ in range(num_dice)]

    def all_match(self, rolls: list[int]) -> bool:
        return bool(rolls) and len(set(rolls)) == 1


dice = Dice()
