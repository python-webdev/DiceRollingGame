from dice_game.domain.models import RollContext, RollResult
from dice_game.domain.modes import GameMode
from dice_game.storage.roll_repository import (
    clear_rolls_by_session,
    paginated_rolls_by_session,
    save_roll,
    session_stats,
)
from dice_game.storage.session_repository import (
    create_game_session,
    get_game_session,
    update_game_session_points,
)


def test_create_and_get_game_session() -> None:
    session = create_game_session()

    fetched = get_game_session(session["id"])

    assert fetched is not None
    assert fetched["id"] == session["id"]
    assert fetched["player_points"] == 0
    assert fetched["status"] == "active"


def test_update_game_session_points() -> None:
    session = create_game_session()

    update_game_session_points(session["id"], 12)

    fetched = get_game_session(session["id"])

    assert fetched is not None
    assert fetched["player_points"] == 12


def test_save_roll_and_paginated_rolls_by_session() -> None:
    session = create_game_session()

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

    save_roll(result)

    rows = paginated_rolls_by_session(
        session["id"],
        limit=10,
        offset=0,
    )

    assert len(rows) == 1
    assert rows[0]["game_session_id"] == session["id"]
    assert rows[0]["rolls"] == [3, 4]
    assert rows[0]["total"] == 7


def test_session_stats() -> None:
    session = create_game_session()

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

    save_roll(first)
    save_roll(second)

    stats = session_stats(session["id"])

    assert stats["total_rolls"] == 2
    assert stats["total_roll_value"] == 9
    assert stats["highest_roll"] == 6
    assert stats["lowest_roll"] == 3
    assert stats["total_matches"] == 1


def test_clear_rolls_by_session() -> None:
    session = create_game_session()

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

    save_roll(result)

    deleted = clear_rolls_by_session(session["id"])
    rows = paginated_rolls_by_session(session["id"], limit=10, offset=0)

    assert deleted == 1
    assert rows == []
