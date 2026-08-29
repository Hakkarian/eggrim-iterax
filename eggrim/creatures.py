from dataclasses import dataclass
import math

from eggrim.world import PLAYER_START_X, PLAYER_START_Y

PILLAR_HP = 999
PILLAR_COUNT = 8
PILLAR_RING_RADIUS_X = 85.0
PILLAR_RING_RADIUS_Y = 45.0
PILLAR_FLASH_FRAMES = 8


@dataclass
class Pillar:
    x: float
    y: float
    hp: int = PILLAR_HP
    flash: int = 0


def spawn_pillars():
    pillars = []
    for index in range(PILLAR_COUNT):
        angle = math.pi * 2 * (index + 0.5) / PILLAR_COUNT
        pillars.append(
            Pillar(
                x=PLAYER_START_X + PILLAR_RING_RADIUS_X * math.cos(angle),
                y=PLAYER_START_Y + PILLAR_RING_RADIUS_Y * math.sin(angle),
            )
        )
    return pillars