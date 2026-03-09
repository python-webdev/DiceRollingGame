from dice_game.domain.models import RollContext, RollResult
from dice_game.domain.modes import GameMode


def test_roll_result_total():

    context = RollContext(
        mode=GameMode.CLASSIC,
        dice_type="D6",
        num_dice=2,
        sides=6,
    )

    result = RollResult(
        context=context, rolls=[3, 4], outcome="draw", points_delta=0, points_total=0
    )

    assert result.total == 7


def test_match_detection():
    context = RollContext(GameMode.CLASSIC, "D6", 2, 6)

    result = RollResult(context, [5, 5], "win", 5, 5)

    assert result.has_match is True


def test_no_match():
    context = RollContext(GameMode.CLASSIC, "D6", 2, 6)

    result = RollResult(context, [2, 4], "draw", 0, 0)

    assert result.has_match is False
