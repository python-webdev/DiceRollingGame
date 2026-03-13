from fastapi.testclient import TestClient


def create_session(client: TestClient) -> str:
    response = client.post("/sessions")
    assert response.status_code == 200

    data = response.json()
    return data["game_session_id"]


def test_create_session(client: TestClient) -> None:
    response = client.post("/sessions")

    assert response.status_code == 200

    data = response.json()
    assert "game_session_id" in data
    assert isinstance(data["game_session_id"], str)
    assert data["player_points"] == 0
    assert data["status"] == "active"
    assert "created_at" in data
    assert "updated_at" in data


def test_get_session(client: TestClient) -> None:
    session_id = create_session(client)

    response = client.get(f"/sessions/{session_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["game_session_id"] == session_id
    assert data["player_points"] == 0
    assert data["status"] == "active"


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

    roll_data = roll_response.json()
    assert roll_data["game_session_id"] == session_id
    assert isinstance(roll_data["rolls"], list)
    assert len(roll_data["rolls"]) == 2
    assert isinstance(roll_data["points_total"], int)

    session_response = client.get(f"/sessions/{session_id}")
    assert session_response.status_code == 200

    session_data = session_response.json()
    assert session_data["player_points"] == roll_data["points_total"]


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

    history_a = response_a.json()
    history_b = response_b.json()

    assert len(history_a) == 2
    assert len(history_b) == 1
    assert all(item["game_session_id"] == session_a for item in history_a)
    assert all(item["game_session_id"] == session_b for item in history_b)


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

    stats_a = response_a.json()
    stats_b = response_b.json()

    assert stats_a["game_session_id"] == session_a
    assert stats_b["game_session_id"] == session_b
    assert stats_a["total_rolls"] == 2
    assert stats_b["total_rolls"] == 1


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
    assert delete_response.json()["deleted"] is True

    missing_response = client.get(f"/sessions/{session_a}")
    assert missing_response.status_code == 404

    existing_response = client.get(f"/sessions/{session_b}")
    assert existing_response.status_code == 200

    history_b = client.get(f"/sessions/{session_b}/history")
    assert history_b.status_code == 200
    assert len(history_b.json()) == 1


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

    history_a = client.get(f"/sessions/{session_a}/history")
    history_b = client.get(f"/sessions/{session_b}/history")

    assert history_a.status_code == 200
    assert history_b.status_code == 200
    assert history_a.json() == []
    assert len(history_b.json()) == 1


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
    session_id = create_session(client)

    client.post(
        f"/sessions/{session_id}/roll",
        json={"mode": "classic", "dice_type": "D6", "num_dice": 2},
    )

    response = client.get(f"/sessions/{session_id}/history/export")

    assert response.status_code == 200

    data = response.json()
    assert data["records"] == 1
    assert data["file"] == f"roll_history_{session_id}.csv"


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

    delete_response = client.delete(f"/sessions/{session_id}/history")
    assert delete_response.status_code == 200

    delete_data = delete_response.json()
    assert delete_data["deleted_records"] == 1
    assert delete_data["player_points"] == 0

    history_response = client.get(f"/sessions/{session_id}/history")
    assert history_response.status_code == 200
    assert history_response.json() == []

    session_response = client.get(f"/sessions/{session_id}")
    assert session_response.status_code == 200
    assert session_response.json()["player_points"] == 0
