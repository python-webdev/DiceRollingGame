from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dice_game.api.app import create_app
from dice_game.storage import sqlite_storage


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    test_db = tmp_path / "test_rolls.db"

    sqlite_storage.DB_PATH = test_db
    app = create_app()

    return TestClient(app)
