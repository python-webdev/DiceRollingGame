from dataclasses import dataclass


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
        self.lowest_total = (
            total if self.lowest_total is None else min(self.lowest_total, total)
        )
        if has_match:
            self.total_matches += 1

    @property
    def average_total(self) -> float:
        return 0.0 if self.roll_count == 0 else self.total_roll_value / self.roll_count


@dataclass
class OverallStats:
    """Statistics across all game sessions in the database."""

    total_rolls: int
    average_total: float | None
    total_matches: int
    highest_total: int | None
    lowest_total: int | None
