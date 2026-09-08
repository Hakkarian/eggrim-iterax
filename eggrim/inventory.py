import pyxel

SCREEN_W = 256
SCREEN_H = 144
MODAL_W = 154
MODAL_H = 115
MODAL_X = (SCREEN_W - MODAL_W) // 2
MODAL_Y = (SCREEN_H - MODAL_H) // 2
HALF_W = MODAL_W // 2
GRID_COLS = 4
GRID_ROWS = 5
CELL_SIZE = 12
CELL_GAP = 2

DITHER_TILE_U = 248
DITHER_TILE_V = 248
BACKDROP_COLOR = 6
PANEL_COLOR = 2
BORDER_COLOR = 3
SILHOUETTE_COLOR = 3

_dither_map = None
_opened = False


def render_backdrop():
    global _dither_map
    rows = [
        "".join(
            f"{BACKDROP_COLOR:x}" if (x + y) % 2 == 0 else "0" for x in range(8)
        )
        for y in range(8)
    ]
    pyxel.images[0].set(DITHER_TILE_U, DITHER_TILE_V, rows)
    _dither_map = pyxel.Tilemap(SCREEN_W // 8, SCREEN_H // 8, 0)
    token = f"{DITHER_TILE_U // 8:02x}{DITHER_TILE_V // 8:02x}"
    _dither_map.set(0, 0, [" ".join([token] * (SCREEN_W // 8)) for _ in range(SCREEN_H // 8)])


def toggle():
    global _opened
    _opened = not _opened


def close():
    global _opened
    _opened = False


def is_open():
    return _opened


TPOSE_HEIGHT = 56


def draw_tpose_placeholder():
    center_x = MODAL_X + HALF_W // 2
    top = MODAL_Y + (MODAL_H - TPOSE_HEIGHT) // 2
    pyxel.circ(center_x, top + 6, 5, SILHOUETTE_COLOR)
    pyxel.line(center_x - 16, top + 20, center_x + 16, top + 20, SILHOUETTE_COLOR)
    pyxel.line(center_x - 16, top + 20, center_x - 16, top + 16, SILHOUETTE_COLOR)
    pyxel.line(center_x + 16, top + 20, center_x + 16, top + 16, SILHOUETTE_COLOR)
    pyxel.rect(center_x - 6, top + 13, 12, 24, SILHOUETTE_COLOR)
    pyxel.line(center_x - 4, top + 37, center_x - 4, top + 56, SILHOUETTE_COLOR)
    pyxel.line(center_x + 4, top + 37, center_x + 4, top + 56, SILHOUETTE_COLOR)


def draw_grid():
    grid_w = GRID_COLS * CELL_SIZE + (GRID_COLS - 1) * CELL_GAP
    grid_h = GRID_ROWS * CELL_SIZE + (GRID_ROWS - 1) * CELL_GAP
    x0 = MODAL_X + HALF_W + (MODAL_W - HALF_W - grid_w) // 2
    y0 = MODAL_Y + (MODAL_H - grid_h) // 2
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell_x = x0 + col * (CELL_SIZE + CELL_GAP)
            cell_y = y0 + row * (CELL_SIZE + CELL_GAP)
            pyxel.rectb(cell_x, cell_y, CELL_SIZE, CELL_SIZE, BORDER_COLOR)


def draw():
    pyxel.bltm(0, 0, _dither_map, 0, 0, SCREEN_W, SCREEN_H, 0)
    pyxel.rect(MODAL_X, MODAL_Y, MODAL_W, MODAL_H, PANEL_COLOR)
    pyxel.rectb(MODAL_X, MODAL_Y, MODAL_W, MODAL_H, BORDER_COLOR)
    divider_x = MODAL_X + HALF_W
    pyxel.line(
        divider_x, MODAL_Y + 1, divider_x, MODAL_Y + MODAL_H - 2, BORDER_COLOR
    )
    draw_tpose_placeholder()
    draw_grid()