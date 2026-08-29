PLAYER_START_X = 128
PLAYER_START_Y = 72
WORLD_RADIUS_X = 120.0
WORLD_RADIUS_Y = 68.0
PILLAR_BASE_RX = 2.0
PILLAR_BASE_RY = 1.5
PLAYER_FEET_RADIUS = 2.0


def outside_world(x, y):
    offset_x = x - PLAYER_START_X
    offset_y = y - PLAYER_START_Y
    return (offset_x / WORLD_RADIUS_X) ** 2 + (offset_y / WORLD_RADIUS_Y) ** 2 > 1.0


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