from dataclasses import dataclass


@dataclass
class Stats:
    roll_count: int = 0
    total_doubles: int = 0
    total_roll_value: int = 0
    highest_roll: int = 0
    lowest_roll: int | None = None

    def update(self, total: int, has_match: bool = False) -> None:

        self.roll_count += 1
        self.total_roll_value += total
        self.highest_roll = max(self.highest_roll, total)
        self.lowest_roll = total if self.lowest_roll is None else min(
            self.lowest_roll,
            total
        )
        if has_match:
            self.total_doubles += 1

    @property
    def average(self) -> float:
        return 0.0 if self.roll_count == 0 else self.total_roll_value / self.roll_count

    def print_stats(self, points_total: int) -> None:
        if self.roll_count == 0:
            print("No rolls yet.\n")
            return

        lowest = self.lowest_roll if self.lowest_roll is not None else "-"
        lines = [
            "\n---- Stats ----",
            f"Completed rolls: {self.roll_count}",
            f"Total points: {points_total}",
            f"Average total: {self.average:.2f}",
            f"Total doubles: {self.total_doubles}",
            f"Highest roll: {self.highest_roll}",
            f"Lowest roll: {lowest}",
            "----------------",
        ]
        print("\n".join(lines))
        print()
