from typing import Any
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


def print_history(records: list[dict[str, Any]]) -> None:
    if not records:
        print("\nNo history records found.\n")
        return

    print("\n---- History ----")
    for r in records:
        time = r.get("time", "?")
        mode = r.get("mode", "?")
        dice_type = r.get("dice_type", "?")
        dice = r.get("dice", "?")
        total = r.get("total", "?")
        rolls = r.get("rolls", [])
        print(f"{time} | {mode:<6} | {dice}×{dice_type} | rolls={rolls} | total={total}")
    print("-----------------\n")


def print_best_roll(record: dict[str, Any] | None) -> None:
    if record is None:
        print("\nNo history yet, so no best roll.\n")
        return
    print("\n---- Best Roll Ever ----")
    print(f"Time: {record.get('time')}")
    print(f"Mode: {record.get('mode')}")
    print(f"Dice: {record.get('dice')}×{record.get('dice_type')}")
    print(f"Rolls: {record.get('rolls')}  Total: {record.get('total')}")
    print(f"Points total after roll: {record.get('points_total')}")
    print("------------------------\n")
