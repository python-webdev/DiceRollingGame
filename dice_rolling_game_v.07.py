import random
from dataclasses import dataclass


# ---------- Config ----------

dice_types: dict[str, int] = {
    "D4": 4,
    "D6": 6,
    "D8": 8,
    "D10": 10,
    "D12": 12,
    "D20": 20,
}

game_modes: set[str] = {"classic", "lucky", "risk"}
min_dice: int = 2


@dataclass(frozen=True)
class GameConfig:
    # Outcome thresholds (normalized 0..1 across min..max range)
    win_ratio: float = 0.75
    draw_ratio: float = 0.55

    # Risk mode threshold (normalized). Below this => penalty.
    risk_penalty_ratio: float = 0.35

    # Points rules
    points_win: int = 5
    points_lose: int = -3
    points_draw: int = 0
    points_lucky_match: int = 10
    points_risk_penalty: int = -3


# ---------- Stats + Result ----------

@dataclass
class Stats:
    roll_count: int = 0
    total_roll_value: int = 0
    total_matches: int = 0  # "all dice match"
    highest_total: int = 0
    lowest_total: int = 10**9  # large sentinel

    def update(self, total: int, has_match: bool) -> None:
        self.roll_count += 1
        self.total_roll_value += total
        self.highest_total = max(self.highest_total, total)
        self.lowest_total = min(self.lowest_total, total)
        if has_match:
            self.total_matches += 1

    @property
    def average_total(self) -> float:
        return 0.0 if self.roll_count == 0 else self.total_roll_value / self.roll_count


@dataclass(frozen=True)
class TurnResult:
    mode: str
    dice_type: str
    num_dice: int
    sides: int
    rolls: list[int]
    total: int
    has_match: bool
    outcome: str
    points_delta: int
    points_total: int


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


def choose_mode() -> str:
    while True:
        mode = input("Choose a mode (Classic/Lucky/Risk): ").strip().lower()
        if mode in game_modes:
            return mode
        print("\nInvalid mode. Please select a valid mode.\n")


def choose_dice_type() -> str:
    prompt = "Choose a dice type (D4, D6, D8, D10, D12, D20): "
    while True:
        dice_type = input(prompt).strip().upper()
        if dice_type in dice_types:
            return dice_type
        print("\nInvalid dice type. Please select a valid dice type.\n")


# ---------- Game logic ----------

def roll_dice(num_dice: int, sides: int) -> list[int]:
    return [random.randint(1, sides) for _ in range(num_dice)]


def all_match(rolls: list[int]) -> bool:
    # For 2 dice this means doubles; for 3+ it means all dice identical.
    return len(set(rolls)) == 1


def normalized_ratio(total: int, num_dice: int, sides: int) -> float:
    """
    Normalize total into 0..1 based on min..max possible totals.
    min_total = num_dice (all 1s)
    max_total = num_dice * sides
    """
    min_total = num_dice
    max_total = num_dice * sides
    span = max_total - min_total
    if span == 0:
        return 0.5  # arbitrary "middle" if range is degenerate
    return (total - min_total) / span


def determine_outcome(cfg: GameConfig, total: int, num_dice: int, sides: int) -> str:
    r = normalized_ratio(total, num_dice, sides)
    if r >= cfg.win_ratio:
        return "win"
    if r >= cfg.draw_ratio:
        return "draw"
    return "lose"


def points_for_turn(
    cfg: GameConfig,
    mode: str,
    total: int,
    num_dice: int,
    sides: int,
    has_match: bool,
) -> int:
    # Lucky jackpot
    if mode == "lucky" and has_match:
        return cfg.points_lucky_match

    # Risk penalty (based on range, not fixed "7")
    if mode == "risk":
        r = normalized_ratio(total, num_dice, sides)
        if r < cfg.risk_penalty_ratio:
            return cfg.points_risk_penalty

    # Otherwise: outcome points
    out = determine_outcome(cfg, total, num_dice, sides)
    if out == "win":
        return cfg.points_win
    if out == "lose":
        return cfg.points_lose
    return cfg.points_draw


# ---------- Printing ----------

def print_turn_result(result: TurnResult) -> None:
    rolled_numbers = ", ".join(map(str, result.rolls))
    print(f"\n🎲 You rolled: {rolled_numbers}")
    print(f"Dice: {result.num_dice} × {result.dice_type} (Total: {result.total})")

    if result.has_match:
        label = "DOUBLES" if result.num_dice == 2 else "ALL MATCH"
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


def print_stats(stats: Stats, points_total: int) -> None:
    if stats.roll_count == 0:
        return

    print("---- Stats ----")
    print(f"Completed rolls: {stats.roll_count}")
    print(f"Total points: {points_total}")
    print(f"Average total: {stats.average_total:.2f}")
    print(f"Total matches: {stats.total_matches}")
    print(f"Highest total: {stats.highest_total}")
    print(f"Lowest total: {stats.lowest_total}")
    print("---------------\n")


# ---------- Main ----------

def main() -> None:
    cfg = GameConfig()
    stats = Stats()
    player_points = 0

    print("--- Welcome to the Dice Rolling Game! ---\n")

    while True:
        user_input = ask_yes_no("Roll the dice? (y/n): ")
        if user_input == "n":
            print("\nThank you for playing! Goodbye!\n")
            print_stats(stats, player_points)
            break

        num_dice = ask_int(
            "How many dice would you like to roll? ", min_value=min_dice)
        mode = choose_mode()
        dice_type = choose_dice_type()
        sides = dice_types[dice_type]

        rolls = roll_dice(num_dice, sides)
        total = sum(rolls)
        has_match = all_match(rolls)

        outcome = determine_outcome(cfg, total, num_dice, sides)
        delta = points_for_turn(cfg, mode, total, num_dice, sides, has_match)
        player_points += delta

        stats.update(total, has_match)

        result = TurnResult(
            mode=mode,
            dice_type=dice_type,
            num_dice=num_dice,
            sides=sides,
            rolls=rolls,
            total=total,
            has_match=has_match,
            outcome=outcome,
            points_delta=delta,
            points_total=player_points,
        )

        print_turn_result(result)
        print_stats(stats, player_points)

        # Lucky mode: if all dice match => immediate extra turn
        if mode == "lucky" and has_match:
            print("🍀 Lucky mode match! Extra turn!\n")
            continue


if __name__ == "__main__":
    main()
