from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, cast

from .models import RollResult

# Using TypedDict is the best practice for JSON structures.
# It provides type safety and IDE autocompletion while remaining a plain dict.


class HistoryRecord(TypedDict):
    time: str
    mode: str
    dice: int
    dice_type: str
    sides: int
    rolls: list[int]
    total: int
    match: bool
    outcome: str
    points_delta: int
    points_total: int


def history_path() -> Path:
    """Returns the default path for the history file."""
    return Path("history.jsonl")


def load_history(path: Path) -> list[HistoryRecord]:
    """Loads and parses the history from a JSONL file."""
    if not path.exists():
        return []

    records: list[HistoryRecord] = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                # cast is used because json.loads returns 'Any' by default
                record = cast(HistoryRecord, json.loads(line))
                records.append(record)
            except json.JSONDecodeError:
                continue

    return records


def record_from_result(result: RollResult) -> HistoryRecord:
    """Converts a RollResult into a HistoryRecord dictionary."""
    return {
        "time": datetime.now(timezone.utc).isoformat(),
        "mode": result.context.mode.name,
        "dice": result.context.num_dice,
        "dice_type": result.context.dice_type,
        "sides": result.context.sides,
        "rolls": result.rolls,
        "total": result.total,
        "match": result.has_match,
        "outcome": result.outcome,
        "points_delta": result.points_delta,
        "points_total": result.points_total,
    }


def append_history(path: Path, result: RollResult) -> HistoryRecord:
    """Appends a new result to the history file and returns the record."""
    record = record_from_result(result)

    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return record


# -------- queries --------


def last_n(history: list[HistoryRecord], n: int) -> list[HistoryRecord]:
    """Returns the most recent n records."""
    return history[-n:]


def filter_history(
    history: list[HistoryRecord],
    *,
    sides: int | None = None,
    dice: int | None = None,
) -> list[HistoryRecord]:
    """Filters the history by number of sides or number of dice."""
    out: list[HistoryRecord] = []

    for r in history:
        if sides is not None and r["sides"] != sides:
            continue

        if dice is not None and r["dice"] != dice:
            continue

        out.append(r)

    return out


def best_roll(history: list[HistoryRecord]) -> HistoryRecord | None:
    """Returns the record with the highest total value."""
    if not history:
        return None

    return max(history, key=lambda r: r["total"])
