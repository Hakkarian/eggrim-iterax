import pyxel

SCREEN_W = 256
SCREEN_H = 144
FPS = 60
MOVE_SPEED = 40.0

from eggrim.assets import load_banks
from eggrim.fog import FOG_HALF, FOG_SIZE

load_banks()


PLAYER_START_X = 128
PLAYER_START_Y = 72
WORLD_RADIUS_X = 120.0
WORLD_RADIUS_Y = 68.0

player = {
    "x": float(PLAYER_START_X),
    "y": float(PLAYER_START_Y),
    "facing": (1.0, 0.0),
    "side": 1.0,
}


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
        player["facing"] = (dx / length, dy / length)
        if player["facing"][0]:
            player["side"] = 1.0 if player["facing"][0] > 0 else -1.0
        player["x"] += player["facing"][0] * MOVE_SPEED / FPS
        player["y"] += player["facing"][1] * MOVE_SPEED / FPS

    offset_x = player["x"] - PLAYER_START_X
    offset_y = player["y"] - PLAYER_START_Y
    if (offset_x / WORLD_RADIUS_X) ** 2 + (offset_y / WORLD_RADIUS_Y) ** 2 > 1.0:
        player["x"] = float(PLAYER_START_X)
        player["y"] = float(PLAYER_START_Y)


def draw():
    pyxel.cls(3)
    facing_x, facing_y = player["facing"]
    if abs(facing_x) >= abs(facing_y):
        px_src, portrait_w = 32, -32 if player["side"] < 0 else 32
    elif facing_y < 0:
        px_src, portrait_w = 96, 32
    else:
        px_src, portrait_w = 64, 32
    pyxel.blt(0, 0, 0, px_src, 0, portrait_w, 32, 3)
    pyxel.blt(
        int(player["x"]) - FOG_HALF,
        int(player["y"]) - FOG_HALF,
        1,
        0,
        0,
        FOG_SIZE,
        FOG_SIZE,
        0,
    )
    sprite_x = int(player["x"]) - 8
    sprite_y = int(player["y"]) - 8
    facing_x, facing_y = player["facing"]
    if abs(facing_x) >= abs(facing_y):
        sprite_w = -16 if facing_x < 0 else 16
        pyxel.blt(sprite_x, sprite_y, 0, 0, 0, sprite_w, 16, 0)
    elif facing_y < 0:
        pyxel.blt(sprite_x, sprite_y, 0, 0, 16, 16, 16, 0)
    else:
        pyxel.blt(sprite_x, sprite_y, 0, 16, 0, 16, 16, 0)


def run():
    pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
    print("Phase 1 complete")
    print("Phase 2 complete")
    pyxel.run(update, draw)
