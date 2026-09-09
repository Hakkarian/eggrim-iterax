from dataclasses import dataclass

import pyxel

from eggrim.zones import TILE

PILLAR_HP = 999
PILLAR_FLASH_FRAMES = 8
PILLAR_SPRITE_U = 128
PILLAR_SPRITE_V = 0
PILLAR_SPRITE_SIZE = 16
ENEMY_ATTACK_FRAMES = 24
ENEMY_SPRITE_W = 24
PLAYER_SPRITE_W = 26
ENEMY_HITBOX_SHRINK = 1.0
ENEMY_COOLDOWN_FRAMES = 60
ENEMY_DAMAGE = 4.0
ENEMY_WALK_SPEED = 16.0
ENEMY_VIEW_FRACTION = 10.0
ENEMY_WANDER_FRAMES = 120


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


@dataclass
class TestEnemy:
    x: float
    y: float
    anim: int = 0
    cooldown: int = 0
    walk_phase: int = 0
    heading_x: float = 0.0
    heading_y: float = 0.0
    wander_timer: int = 0


def spawn_test_enemy(zone):
    start_x, start_y = zone.player_start
    tile_x = int(start_x) // TILE
    tile_y = int(start_y) // TILE
    for steps in ((4,), range(1, 10)):
        for step in steps:
            tx = tile_x - step
            if tx < 0:
                break
            if zone.grid[tile_y][tx] == "#":
                continue
            return TestEnemy(x=tx * TILE + TILE // 2, y=(tile_y + 1) * TILE)
    return TestEnemy(x=start_x - TILE * 3, y=start_y)


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