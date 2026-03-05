from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .config import GameConfig
from .logic import determine_outcome, roll_dice, points_for_turn
from .models import RollContext, RollResult


@dataclass(frozen=True)
class SimulationInputs:
    trials: int
    dice: int
    sides: int


@dataclass(frozen=True)
class SimulationCounts:
    match_count: int
    outcome_counts: dict[str, int]          # win/draw/lose
    total_distribution: dict[int, int]      # total -> frequency


@dataclass(frozen=True)
class SimulationAverages:
    avg_total: float
    avg_points_delta: float


@dataclass(frozen=True)
class SimulationReport:
    config: SimulationInputs
    counts: SimulationCounts
    averages: SimulationAverages

    @property
    def match_probability(self) -> float:
        return 0.0 if self.config.trials == 0 else self.counts.match_count / self.config.trials

    @classmethod
    def empty(cls, context: RollContext):
        """Creates a zeroed-out report for invalid trial counts."""
        return cls(
            config=SimulationInputs(0, context.num_dice, context.sides),
            counts=SimulationCounts(0, {"win": 0, "draw": 0, "lose": 0}, {}),
            averages=SimulationAverages(0.0, 0.0)
        )


def simulate(
    *,
    game_config: GameConfig,
    context: RollContext,
    trials: int,
) -> SimulationReport:
    # 1. Define common input metadata
    config = SimulationInputs(
        trials=max(0, trials),
        dice=context.num_dice,
        sides=context.sides
    )

    # 2. Guard Clause for zero/negative trials
    if trials <= 0:
        return SimulationReport(
            config=config,
            counts=SimulationCounts(0, {"win": 0, "draw": 0, "lose": 0}, {}),
            averages=SimulationAverages(0.0, 0.0)
        )

    # 3. Simulation Logic
    match_count = 0
    outcome_counter: Counter[str] = Counter()
    total_counter: Counter[int] = Counter()
    total_sum = 0
    points_sum = 0

    for _ in range(trials):
        rolls = roll_dice(context)

        # Creating a temporary result to calculate metrics
        temp = RollResult(
            context=context,
            rolls=rolls,
            outcome="",
            points_delta=0,
            points_total=0,
        )

        outcome = determine_outcome(game_config, temp)
        delta = points_for_turn(game_config, temp)

        outcome_counter[outcome] += 1
        total_counter[temp.total] += 1
        total_sum += temp.total
        points_sum += delta

        if temp.has_match:
            match_count += 1

    # 4. Final Assembly
    return SimulationReport(
        config=config,
        counts=SimulationCounts(
            match_count=match_count,
            outcome_counts=dict(outcome_counter),
            total_distribution=dict(total_counter)
        ),
        averages=SimulationAverages(
            avg_total=total_sum / trials,
            avg_points_delta=points_sum / trials
        )
    )
