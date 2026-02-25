from .dice import DICE_TYPES
from .rules import modes


class GameUI:
    @staticmethod
    def ask_yes_no(prompt: str) -> str:
        while True:
            ans = input(prompt).strip().lower()
            if ans in ("y", "n"):
                return ans
            print("\nInvalid input. Please enter 'y' or 'n'.\n")

    @staticmethod
    def ask_int(prompt: str, *, min_value: int | None = None) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                value = int(raw)
            except ValueError:
                print("\nInvalid input. Please enter a valid number.\n")
                continue

            if min_value is not None and value < min_value:
                print(
                    f"\nDice count must be at least {min_value}. Please try again.\n")
                continue

            return value

    @staticmethod
    def choose_mode() -> str:
        while True:
            mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
            if mode in modes:
                return mode
            print("\nInvalid mode. Please select Classic, Lucky, or Risk.\n")

    @staticmethod
    def choose_dice_sides() -> int:
        prompt = "Choose a dice type (D4, D6, D8, D10, D12, D20): "
        while True:
            dice_type = input(prompt).strip().upper()
            if dice_type in DICE_TYPES:
                return DICE_TYPES[dice_type]
            print("\nInvalid dice type. Please select a valid dice type.\n")

    @staticmethod
    def format_rolls(rolls: list[int]) -> str:
        return ", ".join(map(str, rolls))


def ask_yes_no(prompt: str) -> str:
    return GameUI.ask_yes_no(prompt)


def ask_int(prompt: str, *, min_value: int | None = None) -> int:
    return GameUI.ask_int(prompt, min_value=min_value)


def choose_mode() -> str:
    return GameUI.choose_mode()


def choose_dice_sides() -> int:
    return GameUI.choose_dice_sides()


def format_rolls(rolls: list[int]) -> str:
    return GameUI.format_rolls(rolls)
