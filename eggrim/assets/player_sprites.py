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

SPRITE_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in SPRITE_ROWS)
FRONT_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in FRONT_ROWS)
BACK_CHARS = tuple("".join(SPRITE_LETTERS[ch] for ch in row) for row in BACK_ROWS)

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