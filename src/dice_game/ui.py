from .constants import DICE_TYPES, MIN_DICE
from .modes import GameMode
from .models import RollContext


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
            print(
                f"\nDice count must be at least {min_value}. Please try again.\n")
            continue

        return value


def ask_simulation_trials() -> int:
    print("\nSimulation trials options:")
    print("1) 10,000")
    print("2) 100,000")
    print("3) Custom\n")

    while True:
        choice = input("Choose (1-3): ").strip()
        if choice == "1":
            return 10_000
        if choice == "2":
            return 100_000
        if choice == "3":
            return ask_int("Enter trials: ", min_value=1)
        print("\nInvalid choice.\n")


def choose_mode() -> GameMode:
    while True:
        mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
        try:
            return GameMode[mode.upper()]
        except KeyError:
            print("\nInvalid mode. Please select a valid mode.\n")


def choose_dice_type() -> str:
    prompt = "Choose a dice type (D4, D6, D8, D10, D12, D20): "
    while True:
        dice_type = input(prompt).strip().upper()
        if dice_type in DICE_TYPES:
            return dice_type
        print("\nInvalid dice type. Please select a valid dice type.\n")


def get_roll_context():
    # local import avoids circular imports

    num_dice = ask_int(
        "How many dice would you like to roll? ", min_value=MIN_DICE)
    mode = choose_mode()
    dice_type = choose_dice_type()
    sides = DICE_TYPES[dice_type]
    return RollContext(mode=mode, dice_type=dice_type, num_dice=num_dice, sides=sides)


# -------- Menu Asking --------
def ask_menu_action() -> str:
    """
    r = roll
    h = history
    s = simulation
    q = quit
    """
    while True:
        ans = input("(r)oll, (h)istory, (s)imulate, (q)uit: ").strip().lower()
        if ans in ("r", "h", "s", "q"):
            return ans
        print("\nInvalid choice. Enter r, h, s, or q.\n")
