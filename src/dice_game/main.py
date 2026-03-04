# src/dice_game/main.py
from .config import GameConfig
from .models import TurnOutcome, TurnState
from .stats import Stats
from .ui import ask_int, ask_menu_action, get_roll_context
from .logic import (
    roll_dice,
    build_temp_result,
    resolve_turn,
    apply_turn_effects,
    finalize_result,
)
from .printing import (
    print_turn_result,
    print_stats,
    print_history,
    print_best_roll,
)
from .history import (
    default_history_path,
    load_history,
    append_result,
    last_n,
    filter_history,
    best_roll,
)


def play_turn(state: TurnState) -> TurnOutcome:
    context = get_roll_context()
    rolls = roll_dice(context)

    temp_result = build_temp_result(context, rolls, state.player_points)
    outcome, delta = resolve_turn(state.game_config, temp_result)

    extra_turn = apply_turn_effects(state, temp_result, delta)
    result = finalize_result(temp_result, outcome, delta, state.player_points)

    return TurnOutcome(result=result, extra_turn=extra_turn)


def run_history_menu(state: TurnState) -> None:
    while True:
        print("\nHistory menu:")
        print("1) View last N rolls")
        print("2) Filter by sides (d6/d10/d20 etc)")
        print("3) Filter by number of dice")
        print("4) Show best roll ever")
        print("5) Back\n")

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            n = ask_int("How many last rolls? ", min_value=1)
            print_history(last_n(state.history, n))

        elif choice == "2":
            sides = ask_int("Enter sides (e.g., 6/10/20): ", min_value=2)
            print_history(filter_history(state.history, sides=sides))

        elif choice == "3":
            dice = ask_int("Enter number of dice: ", min_value=1)
            print_history(filter_history(state.history, dice=dice))

        elif choice == "4":
            print_best_roll(best_roll(state.history))

        elif choice == "5":
            return
        else:
            print("\nInvalid choice.\n")


def main() -> None:
    history_path = default_history_path()
    history = load_history(history_path)

    state = TurnState(
        game_config=GameConfig(),
        stats=Stats(),
        player_points=0,
        history_path=history_path,
        history=history,
    )

    print("--- Welcome to the Dice Rolling Game! ---")
    print(f"History file: {history_path.resolve()}")
    print(f"Loaded records: {len(state.history)}\n")

    while True:
        action = ask_menu_action()

        if action == "q":
            print("\nThank you for playing! Goodbye!\n")
            print_stats(state.stats, state.player_points)
            break

        if action == "h":
            run_history_menu(state)
            continue

        # action == "r"
        while True:
            outcome = play_turn(state)

            # PRINT
            print_turn_result(outcome.result)
            print_stats(state.stats, state.player_points)

            # SAVE (every roll)
            append_result(state.history_path, state.history, outcome.result)

            if not outcome.extra_turn:
                break

            print("🍀 Lucky mode match! Extra turn! 🎉 🎊\n")
