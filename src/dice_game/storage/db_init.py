import sqlite3

from .connection import connection


def _column_exists(conn: sqlite3.Connection, table_name: str, column_name: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(row["name"] == column_name for row in rows)


def init_db() -> None:
    with connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id TEXT PRIMARY KEY,
                player_points INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS rolls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_session_id TEXT NOT NULL,
                time TEXT NOT NULL,
                mode TEXT NOT NULL,
                dice INTEGER NOT NULL,
                dice_type TEXT NOT NULL,
                sides INTEGER NOT NULL,
                rolls TEXT NOT NULL,
                total INTEGER NOT NULL,
                has_match INTEGER NOT NULL DEFAULT 0,
                outcome TEXT NOT NULL,
                points_delta INTEGER NOT NULL,
                points_total INTEGER NOT NULL,
                FOREIGN KEY (game_session_id) REFERENCES game_sessions(id) ON DELETE CASCADE
            )
            """)

        # Lightweight migration for older DBs
        if not _column_exists(conn, "rolls", "has_match"):
            conn.execute(
                "ALTER TABLE rolls ADD COLUMN has_match INTEGER NOT NULL DEFAULT 0"
            )
