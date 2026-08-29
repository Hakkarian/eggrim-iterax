from dataclasses import dataclass

import pyxel

from eggrim.zones import TILE

PILLAR_HP = 999
PILLAR_FLASH_FRAMES = 8
PILLAR_SPRITE_U = 128
PILLAR_SPRITE_V = 0
PILLAR_SPRITE_SIZE = 16


@dataclass
class Pillar:
    x: float
    y: float
    body: tuple = (0.0, 0.0, 0.0, 0.0)
    hp: int = PILLAR_HP
    flash: int = 0


@dataclass
class Wall:
    tile_x: int
    tile_y: int
    hp: int = PILLAR_HP
    flash: int = 0


def pillar_body_box():
    img = pyxel.images[0]
    xs = []
    ys = []
    for y in range(PILLAR_SPRITE_SIZE):
        for x in range(PILLAR_SPRITE_SIZE):
            if img.pget(PILLAR_SPRITE_U + x, PILLAR_SPRITE_V + y) != 0:
                xs.append(x)
                ys.append(y)
    return (
        min(xs) - PILLAR_SPRITE_SIZE / 2,
        min(ys) - PILLAR_SPRITE_SIZE / 2,
        max(xs) + 1 - PILLAR_SPRITE_SIZE / 2,
        max(ys) + 1 - PILLAR_SPRITE_SIZE / 2,
    )


def spawn_pillars(zone):
    body = pillar_body_box()
    return [Pillar(x=x, y=y, body=body) for x, y in zone.pillar_spawns]


def spawn_walls(zone):
    return {
        (x, y): Wall(tile_x=x, tile_y=y)
        for y in range(zone.height_tiles)
        for x in range(zone.width_tiles)
        if zone.grid[y][x] == "#"
    }