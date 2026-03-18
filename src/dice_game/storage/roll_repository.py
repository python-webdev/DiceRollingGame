import csv
import json
import sqlite3
from pathlib import Path
from typing import TypedDict, cast

from ..domain.config import GameConfig
from ..domain.models import RollResult
from ..domain.stats import OverallStats
from .connection import connection, utc_now_iso
from .history_types import DatabaseRecord


class SessionStatsRecord(TypedDict):
    total_rolls: int
    total_roll_value: int
    highest_roll: int | None
    lowest_roll: int | None
    average_roll: float | None
    total_matches: int


class OverallStatsRecord(TypedDict):
    total_rolls: int
    average_total: float | None
    total_matches: int
    highest_total: int | None
    lowest_total: int | None


CSV_FIELDNAMES = [
    "id",
    "game_session_id",
    "time",
    "mode",
    "dice",
    "dice_type",
    "sides",
    "rolls",
    "total",
    "has_match",
    "outcome",
    "points_delta",
    "points_total",
]


def _write_rows_to_csv(rows: list[sqlite3.Row], file_path: str) -> int:
    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

        for row in rows:
            writer.writerow(dict(row))

    return len(rows)


def save_roll(result: RollResult) -> None:
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO rolls (
                game_session_id,
                time,
                mode,
                dice,
                dice_type,
                sides,
                rolls,
                total,
                has_match,
                outcome,
                points_delta,
                points_total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.context.game_session_id,
                utc_now_iso(),
                result.context.mode.name.lower(),
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


def _row_to_database_record(row: sqlite3.Row) -> DatabaseRecord:
    item = dict(row)
    item["rolls"] = json.loads(item["rolls"])
    return cast(DatabaseRecord, item)


def last_rolls(n: int) -> list[DatabaseRecord]:
    with connection() as conn:
        cur = conn.execute("SELECT * FROM rolls ORDER BY id DESC LIMIT ?", (n,))
        rows = cur.fetchall()
        return [_row_to_database_record(row) for row in rows]


def best_roll() -> DatabaseRecord | None:
    with connection() as conn:
        cur = conn.execute("SELECT * FROM rolls ORDER BY total DESC LIMIT 1")
        row = cur.fetchone()
        return _row_to_database_record(row) if row else None


def filter_rolls(
    *,
    sides: int | None = None,
    dice: int | None = None,
) -> list[DatabaseRecord]:
    query = "SELECT * FROM rolls WHERE 1=1"
    params: list[int] = []

    if sides is not None:
        query += " AND sides = ?"
        params.append(sides)

    if dice is not None:
        query += " AND dice = ?"
        params.append(dice)

    with connection() as conn:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [_row_to_database_record(row) for row in rows]


def clear_rolls(*, reset_ids: bool = False, vacuum: bool = True) -> int:
    with connection() as conn:
        cur = conn.execute("SELECT COUNT(*) AS count FROM rolls")
        row = cur.fetchone()
        count = int(row["count"]) if row else 0

        conn.execute("DELETE FROM rolls")

        if reset_ids:
            conn.execute("DELETE FROM sqlite_sequence WHERE name = 'rolls'")

    if vacuum and count > 0:
        with connection() as conn:
            conn.execute("VACUUM")

    return count


def count_rolls(*, sides: int | None = None, dice: int | None = None) -> int:
    query = "SELECT COUNT(*) AS count FROM rolls WHERE 1=1"
    params: list[int] = []

    if sides is not None:
        query += " AND sides = ?"
        params.append(sides)

    if dice is not None:
        query += " AND dice = ?"
        params.append(dice)

    with connection() as conn:
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
        query += " AND sides = ?"
        params.append(sides)

    if dice is not None:
        query += " AND dice = ?"
        params.append(dice)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with connection() as conn:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return [_row_to_database_record(row) for row in rows]


def paginated_rolls_by_session(
    game_session_id: str,
    *,
    limit: int,
    offset: int,
) -> list[DatabaseRecord]:
    query = """
        SELECT *
        FROM rolls
        WHERE game_session_id = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """

    with connection() as conn:
        cur = conn.execute(query, (game_session_id, limit, offset))
        rows = cur.fetchall()
        return [_row_to_database_record(row) for row in rows]


def clear_rolls_by_session(game_session_id: str) -> int:
    with connection() as conn:
        deleted = conn.execute(
            "DELETE FROM rolls WHERE game_session_id = ?",
            (game_session_id,),
        ).rowcount

    return deleted


def session_stats(game_session_id: str) -> SessionStatsRecord:
    query = """
    SELECT
        COUNT(*) AS total_rolls,
        COALESCE(SUM(total), 0) AS total_roll_value,
        MAX(total) AS highest_roll,
        MIN(total) AS lowest_roll,
        AVG(total) AS average_roll,
        COALESCE(SUM(has_match), 0) AS total_matches
    FROM rolls
    WHERE game_session_id = ?
    """

    with connection() as conn:
        cur = conn.execute(query, (game_session_id,))
        row = cur.fetchone()

    if row is None or int(row["total_rolls"]) == 0:
        return {
            "total_rolls": 0,
            "total_roll_value": 0,
            "highest_roll": None,
            "lowest_roll": None,
            "average_roll": None,
            "total_matches": 0,
        }

    return {
        "total_rolls": int(row["total_rolls"]),
        "total_roll_value": int(row["total_roll_value"]),
        "highest_roll": (
            int(row["highest_roll"]) if row["highest_roll"] is not None else None
        ),
        "lowest_roll": (
            int(row["lowest_roll"]) if row["lowest_roll"] is not None else None
        ),
        "average_roll": (
            round(float(row["average_roll"]), 2)
            if row["average_roll"] is not None
            else None
        ),
        "total_matches": int(row["total_matches"]),
    }


def overall_stats() -> OverallStats:
    query = """
    SELECT
        COUNT(*) AS total_rolls,
        AVG(total) AS average_total,
        SUM(has_match) AS total_matches,
        MAX(total) AS highest_total,
        MIN(total) AS lowest_total
    FROM rolls
    """

    with connection() as conn:
        cur = conn.execute(query)
        row = cur.fetchone()

    if row is None or int(row["total_rolls"]) == 0:
        return OverallStats(
            total_rolls=0,
            average_total=None,
            total_matches=0,
            highest_total=None,
            lowest_total=None,
        )

    return OverallStats(
        total_rolls=int(row["total_rolls"]),
        average_total=(
            round(float(row["average_total"]), 2)
            if row["average_total"] is not None
            else None
        ),
        total_matches=(
            int(row["total_matches"]) if row["total_matches"] is not None else 0
        ),
        highest_total=(
            int(row["highest_total"]) if row["highest_total"] is not None else None
        ),
        lowest_total=(
            int(row["lowest_total"]) if row["lowest_total"] is not None else None
        ),
    )


def export_rolls_to_csv(file_path: str | None = None) -> int:
    if file_path is None:
        config = GameConfig()
        file_path = config.exports.export_path

    query = """
        SELECT
            id,
            game_session_id,
            time,
            mode,
            dice,
            dice_type,
            sides,
            rolls,
            total,
            has_match,
            outcome,
            points_delta,
            points_total
        FROM rolls
        ORDER BY id DESC
    """

    with connection() as conn:
        rows = conn.execute(query).fetchall()

    return _write_rows_to_csv(rows, file_path)


def export_rolls_to_csv_by_session(
    game_session_id: str,
    file_path: str | None = None,
) -> int:
    if file_path is None:
        config = GameConfig()
        base_path = Path(config.exports.export_path)
        file_path = str(base_path.with_name(f"roll_history_{game_session_id}.csv"))

    query = """
        SELECT
            id,
            game_session_id,
            time,
            mode,
            dice,
            dice_type,
            sides,
            rolls,
            total,
            has_match,
            outcome,
            points_delta,
            points_total
        FROM rolls
        WHERE game_session_id = ?
        ORDER BY id DESC
    """

    with connection() as conn:
        rows = conn.execute(query, (game_session_id,)).fetchall()

    return _write_rows_to_csv(rows, file_path)
