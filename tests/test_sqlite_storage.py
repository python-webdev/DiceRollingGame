from dice_game.domain.models import RollContext, RollResult
from dice_game.domain.modes import GameMode
from dice_game.storage import sqlite_storage


def test_create_and_get_game_session() -> None:
    session = sqlite_storage.create_game_session()

    fetched = sqlite_storage.get_game_session(session["id"])

    assert fetched is not None
    assert fetched["id"] == session["id"]
    assert fetched["player_points"] == 0
    assert fetched["status"] == "active"


def test_update_game_session_points() -> None:
    session = sqlite_storage.create_game_session()

    sqlite_storage.update_game_session_points(session["id"], 12)

    fetched = sqlite_storage.get_game_session(session["id"])

    assert fetched is not None
    assert fetched["player_points"] == 12


def test_save_roll_and_paginated_rolls_by_session() -> None:
    session = sqlite_storage.create_game_session()

    context = RollContext(
        game_session_id=session["id"],
        mode=GameMode.CLASSIC,
        dice_type="D6",
        num_dice=2,
        sides=6,
    )
    result = RollResult(
        context=context,
        rolls=[3, 4],
        outcome="draw",
        points_delta=0,
        points_total=0,
    )

    sqlite_storage.save_roll(result)

    rows = sqlite_storage.paginated_rolls_by_session(
        session["id"],
        limit=10,
        offset=0,
    )

    assert len(rows) == 1
    assert rows[0]["game_session_id"] == session["id"]
    assert rows[0]["rolls"] == [3, 4]
    assert rows[0]["total"] == 7


def test_session_stats() -> None:
    session = sqlite_storage.create_game_session()

    first = RollResult(
        context=RollContext(
            game_session_id=session["id"],
            mode=GameMode.CLASSIC,
            dice_type="D6",
            num_dice=2,
            sides=6,
        ),
        rolls=[3, 3],
        outcome="win",
        points_delta=5,
        points_total=5,
    )
    second = RollResult(
        context=RollContext(
            game_session_id=session["id"],
            mode=GameMode.CLASSIC,
            dice_type="D6",
            num_dice=2,
            sides=6,
        ),
        rolls=[1, 2],
        outcome="lose",
        points_delta=-3,
        points_total=2,
    )

    sqlite_storage.save_roll(first)
    sqlite_storage.save_roll(second)

    stats = sqlite_storage.session_stats(session["id"])

    assert stats["total_rolls"] == 2
    assert stats["total_roll_value"] == 9
    assert stats["highest_roll"] == 6
    assert stats["lowest_roll"] == 3
    assert stats["total_matches"] == 1


def test_clear_rolls_by_session() -> None:
    session = sqlite_storage.create_game_session()

    result = RollResult(
        context=RollContext(
            game_session_id=session["id"],
            mode=GameMode.CLASSIC,
            dice_type="D6",
            num_dice=2,
            sides=6,
        ),
        rolls=[2, 5],
        outcome="draw",
        points_delta=0,
        points_total=0,
    )

    sqlite_storage.save_roll(result)

    deleted = sqlite_storage.clear_rolls_by_session(session["id"])
    rows = sqlite_storage.paginated_rolls_by_session(session["id"], limit=10, offset=0)

    assert deleted == 1
    assert rows == []
