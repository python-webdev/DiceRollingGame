from dataclasses import dataclass


@dataclass
class Stats:
    roll_count: int = 0
    total_doubles: int = 0
    total_roll_value: int = 0
    highest_roll: int = 0
    lowest_roll: int | None = None

    def update(self, total: int, has_match: bool) -> None:
        self.roll_count += 1
        self.total_roll_value += total
        self.highest_roll = max(self.highest_roll, total)
        self.lowest_roll = total if self.lowest_roll is None else min(
            self.lowest_roll, total)
        if has_match:
            self.total_doubles += 1

    def average(self) -> float:
        return (self.total_roll_value / self.roll_count) if self.roll_count else 0.0

    def summary_lines(self) -> list[str]:
        if self.roll_count == 0:
            return ["No rolls yet."]
        return [
            f"You have rolled the dice {self.roll_count} times.",
            f"Average roll value: {self.average():.2f}",
            f"Total doubles rolled: {self.total_doubles}",
            f"Highest roll: {self.highest_roll}",
            f"Lowest roll: {self.lowest_roll if self.lowest_roll is not None else 'Not a number'}",
        ]
