import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

from ..domain.config import GameConfig
from ..domain.models import RollResult
from .history_types import HistoryRecord


# Extend HistoryRecord because DB results also have an 'id'
class DatabaseRecord(HistoryRecord):
    id: int


DB_PATH = Path(__file__).resolve().parent / "rolls.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    # This allows us to access columns by name: row["total"]
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rolls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL,
                mode TEXT,
                dice INTEGER,
                dice_type TEXT,
                sides INTEGER,
                rolls TEXT,
                total INTEGER,
                match INTEGER,
                outcome TEXT,
                points_delta INTEGER,
                points_total INTEGER
            )
            """
        )


def save_roll(result: RollResult) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO rolls (
                time, mode, dice, dice_type, sides,
                rolls, total, match, outcome,
                points_delta, points_total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                result.context.mode.name,
                result.context.num_dice,
                result.context.dice_type,
                result.context.sides,
                json.dumps(result.rolls),
                result.total,
                int(result.has_match),
                result.outcome,
                result.points_delta,
                result.points_total,
            ),
        )


# -------- queries --------
def last_rolls(n: int) -> list[DatabaseRecord]:
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM rolls ORDER BY id DESC LIMIT ?", (n,))
        # Convert sqlite3.Row objects to actual dicts for the TypedDict
        rows = cur.fetchall()
        return [cast(DatabaseRecord, dict(row)) for row in rows]


def best_roll() -> DatabaseRecord | None:
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM rolls ORDER BY total DESC LIMIT 1")
        row = cur.fetchone()
        return cast(DatabaseRecord, dict(row)) if row else None


def filter_rolls(
    *, sides: int | None = None, dice: int | None = None
) -> list[DatabaseRecord]:
    query = "SELECT * FROM rolls WHERE 1=1"
    # Changed from Any to int since these specific filters are ints
    params: list[int] = []

    if sides is not None:
        query += " AND sides=?"
        params.append(sides)

    if dice is not None:
        query += " AND dice=?"
        params.append(dice)

    with get_connection() as conn:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [cast(DatabaseRecord, dict(row)) for row in rows]


def clear_rolls(*, reset_ids: bool = False, vacuum: bool = True) -> int:
    with get_connection() as conn:
        cur = conn.execute("SELECT COUNT(*) AS count FROM rolls")
        count = int(cur.fetchone()["count"])

        conn.execute("DELETE FROM rolls")

        if reset_ids:
            conn.execute("DELETE FROM sqlite_sequence WHERE name='rolls'")

    if vacuum and count > 0:
        with get_connection() as conn:
            conn.execute("VACUUM")

    return count


def count_rolls(*, sides: int | None = None, dice: int | None = None) -> int:
    query = "SELECT COUNT(*) AS count FROM rolls WHERE 1=1"
    params: list[int] = []

    if sides is not None:
        query += " AND sides=?"
        params.append(sides)

    if dice is not None:
        query += " AND dice=?"
        params.append(dice)

    with get_connection() as conn:
        cur = conn.execute(query, params)
        row = cur.fetchone()
        return int(row["count"]) if row else 0


def paginated_rolls(
    *,
    limit: int,
    offset: int,
    sides: int | None = None,
    dice: int | None = None,
) -> list[DatabaseRecord]:
    query = "SELECT * FROM rolls WHERE 1=1"
    params: list[int] = []

    if sides is not None:
        query += " AND sides=?"
        params.append(sides)

    if dice is not None:
        query += " AND dice=?"
        params.append(dice)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with get_connection() as conn:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [cast(DatabaseRecord, dict(row)) for row in rows]


def overall_stats() -> dict[str, int | float | None]:
    query = """
SELECT
    COUNT(*) AS total_rolls,
    AVG(total) AS average_total,
    SUM(match) AS total_matches,
    MAX(total) AS highest_total,
    MIN(total) AS lowest_total
FROM rolls
"""

    with get_connection() as conn:
        cur = conn.execute(query)
        row = cur.fetchone()

        if row is None or int(row[0]) == 0:
            return {
                "total_rolls": 0,
                "average_total": None,
                "total_matches": 0,
                "highest_total": None,
                "lowest_total": None,
            }
        return {
            "total_rolls": int(row["total_rolls"]),
            "average_total": float(row["average_total"])
            if row["average_total"] is not None
            else None,
            "total_matches": int(row["total_matches"]),
            "highest_total": int(row["highest_total"])
            if row["highest_total"] is not None
            else None,
            "lowest_total": int(row["lowest_total"])
            if row["lowest_total"] is not None
            else None,
        }


def export_rolls_to_csv(
    file_path: str | None = None,
) -> int:
    """Export all roll history to a CSV file.

    Args:
        file_path: Optional custom path for the CSV file. If None, uses the
                  configured export path (default: src/dice_game/exports/rolls_export.csv).
                  Can be overridden by setting the DICE_GAME_EXPORT_PATH environment variable.

    Returns:
        Number of records exported.

    Example:
        # Use default/configured path
        export_rolls_to_csv()

        # Use custom path
        export_rolls_to_csv("/tmp/my_export.csv")

        # Use environment variable
        # DICE_GAME_EXPORT_PATH="/tmp/export.csv" python3 -m dice_game
    """
    if file_path is None:
        config = GameConfig()
        file_path = config.exports.export_path
    query = """
        SELECT
            id,
            time,
            mode,
            dice,
            dice_type,
            sides,
            rolls,
            total,
            match,
            outcome,
            points_delta,
            points_total
        FROM rolls
        ORDER BY id DESC
    """

    with get_connection() as conn:
        cur = conn.execute(query)
        rows = cur.fetchall()

    fieldnames = [
        "id",
        "time",
        "mode",
        "dice",
        "dice_type",
        "sides",
        "rolls",
        "total",
        "match",
        "outcome",
        "points_delta",
        "points_total",
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(dict(row))

    return len(rows)
