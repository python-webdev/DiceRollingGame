from __future__ import annotations

from dataclasses import dataclass

from .config import GameConfig
from .modes import GameMode
from .stats import Stats


@dataclass(frozen=True)
class RollContext:
    game_session_id: str
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

        if max_possible == min_possible:
            return 1.0

        return (self.total - min_possible) / (max_possible - min_possible)


@dataclass
class TurnState:
    game_config: GameConfig
    player_points: int = 0
    stats: Stats | None = None


@dataclass(frozen=True)
class TurnOutcome:
    result: RollResult
    extra_turn: bool
