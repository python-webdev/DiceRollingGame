from .domain.config import GameConfig
from .domain.models import TurnOutcome, TurnState
from .domain.stats import Stats
from .cli.ui import (
    ask_int,
    ask_menu_action,
    get_roll_context,
    ask_simulation_trials,
)
from .services.logic import (
    roll_dice,
    build_temp_result,
    resolve_turn,
    apply_turn_effects,
    finalize_result,
)
from .cli.printing import (
    print_turn_result,
    print_stats,
    print_history,
    print_best_roll,
    print_simulation_report,
    print_distribution_sorted,
)

from .services.simulation import simulate
from .storage.sqlite_storage import (
    clear_rolls,
    init_db,
    save_roll,
    last_rolls,
    filter_rolls,
    best_roll as best_roll_db,
)


def play_turn(state: TurnState) -> TurnOutcome:
    context = get_roll_context()
    rolls = roll_dice(context)

    temp_result = build_temp_result(context, rolls, state.player_points)
    outcome, delta = resolve_turn(state.game_config, temp_result)

    extra_turn = apply_turn_effects(state, temp_result, delta)
    result = finalize_result(temp_result, outcome, delta, state.player_points)

    return TurnOutcome(result=result, extra_turn=extra_turn)


def run_history_menu() -> None:
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
            print_history(last_rolls(n))

        elif choice == "2":
            sides = ask_int("Enter sides (e.g., 6/10/20): ", min_value=2)
            print_history(filter_rolls(sides=sides))

        elif choice == "3":
            dice = ask_int("Enter number of dice: ", min_value=1)
            print_history(filter_rolls(dice=dice))

        elif choice == "4":
            print_best_roll(best_roll_db())

        elif choice == "5":
            return
        else:
            print("\nInvalid choice.\n")


def main() -> None:
    init_db()

    state = TurnState(
        game_config=GameConfig(),
        stats=Stats(),
        player_points=0,
    )

    print("--- Welcome to the Dice Rolling Game! ---")

    while True:
        action = ask_menu_action()

        if action == "s":
            context = get_roll_context()

            trials = ask_simulation_trials()
            report = simulate(
                game_config=state.game_config,
                context=context,
                trials=trials,
            )
            print_simulation_report(report, top_n_totals=10)
            print_distribution_sorted(report)
            continue

        if action == "q":
            print("\nThank you for playing! Goodbye!\n")
            print_stats(state.stats, state.player_points)
            break

        if action == "c":
            confirm = input(
                "\nAre you sure you want to clear history? This cannot be undone. (y/n): ").strip().lower()
            if confirm == "y":
                deleted = clear_rolls(reset_ids=True)
                print(f"\nHistory cleared. Deleted {deleted} records.\n")
            else:
                print("\nClear history cancelled.\n")
            continue

        if action == "h":
            run_history_menu()
            continue

        while True:
            outcome = play_turn(state)

            # PRINT
            print_turn_result(outcome.result)
            print_stats(state.stats, state.player_points)

            # SAVE (every roll)
            save_roll(outcome.result)

            if not outcome.extra_turn:
                break

            print("🍀 Lucky mode match! Extra turn! 🎉 🎊\n")
