from .cli.printing import (
    print_best_roll,
    print_distribution_sorted,
    print_history,
    print_history_page_info,
    print_session_stats,
    print_simulation_report,
    print_turn_result,
)
from .cli.printing import (
    print_overall_stats as print_overall_stats_from_db,
)
from .cli.ui import (
    ask_int,
    ask_menu_action,
    ask_simulation_trials,
    get_roll_context,
)
from .domain.config import GameConfig
from .domain.models import TurnOutcome, TurnState
from .domain.stats import Stats
from .services.logic import (
    apply_turn_effects,
    build_temp_result,
    finalize_result,
    resolve_turn,
    roll_dice,
)
from .services.simulation import simulate
from .storage.connection import init_db
from .storage.roll_repository import (
    best_roll as best_roll_db,
)
from .storage.roll_repository import (
    clear_rolls,
    count_rolls,
    export_rolls_to_csv,
    paginated_rolls,
    save_roll,
)
from .storage.roll_repository import (
    overall_stats as overall_stats_db,
)
from .storage.session_repository import create_game_session


def play_turn(state: TurnState) -> TurnOutcome:
    context = get_roll_context(state.game_session_id)
    rolls = roll_dice(context)

    temp_result = build_temp_result(context, rolls, state.player_points)
    outcome, delta = resolve_turn(state.game_config, temp_result)

    extra_turn = apply_turn_effects(state, temp_result, delta)
    result = finalize_result(temp_result, outcome, delta, state.player_points)

    return TurnOutcome(result=result, extra_turn=extra_turn)


def browse_history_paginated(
    *,
    page_size: int = 10,
    sides: int | None = None,
    dice: int | None = None,
) -> None:
    total = count_rolls(sides=sides, dice=dice)

    if total == 0:
        print("\nNo history records found.\n")
        return

    offset = 0

    while True:
        records = paginated_rolls(
            offset=offset,
            limit=page_size,
            sides=sides,
            dice=dice,
        )

        print_history_page_info(
            offset=offset,
            page_size=page_size,
            total=total,
        )
        print_history(records)

        commands: list[str] = []
        if offset + page_size < total:
            commands.append("n)ext page")
        if offset > 0:
            commands.append("p)revious page")
        commands.append("q)uit")

        print(", ".join(commands))
        choice = input("Choose: ").strip().lower()

        if choice == "n":
            if offset + page_size < total:
                offset += page_size
            else:
                print("\nAlready at the last page.\n")

        elif choice == "p":
            if offset > 0:
                offset = max(0, offset - page_size)
            else:
                print("\nAlready at the first page.\n")

        elif choice == "q":
            return
        else:
            print("\nInvalid choice.\n")


def run_history_menu() -> None:
    while True:
        print("\nHistory menu:")
        print("1) View paginated history")
        print("2) Filter by sides (e.g., 4/6/8)")
        print("3) Filter by number of dice")
        print("4) Show best roll ever")
        print("5) Back\n")

        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            browse_history_paginated(page_size=10)

        elif choice == "2":
            sides = ask_int("Enter sides (e.g., 4/6/8): ", min_value=2)
            browse_history_paginated(page_size=10, sides=sides)

        elif choice == "3":
            dice = ask_int("Enter number of dice: ", min_value=1)
            browse_history_paginated(page_size=10, dice=dice)

        elif choice == "4":
            print_best_roll(best_roll_db())

        elif choice == "5":
            return
        else:
            print("\nInvalid choice.\n")


def main() -> None:
    init_db()

    # Create a new game session
    session = create_game_session()

    state = TurnState(
        game_config=GameConfig(),
        game_session_id=session["id"],
        stats=Stats(),
        player_points=0,
    )

    print("--- Welcome to the Dice Rolling Game! ---")

    while True:
        action = ask_menu_action()

        if action == "s":
            context = get_roll_context(state.game_session_id)

            trials = ask_simulation_trials()
            report = simulate(
                game_config=state.game_config,
                context=context,
                trials=trials,
            )
            print_simulation_report(report, top_n_totals=10)
            print_distribution_sorted(report)
            continue

        if action == "t":
            stats_data = overall_stats_db()
            print_overall_stats_from_db(stats_data)
            continue

        if action == "q":
            print("\nThank you for playing! Goodbye!\n")
            print_session_stats(state.stats, state.player_points)
            break

        if action == "c":
            confirm = (
                input(
                    "\nAre you sure you want to clear history? This cannot be undone. (y/n): "
                )
                .strip()
                .lower()
            )
            if confirm == "y":
                deleted = clear_rolls(reset_ids=True)
                print(f"\nHistory cleared. Deleted {deleted} records.\n")
            else:
                print("\nClear history cancelled.\n")
            continue

        if action == "h":
            run_history_menu()
            continue

        if action == "e":
            export = export_rolls_to_csv()

            if export == 0:
                print("\nNo history to export.\n")
            else:
                config = GameConfig()
                export_path = config.exports.export_path
                print(f"\nHistory exported: {export} records to '{export_path}'.\n")
            continue

        while True:
            outcome = play_turn(state)

            # PRINT
            print_turn_result(outcome.result)
            print_session_stats(state.stats, state.player_points)

            # SAVE (every roll)
            save_roll(outcome.result)

            if not outcome.extra_turn:
                break

            print("🍀 Lucky mode match! Extra turn! 🎉 🎊\n")
