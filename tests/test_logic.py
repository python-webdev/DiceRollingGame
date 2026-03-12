from dice_game.domain.config import GameConfig
from dice_game.domain.models import RollContext, RollResult, TurnState
from dice_game.domain.modes import GameMode
from dice_game.domain.stats import Stats
from dice_game.services.logic import (
    apply_turn_effects,
    build_temp_result,
    resolve_turn,
)


def test_roll_result_total():

    context = RollContext(
        game_session_id="test-session",
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
    context = RollContext(
        game_session_id="test-session",
        mode=GameMode.CLASSIC,
        dice_type="D6",
        num_dice=2,
        sides=6,
    )

    result = RollResult(context, [5, 5], "win", 5, 5)

    assert result.has_match is True


def test_no_match():
    context = RollContext(
        game_session_id="test-session",
        mode=GameMode.CLASSIC,
        dice_type="D6",
        num_dice=2,
        sides=6,
    )

    result = RollResult(context, [2, 4], "draw", 0, 0)

    assert result.has_match is False


def test_lucky_mode_match_grants_extra_turn():
    state = TurnState(
        game_config=GameConfig(),
        game_session_id="test-session",
        stats=Stats(),
        player_points=0,
    )

    context = RollContext(
        game_session_id="test-session",
        mode=GameMode.LUCKY,
        dice_type="D6",
        num_dice=2,
        sides=6,
    )

    rolls = [4, 4]
    temp_result = build_temp_result(context, rolls, state.player_points)
    _, delta = resolve_turn(state.game_config, temp_result)
    extra_turn = apply_turn_effects(state, temp_result, delta)

    assert temp_result.is_lucky_match is True
    assert extra_turn is True
