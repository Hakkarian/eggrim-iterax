from dataclasses import dataclass
from enum import Enum, auto

STAT_MAX = 100.0


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

    @property
    def view(self):
        facing_x, facing_y = self.facing
        if abs(facing_x) >= abs(facing_y):
            return Facing.LEFT if self.side < 0 else Facing.RIGHT
        return Facing.UP if facing_y < 0 else Facing.DOWN