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
FRONT_ROWS = (
    ".....WWWWWW.....",
    "....WWWWWWWW....",
    "....WHHHHHHW....",
    "....HHHHHHHH....",
    "....HKHHHHKH....",
    "....HHHHHHHH....",
    ".....WWWWWW.....",
    ".....WWWWWW.....",
    "...BBBBBBBBBB...",
    "..SBBBBBBBBBBS..",
    "..SBBBBBBBBBBS..",
    "....BBBBBBBB....",
    "....BGGGGGGB....",
    "....BB....BB....",
    "....BB....BB....",
    "...SS......SS...",
)
BACK_ROWS = (
    ".....WWWWWW.....",
    "....WWWWWWWW....",
    "....WWWWWWWW....",
    "....WWWWWWWW....",
    "....WWWWWWWW....",
    ".....WWWWWW.....",
    "...BBBBBBBBBB...",
    "..SBBBBWGBBBBS..",
    "..SBBBBGWBBBBS..",
    "..SBBBBWGBBBBS..",
    "...BBBBGWBBBB...",
    "....BBBBBBBB....",
    "....BBBBBBBB....",
    "....BB....BB....",
    "....BB....BB....",
    "...SS......SS...",
)
PORTRAIT_FRONT_ROWS = (
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN",
    "NNNNNNNNNNNKKKKKKKKKKNNNNNNNNNNN",
    "NNNNNNNNNNKWGGWWGGWWGKNNNNNNNNNN",
    "NNNNNNNNNNKWGWGGWGWWGKNNNNNNNNNN",
    "NNNNNNNNNNKWWGGWWGGWWKNNNNNNNNNN",
    "NNNNNNNNNNKWWHHHHHHWWKNNNNNNNNNN",
    "NNNNNNNNNKWWHHHHHHHHWWKNNNNNNNNN",
    "NNNNNNNNNKHHHHHHHHHHHHHHKNNNNNNN",
    "NNNNNNNNNKHHKKHHHHHHKKHHKNNNNNNN",
    "NNNNNNNNNKHHHHHHHHHHHHHHKNNNNNNN",
    "NNNNNNNNNKHHHHHJJJHHHHHHKNNNNNNN",
    "NNNNNNNNNKHHHHHJJJHHHHHHKNNNNNNN",
    "NNNNNNNNNKKWWWWWWWWWWWWKKNNNNNNN",
    "NNNNNNNNNKWWGGWWWWWWGGWWKNNNNNNN",
    "NNNNNNNNNKWGGWWWWWWWWGGWKNNNNNNN",
    "NNNNNNNNNKWGGWWWWWWWWGGWKNNNNNNN",
    "NNNNNNNNNNKWGGWWWWWWGGWKNNNNNNNN",
    "NNNNNNNNNNKWGGWWWWWWGGWKNNNNNNNN",
    "NNNNNNNNNNNKWWWWWWWWWWKNNNNNNNNN",
    "NNNNNNNNNNNKWWWWWWWWWWKNNNNNNNNN",
    "NNNNNNNNNNNNKWWWWWWWWKNNNNNNNNNN",
    "NNNNNNNNNNNNNKWWWWWWKNNNNNNNNNNN",
    "NNNNNNNNNNNNNNKHHHHKNNNNNNNNNNNN",
    "NNNNNNNBBBBKHHHHHHHHKBBBBNNNNNNN",
    "NNNNNBBBBBBKHHHHHHHHKBBBBBBNNNNN",
    "NNNNBBBBBBBBBBKKKKBBBBBBBBBBNNNN",
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
)

