import pyxel

FOG_RGB = (225, 235, 250)
FOG_COLOR = 15

PILLAR_TINT_STEPS = 11
PILLAR_VIS_INNER = 45.0
PILLAR_VIS_OUTER = 105.0

TILE_TINT_SRC_X = (0, 8, 16)
TILE_TINT_SRC_Y = 128
TILE_TINT_V = 48

WALL_FLASH_U = 96
WALL_FLASH_V = 64


def palette_rgb(value):
    return ((value >> 16) & 255, (value >> 8) & 255, value & 255)


def nearest_fog_palette(rgb):
    best = 1
    best_dist = None
    for col in range(1, 16):
        pal = palette_rgb(pyxel.colors[col])
        dist = sum((pal[i] - rgb[i]) ** 2 for i in range(3))
        if best_dist is None or dist < best_dist:
            best, best_dist = col, dist
    return best


def blend_color_to_fog(rgb, alpha):
    return tuple(rgb[i] + (FOG_RGB[i] - rgb[i]) * alpha for i in range(3))


def pillar_tint_level(dist):
    if dist >= PILLAR_VIS_OUTER:
        return None
    if dist <= PILLAR_VIS_INNER:
        return 0
    return round(
        (dist - PILLAR_VIS_INNER) / (PILLAR_VIS_OUTER - PILLAR_VIS_INNER) * (PILLAR_TINT_STEPS - 1)
    )


def render_pillar_tints():
    src = pyxel.images[0]
    dst = pyxel.images[2]
    for level in range(PILLAR_TINT_STEPS):
        alpha = level / (PILLAR_TINT_STEPS - 1)
        rows = []
        for y in range(16):
            chars = []
            for x in range(16):
                col = src.pget(128 + x, y)
                if col == 0:
                    chars.append("0")
                else:
                    rgb = palette_rgb(pyxel.colors[col])
                    chars.append("0123456789abcdef"[nearest_fog_palette(blend_color_to_fog(rgb, alpha))])
            rows.append("".join(chars))
        dst.set(16 * level, 32, rows)


def render_tile_tints():
    pyxel.colors[FOG_COLOR] = (FOG_RGB[0] << 16) | (FOG_RGB[1] << 8) | FOG_RGB[2]
    src = pyxel.images[0]
    dst = pyxel.images[2]
    for type_index, src_x in enumerate(TILE_TINT_SRC_X):
        for level in range(PILLAR_TINT_STEPS):
            alpha = level / (PILLAR_TINT_STEPS - 1)
            rows = []
            for y in range(8):
                chars = []
                for x in range(8):
                    col = src.pget(src_x + x, TILE_TINT_SRC_Y + y)
                    if col == 0:
                        chars.append("0")
                    else:
                        rgb = palette_rgb(pyxel.colors[col])
                        chars.append(
                            "0123456789abcdef"[nearest_fog_palette(blend_color_to_fog(rgb, alpha))]
                        )
                rows.append("".join(chars))
            dst.set(level * 8, TILE_TINT_V + type_index * 8, rows)
    flash_rows = []
    for y in range(8):
        chars = []
        for x in range(8):
            col = src.pget(16 + x, TILE_TINT_SRC_Y + y)
            chars.append("0" if col == 0 else "7")
        flash_rows.append("".join(chars))
    dst.set(WALL_FLASH_U, WALL_FLASH_V, flash_rows)