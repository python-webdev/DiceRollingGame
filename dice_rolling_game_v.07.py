import random
from typing import Final

# ---------- Config ----------
DICE_TYPES: Final[dict[str, int]] = {
    "D4": 4,
    "D6": 6,
    "D8": 8,
    "D10": 10,
    "D12": 12,
    "D20": 20,
}

MIN_DICE: Final[int] = 2
GAME_MODES: Final[set[str]] = {"classic", "lucky", "risk"}


# ---------- "Config objects" as dicts ----------
def make_game_config() -> dict:
    return {
        "points": {
            "win": 5,
            "lose": -3,
            "draw": 0,
            "lucky_match": 10,
            "risk_penalty": -3,
        },
        "thresholds": {
            "win_ratio": 0.75,
            "draw_ratio": 0.55,
            "risk_penalty_ratio": 0.35,
        },
    }


# ---------- Stats as dict ----------
def make_stats() -> dict:
    return {
        "roll_count": 0,
        "total_matches": 0,
        "total_roll_value": 0,
        "highest_total": 0,
        "lowest_total": None,  # type: int | None
    }


def update_stats(stats: dict, total: int, has_match: bool = False) -> None:
    stats["roll_count"] += 1
    stats["total_roll_value"] += total
    stats["highest_total"] = max(stats["highest_total"], total)
    stats["lowest_total"] = total if stats["lowest_total"] is None else min(
        stats["lowest_total"],
        total
    )
    if has_match:
        stats["total_matches"] += 1


def average_total(stats: dict) -> float:
    return 0.0 if stats["roll_count"] == 0 else stats["total_roll_value"] / stats["roll_count"]


# ---------- Input helpers ----------
def ask_yes_no(prompt: str) -> str:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "n"):
            return ans
        print("\nInvalid input. Please enter 'y' or 'n'.\n")


