import random

dice_types = {
    "D4": 4,
    "D6": 6,
    "D8": 8,
    "D10": 10,
    "D12": 12,
    "D20": 20
}
game_modes = {"classic", "lucky", "risk"}
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
            print(
                f"\nDice count must be at least {min_value}. Please try again.\n")
            continue

        return value


def choose_mode() -> str:
    while True:
        mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
        if mode in game_modes:
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


def outcome_from_total(total: int, num_dice: int, sides: int) -> str:
    """
    Scalable outcome based on % of max total.
    win  >= 75% of max
    draw >= 60% of max
    lose <  60% of max
    """
    max_total = num_dice * sides
    # ceil without importing math
    win_cutoff = int(max_total * 0.75 + 0.999999)
    draw_cutoff = int(max_total * 0.60 + 0.999999)  # ceil

    if total >= win_cutoff:
        return "win"
    if total >= draw_cutoff:
        return "draw"
    return "lose"


def apply_points(mode: str, total: int, has_match: bool, num_dice: int, sides: int) -> int:
    """
    Points are balanced across different dice sizes using % of max total.

    Base points:
      win  => +5
      draw =>  0
      lose => -3

    Lucky:
      if all dice match => +10 (bonus) and extra turn (handled in main)

    Risk:
      if total < 35% of max => -3 (risk penalty)
    """
    max_total = num_dice * sides
    risk_cutoff = int(max_total * 0.35)  # floor is fine for penalty threshold

    # Lucky bonus overrides normal scoring
    if mode == "lucky" and has_match:
        return 10

    # Risk penalty overrides normal scoring when really low
    if mode == "risk" and total < risk_cutoff:
        return -3

    out = outcome_from_total(total, num_dice, sides)
    if out == "win":
        return 5
    if out == "lose":
        return -3
    return 0


def get_outcome_message(mode: str, total: int, has_match: bool, num_dice: int, sides: int) -> str:
    max_total = num_dice * sides
    risk_cutoff = int(max_total * 0.35)

    if mode == "lucky" and has_match:
        return "(All dice match! +10 points and extra turn!)"

    if mode == "risk" and total < risk_cutoff:
        return "(Risk penalty! -3 points!)"

    out = outcome_from_total(total, num_dice, sides)
    if out == "win":
        return "(Congratulations! You win!)"
    if out == "draw":
        return "(It's a draw! Try again!)"
    return "(Sorry, you lose!)"


def print_turn_result(rolls: list[int], total: int, points_delta: int, points_total: int, message: str) -> None:
    rolled_numbers = ", ".join(map(str, rolls))
    print(f"\n🎲 You rolled: {rolled_numbers} {message}")

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
    print(f"Lowest roll: {stats['lowest_roll']}")
    print(f"Player points: {stats['player_points']}\n")


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
        delta = apply_points(mode, total, has_match, num_dice, sides)
        player_points += delta
        stats["player_points"] = player_points

        # lucky doubles => extra turn, but still counts as a completed roll in your current design
        # If you want it NOT to count, move update_stats below the "continue".
        update_stats(stats, total, has_match)

        msg = get_outcome_message(mode, total, has_match, num_dice, sides)
        print_turn_result(rolls, total, delta, player_points, msg)
        print_stats(stats)

        # Lucky mode: doubles => extra turn immediately
        if mode == "lucky" and has_match:
            continue


if __name__ == "__main__":
    main()
