PLAYER_START_X = 128
PLAYER_START_Y = 72
PLAYER_ZONE_MARGIN = 12.0
PILLAR_BASE_RX = 2.0
PILLAR_BASE_RY = 1.5
PLAYER_FEET_RADIUS = 2.0


def outside_zone(zone, x, y):
    return (
        x < PLAYER_ZONE_MARGIN
        or y < PLAYER_ZONE_MARGIN
        or x > zone.width_px - PLAYER_ZONE_MARGIN
        or y > zone.height_px - PLAYER_ZONE_MARGIN
    )


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