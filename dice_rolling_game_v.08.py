import random
from dataclasses import dataclass
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

GAME_MODES: Final[set[str]] = {"classic", "lucky", "risk"}
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
    points: PointsConfig = PointsConfig()
    thresholds: ThresholdConfig = ThresholdConfig()


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
    lowest_total: int = 10**9  # sentinel

    def update(self, total: int, has_match: bool = False, count_roll: bool = True) -> None:
        if has_match:
            self.total_matches += 1

        if not count_roll:
            return
        self.roll_count += 1
        self.total_roll_value += total
        self.highest_total = max(self.highest_total, total)
        self.lowest_total = min(self.lowest_total, total)

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


def choose_mode() -> GameMode:
    while True:
        mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
        if mode in GAME_MODES:
            return GameMode[mode.upper()]
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
        print(f"Match: {label} ✅")
    else:
        print("Match: no")

    print(f"Outcome: {result.outcome.upper()}")

    if result.points_delta > 0:
        print(f"Points: +{result.points_delta}")
    elif result.points_delta < 0:
        print(f"Points: {result.points_delta}")
    else:
        print("Points: 0")

    print(f"Total points: {result.points_total}\n")


def print_stats(stats: Stats, points_total: int, hide_roll_count: bool = False) -> None:
    if stats.roll_count == 0:
        print("No rolls yet.\n")
        return
    lines = []
    if not hide_roll_count:
        lines.append(f"You have rolled the dice {stats.roll_count} times.\n")

    lines.extend([
        "---- Stats ----",
        f"Completed rolls: {stats.roll_count}",
        f"Total points: {points_total}",
        f"Average total: {stats.average_total:.2f}",
        f"Total matches: {stats.total_matches}",
        f"Highest total: {stats.highest_total}",
        f"Lowest total: {stats.lowest_total}",
        '----------------',
    ])
    print(f"{'\n'.join(lines)}\n")


# ---------- Main ----------
def main() -> None:
    game_config = GameConfig()
    stats = Stats()
    player_points = 0

    print("--- Welcome to the Dice Rolling Game! ---")

    while True:
        user_input = ask_yes_no("Roll the dice? (y/n): ")
        if user_input == "n":
            print("\nThank you for playing! Goodbye!\n")
            print_stats(stats, player_points)
            break

        num_dice = ask_int(
            "How many dice would you like to roll? ", min_value=MIN_DICE)
        mode = choose_mode()
        dice_type = choose_dice_type()
        sides = DICE_TYPES[dice_type]

        context = RollContext(mode=mode, dice_type=dice_type,
                              num_dice=num_dice, sides=sides)
        rolls = roll_dice(context)
        # total = sum(rolls)
        temp_result = RollResult(
            context=context,
            rolls=rolls,
            outcome="",
            points_delta=0,
            points_total=player_points,
        )
        has_match = temp_result.has_match
        count_roll = not (mode == GameMode.LUCKY and has_match)

        outcome = determine_outcome(game_config, temp_result)
        delta = points_for_turn(game_config, temp_result)
        player_points += delta

        stats.update(temp_result.total, has_match, count_roll=count_roll)

        result = RollResult(
            context=context,
            rolls=rolls,
            outcome=outcome,
            points_delta=delta,
            points_total=player_points,
        )

        print_turn_result(result)
        print_stats(stats, player_points, hide_roll_count=(
            mode == GameMode.LUCKY and has_match))

        # Lucky mode: if all dice match => immediate extra turn
        if mode == GameMode.LUCKY and has_match:
            print("🍀 Lucky mode match! Extra turn!\n")
            continue


if __name__ == "__main__":
    main()
