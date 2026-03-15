from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dice_game.api.app import create_app
from dice_game.storage import connection


@pytest.fixture(autouse=True)
def test_db(tmp_path: Path) -> None:
    test_db_path = tmp_path / "test_rolls.db"
    connection.DB_PATH = test_db_path
    connection.init_db()


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)
