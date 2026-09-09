import math

import pyxel

from eggrim.assets.portraits_painted import (
    HERO_PAINTED_BANK,
    HERO_PAINTED_POS,
    PAINTED_ROWS,
)
from eggrim.fog import nearest_fog_palette, palette_rgb

PORTRAIT_SIZE = 128
THUMB_SIZE = 64
PORTRAIT_KEYS = ("side", "front", "back")
PORTRAIT_BANKS = {"side": (1, 0, 0), "front": (1, 128, 0), "back": (1, 0, 128)}
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

BACKGROUND = 5
SKIN = 8
HAIR_LIGHT = 7
HAIR_MID = 6
HAIR_DARK = 13
SHIRT = 12
SHIRT_SEAM = 1
GLASS_RIM = 6
GLASS_GLINT = 7
LENS = 0
EYE = 1
BANDANA = 2
BANDANA_DARK = 1
OUTLINE = 0
PART_LINE = 13
HEAD_CX = 64


def hair_shade(x, y):
    flow = x + math.sin(y * 0.21) * 6.0
    return (HAIR_LIGHT, HAIR_MID, HAIR_DARK)[int(flow // 6) % 3]


def beard_shade(x, y):
    return HAIR_LIGHT if (x + y) // 3 % 2 else HAIR_MID


def bandana_silver_shade(x, y, top, bottom):
    t = (y - top) / (bottom - top)
    level = t + 0.06 * math.sin((x + math.sin(y * 0.31) * 3.0) * 0.4)
    if level < 0.35:
        return HAIR_LIGHT
    if level < 0.7:
        return HAIR_MID
    return HAIR_DARK


def mask_half(y):
    return ellipse_half(HEAD_CX, 54, 30, 36, y) - 0.5


def lens_shade(x, y, cy, ry):
    t = (y - cy) / ry
    if t < -0.35:
        return GLASS_GLINT
    if t < 0.25:
        return GLASS_RIM
    return HAIR_DARK


def new_canvas():
    return [[BACKGROUND for x in range(PORTRAIT_SIZE)] for y in range(PORTRAIT_SIZE)]


def ellipse_half(cx, cy, rx, ry, y):
    t = 1.0 - ((y - cy) / ry) ** 2
    return rx * t ** 0.5 if t > 0.0 else 0.0


def paint_ellipse(grid, cx, cy, rx, ry, color_fn):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        if not 0 <= y < PORTRAIT_SIZE:
            continue
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if not 0 <= x < PORTRAIT_SIZE:
                continue
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            if dx * dx + dy * dy <= 1.0:
                grid[y][x] = color_fn(x, y)


def paint_shirt(grid, top, span):
    for y in range(top, PORTRAIT_SIZE):
        t = (y - top) / (PORTRAIT_SIZE - top)
        half = span + 34 * t
        for x in range(max(0, HEAD_CX - int(half)), min(PORTRAIT_SIZE - 1, HEAD_CX + int(half)) + 1):
            grid[y][x] = SHIRT
    for i in range(14):
        y = top + i
        for x in range(HEAD_CX - i // 3, HEAD_CX + i // 3 + 1):
            if 0 <= x < PORTRAIT_SIZE:
                grid[y][x] = SHIRT_SEAM


def paint_outline(grid):
    filled = [
        [grid[y][x] != BACKGROUND for x in range(PORTRAIT_SIZE)]
        for y in range(PORTRAIT_SIZE)
    ]
    for y in range(PORTRAIT_SIZE):
        for x in range(PORTRAIT_SIZE):
            if grid[y][x] != BACKGROUND:
                continue
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if (
                    0 <= nx < PORTRAIT_SIZE
                    and 0 <= ny < PORTRAIT_SIZE
                    and filled[ny][nx]
                ):
                    grid[y][x] = OUTLINE
                    break


def spike_extension(theta, spikes):
    ext = 0.0
    for ang, length, width in spikes:
        gap = abs(((theta - ang + math.pi) % (2 * math.pi)) - math.pi)
        if gap < width:
            ext = max(ext, length * (1.0 - gap / width))
    return ext


def ellipse_radius(rx, ry, theta):
    return 1.0 / math.sqrt(
        (math.cos(theta) / rx) ** 2 + (math.sin(theta) / ry) ** 2
    )


FRONT_SPIKES = (
    (math.pi / 2, 14.0, 0.17),
    (math.pi / 2 - 0.4, 11.0, 0.16),
    (math.pi / 2 + 0.4, 11.0, 0.16),
    (math.pi / 2 - 0.8, 9.0, 0.15),
    (math.pi / 2 + 0.8, 9.0, 0.15),
    (math.pi / 2 - 1.2, 8.0, 0.14),
    (math.pi / 2 + 1.2, 8.0, 0.14),
    (0.3, 7.0, 0.13),
    (math.pi - 0.3, 7.0, 0.13),
)


def paint_grid_front():
    grid = new_canvas()
    paint_shirt(grid, top=102, span=44)
    paint_ellipse(grid, HEAD_CX, 54, 30, 36, lambda x, y: SKIN)
    paint_crown_front(grid)
    paint_locks_front(grid)
    paint_bandana_front(grid)
    paint_glasses_front(grid)
    paint_outline(grid)
    return grid


def hairline_front(x):
    line = 40.0 + 2.5 * math.sin(x * 0.5)
    for center, depth in ((47.0, 8.0), (64.0, 10.0), (81.0, 8.0)):
        d = abs(x - center) / 6.5
        if d < 1.0:
            line += depth * (1.0 - d)
    return line


def paint_crown_front(grid):
    for y in range(8, 54):
        for x in range(20, 109):
            dx = (x - HEAD_CX) / 30.0
            dy = (y - 54) / 36.0
            if dx * dx + dy * dy <= 1.0 and y <= hairline_front(x):
                grid[y][x] = hair_shade(x, y)
            elif grid[y][x] == BACKGROUND:
                theta = math.atan2(54.0 - y, x - HEAD_CX)
                dist = math.hypot(x - HEAD_CX, y - 54.0)
                r = ellipse_radius(30.0, 36.0, theta)
                if dist <= r + spike_extension(theta, FRONT_SPIKES):
                    grid[y][x] = hair_shade(x, y)
    for y in range(10, 26):
        for x in range(63, 66):
            if grid[y][x] != BACKGROUND:
                grid[y][x] = PART_LINE


def curtain_shade(x, y, edge_distance):
    shade = hair_shade(x, y)
    if y < 82 and edge_distance < 9 and shade == HAIR_LIGHT:
        return HAIR_MID
    return shade


def paint_locks_front(grid):
    for y in range(30, 120):
        if y <= 88:
            inner = HEAD_CX - max(ellipse_half(HEAD_CX, 54, 30, 36, y) - 5.0, 15.0)
        else:
            inner = HEAD_CX - 15.0
        width = 19.0 - (y - 30) * 0.1 + 2.2 * math.sin(y * 0.43)
        if y > 108:
            width = (120.0 - y) * 0.8
        if width <= 1.0:
            continue
        outer = inner - width
        for x in range(max(18, int(outer)), min(HEAD_CX, int(inner)) + 1):
            grid[y][x] = curtain_shade(x, y, inner - x)
        for x in range(
            max(HEAD_CX, int(PORTRAIT_SIZE - 1 - inner)),
            min(110, int(PORTRAIT_SIZE - 1 - outer)) + 1,
        ):
            grid[y][x] = curtain_shade(x, y, x - (PORTRAIT_SIZE - 1 - inner))


def paint_glasses_front(grid):
    for cx in (48, 80):
        paint_ellipse(grid, cx, 58, 11, 9, lambda x, y: GLASS_RIM)
        paint_ellipse(grid, cx, 58, 8, 6, lambda x, y: lens_shade(x, y, 58, 6))
        for dx in range(-6, 7):
            for y in (49, 50):
                if grid[y][cx + dx] == GLASS_RIM:
                    grid[y][cx + dx] = GLASS_GLINT
    for y in (56, 57, 58):
        for x in (60, 61, 62, 63, 64, 65, 66, 67, 68):
            grid[y][x] = GLASS_RIM
    for x in range(28, 36):
        grid[56][x] = GLASS_RIM
        grid[57][x] = GLASS_RIM
    for x in range(92, 101):
        grid[56][x] = GLASS_RIM
        grid[57][x] = GLASS_RIM


def paint_bandana_front(grid):
    for y in range(70, 90):
        t = (y - 70.0) / 20.0
        half = 24.0 * (1.0 - t)
        if half <= 0.5:
            continue
        for x in range(int(HEAD_CX - half), int(HEAD_CX + half) + 1):
            grid[y][x] = bandana_silver_shade(x, y, 70, 90)


def paint_beard_front(grid):
    for y in range(84, 106):
        half = 17.0 if y < 96 else 17.0 - (y - 96) * 1.1
        for x in range(HEAD_CX - int(half), HEAD_CX + int(half) + 1):
            grid[y][x] = beard_shade(x, y)
    for y in range(74, 91):
        for x in range(30, 99):
            dx = (x - HEAD_CX) / 30.0
            dy = (y - 54) / 36.0
            if dx * dx + dy * dy <= 1.0 and abs(x - HEAD_CX) >= 18:
                grid[y][x] = beard_shade(x, y)


def paint_grid_side():
    grid = new_canvas()
    paint_shirt(grid, top=104, span=46)
    paint_ellipse(grid, 70, 54, 26, 34, lambda x, y: SKIN)
    paint_crown_side(grid)
    paint_back_mass_side(grid)
    paint_ellipse(grid, 64, 64, 4, 6, lambda x, y: SKIN)
    paint_bandana_side(grid)
    paint_glasses_side(grid)
    paint_outline(grid)
    return grid


SIDE_SPIKES = (
    (math.pi / 2, 14.0, 0.15),
    (math.pi / 2 - 0.45, 10.0, 0.14),
    (math.pi / 2 + 0.45, 12.0, 0.15),
    (math.pi / 2 + 0.95, 9.0, 0.14),
    (math.pi / 2 - 0.95, 8.0, 0.13),
    (math.pi - 0.4, 8.0, 0.14),
    (math.pi - 0.9, 7.0, 0.13),
)


def paint_crown_side(grid):
    for y in range(8, 54):
        for x in range(40, 104):
            cap_dx = (x - 72) / 30.0
            cap_dy = (y - 32) / 20.0
            dx = (x - 70) / 26.0
            dy = (y - 54) / 34.0
            in_head = dx * dx + dy * dy <= 1.0
            top_edge = 54.0 - 34.0 * (1.0 - dx * dx) ** 0.5 if in_head else 200.0
            if cap_dx * cap_dx + cap_dy * cap_dy <= 1.0 or (in_head and y <= top_edge + 14.0):
                grid[y][x] = hair_shade(x, y)
    for y in range(4, 54):
        for x in range(30, 110):
            if grid[y][x] != BACKGROUND:
                continue
            theta = math.atan2(54.0 - y, x - 70)
            if theta < 0.45:
                continue
            dist = math.hypot(x - 70, y - 54.0)
            r = ellipse_radius(26.0, 34.0, theta)
            if dist <= r + spike_extension(theta, SIDE_SPIKES):
                grid[y][x] = hair_shade(x, y)


def paint_back_mass_side(grid):
    for y in range(20, 98):
        fall = max(0.0, (y - 30) / 50.0)
        inner = 56.0 + 4.0 * fall + 2.0 * math.sin(y * 0.22 + 1.0)
        outer = 36.0 + 4.0 * fall + 3.5 * math.sin(y * 0.29)
        if y > 78:
            outer = inner - (98.0 - y) * 1.1
        if outer >= inner:
            continue
        for x in range(max(0, int(outer)), min(PORTRAIT_SIZE - 1, int(inner)) + 1):
            grid[y][x] = curtain_shade(x, y, inner - x)


def paint_beard_side(grid):
    paint_ellipse(grid, 84, 94, 14, 10, beard_shade)


def paint_glasses_side(grid):
    paint_ellipse(grid, 82, 56, 10, 8, lambda x, y: GLASS_RIM)
    paint_ellipse(grid, 82, 56, 7, 5, lambda x, y: lens_shade(x, y, 56, 5))
    for dx in range(-5, 6):
        for y in (48, 49):
            if grid[y][82 + dx] == GLASS_RIM:
                grid[y][82 + dx] = GLASS_GLINT
    for x in range(64, 76):
        grid[54][x] = GLASS_RIM
        grid[55][x] = GLASS_RIM


def paint_bandana_side(grid):
    for y in range(70, 88):
        t = (y - 70.0) / 18.0
        right = 92.0 - 11.0 * t
        left = 75.0 + 6.0 * t
        if right - left <= 0.5:
            continue
        for x in range(int(left), int(right) + 1):
            grid[y][x] = bandana_silver_shade(x, y, 70, 88)


BACK_SPIKES = (
    (math.pi / 2, 16.0, 0.15),
    (math.pi / 2 - 0.42, 13.0, 0.14),
    (math.pi / 2 + 0.42, 13.0, 0.14),
    (math.pi / 2 - 0.9, 11.0, 0.14),
    (math.pi / 2 + 0.9, 11.0, 0.14),
    (math.pi / 2 - 1.35, 10.0, 0.14),
    (math.pi / 2 + 1.35, 10.0, 0.14),
    (0.12, 9.0, 0.12),
    (math.pi - 0.12, 9.0, 0.12),
)


def paint_back_spikes(grid):
    for y in range(0, 112):
        for x in range(10, 119):
            theta = math.atan2(56.0 - y, x - HEAD_CX)
            dist = math.hypot(x - HEAD_CX, y - 56.0)
            r = ellipse_radius(36.0, 38.0, theta)
            if (
                dist <= r + spike_extension(theta, BACK_SPIKES)
                and y <= 106.0 + 4.0 * math.sin(x * 0.37)
            ):
                grid[y][x] = hair_shade(x, y)


def paint_grid_back():
    grid = new_canvas()
    paint_shirt(grid, top=102, span=44)
    paint_back_spikes(grid)
    for y in range(12, 28):
        for x in range(63, 66):
            if grid[y][x] != BACKGROUND:
                grid[y][x] = PART_LINE
    paint_outline(grid)
    return grid


def paint_portraits():
    grids = {
        "front": paint_grid_front(),
        "side": paint_grid_side(),
        "back": paint_grid_back(),
    }
    for key, grid in grids.items():
        bank, u, v = PORTRAIT_BANKS[key]
        pyxel.images[bank].set(u, v, to_char_rows(grid))
    return grids


def to_char_rows(grid):
    return [
        "".join("0123456789abcdef"[col] for col in row)
        for row in grid
    ]


def thumb_grid_from_rows(rows):
    return [[int(ch, 16) for ch in row] for row in rows]


PAINTED_BG_CHAR = "3"
PAINTED_SKY_CHAR = "f"
PAINTED_COLKEY = 15
HERO_PAINTED_SIZE = 64


def painted_hero_rows(key):
    return [
        "".join(
            PAINTED_SKY_CHAR if ch == PAINTED_BG_CHAR else ch
            for ch in row
        )
        for row in PAINTED_ROWS[key]
    ]


def render_painted_hero():
    for key, (u, v) in HERO_PAINTED_POS.items():
        pyxel.images[HERO_PAINTED_BANK].set(u, v, painted_hero_rows(key))


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