import pyxel

HUD_BAR_X = 78
HEALTH_BAR_Y = 129
STAMINA_BAR_Y = 136
HUD_BAR_W = 100
HUD_BAR_H = 6
HEALTH_COLOR = 8
STAMINA_COLOR = 11
HUD_BACK_COLOR = 1
HUD_BORDER_COLOR = 0

MINIMAP_X = 190
MINIMAP_Y = 2
MINIMAP_BORDER_COLOR = 5
MINIMAP_VIEW_COLOR = 6
MINIMAP_PILLAR_COLOR = 12
MINIMAP_PLAYER_COLOR = 8


def draw_minimap(zone, player, pillars, cam_x, cam_y):
    pyxel.rect(MINIMAP_X - 1, MINIMAP_Y - 1, zone.width_tiles + 2, zone.height_tiles + 2, HUD_BORDER_COLOR)
    pyxel.rectb(MINIMAP_X - 1, MINIMAP_Y - 1, zone.width_tiles + 2, zone.height_tiles + 2, MINIMAP_BORDER_COLOR)
    pyxel.rectb(
        MINIMAP_X + cam_x // 8,
        MINIMAP_Y + cam_y // 8,
        32,
        18,
        MINIMAP_VIEW_COLOR,
    )
    for pillar in pillars:
        pyxel.pset(MINIMAP_X + int(pillar.x) // 8, MINIMAP_Y + int(pillar.y) // 8, MINIMAP_PILLAR_COLOR)
    player_px = min(zone.width_tiles - 2, max(0, int(player.x) // 8 - 1))
    player_py = min(zone.height_tiles - 2, max(0, int(player.y) // 8 - 1))
    pyxel.rect(MINIMAP_X + player_px, MINIMAP_Y + player_py, 2, 2, MINIMAP_PLAYER_COLOR)


def draw_bar(x, y, width, height, fill_color, value, value_max):
    pyxel.rectb(x - 1, y - 1, width + 2, height + 2, HUD_BORDER_COLOR)
    pyxel.rect(x, y, width, height, HUD_BACK_COLOR)
    fill_w = round(width * value / value_max)
    if fill_w > 0:
        pyxel.rect(x, y, fill_w, height, fill_color)