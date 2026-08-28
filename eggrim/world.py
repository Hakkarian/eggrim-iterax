PLAYER_START_X = 128
PLAYER_START_Y = 72
WORLD_RADIUS_X = 120.0
WORLD_RADIUS_Y = 68.0


def outside_world(x, y):
    offset_x = x - PLAYER_START_X
    offset_y = y - PLAYER_START_Y
    return (offset_x / WORLD_RADIUS_X) ** 2 + (offset_y / WORLD_RADIUS_Y) ** 2 > 1.0