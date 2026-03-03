from dataclasses import dataclass, field


@dataclass(frozen=True)
class PointsConfig:
    win: int = 5
    lose: int = 3
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
    points: PointsConfig = field(default_factory=PointsConfig)
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)
