import pyxel


SPRITE_LETTERS = {
    ".": "0", "H": "8", "W": "7", "G": "6", "B": "c",
    "L": "6", "C": "1", "S": "7", "J": "9", "K": "0", "N": "5", "D": "e", "M": "c",
    "E": "d", "F": "5",
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


def load_banks():
    pyxel.images[0].set(0, 0, SPRITE_CHARS)
    pyxel.images[0].set(16, 0, FRONT_CHARS)
    pyxel.images[0].set(0, 16, BACK_CHARS)
    pyxel.images[0].set(32, 0, PORTRAIT_CHARS)
    pyxel.images[0].set(64, 0, PORTRAIT_FRONT_CHARS)
    pyxel.images[0].set(96, 0, PORTRAIT_BACK_CHARS)
    pyxel.images[0].set(128, 0, PILLAR_CHARS)
    pyxel.images[0].set(0, 48, SIDE_ATTACK_CHARS)
    pyxel.images[0].set(16, 48, FRONT_ATTACK_CHARS)
    pyxel.images[0].set(32, 48, BACK_ATTACK_CHARS)
    pyxel.images[0].set(0, 32, SIDE_WALK_CHARS)
    pyxel.images[0].set(16, 32, FRONT_WALK_CHARS)
    pyxel.images[0].set(32, 32, BACK_WALK_CHARS)
    pyxel.images[0].set(48, 32, SIDE_HALF_CHARS)
    pyxel.images[0].set(64, 32, FRONT_HALF_CHARS)
    pyxel.images[0].set(80, 32, BACK_HALF_CHARS)
    pyxel.images[0].set(96, 32, SIDE_BLEND_CHARS)
    pyxel.images[0].set(112, 32, FRONT_BLEND_CHARS)
    pyxel.images[0].set(128, 32, BACK_BLEND_CHARS)
    pyxel.images[0].set(144, 32, SIDE_FADE_CHARS)
    pyxel.images[0].set(160, 32, FRONT_FADE_CHARS)
    pyxel.images[0].set(176, 32, BACK_FADE_CHARS)
    render_pillar_flash()


def render_pillar_flash():
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            col = pyxel.images[0].pget(128 + x, y)
            row.append("0" if col == 0 else "7")
        rows.append("".join(row))
    pyxel.images[2].set(48, 16, rows)


PILLAR_LETTERS = {".": "0", "W": "7", "G": "d"}

PILLAR_ROWS = (
    "....WWWWWW......",
    "....WGGGGW......",
    "....WGGGGW......",
    "....WGGGGW......",
    "....WWWWWW......",
    ".....GGGG.......",
    ".....GGGW.......",
    ".....GGGW.......",
    ".....GGGW.......",
    ".....GGGW.......",
    ".....GGGW.......",
    ".....GGGW.......",
    ".....GGGW.......",
    ".....GGGW.......",
    "....WGGGGW......",
    "....WWWWWW......",
)

PILLAR_CHARS = tuple(
    "".join(PILLAR_LETTERS[ch] for ch in row)
    for row in PILLAR_ROWS
)

FRONT_HAND_CELLS = {(2, 9), (13, 9), (2, 10), (13, 10)}
BACK_HAND_CELLS = {(2, 7), (13, 7), (2, 8), (13, 8), (2, 9), (13, 9)}

SPRITE_ATTACK_ROWS = tuple(row.replace("L", ".") for row in SPRITE_ROWS)
FRONT_ATTACK_ROWS = tuple(
    "".join("." if (x, y) in FRONT_HAND_CELLS else ch for x, ch in enumerate(row))
    for y, row in enumerate(FRONT_ROWS)
)
BACK_ATTACK_ROWS = tuple(
    "".join("." if (x, y) in BACK_HAND_CELLS else ch for x, ch in enumerate(row))
    for y, row in enumerate(BACK_ROWS)
)

SIDE_ATTACK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in SPRITE_ATTACK_ROWS)
FRONT_ATTACK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in FRONT_ATTACK_ROWS)
BACK_ATTACK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in BACK_ATTACK_ROWS)

SIDE_WALK_ROWS = SPRITE_ROWS[:11] + (
    "....BB..BB......",
    "...BB....BB.....",
    "..SS......SS....",
)
FRONT_WALK_ROWS = FRONT_ROWS[:13] + (
    "...BB......BB...",
    "...BB......BB...",
    "..SS........SS..",
)
BACK_WALK_ROWS = BACK_ROWS[:13] + (
    "...BB......BB...",
    "...BB......BB...",
    "..SS........SS..",
)

SIDE_WALK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in SIDE_WALK_ROWS)
FRONT_WALK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in FRONT_WALK_ROWS)
BACK_WALK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in BACK_WALK_ROWS)

SIDE_HALF_ROWS = SPRITE_ROWS[:11] + (
    "....BB.BB.......",
    "....BB..BB......",
    "...SS....SS.....",
)
FRONT_HALF_ROWS = FRONT_ROWS[:13] + (
    "....BB....BB....",
    "...BB......BB...",
    "...SS......SS...",
)
BACK_HALF_ROWS = BACK_ROWS[:13] + (
    "....BB....BB....",
    "...BB......BB...",
    "...SS......SS...",
)

SIDE_HALF_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in SIDE_HALF_ROWS)
FRONT_HALF_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in FRONT_HALF_ROWS)
BACK_HALF_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in BACK_HALF_ROWS)

FRONT_BLEND_ROWS = tuple(
    "".join("E" if (x, y) in FRONT_HAND_CELLS else ch for x, ch in enumerate(row))
    for y, row in enumerate(FRONT_ROWS)
)
BACK_BLEND_ROWS = tuple(
    "".join("E" if (x, y) in BACK_HAND_CELLS else ch for x, ch in enumerate(row))
    for y, row in enumerate(BACK_ROWS)
)
SIDE_BLEND_ROWS = tuple(row.replace("L", "E") for row in SPRITE_ROWS)

FRONT_FADE_ROWS = tuple(
    "".join("F" if (x, y) in FRONT_HAND_CELLS else ch for x, ch in enumerate(row))
    for y, row in enumerate(FRONT_ROWS)
)
BACK_FADE_ROWS = tuple(
    "".join("F" if (x, y) in BACK_HAND_CELLS else ch for x, ch in enumerate(row))
    for y, row in enumerate(BACK_ROWS)
)
SIDE_FADE_ROWS = tuple(row.replace("L", "F") for row in SPRITE_ROWS)

SIDE_BLEND_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in SIDE_BLEND_ROWS)
FRONT_BLEND_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in FRONT_BLEND_ROWS)
BACK_BLEND_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in BACK_BLEND_ROWS)
SIDE_FADE_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in SIDE_FADE_ROWS)
FRONT_FADE_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in FRONT_FADE_ROWS)
BACK_FADE_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in BACK_FADE_ROWS)
