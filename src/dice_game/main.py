from dice_game.dice import roll_dice, all_match
from dice_game.rules import outcome_from_total, apply_points
from dice_game.stats import Stats
from dice_game.ui import ask_yes_no, ask_int, choose_mode, choose_dice_sides, format_rolls

min_dice = 2


def print_turn(mode: str, rolls: list[int], total: int, has_match: bool, delta: int, points: int) -> None:
    rolled_numbers = format_rolls(rolls)

    # Lucky doubles message (special)
    if mode == "lucky" and has_match:
        print(
            f"\nYou rolled: {rolled_numbers} (Doubles! You get an extra turn!)")
        print(f"Points +{delta}. Your current points: {points}")
        print(f"Total score: {total}\n")
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

    if delta > 0:
        print(f"Points +{delta}. Your current points: {points}")
    elif delta < 0:
        print(f"Points {delta}. Your current points: {points}")
    else:
        print(f"Your current points: {points}")

    print(f"Total score: {total}\n")


def main() -> None:
    stats = Stats()
    player_points = 0

    while True:
        choice = ask_yes_no("Roll the dice? (y/n): ")
        if choice == "n":
            print("\nThank you for playing! Goodbye!\n")
            for line in stats.summary_lines():
                print(line)
            print(f"Final points: {player_points}\n")
            break

        num_dice = ask_int(
            "How many dice would you like to roll? ", min_value=min_dice)
        mode = choose_mode()
        sides = choose_dice_sides()

        rolls = roll_dice(num_dice, sides)
        total = sum(rolls)
        has_match = all_match(rolls)

        delta = apply_points(mode, total, has_match)
        player_points += delta

        # If you want "extra turn" NOT to count as a roll, move stats.update below the continue.
        stats.update(total, has_match)

        print_turn(mode, rolls, total, has_match, delta, player_points)

        for line in stats.summary_lines():
            print(line)
        print(f"Current points: {player_points}\n")

        if mode == "lucky" and has_match:
            continue


if __name__ == "__main__":
    main()
