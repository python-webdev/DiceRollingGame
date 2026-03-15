from pathlib import Path

from fastapi.testclient import TestClient

from src.dice_game.api.schemas import (
    DeleteHistoryResponse,
    DeleteSessionResponse,
    ExportHistoryResponse,
    HistoryItemResponse,
    RollResponse,
    SessionResponse,
    StatsResponse,
)


def cleanup_test_csv_files() -> None:
    """Remove any leftover CSV files from previous test runs."""
    exports_dir = Path("src/dice_game/exports")
    if exports_dir.exists():
        # Remove CSV files that match the test pattern (UUID-based filenames)
        for csv_file in exports_dir.glob("roll_history_*.csv"):
            try:
                csv_file.unlink()
            except OSError:
                pass  # Ignore if file can't be deleted


def create_session(client: TestClient) -> str:
    response = client.post("/sessions")
    assert response.status_code == 200

    # Validate response structure with schema
    session = SessionResponse.model_validate(response.json())
    return session.game_session_id


def test_create_session(client: TestClient) -> None:
    response = client.post("/sessions")
    assert response.status_code == 200

    # Schema validates structure, types, and required fields
    session = SessionResponse.model_validate(response.json())

    # Business logic assertions
    assert session.player_points == 0
    assert session.status == "active"
    assert session.game_session_id  # Non-empty UUID
    assert session.created_at  # Non-empty timestamp
    assert session.updated_at  # Non-empty timestamp


def test_get_session(client: TestClient) -> None:
    session_id = create_session(client)

    response = client.get(f"/sessions/{session_id}")
    assert response.status_code == 200

    # Schema validation + business logic
    session = SessionResponse.model_validate(response.json())
    assert session.game_session_id == session_id
    assert session.player_points == 0
    assert session.status == "active"


def test_roll_updates_session_points(client: TestClient) -> None:
    session_id = create_session(client)

    roll_response = client.post(
        f"/sessions/{session_id}/roll",
        json={
            "mode": "classic",
            "dice_type": "D6",
            "num_dice": 2,
        },
    )
    assert roll_response.status_code == 200

    # Schema validation for roll response
    roll = RollResponse.model_validate(roll_response.json())

    # Business logic assertions
    assert roll.game_session_id == session_id
    assert len(roll.rolls) == 2
    assert roll.total == sum(roll.rolls)  # Verify calculation
    assert all(1 <= dice_value <= 6 for dice_value in roll.rolls)  # D6 range

    session_response = client.get(f"/sessions/{session_id}")
    assert session_response.status_code == 200

    # Schema validation for session response
    session = SessionResponse.model_validate(session_response.json())
    assert session.player_points == roll.points_total


