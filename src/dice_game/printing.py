from .stats import Stats
from .models import RollResult


def print_turn_result(result: RollResult) -> None:
    rolled_numbers = ", ".join(map(str, result.rolls))
    print(f"\n🎲 You rolled: {rolled_numbers}")
    print(
        f"Dice: {result.context.num_dice} × {result.context.dice_type} (Total: {result.total})")

    if result.has_match:
        label = "DOUBLES" if result.context.num_dice == 2 else "ALL MATCH"
        print(f"Match: {label} 🏆")
    else:
        print("Match: No")

    print(f"Outcome: {result.outcome.upper()}")

    if result.points_delta > 0:
        print(f"Points: +{result.points_delta}")
    elif result.points_delta < 0:
        print(f"Points: {result.points_delta}")
    else:
        print("Points: 0")


def print_stats(stats: Stats, points_total: int) -> None:
    if stats.roll_count == 0:
        print("No rolls yet.\n")
        return

    lowest = stats.lowest_total if stats.lowest_total is not None else "-"
    lines = [
        "\n---- Stats ----",
        f"Completed rolls: {stats.roll_count}",
        f"Total points: {points_total}",
        f"Average total: {stats.average_total:.2f}",
        f"Total matches: {stats.total_matches}",
        f"Highest total: {stats.highest_total}",
        f"Lowest total: {lowest}",
        "----------------",
    ]
    print("\n".join(lines))
    print()
