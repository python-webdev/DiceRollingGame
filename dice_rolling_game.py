import random

# Step 1: Track how many completed rolls the player has made.
# Step 2: Keep the game running in a while loop until the player chooses to quit.
# Step 3: Ask if the player wants to roll or stop.
# Step 4: Ask how many dice to roll.
# Step 5: Validate that dice count is a valid number.
# Step 6: Enforce a minimum of 2 dice.
# Step 7: Roll each die, compute total, and format output text.
# Step 8: Check for doubles (all dice matching) for an extra turn.
# Step 9: Determine win/lose/draw from total score.
# Step 10: Show score, update completed roll count, and report progress.
# Step 11: Exit the game loop when player chooses to stop.
# Step 12: Handle invalid main-menu input.
# Step 13: Add Modes (Classic (normal dice), Lucky (win or doubles), Risk (if total < 7 lose points)))
# Step 14: Add Player Points to track score across rounds (e.g +10 for points double, +5 if total > 8, -3 if total < 5)
# Step 15: Add Statistics (total rolls, total doubles, average roll value, highest roll, lowest roll)
# Step 16: Add dice types (e.g. D4, D6, D8, D10, D12, D20) and allow player to choose which type of dice to roll.

dice_types = {
    'D4': 4,
    'D6': 6,
    'D8': 8,
    'D10': 10,
    'D12': 12,
    'D20': 20
}
modes = {'classic', 'lucky', 'risk'}
min_dice = 2


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
        print("\nInvalid mode. Please select a valid mode.\n")


def choose_dice_sides() -> int:
    prompt = "Choose a dice type (D4, D6, D8, D10, D12, D20): "
    while True:
        dice_type = input(prompt).strip().upper()
        if dice_type in dice_types:
            return dice_types[dice_type]
        print("\nInvalid dice type. Please select a valid dice type.\n")


def roll_dice(num_dice: int, sides: int) -> list[int]:
    return [random.randint(1, sides) for _ in range(num_dice)]


def all_match(rolls: list[int]) -> bool:
    return len(set(rolls)) == 1


def outcome_from_total(total: int) -> str:
    """Return 'win', 'draw', or 'lose' based on your rule."""
    if total > 10:
        return "win"
    if total == 10:
        return "draw"
    return "lose"


def apply_points(mode: str, total: int, has_match: bool) -> int:
    """
    Returns point delta for this turn.
    Your rules:
    +10 for doubles (lucky mode extra turn)
    +5 if total > 8 (we'll interpret as win condition in your current code: total > 10 -> +5)
    -3 if total < 5 / losing / risky (<7)
    """
    if mode == "lucky" and has_match:
        return 10

    if mode == "risk" and total < 7:
        return -3

    # In your current code: win => +5, lose => -3, draw => 0
    out = outcome_from_total(total)
    if out == "win":
        return 5
    if out == "lose":
        return -3
    return 0


def print_turn_result(mode: str, rolls: list[int], total: int, has_match: bool, points_delta: int, points_total: int) -> None:
    rolled_numbers = ", ".join(map(str, rolls))

    if mode == "lucky" and has_match:
        print(
            f"\nYou rolled: {rolled_numbers} (Doubles! You get an extra turn!)")
        print(f"Points +{points_delta}. Your current points: {points_total}\n")
        return

    out = outcome_from_total(total)
    if mode == "risk" and total < 7:
        print(f"\nYou rolled: {rolled_numbers} (Risky! You lose points!)")
    elif out == "win":
        print(f"\nYou rolled: {rolled_numbers} (Congratulations! You win!)")
    elif out == "draw":
        print(f"\nYou rolled: {rolled_numbers} (It's a draw! Try again!)")
    else:
        print(f"\nYou rolled: {rolled_numbers} (Sorry, you lose!)")

    if points_delta > 0:
        print(f"Points +{points_delta}. Your current points: {points_total}")
    elif points_delta < 0:
        print(f"Points {points_delta}. Your current points: {points_total}")
    else:
        print(f"Your current points: {points_total}")

    print(f"Total score: {total}")


def update_stats(stats: dict, total: int, has_match: bool) -> None:
    stats["roll_count"] += 1
    stats["total_roll_value"] += total
    stats["highest_roll"] = max(stats["highest_roll"], total)
    stats["lowest_roll"] = min(stats["lowest_roll"], total)
    if has_match:
        stats["total_doubles"] += 1


def print_stats(stats: dict) -> None:
    rc = stats["roll_count"]
    if rc == 0:
        return

    average = stats["total_roll_value"] / rc
    print(f"You have rolled the dice {rc} times.\n")
    print(f"Average roll value: {average:.2f}")
    print(f"Total doubles rolled: {stats['total_doubles']}")
    print(f"Highest roll: {stats['highest_roll']}")
    print(f"Lowest roll: {stats['lowest_roll']}\n")


def main() -> None:
    player_points = 0
    stats = {
        "roll_count": 0,
        "player_points": 0,
        "total_doubles": 0,
        "total_roll_value": 0,
        "highest_roll": 0,
        "lowest_roll": float("inf"),
    }

    while True:
        user_input = ask_yes_no("Roll the dice? (y/n): ")
        if user_input == "n":
            print("\nThank you for playing! Goodbye!")
            # final stats
            print_stats(stats)
            break

        num_dice = ask_int(
            "How many dice would you like to roll? ", min_value=min_dice)
        mode = choose_mode()
        sides = choose_dice_sides()

        rolls = roll_dice(num_dice, sides)
        total = sum(rolls)
        has_match = all_match(rolls)

        # points
        delta = apply_points(mode, total, has_match)
        player_points += delta
        stats["player_points"] = player_points

        # lucky doubles => extra turn, but still counts as a completed roll in your current design
        # If you want it NOT to count, move update_stats below the "continue".
        update_stats(stats, total, has_match)

        print_turn_result(mode, rolls, total, has_match, delta, player_points)
        print_stats(stats)

        # Lucky mode: doubles => extra turn immediately
        if mode == "lucky" and has_match:
            continue


if __name__ == "__main__":
    main()
