from dataclasses import dataclass
from enum import Enum, auto

STAT_MAX = 100.0
SPRINT_MULTIPLIER = 2.0
SPRINT_DRAIN = 30.0
STAMINA_REGEN = 20.0
SPRINT_MIN_START = 10.0
BLOCK_DRAIN = 30.0
BLOCK_MIN_START = 10.0


class Facing(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


@dataclass
class Player:
    x: float
    y: float
    facing: tuple
    side: float
    health: float = STAT_MAX
    stamina: float = STAT_MAX
    sprinting: bool = False
    blocking: bool = False

    @property
    def view(self):
        facing_x, facing_y = self.facing
        if abs(facing_x) >= abs(facing_y):
            return Facing.LEFT if self.side < 0 else Facing.RIGHT
        return Facing.UP if facing_y < 0 else Facing.DOWN