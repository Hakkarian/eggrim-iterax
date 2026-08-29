from enum import Enum, auto


class GameState(Enum):
    FOUNDATION = auto()
    FOG = auto()
    HUD = auto()
    COMBAT = auto()