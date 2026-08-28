import pyxel

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


PILLAR_TINT_ALPHAS = (0.3, 0.55, 0.8)
PILLAR_RING_RADII = (45.0, 75.0, 105.0)


def blend_color_to_fog(rgb, alpha):
    return tuple(rgb[i] + (FOG_RGB[i] - rgb[i]) * alpha for i in range(3))


def pillar_tint_level(dist):
    for level, radius in enumerate(PILLAR_RING_RADII):
        if dist <= radius:
            return level - 1
    return len(PILLAR_TINT_ALPHAS) - 1


def render_pillar_tints():
    src = pyxel.images[0]
    dst = pyxel.images[2]
    for level, alpha in enumerate(PILLAR_TINT_ALPHAS):
        rows = []
        for y in range(16):
            chars = []
            for x in range(16):
                col = src.pget(96 + x, 16 + y)
                if col == 0:
                    chars.append("0")
                else:
                    rgb = palette_rgb(pyxel.colors[col])
                    chars.append("0123456789abcdef"[nearest_fog_palette(blend_color_to_fog(rgb, alpha))])
            rows.append("".join(chars))
        dst.set(16 * level, 16, rows)


render_fog()