import pyxel

from eggrim.assets.portraits_painted import PAINTED_ROWS
from eggrim.fog import nearest_fog_palette, palette_rgb

THUMB_SIZE = 64
PORTRAIT_KEYS = ("side", "front", "back")
PORTRAIT_THUMB_BANK = 0
PORTRAIT_THUMB_POS = {"side": (0, 64), "front": (64, 64), "back": (128, 64)}
PORTRAIT_BLEND_STEPS = ((1, 1 / 3), (2, 2 / 3))
BLEND_SLOTS = (
    (2, 0, 96),
    (2, 64, 96),
    (2, 128, 96),
    (2, 192, 96),
    (2, 0, 160),
    (2, 64, 160),
    (2, 128, 160),
    (2, 192, 160),
    (0, 0, 136),
    (0, 64, 136),
    (1, 64, 0),
    (1, 192, 0),
)
PORTRAIT_BLEND_POS = {}


def thumb_grid_from_rows(rows):
    return [[int(ch, 16) for ch in row] for row in rows]


PAINTED_BG_CHAR = "3"
PAINTED_SKY_CHAR = "f"


def painted_hero_rows(key):
    return [
        "".join(
            PAINTED_SKY_CHAR if ch == PAINTED_BG_CHAR else ch
            for ch in row
        )
        for row in PAINTED_ROWS[key]
    ]


PORTRAIT_PAINTED_VIEWS = {"side": "right", "front": "front", "back": "back"}


def thumb_rows(view):
    return painted_hero_rows(PORTRAIT_PAINTED_VIEWS[view])


def render_thumbs():
    for key in PORTRAIT_KEYS:
        u, v = PORTRAIT_THUMB_POS[key]
        pyxel.images[PORTRAIT_THUMB_BANK].set(u, v, thumb_rows(key))


def render_portrait_blends():
    thumb_grids = {
        key: thumb_grid_from_rows(thumb_rows(key)) for key in PORTRAIT_KEYS
    }
    slot = 0
    for a in PORTRAIT_KEYS:
        for b in PORTRAIT_KEYS:
            if a == b:
                continue
            for step_index, alpha in PORTRAIT_BLEND_STEPS:
                rows = []
                for y in range(THUMB_SIZE):
                    chars = []
                    for x in range(THUMB_SIZE):
                        rgb_a = palette_rgb(pyxel.colors[thumb_grids[a][y][x]])
                        rgb_b = palette_rgb(pyxel.colors[thumb_grids[b][y][x]])
                        rgb = tuple(
                            rgb_a[i] * (1 - alpha) + rgb_b[i] * alpha for i in range(3)
                        )
                        chars.append("0123456789abcdef"[nearest_fog_palette(rgb)])
                    rows.append("".join(chars))
                bank, u, v = BLEND_SLOTS[slot]
                PORTRAIT_BLEND_POS[(a, b, step_index)] = (bank, u, v)
                pyxel.images[bank].set(u, v, rows)
                slot += 1