import random

from ..domain.config import GameConfig
from ..domain.models import RollContext, RollResult, TurnState


def roll_dice(context: RollContext) -> list[int]:
    return [random.randint(1, context.sides) for _ in range(context.num_dice)]


def determine_outcome(game_config: GameConfig, result: RollResult) -> str:
    ratio = result.normalized_ratio

    if ratio >= game_config.thresholds.win_ratio:
        return "win"
    if ratio >= game_config.thresholds.draw_ratio:
        return "draw"
    return "lose"


def points_for_turn(game_config: GameConfig, result: RollResult) -> int:
    if result.is_lucky_match:
        return game_config.points.lucky_match

    if result.is_risk:
        if result.normalized_ratio < game_config.thresholds.risk_penalty_ratio:
            return game_config.points.risk_penalty

    outcome = determine_outcome(game_config, result)
    if outcome == "win":
        return game_config.points.win
    if outcome == "lose":
        return game_config.points.lose
    return game_config.points.draw


def build_temp_result(context: RollContext, rolls: list[int], player_points: int) -> RollResult:
    return RollResult(
        context=context,
        rolls=rolls,
        outcome="",
        points_delta=0,
        points_total=player_points,
    )


def resolve_turn(game_config: GameConfig, temp_result: RollResult) -> tuple[str, int]:
    outcome = determine_outcome(game_config, temp_result)
    delta = points_for_turn(game_config, temp_result)
    return outcome, delta


def apply_turn_effects(state: TurnState, temp_result: RollResult, delta: int) -> bool:
    extra_turn = temp_result.is_lucky_match

    state.player_points += delta
    state.stats.update(
        temp_result.total,
        temp_result.has_match,
    )
    return extra_turn


def finalize_result(temp_result: RollResult, outcome: str, delta: int, player_points: int) -> RollResult:
    return RollResult(
        context=temp_result.context,
        rolls=temp_result.rolls,
        outcome=outcome,
        points_delta=delta,
        points_total=player_points,
    )
