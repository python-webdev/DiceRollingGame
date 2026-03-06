import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

from .models import RollResult
from .history import HistoryRecord


# Extend HistoryRecord because DB results also have an 'id'
class DatabaseRecord(HistoryRecord):
    id: int


# DB_PATH = Path("rolls.db")
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
        cur = conn.execute(
            "SELECT * FROM rolls ORDER BY id DESC LIMIT ?", (n,)
        )
        # Convert sqlite3.Row objects to actual dicts for the TypedDict
        rows = cur.fetchall()
        return [cast(DatabaseRecord, dict(row)) for row in rows]


def best_roll() -> DatabaseRecord | None:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT * FROM rolls ORDER BY total DESC LIMIT 1"
        )
        row = cur.fetchone()
        return cast(DatabaseRecord, dict(row)) if row else None


def filter_rolls(*, sides: int | None = None, dice: int | None = None) -> list[DatabaseRecord]:
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
        cur = conn.execute("SELECT COUNT(*) AS c FROM rolls")
        count = int(cur.fetchone()["c"])

        conn.execute("DELETE FROM rolls")

        if reset_ids:
            conn.execute("DELETE FROM sqlite_sequence WHERE name='rolls'")

    if vacuum and count > 0:
        with get_connection() as conn:
            conn.execute("VACUUM")

    return count
