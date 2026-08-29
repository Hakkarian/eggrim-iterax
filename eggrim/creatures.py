from dataclasses import dataclass

PILLAR_HP = 999
PILLAR_FLASH_FRAMES = 8


@dataclass
class Pillar:
    x: float
    y: float
    hp: int = PILLAR_HP
    flash: int = 0


def spawn_pillars(zone):
    return [Pillar(x=x, y=y) for x, y in zone.pillar_spawns]