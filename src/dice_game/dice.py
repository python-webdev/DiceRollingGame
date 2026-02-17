import random

dice_types = {
    'D4': 4,
    'D6': 6,
    'D8': 8,
    'D10': 10,
    'D12': 12,
    'D20': 20
}


def roll_dice(num_dice: int, sides: int) -> list[int]:
    return [random.randint(1, sides) for _ in range(num_dice)]


def all_match(rolls: list[int]) -> bool:
    return len(set(rolls)) == 1
