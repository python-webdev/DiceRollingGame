from dataclasses import dataclass


@dataclass
class Stats:
    roll_count: int = 0
    total_doubles: int = 0
    total_roll_value: int = 0
    highest_roll: int = 0
    lowest_roll: int | None = None

    def update(self, total: int, *, count_roll: bool = True, has_match: bool = False) -> None:
        if has_match:
            self.total_doubles += 1

        if not count_roll:
            return

        self.roll_count += 1
        self.total_roll_value += total
        self.highest_roll = max(self.highest_roll, total)
        self.lowest_roll = (
            total if self.lowest_roll is None else min(self.lowest_roll, total))

    def average(self) -> float:
        return (self.total_roll_value / self.roll_count) if self.roll_count else 0.0

    def summary_lines(self, *, hide_roll_count: bool = False) -> list[str]:
        if self.roll_count == 0:
            return ["No rolls yet."]
        lines = []
        if not hide_roll_count:
            lines.append(f"You have rolled the dice {self.roll_count} times.")
        lines.extend([
            f"Average roll value: {self.average():.2f}",
            f"Total doubles rolled: {self.total_doubles}",
            f"Highest roll: {self.highest_roll}",
            f"Lowest roll: {self.lowest_roll if self.lowest_roll is not None else 'Not a number'}",
        ])
        return lines