PORTRAIT_BACK_ROWS = (
    "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN",
    "NNNNNNNNNNNKKKKKKKKKKNNNNNNNNNNN",
    "NNNNNNNNNNKWGGWWGGWWGKNNNNNNNNNN",
    "NNNNNNNNNNKWGWGGWGWWGKNNNNNNNNNN",
    "NNNNNNNNNNKWWGGWWGGWWKNNNNNNNNNN",
    "NNNNNNNNNNKWWWWWWWWWWKNNNNNNNNNN",
    "NNNNNNNNNKWWWWWWWWWWWWWKNNNNNNNN",
    "NNNNNNNNNKWWWWWWWWWWWWWWKNNNNNNN",
    "NNNNNNNNNKWWWWWGWWGWWWWWKNNNNNNN",
    "NNNNNNNNNKWWWWWGGGGWWWWWKNNNNNNN",
    "NNNNNNNNNKWWWWWGWWGWWWWWKNNNNNNN",
    "NNNNNNNNNKWWWWWGGGGWWWWWKNNNNNNN",
    "NNNNNNNNNKWWWWWWGGWWWWWWKNNNNNNN",
    "NNNNNNNNNKHHHHHGWWGHHHHHKNNNNNNN",
    "NNNNNNNNNKHHHHHGWWGHHHHHKNNNNNNN",
    "NNNNNNNNNKHHHHHGGGGHHHHHKNNNNNNN",
    "NNNNNNNNNKHHHHHGWWGHHHHHKNNNNNNN",
    "NNNNNNNNNKKHHHHGWWGHHHHKKKNNNNNN",
    "NNNNNNNNNNNKHHHWWWWHHHKNNNNNNNNN",
    "NNNNNNNBBBBKHHWWWWHHKBBBBNNNNNNN",
    "NNNNNBBBBBBKHHWWWWHHKBBBBBBNNNNN",
    "NNNNBBBBBBBBKWWWWKBBBBBBBBNNNNNN",
    "NNNNNBBBBBBBBBBKKKBBBBBBBBBBNNNN",
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
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
FRONT_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in FRONT_ROWS)
BACK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in BACK_ROWS)
PORTRAIT_CHARS = tuple(
    "".join("0123456789abcdef"[int(SPRITE_LETTERS[ch], 16)] for ch in row)
    for row in PORTRAIT_ROWS
)
PORTRAIT_FRONT_CHARS = tuple(
    "".join("0123456789abcdef"[int(SPRITE_LETTERS[ch], 16)] for ch in row)
    for row in PORTRAIT_FRONT_ROWS
)
PORTRAIT_BACK_CHARS = tuple(
    "".join("0123456789abcdef"[int(SPRITE_LETTERS[ch], 16)] for ch in row)
    for row in PORTRAIT_BACK_ROWS
)

pyxel.images[0].set(0, 0, SPRITE_CHARS)
pyxel.images[0].set(16, 0, FRONT_CHARS)
pyxel.images[0].set(0, 16, BACK_CHARS)
pyxel.images[0].set(32, 0, PORTRAIT_CHARS)
pyxel.images[0].set(64, 0, PORTRAIT_FRONT_CHARS)
pyxel.images[0].set(96, 0, PORTRAIT_BACK_CHARS)
pyxel.images[0].set(32, 0, PORTRAIT_CHARS)

FOG_SIZE = 120
FOG_HALF = 60
FOG_RGB = (225, 235, 250)


def palette_rgb(value):
    return ((value >> 16) & 255, (value >> 8) & 255, value & 255)


def blend_floor_to_fog(dist):
    floor = palette_rgb(pyxel.colors[3])
    alpha = dist / FOG_HALF
    return tuple(floor[i] + (FOG_RGB[i] - floor[i]) * alpha for i in range(3))


def nearest_fog_palette(rgb):
    best = 1
    best_dist = None
    for col in range(1, 16):
        pal = palette_rgb(pyxel.colors[col])
        dist = sum((pal[i] - rgb[i]) ** 2 for i in range(3))
        if best_dist is None or dist < best_dist:
            best, best_dist = col, dist
    return best


def render_fog():
    pyxel.colors[15] = (FOG_RGB[0] << 16) | (FOG_RGB[1] << 8) | FOG_RGB[2]
    rows = []
    for y in range(FOG_SIZE):
        chars = []
        for x in range(FOG_SIZE):
            offset_x = x - FOG_HALF + 0.5
            offset_y = y - FOG_HALF + 0.5
            dist = (offset_x * offset_x + offset_y * offset_y) ** 0.5
            if dist >= FOG_HALF:
                chars.append("0")
            else:
                chars.append("0123456789abcdef"[nearest_fog_palette(blend_floor_to_fog(dist))])
        rows.append("".join(chars))
    pyxel.images[1].set(0, 0, rows)


render_fog()

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


pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
print("Phase 1 complete")
print("Phase 2 complete")
pyxel.run(update, draw)