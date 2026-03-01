import random
from dataclasses import dataclass, field
from typing import Final
from enum import Enum, auto


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


# ---------- Game Config ----------
@dataclass(frozen=True)
class PointsConfig:
    win: int = 5
    lose: int = -3
    draw: int = 0
    lucky_match: int = 10
    risk_penalty: int = -3


@dataclass(frozen=True)
class ThresholdConfig:
    win_ratio: float = 0.75
    draw_ratio: float = 0.55
    risk_penalty_ratio: float = 0.35


@dataclass(frozen=True)
class GameConfig:
    points: PointsConfig = field(default_factory=PointsConfig)
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)


# ---------- Game Modes ----------
class GameMode(Enum):
    CLASSIC = auto()
    LUCKY = auto()
    RISK = auto()


# ---------- Stats ----------
@dataclass
class Stats:
    roll_count: int = 0
    total_matches: int = 0  # "all dice match"
    total_roll_value: int = 0
    highest_total: int = 0
    lowest_total: int | None = None

    def update(self, total: int, has_match: bool = False) -> None:
        self.roll_count += 1
        self.total_roll_value += total
        self.highest_total = max(self.highest_total, total)
        self.lowest_total = total if self.lowest_total is None else min(
            self.lowest_total, total)
        if has_match:
            self.total_matches += 1

    @property
    def average_total(self) -> float:
        return 0.0 if self.roll_count == 0 else self.total_roll_value / self.roll_count


# ---------- Results ----------
@dataclass(frozen=True)
class RollContext:
    mode: GameMode
    dice_type: str
    num_dice: int
    sides: int


@dataclass(frozen=True)
class RollResult:
    context: RollContext
    rolls: list[int]
    outcome: str
    points_delta: int
    points_total: int

    @property
    def total(self) -> int:
        return sum(self.rolls)

    @property
    def has_match(self) -> bool:
        return bool(self.rolls) and len(set(self.rolls)) == 1

    @property
    def is_lucky_match(self) -> bool:
        return self.context.mode == GameMode.LUCKY and self.has_match

    @property
    def is_risk(self) -> bool:
        return self.context.mode == GameMode.RISK

    @property
    def normalized_ratio(self) -> float:
        """Returns the roll quality from 0.0 (all 1s) to 1.0 (all max)."""
        min_possible = self.context.num_dice
        max_possible = self.context.num_dice * self.context.sides

        # Avoid division by zero (though num_dice should be >= 1)
        if max_possible == min_possible:
            return 1.0

        return (self.total - min_possible) / (max_possible - min_possible)


@dataclass
class TurnState:
    game_config: GameConfig
    stats: Stats
    player_points: int = 0


@dataclass(frozen=True)
class TurnOutcome:
    result: RollResult
    extra_turn: bool

# ---------- Input helpers ----------


def ask_yes_no(prompt: str) -> str:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "n"):
            return ans
        print("\nInvalid input. Please enter 'y' or 'n'.\n")


def ask_int(prompt: str, *, min_value: int | None = None) -> int:
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


def choose_mode() -> GameMode:
    while True:
        mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
        try:
            return GameMode[mode.upper()]
        except KeyError:
            print("\nInvalid mode. Please select a valid mode.\n")


def choose_dice_type() -> str:
    prompt = "Choose a dice type (D4, D6, D8, D10, D12, D20): "
    while True:
        dice_type = input(prompt).strip().upper()
        if dice_type in DICE_TYPES:
            return dice_type
        print("\nInvalid dice type. Please select a valid dice type.\n")


# ---------- Game logic ----------
def roll_dice(context: RollContext) -> list[int]:
    return [random.randint(1, context.sides) for _ in range(context.num_dice)]


def determine_outcome(game_config: GameConfig, result: RollResult) -> str:
    ratio = result.normalized_ratio

    if ratio >= game_config.thresholds.win_ratio:
        return "win"
    if ratio >= game_config.thresholds.draw_ratio:
        return "draw"
    return "lose"


def points_for_turn(
    game_config: GameConfig,
    result: RollResult,
) -> int:
    # Lucky jackpot
    if result.is_lucky_match:
        return game_config.points.lucky_match

    # Risk penalty (based on range, not fixed number)
    if result.is_risk:
        if result.normalized_ratio < game_config.thresholds.risk_penalty_ratio:
            return game_config.points.risk_penalty

    # Otherwise: outcome points
    outcome = determine_outcome(game_config, result)
    if outcome == "win":
        return game_config.points.win
    if outcome == "lose":
        return game_config.points.lose
    return game_config.points.draw


# ---------- Printing ----------
def print_turn_result(result: RollResult) -> None:
    rolled_numbers = ", ".join(map(str, result.rolls))
    print(f"\n🎲 You rolled: {rolled_numbers}")
    print(
        f"Dice: {result.context.num_dice} × {result.context.dice_type} (Total: {result.total})")

    if result.has_match:
        label = "DOUBLES" if result.context.num_dice == 2 else "ALL MATCH"
        print(f"Match: {label} 🏆")
    else:
        print("Match: No")

    print(f"Outcome: {result.outcome.upper()}")

    if result.points_delta > 0:
        print(f"Points: +{result.points_delta}")
    elif result.points_delta < 0:
        print(f"Points: {result.points_delta}")
    else:
        print("Points: 0")


def print_stats(stats: Stats, points_total: int) -> None:
    if stats.roll_count == 0:
        print("No rolls yet.\n")
        return

    lowest = stats.lowest_total if stats.lowest_total is not None else "-"
    lines = [
        "\n---- Stats ----",
        f"Completed rolls: {stats.roll_count}",
        f"Total points: {points_total}",
        f"Average total: {stats.average_total:.2f}",
        f"Total matches: {stats.total_matches}",
        f"Highest total: {stats.highest_total}",
        f"Lowest total: {lowest}",
        "----------------",
    ]
    print("\n".join(lines))
    print()


# ---------- Main ----------
def get_roll_context() -> RollContext:
    num_dice = ask_int(
        "How many dice would you like to roll? ", min_value=MIN_DICE)
    mode = choose_mode()
    dice_type = choose_dice_type()
    sides = DICE_TYPES[dice_type]
    return RollContext(mode=mode, dice_type=dice_type, num_dice=num_dice, sides=sides)


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


def apply_turn_effects(
        state: TurnState,
        temp_result: RollResult,
        delta: int,
) -> bool:
    """
    Mutates state (points + stats)
    and returns extra_turn (bool)
    """
    extra_turn = temp_result.is_lucky_match

    state.player_points += delta
    state.stats.update(
        temp_result.total,
        temp_result.has_match,
    )
    return extra_turn


def finalize_result(
    temp_result: RollResult,
    outcome: str,
    delta: int,
    player_points: int,
) -> RollResult:
    return RollResult(
        context=temp_result.context,
        rolls=temp_result.rolls,
        outcome=outcome,
        points_delta=delta,
        points_total=player_points,
    )


def play_turn(
    state: TurnState,
) -> TurnOutcome:
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


if __name__ == "__main__":
    main()
