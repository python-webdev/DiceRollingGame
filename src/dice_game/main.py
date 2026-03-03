from .config import GameConfig
from .models import TurnOutcome, TurnState
from .stats import Stats
from .ui import ask_yes_no, get_roll_context
from .logic import (
    roll_dice,
    build_temp_result,
    resolve_turn,
    apply_turn_effects,
    finalize_result,
)
from .printing import print_turn_result, print_stats


def play_turn(state: TurnState) -> TurnOutcome:
    context = get_roll_context()
    rolls = roll_dice(context)

    temp_result = build_temp_result(context, rolls, state.player_points)
    outcome, delta = resolve_turn(state.game_config, temp_result)

    extra_turn = apply_turn_effects(state, temp_result, delta)
    result = finalize_result(temp_result, outcome, delta, state.player_points)

    return TurnOutcome(result=result, extra_turn=extra_turn)


def main() -> None:
    state = TurnState(game_config=GameConfig(), stats=Stats(), player_points=0)

    print("--- Welcome to the Dice Rolling Game! ---")

    while True:
        if ask_yes_no("Roll the dice? (y/n): ") == "n":
            print("\nThank you for playing! Goodbye!\n")
            print_stats(state.stats, state.player_points)
            break

        while True:
            outcome = play_turn(state)

            print_turn_result(outcome.result)
            print_stats(state.stats, state.player_points)

            if not outcome.extra_turn:
                break

            print("🍀 Lucky mode match! Extra turn! 🎉 🎊\n")
