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

HEALTH_VALUE = 100
STAMINA_VALUE = 100
VALUE_MAX = 100


def draw_bar(x, y, width, height, fill_color, value, value_max):
    pyxel.rectb(x - 1, y - 1, width + 2, height + 2, HUD_BORDER_COLOR)
    pyxel.rect(x, y, width, height, HUD_BACK_COLOR)
    fill_w = round(width * value / value_max)
    if fill_w > 0:
        pyxel.rect(x, y, fill_w, height, fill_color)