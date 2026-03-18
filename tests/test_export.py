from dice_game.storage import roll_repository
from dice_game.storage.connection import connection


def test_csv_export_creates_file(tmp_path):
    csv_path = tmp_path / "rolls_export.csv"
    roll_repository.export_rolls_to_csv(str(csv_path))
    assert csv_path.exists()


def test_csv_contains_headers(tmp_path):
    csv_path = tmp_path / "rolls_export.csv"
    roll_repository.export_rolls_to_csv(str(csv_path))

    content = csv_path.read_text()
    assert "id,time,mode" in content


def test_csv_export_contains_expected_rows(tmp_path, unique_session_id):
    csv_path = tmp_path / "rolls_export.csv"

    # Insert test data
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
                unique_session_id,
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
                unique_session_id,
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
        conn.commit()

    roll_repository.export_rolls_to_csv(str(csv_path))

    content = csv_path.read_text()
    assert "LUCKY" in content
    assert "D8" in content
    assert "[8, 8]" in content
