import pyxel

from eggrim.world import PLAYER_FEET_OFFSET_Y
from eggrim.zones import TILE

SCARF_SPAWN_TILES = 3
SCARF_PULSE_FRAMES = 20
SCARF_BODY_COLOR = 4
SCARF_FOLD_COLOR = 5
SCARF_GLOW_COLOR = 9


class Scarf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.on_map = True


def open_tile(zone, tile_x, tile_y):
    return (
        0 <= tile_y < zone.height_tiles
        and 0 <= tile_x < zone.width_tiles
        and zone.grid[tile_y][tile_x] != "#"
    )


def spawn_scarf(zone, start_x, start_y):
    base_x = int(start_x) // TILE
    base_y = (int(start_y) + int(PLAYER_FEET_OFFSET_Y)) // TILE
    for radius in range(SCARF_SPAWN_TILES, SCARF_SPAWN_TILES + 3):
        for tile_y in range(base_y - radius, base_y + radius + 1):
            for tile_x in range(base_x - radius, base_x + radius + 1):
                if max(abs(tile_x - base_x), abs(tile_y - base_y)) != radius:
                    continue
                if open_tile(zone, tile_x, tile_y):
                    return Scarf(tile_x * TILE + TILE // 2, tile_y * TILE + TILE // 2)
    return Scarf(start_x + SCARF_SPAWN_TILES * TILE, start_y)


def draw_map_scarf(scarf):
    if not scarf.on_map:
        return
    x = int(scarf.x)
    y = int(scarf.y)
    if pyxel.frame_count % (SCARF_PULSE_FRAMES * 2) < SCARF_PULSE_FRAMES:
        pyxel.circb(x, y - 1, 7, SCARF_GLOW_COLOR)
    pyxel.rect(x - 4, y - 2, 8, 3, SCARF_BODY_COLOR)
    pyxel.rect(x - 4, y - 2, 8, 1, SCARF_FOLD_COLOR)
    pyxel.rect(x + 2, y + 1, 2, 3, SCARF_BODY_COLOR)
    pyxel.pix(x + 3, y + 4, SCARF_FOLD_COLOR)