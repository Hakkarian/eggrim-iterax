import pyxel

SCREEN_W = 256
SCREEN_H = 144
FPS = 60
MOVE_SPEED = 40.0

from eggrim.assets import load_banks
from eggrim.fog import FOG_HALF, FOG_SIZE
from eggrim.hud import (
    HEALTH_BAR_Y,
    HEALTH_COLOR,
    HEALTH_VALUE,
    HUD_BAR_H,
    HUD_BAR_W,
    HUD_BAR_X,
    STAMINA_BAR_Y,
    STAMINA_COLOR,
    STAMINA_VALUE,
    VALUE_MAX,
    draw_bar,
)
from eggrim.player import Facing, Player
from eggrim.states import announce_progress
from eggrim.world import PLAYER_START_X, PLAYER_START_Y, outside_world

load_banks()

player = Player(
    x=float(PLAYER_START_X),
    y=float(PLAYER_START_Y),
    facing=(1.0, 0.0),
    side=1.0,
)


def update():
    dx = (
        (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT))
        - (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT))
    )
    dy = (
        (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN))
        - (pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP))
    )
    if dx or dy:
        length = (dx * dx + dy * dy) ** 0.5
        player.facing = (dx / length, dy / length)
        if player.facing[0]:
            player.side = 1.0 if player.facing[0] > 0 else -1.0
        player.x += player.facing[0] * MOVE_SPEED / FPS
        player.y += player.facing[1] * MOVE_SPEED / FPS

    if outside_world(player.x, player.y):
        player.x = float(PLAYER_START_X)
        player.y = float(PLAYER_START_Y)


def draw():
    pyxel.cls(3)
    view = player.view
    pyxel.blt(
        int(player.x) - FOG_HALF,
        int(player.y) - FOG_HALF,
        1,
        0,
        0,
        FOG_SIZE,
        FOG_SIZE,
        0,
    )
    sprite_x = int(player.x) - 8
    sprite_y = int(player.y) - 8
    if view in (Facing.LEFT, Facing.RIGHT):
        sprite_w = -16 if view is Facing.LEFT else 16
        pyxel.blt(sprite_x, sprite_y, 0, 0, 0, sprite_w, 16, 0)
    elif view is Facing.UP:
        pyxel.blt(sprite_x, sprite_y, 0, 0, 16, 16, 16, 0)
    else:
        pyxel.blt(sprite_x, sprite_y, 0, 16, 0, 16, 16, 0)
    draw_bar(
        HUD_BAR_X,
        HEALTH_BAR_Y,
        HUD_BAR_W,
        HUD_BAR_H,
        HEALTH_COLOR,
        HEALTH_VALUE,
        VALUE_MAX,
    )
    draw_bar(
        HUD_BAR_X,
        STAMINA_BAR_Y,
        HUD_BAR_W,
        HUD_BAR_H,
        STAMINA_COLOR,
        STAMINA_VALUE,
        VALUE_MAX,
    )
    if view in (Facing.LEFT, Facing.RIGHT):
        px_src, portrait_w = 32, -32 if view is Facing.LEFT else 32
    elif view is Facing.UP:
        px_src, portrait_w = 96, 32
    else:
        px_src, portrait_w = 64, 32
    pyxel.blt(0, 0, 0, px_src, 0, portrait_w, 32, 3)


def run():
    pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
    announce_progress()
    pyxel.run(update, draw)