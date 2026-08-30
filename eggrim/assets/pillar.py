import pyxel

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


def render_pillar_flash():
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            col = pyxel.images[0].pget(128 + x, y)
            row.append("0" if col == 0 else "7")
        rows.append("".join(row))
    pyxel.images[2].set(48, 16, rows)