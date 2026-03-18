import sys
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dice_game.api.app import create_app
from dice_game.storage.connection import connection
from dice_game.storage.db_init import init_db


@pytest.fixture(autouse=True)
def test_db(tmp_path: Path, monkeypatch) -> None:
    """Automatically set up isolated test database for each test."""
    test_db_path = tmp_path / f"test_rolls_{uuid.uuid4().hex[:8]}.db"

    # Access the connection module directly from sys.modules
    connection_module = sys.modules["dice_game.storage.connection"]
    monkeypatch.setattr(connection_module, "DB_PATH", test_db_path)
    init_db()

    # Ensure foreign keys are enabled
    with connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.commit()


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


@pytest.fixture
def unique_session_id() -> str:
    """Generate unique session ID for tests."""
    return f"test-session-{uuid.uuid4().hex[:8]}"
