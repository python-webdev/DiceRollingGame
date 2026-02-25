from dataclasses import dataclass
from typing import ClassVar, Set


@dataclass(frozen=True)
class DiceGameRules:
    MODES: ClassVar[Set[str]] = {"classic", "lucky", "risk"}

    def outcome_from_total(self, total: int) -> str:
        """Return 'win', 'draw', or 'lose' based on your rule."""
        if total > 10:
            return "win"
        if total == 10:
            return "draw"
        return "lose"

    def apply_points(self, mode: str, total: int, has_match: bool) -> int:
        """
        Returns point delta for this turn.
        Point rules:
        +10 for doubles (lucky mode extra turn)
        +5 if total > 10 (we'll interpret as win condition in your current code: total > 10 -> +5)
        -3 if total < 5 / losing / risky (<7)
        """
        if mode == "lucky" and has_match:
            return 10

        if mode == "risk" and total < 7:
            return -3

        # In your current code: win => +5, lose => -3, draw => 0
        out = self.outcome_from_total(total)
        if out == "win":
            return 5
        if out == "lose":
            return -3
        return 0


rules = DiceGameRules()
modes = DiceGameRules.MODES
