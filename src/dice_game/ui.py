from dice_game.dice import dice_types
from dice_game.rules import modes


def ask_yes_no(prompt: str) -> str:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "n"):
            return ans
        print("\nInvalid input. Please enter 'y' or 'n'.\n")


def ask_int(prompt: str, *, min_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")
            continue

        if min_value is not None and value < min_value:
            print(f"\nValue must be at least {min_value}. Please try again.\n")
            continue

        return value


def choose_mode() -> str:
    while True:
        mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
        if mode in modes:
            return mode
        print("\nInvalid mode. Please select Classic, Lucky, or Risk.\n")


def choose_dice_sides() -> int:
    prompt = "Choose a dice type (D4, D6, D8, D10, D12, D20): "
    while True:
        dice_type = input(prompt).strip().upper()
        if dice_type in dice_types:
            return dice_types[dice_type]
        print("\nInvalid dice type. Please select a valid dice type.\n")


def format_rolls(rolls: list[int]) -> str:
    return ", ".join(map(str, rolls))
