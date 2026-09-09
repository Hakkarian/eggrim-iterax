import json
import os

import pyxel
from PIL import Image

CURSOR_DIR = os.path.join(os.path.dirname(__file__), "assets", "drawn", "cursor")
PALETTE_JSON = os.path.join(
    os.path.dirname(__file__), "assets", "drawn", "readmey_locked", "hero_palette.json"
)
SPRITE_SOURCES = {
    "arrow": ("cursor_arrow_small.png", (3, 2, 64, 64), "arrow"),
    "open": ("cursor_hand.png", (48, 0, 61, 19), "hand"),
    "grab_curled": ("cursor_hand.png", (0, 5, 13, 19), "hand"),
}
MAX_SPRITE_SIZE = (12, 12)

_sprites = {}
_state = None
_mouse_applied = True


def _apply_mouse(visible):
    global _mouse_applied
    if _mouse_applied != visible:
        pyxel.mouse(visible)
        _mouse_applied = visible


def _palette_index_map():
    slots = json.load(open(PALETTE_JSON))["palette"]
    palette = [
        tuple(int(rgb[i : i + 2], 16) for i in (1, 3, 5)) for rgb in slots
    ]
    index_by_rgb = {rgb: index + 1 for index, rgb in enumerate(palette)}
    return palette, index_by_rgb


def _dominant_colors(region, count):
    raw_counts = {}
    src = region.load()
    for y in range(region.height):
        for x in range(region.width):
            r, g, b, a = src[x, y]
            if a:
                raw_counts[(r, g, b)] = raw_counts.get((r, g, b), 0) + 1
    return sorted(raw_counts, key=lambda rgb: -raw_counts[rgb])[:count]


def _dominant_palette_map(dominant, palette):
    return {
        rgb: min(
            palette,
            key=lambda c: (c[0] - rgb[0]) ** 2
            + (c[1] - rgb[1]) ** 2
            + (c[2] - rgb[2]) ** 2,
        )
        for rgb in dominant
    }


def _voted_cells(region, tw, th, dominant, palette_map, index_by_rgb):
    sw, sh = region.size
    src = region.load()
    pixels = []
    for ty in range(th):
        for tx in range(tw):
            x0, x1 = tx * sw // tw, (tx + 1) * sw // tw
            y0, y1 = ty * sh // th, (ty + 1) * sh // th
            counts = {}
            for y in range(y0, y1):
                for x in range(x0, x1):
                    r, g, b, a = src[x, y]
                    if a < 128:
                        continue
                    rgb = min(
                        dominant,
                        key=lambda c: (c[0] - r) ** 2
                        + (c[1] - g) ** 2
                        + (c[2] - b) ** 2,
                    )
                    counts[rgb] = counts.get(rgb, 0) + 1
            area = (x1 - x0) * (y1 - y0)
            if sum(counts.values()) < area // 2:
                continue
            rgb = max(counts, key=lambda c: counts[c])
            pixels.append((tx, ty, index_by_rgb[palette_map[rgb]]))
    return pixels


def _load():
    global _sprites, _hotspots
    if _sprites:
        return
    palette, index_by_rgb = _palette_index_map()
    regions = {}
    for name, (file_name, crop, group) in SPRITE_SOURCES.items():
        img = Image.open(os.path.join(CURSOR_DIR, file_name)).convert("RGBA")
        regions[name] = (group, img.crop(crop))
    scales = {}
    for name, (group, region) in regions.items():
        fit = min(
            MAX_SPRITE_SIZE[0] / region.width,
            MAX_SPRITE_SIZE[1] / region.height,
            1.0,
        )
        scales.setdefault(group, []).append(fit)
    group_scales = {}
    for group, fits in scales.items():
        group_scales[group] = min(fits)
    _sprites = {}
    _hotspots = {}
    for name, (group, region) in regions.items():
        scale = group_scales[group]
        tw = max(1, round(region.width * scale))
        th = max(1, round(region.height * scale))
        if scale < 0.4:
            dominant = _dominant_colors(region, 4)
            palette_map = _dominant_palette_map(dominant, palette)
            pixels = _voted_cells(
                region, tw, th, dominant, palette_map, index_by_rgb
            )
        else:
            if scale < 1.0:
                region = region.resize((tw, th), Image.NEAREST)
            pixels = []
            for y in range(region.height):
                for x in range(region.width):
                    r, g, b, a = region.getpixel((x, y))
                    if a == 0:
                        continue
                    rgb = min(
                        palette,
                        key=lambda c: (c[0] - r) ** 2
                        + (c[1] - g) ** 2
                        + (c[2] - b) ** 2,
                    )
                    pixels.append((x, y, index_by_rgb[rgb]))
        _sprites[name] = (tw, th, pixels)
        _hotspots[name] = (tw // 2, th // 2)


def reset():
    global _state
    _state = None
    _apply_mouse(False)


def show(kind):
    global _state
    _state = kind


def draw():
    _load()
    if _state is None:
        _apply_mouse(False)
        return
    _apply_mouse(False)
    if _state == "grab":
        sprite_name = "grab_curled"
    else:
        sprite_name = _state
    width, height, pixels = _sprites[sprite_name]
    hx, hy = _hotspots[sprite_name]
    mx = pyxel.mouse_x - hx
    my = pyxel.mouse_y - hy
    for x, y, color_index in pixels:
        px = mx + x
        py_ = my + y
        if 0 <= px < pyxel.width and 0 <= py_ < pyxel.height:
            pyxel.pset(px, py_, color_index)