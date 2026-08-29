PLAYER_START_X = 128
PLAYER_START_Y = 72
PLAYER_ZONE_MARGIN = 12.0
PILLAR_BASE_RX = 2.0
PILLAR_BASE_RY = 1.5
PLAYER_FEET_RADIUS = 2.0

from eggrim.zones import TILE


def outside_zone(zone, x, y):
    return (
        x < PLAYER_ZONE_MARGIN
        or y < PLAYER_ZONE_MARGIN
        or x > zone.width_px - PLAYER_ZONE_MARGIN
        or y > zone.height_px - PLAYER_ZONE_MARGIN
    )


def feet_hits_wall(zone, x, y):
    radius = PLAYER_FEET_RADIUS
    tile_x0 = max(0, int((x - radius) // TILE))
    tile_x1 = min(zone.width_tiles - 1, int((x + radius) // TILE))
    tile_y0 = max(0, int((y - radius) // TILE))
    tile_y1 = min(zone.height_tiles - 1, int((y + radius) // TILE))
    for tile_y in range(tile_y0, tile_y1 + 1):
        row = zone.grid[tile_y]
        for tile_x in range(tile_x0, tile_x1 + 1):
            if row[tile_x] != "#":
                continue
            wall_x0 = tile_x * TILE
            wall_y0 = tile_y * TILE
            near_x = max(wall_x0, min(x, wall_x0 + TILE))
            near_y = max(wall_y0, min(y, wall_y0 + TILE))
            if (near_x - x) ** 2 + (near_y - y) ** 2 <= radius * radius:
                return True
    return False


def resolve_pillars(player, pillars):
    for pillar in pillars:
        offset_x = player.x - pillar.x
        offset_y = player.y - pillar.y
        bound_x = PILLAR_BASE_RX + PLAYER_FEET_RADIUS
        bound_y = PILLAR_BASE_RY + PLAYER_FEET_RADIUS
        if offset_x == 0 and offset_y == 0:
            continue
        scale = ((offset_x / bound_x) ** 2 + (offset_y / bound_y) ** 2) ** 0.5
        if scale < 1.0:
            player.x = pillar.x + offset_x / scale
            player.y = pillar.y + offset_y / scale