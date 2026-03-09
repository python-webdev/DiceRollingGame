from dice_game.storage import sqlite_storage
from dice_game.storage.sqlite_storage import export_rolls_to_csv


def test_csv_export_creates_file(tmp_path):
    filepath = tmp_path / "rolls_export.csv"

    export_rolls_to_csv(filepath)

    assert filepath.exists()


def test_csv_contains_headers(tmp_path):
    filepath = tmp_path / "rolls_export.csv"

    export_rolls_to_csv(filepath)

    test = filepath.read_text()

    assert "id,time,mode" in test


def test_csv_export_contains_expected_rows(tmp_path, monkeypatch):

    db_path = tmp_path / "test.db"
    csv_path = tmp_path / "rolls_export.csv"

    monkeypatch.setattr(sqlite_storage, "DB_PATH", db_path)
    sqlite_storage.init_db()

    with sqlite_storage.get_connection() as conn:
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

    exported = sqlite_storage.export_rolls_to_csv(str(csv_path))
    text = csv_path.read_text(encoding="utf-8")

    assert exported == 1
    assert (
        "id,time,mode,dice,dice_type,sides,rolls,total,match,outcome,points_delta,points_total"
        in text
    )
    assert "LUCKY" in text
    assert "D8" in text
    assert "[8, 8]" in text
    assert "16" in text
