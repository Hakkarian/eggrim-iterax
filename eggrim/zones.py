from pathlib import Path

import pyxel

TILE = 8

TILE_FLOOR_A = "0010"
TILE_FLOOR_B = "0110"
TILE_WALL = "0210"
LEGEND = {
    ".": TILE_FLOOR_A,
    ",": TILE_FLOOR_B,
    "#": TILE_WALL,
    "P": TILE_FLOOR_A,
    "@": TILE_FLOOR_A,
    "D": TILE_FLOOR_A,
}

ENTITY_MARKERS = {"P": "pillar", "@": "player_start", "D": "door"}
CHUNK_TILES = 32
TILE_TYPE_INDEX = {".": 0, ",": 1, "#": 2, "P": 0, "@": 0, "D": 0}

ZONE_LINKS = {
    ("arena", 0): ("chamber", 0),
    ("chamber", 0): ("arena", 0),
}


class Zone:
    def __init__(self, name, chunks, width_tiles, height_tiles, markers, grid):
        self.name = name
        self.chunks = chunks
        self.width_tiles = width_tiles
        self.height_tiles = height_tiles
        self.width_px = width_tiles * TILE
        self.height_px = height_tiles * TILE
        self.markers = markers
        self.pillar_spawns = [
            ((x + 0.5) * TILE, (y + 0.5) * TILE) for x, y in markers["pillar"]
        ]
        self.doors = list(markers["door"])
        start = (
            markers["player_start"][0]
            if markers["player_start"]
            else (width_tiles / 2 - 0.5, height_tiles / 2 - 0.5)
        )
        self.player_start = ((start[0] + 0.5) * TILE, (start[1] + 0.5) * TILE)
        self.grid = grid


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
    markers = {kind: [] for kind in ENTITY_MARKERS.values()}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in ENTITY_MARKERS:
                markers[ENTITY_MARKERS[ch]].append((x, y))
    chunks = []
    for chunk_y in range(0, len(rows), CHUNK_TILES):
        for chunk_x in range(0, width, CHUNK_TILES):
            chunk_rows = [
                row[chunk_x : chunk_x + CHUNK_TILES]
                for row in rows[chunk_y : chunk_y + CHUNK_TILES]
            ]
            chunk_data = [
                " ".join(LEGEND[ch] for ch in row) for row in chunk_rows
            ]
            tilemap = pyxel.Tilemap(len(chunk_rows[0]), len(chunk_rows), 0)
            tilemap.set(0, 0, chunk_data)
            chunks.append((chunk_x, chunk_y, tilemap))
    zone = Zone(name, chunks, width, len(rows), markers, rows)
    _zones_cache[name] = zone
    return zone