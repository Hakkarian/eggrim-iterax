from pathlib import Path

TILE = 8

ENTITY_MARKERS = {"P": "pillar", "@": "player_start", "D": "door"}
TILE_TYPE_INDEX = {".": 0, ",": 1, "#": 2, "P": 0, "@": 0, "D": 0}

ZONE_LINKS = {
    ("arena", 0): ("chamber", 0),
    ("chamber", 0): ("arena", 0),
}


class Zone:
    def __init__(self, name, width_tiles, height_tiles, markers, grid):
        self.name = name
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
    zone = Zone(name, width, len(rows), markers, rows)
    _zones_cache[name] = zone
    return zone