def ask_int(prompt: str, min_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")
            continue

        if min_value is not None and value < min_value:
            print(
                f"\nDice count must be at least {min_value}. Please try again.\n")
            continue

        return value


def choose_mode() -> str:
    while True:
        mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
        if mode in GAME_MODES:
            return mode
        print("\nInvalid mode. Please select a valid mode.\n")


def choose_dice_type() -> str:
    prompt = "Choose a dice type (D4, D6, D8, D10, D12, D20): "
    while True:
        dice_type = input(prompt).strip().upper()
        if dice_type in DICE_TYPES:
            return dice_type
        print("\nInvalid dice type. Please select a valid dice type.\n")


# ---------- Roll context/result as dict ----------
def make_roll_context(*, mode: str, dice_type: str, num_dice: int, sides: int) -> dict:
    return {
        "mode": mode,
        "dice_type": dice_type,
        "num_dice": num_dice,
        "sides": sides,
    }


def make_temp_result(context: dict, rolls: list[int], points_total: int) -> dict:
    return {
        "context": context,
        "rolls": rolls,
        "outcome": "",
        "points_delta": 0,
        "points_total": points_total,
    }


def total_of(result: dict) -> int:
    return sum(result["rolls"])


def has_match(result: dict) -> bool:
    rolls = result["rolls"]
    return bool(rolls) and len(set(rolls)) == 1


def is_lucky_match(result: dict) -> bool:
    return result["context"]["mode"] == "lucky" and has_match(result)


def is_risk(result: dict) -> bool:
    return result["context"]["mode"] == "risk"


def normalized_ratio(result: dict) -> float:
    ctx = result["context"]
    min_possible = ctx["num_dice"]
    max_possible = ctx["num_dice"] * ctx["sides"]

    if max_possible == min_possible:
        return 1.0

    return (total_of(result) - min_possible) / (max_possible - min_possible)


# ---------- Game logic ----------
def roll_dice(context: dict) -> list[int]:
    return [random.randint(1, context["sides"]) for _ in range(context["num_dice"])]


def determine_outcome(game_config: dict, result: dict) -> str:
    ratio = normalized_ratio(result)
    thresholds = game_config["thresholds"]

    if ratio >= thresholds["win_ratio"]:
        return "win"
    if ratio >= thresholds["draw_ratio"]:
        return "draw"
    return "lose"


def points_for_turn(game_config: dict, result: dict) -> int:
    points = game_config["points"]
    thresholds = game_config["thresholds"]

    # Lucky jackpot
    if is_lucky_match(result):
        return points["lucky_match"]

    # Risk penalty
    if is_risk(result):
        if normalized_ratio(result) < thresholds["risk_penalty_ratio"]:
            return points["risk_penalty"]

    # Otherwise: outcome points
    out = determine_outcome(game_config, result)
    if out == "win":
        return points["win"]
    if out == "lose":
        return points["lose"]
    return points["draw"]


# ---------- Printing ----------
def print_turn_result(result: dict) -> None:
    context_info = result["context"]
    rolls = result["rolls"]
    rolled_numbers = ", ".join(map(str, rolls))

    total_roll_value = total_of(result)
    match = has_match(result)

    print(f"\n🎲 You rolled: {rolled_numbers}")
    print(
        f"Dice: {context_info['num_dice']} × {context_info['dice_type']} (Total: {total_roll_value})")

    if match:
        label = "DOUBLES" if context_info["num_dice"] == 2 else "ALL MATCH"
        print(f"Match: {label} 🏆")
    else:
        print("Match: No")

    print(f"Outcome: {result['outcome'].upper()}")

    delta = result["points_delta"]
    if delta > 0:
        print(f"Points: +{delta}")
    elif delta < 0:
        print(f"Points: {delta}")
    else:
        print("Points: 0")


def print_stats(stats: dict, points_total: int) -> None:
    if stats["roll_count"] == 0:
        print("No rolls yet.\n")
        return

    lowest = stats['lowest_roll'] if stats['lowest_roll'] != float('inf') else 0
    lines = []
    if not hide_roll_count:
        lines.append(f"You have rolled the dice {roll_count} times.\n")

    lowest = stats["lowest_total"] if stats["lowest_total"] is not None else "-"
    lines = [
        "\n---- Stats ----",
        f"Completed rolls: {stats['roll_count']}",
        f"Total points: {points_total}",
        f"Average total: {average_total(stats):.2f}",
        f"Total matches: {stats['total_matches']}",
        f"Highest total: {stats['highest_total']}",
        f"Lowest total: {lowest}",
        "----------------",
    ]
    print("\n".join(lines))
    print()


# ---------- Turn / State ----------
def make_state() -> dict:
    return {
        "game_config": make_game_config(),
        "stats": make_stats(),
        "player_points": 0,
    }


def get_roll_context() -> dict:
    num_dice = ask_int(
        "How many dice would you like to roll? ", min_value=MIN_DICE)
    mode = choose_mode()
    dice_type = choose_dice_type()
    sides = DICE_TYPES[dice_type]
    return make_roll_context(mode=mode, dice_type=dice_type, num_dice=num_dice, sides=sides)


def resolve_turn(game_config: dict, temp_result: dict) -> tuple[str, int]:
    out = determine_outcome(game_config, temp_result)
    delta = points_for_turn(game_config, temp_result)
    return out, delta


def apply_turn_effects(state: dict, temp_result: dict, delta: int) -> bool:
    """
    Mutates state (points + stats) and returns extra_turn (bool).
    """
    extra_turn = is_lucky_match(temp_result)

    state["player_points"] += delta
    update_stats(state["stats"], total_of(temp_result), has_match(temp_result))

    return extra_turn


def finalize_result(temp_result: dict, outcome: str, delta: int, points_total: int) -> dict:
    return {
        "context": temp_result["context"],
        "rolls": temp_result["rolls"],
        "outcome": outcome,
        "points_delta": delta,
        "points_total": points_total,
    }


def play_turn(state: dict) -> dict:
    context = get_roll_context()
    rolls = roll_dice(context)

    temp_result = make_temp_result(context, rolls, state["player_points"])
    outcome, delta = resolve_turn(state["game_config"], temp_result)

    extra_turn = apply_turn_effects(state, temp_result, delta)
    result = finalize_result(
        temp_result, outcome,
        delta, state["player_points"]
    )

    return {"result": result, "extra_turn": extra_turn}


def main() -> None:
    state = make_state()

    print("--- Welcome to the Dice Rolling Game! ---")

    while True:
        if ask_yes_no("Roll the dice? (y/n): ") == "n":
            print("\nThank you for playing! Goodbye!\n")
            print_stats(state["stats"], state["player_points"])
            break

        while True:
            outcome = play_turn(state)

            print_turn_result(outcome["result"])
            print_stats(state["stats"], state["player_points"])

            if not outcome["extra_turn"]:
                break

            print("🍀 Lucky mode match! Extra turn! 🎉 🎊\n")


if __name__ == "__main__":
    main()
