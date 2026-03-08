import os
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
class ExportConfig:
    """Configuration for data export functionality.
    
    Attributes:
        export_path: Path where CSV exports will be saved. Can be overridden 
                    by setting the DICE_GAME_EXPORT_PATH environment variable.
                    
    Example usage:
        # Use default path
        python3 -m dice_game
        
        # Use custom path via environment variable
        DICE_GAME_EXPORT_PATH="/home/user/my_exports.csv" python3 -m dice_game
    """
    export_path: str = field(default_factory=lambda: os.getenv(
        "DICE_GAME_EXPORT_PATH", 
        "src/dice_game/exports/rolls_export.csv"
    ))


@dataclass(frozen=True)
class GameConfig:
    points: PointsConfig = field(default_factory=PointsConfig)
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)
    exports: ExportConfig = field(default_factory=ExportConfig)
