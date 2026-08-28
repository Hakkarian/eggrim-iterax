import pyxel

SCREEN_W = 256
SCREEN_H = 144
FPS = 60
MOVE_SPEED = 40.0

SPRITE_LETTERS = {
    ".": "0", "H": "8", "W": "7", "G": "6", "B": "c",
    "L": "6", "C": "1", "S": "7", "J": "9", "K": "0", "N": "5", "D": "e", "M": "c",
}
SPRITE_ROWS = (
    "......WGWG......",
    ".....WGWHH......",
    ".....WGWGHG.....",
    ".....WGWHWWH....",
    "......W.HH......",
    ".CCWBBBBBLL.....",
    ".CCBBBBBBLLB....",
    ".CC.BBBBLL.B....",
    ".CC.BBBBLL.B....",
    ".CC.BBBBLL.B....",
    ".CC.SBBLL..S....",
    "....BB.BB.......",
    "....BB.BB.......",
    "...SS...SS......",
    "................",
    "................",
)
PORTRAIT_ROWS = (
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN",
    "NNNNNNNNNNNNNNKKKKKKKKKKNNNNNNNN",
    "NNNNNNNNNNNNNNKWGGWWGGWWKNNNNNNN",
    "NNNNNNNNNNNNNKKWGWGGWGGWWKKNNNNN",
    "NNNNNNNNNNNNNKKGGWWGGWGGWKKNNNNN",
    "NNNNNNNNNNNNNKKKHHHHHHHHHHHKNNNN",
    "NNNNNNNNNNNNKHHHHHHJHHJHHHHHHKNN",
    "NNNNNNNNNNNKHHHHHHHHHJHHHHHHHKNN",
    "NNNNNNNNNNNKHHHHHHHHKKKKKKKKKNNN",
    "NNNNNNNNNNKHHHHHHHHHHHHHKWHKNNNN",
    "NNNNNNNNNNKHHHHHHHHHHHHHKWHKNNNN",
    "NNNNNNNNNKKHHHHHHHHHHHHHHHHKKNNN",
    "NNNNNNNNNKKHHHHHHHHHHHHHHHHHHKNN",
    "NNNNNNNNNKKHHHHGGKGGWWWWWWWKKNNN",
    "NNNNNNNNNKKKHHGGGGGWGWGWGWWKKNNN",
    "NNNNNNNNNKKKHHHGWWGWGWGWGWGKKNNN",
"NNNNNNNNNKKKHHHGWGWGWGWGWGWKKNNN",
    "NNNNNNNNNKKKHHHGWGWGWGWGWGWKKNNN",
    "NNNNNNNNNKKKHHHWWGWWWGWWWGKKKKNN",
    "NNNNNNNNNKKKKHHHWWWWWWWWWKKNNNNN",
    "NNNNNNNNNKKKHHHHHHHHHHHHKKKNNNNN",
    "NNNNNNNNNKKKKHHHHHHHHHHHKKKNNNNN",
    "NNNNNNNNNKKKHHHHHHHHHHHKKKNNNNNN",
    "NNNNNNNNNNKKHHHHHHHHHHKKNNNNNNNN",
    "NNNNNNNNNNNKKKKKKKKKKKKKNNNNNNNN",
    "NNNNNNNNKKKKKKKKKKKKKKKKNNNNNNNN",
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
)
SPRITE_CHARS = tuple(
    "".join(SPRITE_LETTERS[ch] for ch in row) for row in SPRITE_ROWS
)
PORTRAIT_CHARS = tuple(
    "".join("0123456789abcdef"[int(SPRITE_LETTERS[ch], 16)] for ch in row)
    for row in PORTRAIT_ROWS
)

pyxel.images[0].set(0, 0, SPRITE_CHARS)
pyxel.images[0].set(32, 0, PORTRAIT_CHARS)

PLAYER_START_X = 128
PLAYER_START_Y = 72

player = {"x": float(PLAYER_START_X), "y": float(PLAYER_START_Y), "facing": (1.0, 0.0)}


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
        player["x"] += player["facing"][0] * MOVE_SPEED / FPS
        player["y"] += player["facing"][1] * MOVE_SPEED / FPS


def draw():
    pyxel.cls(3)
    pyxel.blt(0, 0, 0, 32, 0, 32, 32, 3)
    sprite_x = int(player["x"]) - 8
    sprite_y = int(player["y"]) - 8
    if player["facing"][0] < 0:
        pyxel.blt(sprite_x + 16, sprite_y, 0, 0, 0, -16, 16, 0)
    else:
        pyxel.blt(sprite_x, sprite_y, 0, 0, 0, 16, 16, 0)


pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
pyxel.run(update, draw)