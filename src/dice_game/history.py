# src/dice_game/history.py
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import RollResult


def default_history_path() -> Path:
    """
    Save in project root when you run from root.
    If you run elsewhere, it saves relative to your current working directory.
    """
    return Path("history.json")


def load_history(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
    except json.JSONDecodeError:
        pass
    return []


def save_history(path: Path, history: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(history, indent=2), encoding="utf-8")


def record_from_result(result: RollResult) -> dict[str, Any]:
    # NOTE: we store minimal useful info + full context.
    return {
        "time": datetime.now(timezone.utc).isoformat(),
        "mode": result.context.mode.name,
        "dice_type": result.context.dice_type,
        "dice": result.context.num_dice,
        "sides": result.context.sides,
        "rolls": list(result.rolls),
        "total": result.total,
        "has_match": result.has_match,
        "outcome": result.outcome,
        "points_delta": result.points_delta,
        "points_total": result.points_total,
    }


def append_result(path: Path, history: list[dict[str, Any]], result: RollResult) -> None:
    history.append(record_from_result(result))
    save_history(path, history)


# -------- queries --------

def last_n(history: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    if n <= 0:
        return []
    return history[-n:]


def filter_history(
    history: list[dict[str, Any]],
    *,
    sides: int | None = None,
    dice: int | None = None,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for r in history:
        if sides is not None and r.get("sides") != sides:
            continue
        if dice is not None and r.get("dice") != dice:
            continue
        out.append(r)
    return out


def best_roll(history: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not history:
        return None
    # “best” = highest total (simple + clear)
    return max(history, key=lambda r: int(r.get("total", 0)))
