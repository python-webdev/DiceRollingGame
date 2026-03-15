from dice_game.storage import roll_repository
from dice_game.storage.connection import connection, init_db


def test_csv_export_creates_file(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    csv_path = tmp_path / "rolls_export.csv"

    monkeypatch.setattr("dice_game.storage.connection.DB_PATH", db_path)
    init_db()

    roll_repository.export_rolls_to_csv(str(csv_path))

    assert csv_path.exists()


def test_csv_contains_headers(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    csv_path = tmp_path / "rolls_export.csv"

    monkeypatch.setattr("dice_game.storage.connection.DB_PATH", db_path)
    init_db()

    roll_repository.export_rolls_to_csv(str(csv_path))

    test = csv_path.read_text()

    assert "id,time,mode" in test


def test_csv_export_contains_expected_rows(tmp_path, monkeypatch):

    db_path = tmp_path / "test.db"
    csv_path = tmp_path / "rolls_export.csv"

    monkeypatch.setattr("dice_game.storage.connection.DB_PATH", db_path)
    init_db()

    with connection() as conn:
        # Create the game session first to satisfy foreign key constraint
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
                "test-session-1",
                10,
                "active",
                "2026-03-08T09:59:00+00:00",
                "2026-03-08T10:00:00+00:00",
            ),
        )

        # Now insert the roll
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
                "test-session-1",
                "2026-03-08T10:00:00+00:00",
                "LUCKY",
                2,
                "D8",
                8,
                "[8, 8]",
                16,
                1,
                "win",
                10,
                10,
            ),
        )

    exported = roll_repository.export_rolls_to_csv(str(csv_path))
    text = csv_path.read_text(encoding="utf-8")

    assert exported == 1
    assert (
        "id,game_session_id,time,mode,dice,dice_type,sides,rolls,total,has_match,outcome,points_delta,points_total"
        in text
    )
    assert "LUCKY" in text
    assert "D8" in text
    assert "[8, 8]" in text
    assert "16" in text
    assert "1" in text
