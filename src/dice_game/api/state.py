from ..domain.config import GameConfig
from ..domain.models import TurnState
from ..domain.stats import Stats

state = TurnState(
    game_config=GameConfig(),
    stats=Stats(),
    player_points=0,
)
