import json

from ..domain.models import RollResult
from ..domain.stats import Stats
from ..services.simulation import SimulationReport
from ..storage.history_types import HistoryRecord


def _format_rolls(value: object) -> str:
    """
    DB stores rolls as JSON text; JSON history might store as list.
    Return a nice string in both cases.
    """
    if isinstance(value, list):
        return "[" + ", ".join(map(str, value)) + "]"

    if isinstance(value, str):
        # try decode JSON string like "[1,2,3]"
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return "[" + ", ".join(map(str, parsed)) + "]"
        except json.JSONDecodeError:
            pass
        # fallback: raw string
        return value

    return str(value)


def print_turn_result(result: RollResult) -> None:
    rolled_numbers = ", ".join(map(str, result.rolls))
    print(f"\n🎲 You rolled: {rolled_numbers}")
    print(
        f"Dice: {result.context.num_dice} × {result.context.dice_type} (Total: {result.total})"
    )

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


def print_session_stats(stats: Stats, points_total: int) -> None:
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


def print_history(records: list[HistoryRecord]) -> None:
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
        rolls = _format_rolls(r.get("rolls", []))
        print(
            f"{time} | {mode:<6} | {dice}×{dice_type} | rolls={rolls} | total={total}"
        )
    print("-----------------\n")


def print_best_roll(record: HistoryRecord | None) -> None:
    if record is None:
        print("\nNo history yet, so no best roll.\n")
        return
    print("\n---- Best Roll Ever ----")
    print(f"Time: {record.get('time')}")
    print(f"Mode: {record.get('mode')}")
    print(f"Dice: {record.get('dice')}×{record.get('dice_type')}")
    print(f"Rolls: {_format_rolls(record.get('rolls'))}  Total: {record.get('total')}")
    print(f"Points total after roll: {record.get('points_total')}")
    print("------------------------\n")


def print_simulation_report(
    report: SimulationReport, *, top_n_totals: int = 10
) -> None:
    trials = report.config.trials
    if trials == 0:
        print("\nSimulation: No trials were run, so no report to show.\n")
        return

    win = report.counts.outcome_counts.get("win", 0)
    draw = report.counts.outcome_counts.get("draw", 0)
    lose = report.counts.outcome_counts.get("lose", 0)

    print("\n----- Simulation Report -----")
    print(f"Trials: {trials}")
    print(f"Dice: {report.config.dice} × D{report.config.sides}")
    print(f"Match count: {report.counts.match_count}")
    print(
        f"Match probability: {report.match_probability:.4f} ({report.match_probability * 100:.2f}%)"
    )
    print()

    print("Outcomes:")
    print(f"  WIN : {win} ({win / trials * 100:.2f}%)")
    print(f"  DRAW: {draw} ({draw / trials * 100:.2f}%)")
    print(f"  LOSE: {lose} ({lose / trials * 100:.2f}%)")
    print()

    print(f"Average total: {report.averages.avg_total:.2f}")
    print(f"Average points delta: {report.averages.avg_points_delta:.2f}")
    print()

    items = sorted(
        report.counts.total_distribution.items(),
        key=lambda kv: kv[1],
        reverse=True,
    )

    print(f"Top {min(top_n_totals, len(items))} totals by frequency:")
    for total, freq in items[:top_n_totals]:
        print(f"  total={total:<3}  freq={freq:<6}  ({freq / trials * 100:.2f}%)")

    observed_totals = list(report.counts.total_distribution.keys())
    if observed_totals:
        print()
        print(f"Observed total range: {min(observed_totals)} .. {max(observed_totals)}")

    print("-----------------------------\n")


def print_distribution_sorted(report: SimulationReport) -> None:
    trials = report.config.trials
    dist = report.counts.total_distribution
    if not dist:
        return
    print("\nDistribution (sorted by total):")
    for total in sorted(dist):
        freq = dist[total]
        print(f"  {total:>3}: {freq:<6} ({freq / trials * 100:.2f}%)")
    print()


def print_history_page_info(
    *,
    offset: int,
    page_size: int,
    total: int,
) -> None:
    if total == 0:
        print("\nShowing 0 of 0 records.\n")
        return

    start = offset + 1
    end = min(offset + page_size, total)
    print(f"\nShowing records {start}-{end} of {total} records.\n")


def print_overall_stats(
    stats: dict[str, int | float | None],
) -> None:
    total_rolls = int(stats["total_rolls"] or 0)

    if total_rolls == 0:
        print("\nNo rolls in history, so no stats to show.\n")
        return

    average_total = stats["average_total"]
    total_matches = int(stats["total_matches"] or 0)
    highest_total = stats["highest_total"]
    lowest_total = stats["lowest_total"]

    print("\n---- Database Overall Stats ----")
    print(f"Total rolls: {total_rolls}")
    print(
        f"Average total: {average_total:.2f}"
        if average_total is not None
        else "Average total is not available"
    )
    print(f"Total matches: {total_matches}")
    print(
        f"Highest total: {highest_total}"
        if highest_total is not None
        else "Highest total is not available"
    )
    print(
        f"Lowest total: {lowest_total}"
        if lowest_total is not None
        else "Lowest total is not available"
    )
    print("--------------------------------\n")
