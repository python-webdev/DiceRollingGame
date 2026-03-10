from dice_game.storage import sqlite_storage


def test_empty_database_has_zero_rows(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"

    monkeypatch.setattr(sqlite_storage, "DB_PATH", db_path)

    sqlite_storage.init_db()

    assert sqlite_storage.count_rolls() == 0