def test_roll_with_invalid_session_returns_404(client: TestClient) -> None:
    response = client.post(
        "/sessions/not-a-real-session/roll",
        json={
            "mode": "classic",
            "dice_type": "D6",
            "num_dice": 2,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Game session not found"


def test_roll_with_invalid_dice_type_returns_400(client: TestClient) -> None:
    session_id = create_session(client)

    response = client.post(
        f"/sessions/{session_id}/roll",
        json={
            "mode": "classic",
            "dice_type": "D999",
            "num_dice": 2,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid dice type"


def test_roll_with_invalid_mode_returns_400(client: TestClient) -> None:
    session_id = create_session(client)

    response = client.post(
        f"/sessions/{session_id}/roll",
        json={
            "mode": "nonsense",
            "dice_type": "D6",
            "num_dice": 2,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid game mode"


def test_history_returns_only_that_sessions_rolls(client: TestClient) -> None:
    session_a = create_session(client)
    session_b = create_session(client)

    client.post(
        f"/sessions/{session_a}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )
    client.post(
        f"/sessions/{session_a}/roll",
        json={"mode": "lucky", "dice_type": "D6", "num_dice": 2},
    )
    client.post(
        f"/sessions/{session_b}/roll",
        json={"mode": "risk", "dice_type": "D8", "num_dice": 3},
    )

    response_a = client.get(f"/sessions/{session_a}/history")
    response_b = client.get(f"/sessions/{session_b}/history")

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    # Schema validation for history list responses
    history_a = [HistoryItemResponse.model_validate(item) for item in response_a.json()]
    history_b = [HistoryItemResponse.model_validate(item) for item in response_b.json()]

    # Business logic assertions
    assert len(history_a) == 2
    assert len(history_b) == 1
    assert all(item.game_session_id == session_a for item in history_a)
    assert all(item.game_session_id == session_b for item in history_b)

    # Verify modes are correct
    assert {item.mode for item in history_a} == {"classic", "lucky"}
    assert history_b[0].mode == "risk"


def test_stats_reflect_only_that_session(client: TestClient) -> None:
    session_a = create_session(client)
    session_b = create_session(client)

    client.post(
        f"/sessions/{session_a}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )
    client.post(
        f"/sessions/{session_a}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )
    client.post(
        f"/sessions/{session_b}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )

    response_a = client.get(f"/sessions/{session_a}/stats")
    response_b = client.get(f"/sessions/{session_b}/stats")

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    # Schema validation for stats responses
    stats_a = StatsResponse.model_validate(response_a.json())
    stats_b = StatsResponse.model_validate(response_b.json())

    # Business logic assertions
    assert stats_a.game_session_id == session_a
    assert stats_b.game_session_id == session_b
    assert stats_a.total_rolls == 2
    assert stats_b.total_rolls == 1


def test_deleting_one_session_does_not_affect_another(client: TestClient) -> None:
    session_a = create_session(client)
    session_b = create_session(client)

    client.post(
        f"/sessions/{session_a}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )
    client.post(
        f"/sessions/{session_b}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )

    delete_response = client.delete(f"/sessions/{session_a}")
    assert delete_response.status_code == 200

    # Schema validation for delete response
    delete_result = DeleteSessionResponse.model_validate(delete_response.json())
    assert delete_result.deleted is True

    missing_response = client.get(f"/sessions/{session_a}")
    assert missing_response.status_code == 404

    existing_response = client.get(f"/sessions/{session_b}")
    assert existing_response.status_code == 200

    # Schema validation for existing session
    session_b_data = SessionResponse.model_validate(existing_response.json())
    assert session_b_data.game_session_id == session_b

    history_b = client.get(f"/sessions/{session_b}/history")
    assert history_b.status_code == 200

    # Schema validation for history
    history_items = [
        HistoryItemResponse.model_validate(item) for item in history_b.json()
    ]
    assert len(history_items) == 1


def test_delete_history_clears_only_that_sessions_rolls(client: TestClient) -> None:
    session_a = create_session(client)
    session_b = create_session(client)

    client.post(
        f"/sessions/{session_a}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )
    client.post(
        f"/sessions/{session_b}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )

    delete_response = client.delete(f"/sessions/{session_a}/history")
    assert delete_response.status_code == 200

    # Schema validation for delete history response
    delete_result = DeleteHistoryResponse.model_validate(delete_response.json())
    assert delete_result.deleted_records == 1
    assert delete_result.player_points == 0  # Points reset after delete

    history_a = client.get(f"/sessions/{session_a}/history")
    history_b = client.get(f"/sessions/{session_b}/history")

    assert history_a.status_code == 200
    assert history_b.status_code == 200

    # Validate empty history for session A
    assert history_a.json() == []

    # Schema validation for session B history (should still have 1 item)
    history_b_items = [
        HistoryItemResponse.model_validate(item) for item in history_b.json()
    ]
    assert len(history_b_items) == 1


def test_get_history_with_invalid_session_returns_404(client: TestClient) -> None:
    response = client.get("/sessions/not-a-real-session/history")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game session not found"


def test_delete_history_with_invalid_session_returns_404(client: TestClient) -> None:
    response = client.delete("/sessions/not-a-real-session/history")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game session not found"


def test_export_with_invalid_session_returns_404(client: TestClient) -> None:
    response = client.get("/sessions/not-a-real-session/history/export")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game session not found"


def test_export_history_returns_404_when_session_has_no_rolls(
    client: TestClient,
) -> None:
    session_id = create_session(client)

    response = client.get(f"/sessions/{session_id}/history/export")

    assert response.status_code == 404
    assert response.json()["detail"] == "No rolls to export"


def test_export_history_success(client: TestClient) -> None:
    # Cleanup any leftover CSV files from previous runs
    cleanup_test_csv_files()

    session_id = create_session(client)
    csv_file = Path("src/dice_game/exports") / f"roll_history_{session_id}.csv"

    try:
        client.post(
            f"/sessions/{session_id}/roll",
            json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
        )

        response = client.get(f"/sessions/{session_id}/history/export")
        assert response.status_code == 200

        # Schema validation for export response
        export_result = ExportHistoryResponse.model_validate(response.json())
        assert export_result.records == 1
        assert export_result.file == f"roll_history_{session_id}.csv"
        assert "exported" in export_result.message.lower()  # Verify message content

        # Verify the file was actually created
        assert csv_file.exists(), "CSV file should have been created"

    finally:
        # Cleanup: Always remove the exported CSV file
        if csv_file.exists():
            csv_file.unlink()  # Delete the file


def test_get_session_with_invalid_id_returns_404(client: TestClient) -> None:
    response = client.get("/sessions/not-a-real-session")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game session not found"


def test_delete_session_with_invalid_id_returns_404(client: TestClient) -> None:
    response = client.delete("/sessions/not-a-real-session")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game session not found"


def test_stats_with_invalid_session_returns_404(client: TestClient) -> None:
    response = client.get("/sessions/not-a-real-session/stats")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game session not found"


def test_history_rejects_negative_offset(client: TestClient) -> None:
    session_id = create_session(client)

    response = client.get(f"/sessions/{session_id}/history?offset=-1")

    assert response.status_code == 422


def test_history_rejects_invalid_limit(client: TestClient) -> None:
    session_id = create_session(client)

    response = client.get(f"/sessions/{session_id}/history?limit=0")

    assert response.status_code == 422


def test_delete_history_resets_points_and_clears_rolls(client: TestClient) -> None:
    session_id = create_session(client)

    roll_response = client.post(
        f"/sessions/{session_id}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )
    assert roll_response.status_code == 200

    # Verify roll was successful
    RollResponse.model_validate(roll_response.json())

    delete_response = client.delete(f"/sessions/{session_id}/history")
    assert delete_response.status_code == 200

    # Schema validation for delete response
    delete_result = DeleteHistoryResponse.model_validate(delete_response.json())
    assert delete_result.deleted_records == 1
    assert delete_result.player_points == 0  # Points reset

    history_response = client.get(f"/sessions/{session_id}/history")
    assert history_response.status_code == 200
    assert history_response.json() == []  # History cleared

    session_response = client.get(f"/sessions/{session_id}")
    assert session_response.status_code == 200

    # Schema validation for updated session
    session = SessionResponse.model_validate(session_response.json())
    assert session.player_points == 0  # Confirm points were reset
