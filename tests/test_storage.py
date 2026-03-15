from dice_game.storage.connection import init_db
from dice_game.storage.roll_repository import count_rolls


def test_empty_database_has_zero_rows(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"

    monkeypatch.setattr("dice_game.storage.connection.DB_PATH", db_path)

    init_db()

    assert count_rolls() == 0
