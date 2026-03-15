from dice_game.storage.connection import connection, init_db
from dice_game.storage.roll_repository import paginated_rolls


def test_first_page_returns_rows():
    rows = paginated_rolls(offset=0, limit=10)

    assert isinstance(rows, list)


def test_offset_beyond_rows_returns_empty():
    rows = paginated_rolls(offset=1000, limit=10)

    assert rows == []


def test_paginated_rolls_returns_remaining_rows_on_last_page(tmp_path, monkeypatch):

    db_path = tmp_path / "test.db"
    monkeypatch.setattr("dice_game.storage.connection.DB_PATH", db_path)
    init_db()

    # Insert 11 fake rows
    with connection() as conn:
        # First create all the game sessions to satisfy foreign key constraints
        for i in range(11):
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
                    f"test-session-{i}",
                    0,
                    "active",
                    f"2026-03-08T09:59:{i:02d}+00:00",
                    f"2026-03-08T10:00:{i:02d}+00:00",
                ),
            )

        # Now insert the rolls
        for i in range(11):
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
                    f"test-session-{i}",
                    f"2026-03-08T10:00:{i:02d}+00:00",
                    "CLASSIC",
                    2,
                    "D6",
                    6,
                    "[1, 2]",
                    3,
                    0,
                    "draw",
                    0,
                    0,
                ),
            )

    page_1 = paginated_rolls(limit=10, offset=0)
    page_2 = paginated_rolls(limit=10, offset=10)

    assert len(page_1) == 10
    assert len(page_2) == 1
