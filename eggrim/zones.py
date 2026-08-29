from pathlib import Path

import pyxel

TILE = 8

TILE_FLOOR_A = "0010"
TILE_FLOOR_B = "0110"
TILE_WALL = "0210"
LEGEND = {".": TILE_FLOOR_A, ",": TILE_FLOOR_B, "#": TILE_WALL, "P": TILE_FLOOR_A}

ENTITY_MARKERS = {"P": "pillar"}


class Zone:
    def __init__(self, name, tilemap, markers):
        self.name = name
        self.tilemap = tilemap
        self.width_tiles = tilemap.width
        self.height_tiles = tilemap.height
        self.width_px = tilemap.width * TILE
        self.height_px = tilemap.height * TILE
        self.markers = markers
        self.pillar_spawns = markers["pillar"]


_zones_cache = {}


def render_tiles():
    pyxel.images[0].set(0, 128, ("33333333",) * 8)
    pyxel.images[0].set(
        8,
        128,
        (
            "33333333",
            "33333333",
            "33313333",
            "33333333",
            "33333313",
            "33333333",
            "33133333",
            "33333333",
        ),
    )
    pyxel.images[0].set(
        16,
        128,
        (
            "00000000",
            "05555550",
            "05555550",
            "05555550",
            "05555550",
            "05555550",
            "05555550",
            "00000000",
        ),
    )


def load_zone(name):
    if name in _zones_cache:
        return _zones_cache[name]
    path = Path(__file__).parent / "zones" / f"{name}.txt"
    rows = [line for line in path.read_text().splitlines() if line.strip()]
    width = max(len(row) for row in rows)
    data = [
        " ".join(LEGEND[ch] for ch in row.ljust(width))
        for row in rows
    ]
    markers = {kind: [] for kind in ENTITY_MARKERS.values()}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in ENTITY_MARKERS:
                markers[ENTITY_MARKERS[ch]].append(((x + 0.5) * TILE, (y + 0.5) * TILE))
    tilemap = pyxel.Tilemap(width, len(rows), 0)
    tilemap.set(0, 0, data)
    zone = Zone(name, tilemap, markers)
    _zones_cache[name] = zone
    return zone