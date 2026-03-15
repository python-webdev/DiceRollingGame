import uuid
from typing import TypedDict, cast

from .connection import connection, utc_now_iso


class GameSessionRecord(TypedDict):
    id: str
    player_points: int
    status: str
    created_at: str
    updated_at: str


def create_game_session() -> GameSessionRecord:
    session_id = str(uuid.uuid4())
    now = utc_now_iso()

    with connection() as conn:
        conn.execute(
            """
            INSERT INTO game_sessions (
                id,
                player_points,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, 0, "active", now, now),
        )

    return {
        "id": session_id,
        "player_points": 0,
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }


def get_game_session(session_id: str) -> GameSessionRecord | None:
    with connection() as conn:
        row = conn.execute(
            """
            SELECT
                id,
                player_points,
                status,
                created_at,
                updated_at
            FROM game_sessions
            WHERE id = ?
            """,
            (session_id,),
        ).fetchone()

    if row is None:
        return None

    return cast(GameSessionRecord, dict(row))


def update_game_session_points(session_id: str, player_points: int) -> None:
    now = utc_now_iso()

    with connection() as conn:
        conn.execute(
            """
            UPDATE game_sessions
            SET player_points = ?, updated_at = ?
            WHERE id = ?
            """,
            (player_points, now, session_id),
        )


def reset_game_session_points(session_id: str) -> None:
    now = utc_now_iso()

    with connection() as conn:
        conn.execute(
            """
            UPDATE game_sessions
            SET player_points = ?, updated_at = ?
            WHERE id = ?
            """,
            (0, now, session_id),
        )


def delete_game_session(session_id: str) -> int:
    with connection() as conn:
        deleted = conn.execute(
            "DELETE FROM game_sessions WHERE id = ?",
            (session_id,),
        ).rowcount

    return deleted
