import uuid

from dice_game.storage.connection import connection
from dice_game.storage.roll_repository import paginated_rolls


def test_first_page_returns_rows():
    rows = paginated_rolls(offset=0, limit=10)
    assert isinstance(rows, list)


def test_offset_beyond_rows_returns_empty():
    rows = paginated_rolls(offset=1000, limit=10)
    assert rows == []


def test_paginated_rolls_returns_remaining_rows_on_last_page():
    # Insert 11 fake rows with unique session IDs
    with connection() as conn:
        # First create all the game sessions to satisfy foreign key constraints
        session_ids = []
        for i in range(11):
            session_id = f"test-session-{uuid.uuid4().hex[:8]}-{i}"
            session_ids.append(session_id)
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
                (
                    session_id,
                    0,
                    "active",
                    f"2026-03-08T09:59:{i:02d}+00:00",
                    f"2026-03-08T10:00:{i:02d}+00:00",
                ),
            )

        # Then insert rolls for each session
        for i, session_id in enumerate(session_ids):
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
                    session_id,
                    f"2026-03-08T10:00:{i:02d}+00:00",
                    "classic",
                    2,
                    "D6",
                    6,
                    "[3, 4]",
                    7,
                    0,
                    "lose",
                    -3,
                    -3,
                ),
            )
        conn.commit()

    # Test pagination: get first 10 rows
    first_page = paginated_rolls(offset=0, limit=10)
    assert len(first_page) == 10

    # Test pagination: get remaining row (should be 1)
    second_page = paginated_rolls(offset=10, limit=10)
    assert len(second_page) == 1
