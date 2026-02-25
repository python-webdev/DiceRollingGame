# src/dice_game/main.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .dice import Dice
from .rules import DiceGameRules
from .stats import Stats
from .ui import GameUI

MIN_DICE = 2


class UIProtocol(Protocol):
    @classmethod
    def ask_yes_no(cls, prompt: str) -> str: ...

    @classmethod
    def ask_int(cls, prompt: str, *, min_value: int | None = None) -> int: ...

    @classmethod
    def choose_mode(cls) -> str: ...

    @classmethod
    def choose_dice_sides(cls) -> int: ...

    @classmethod
    def format_rolls(cls, rolls: list[int]) -> str: ...


@dataclass
class TurnDisplay:
    mode: str
    rolls: list[int]
    total: int
    has_match: bool
    delta: int
    points: int


def print_turn_outcome(turn: TurnDisplay) -> bool:
    rolled_numbers = GameUI.format_rolls(turn.rolls)

    if turn.mode == "lucky" and turn.has_match:
        print(
            f"\nYou rolled: {rolled_numbers} (Doubles! You get an extra turn!)")
        return True

    out = DiceGameRules().outcome_from_total(turn.total)

    if turn.mode == "risk" and turn.total < 7:
        print(f"\nYou rolled: {rolled_numbers} (Risky! You lose points!)")
    elif out == "win":
        print(f"\nYou rolled: {rolled_numbers} (Congratulations! You win!)")
    elif out == "draw":
        print(f"\nYou rolled: {rolled_numbers} (It's a draw! Try again!)")
    else:
        print(f"\nYou rolled: {rolled_numbers} (Sorry, you lose!)")

    return False


def print_turn_points(delta: int, points: int, total: int) -> None:
    if delta > 0:
        print(f"Points +{delta}. Your current points: {points}")
    elif delta < 0:
        print(f"Points {delta}. Your current points: {points}")
    else:
        print(f"Your current points: {points}")

    print(f"Total score: {total}\n")


def print_turn(turn: TurnDisplay) -> None:
    print_turn_outcome(turn)
    print_turn_points(turn.delta, turn.points, turn.total)


class DiceGame:
    def __init__(
        self,
        *,
        ui: type[UIProtocol] | None = None,
        min_dice: int = MIN_DICE,
        stats: Stats | None = None,
    ) -> None:
        self.ui: type[UIProtocol] = ui if ui is not None else GameUI
        self.min_dice = min_dice
        self.stats = stats if stats is not None else Stats()
        self.player_points = 0

    def print_progress(self) -> None:
        for line in self.stats.summary_lines():
            print(line)
        print(f"Current points: {self.player_points}\n")

    def print_goodbye(self) -> None:
        print("\nThank you for playing! Goodbye!\n")
        for line in self.stats.summary_lines():
            print(line)
        print(f"Final points: {self.player_points}\n")

    def play_turn(self) -> bool:
        num_dice = self.ui.ask_int(
            "How many dice would you like to roll? ", min_value=self.min_dice)
        mode = self.ui.choose_mode()
        sides = self.ui.choose_dice_sides()

        dice = Dice(type=f"D{sides}")
        rolls = dice.roll_dice(num_dice)
        total = sum(rolls)
        has_match = dice.all_match(rolls)

        delta = DiceGameRules().apply_points(mode, total, has_match)
        self.player_points += delta

        self.stats.update(total, has_match)

        turn = TurnDisplay(
            mode=mode,
            rolls=rolls,
            total=total,
            has_match=has_match,
            delta=delta,
            points=self.player_points,
        )
        print_turn(turn)
        self.print_progress()

        return mode == "lucky" and has_match

    def run(self) -> None:
        while True:
            choice = self.ui.ask_yes_no("Roll the dice? (y/n): ")
            if choice == "n":
                self.print_goodbye()
                break

            should_repeat = self.play_turn()
            if should_repeat:
                continue


def main() -> None:
    game = DiceGame()
    game.run()


if __name__ == "__main__":
    main()
