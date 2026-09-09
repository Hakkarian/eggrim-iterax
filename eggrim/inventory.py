import pyxel

from eggrim import cursor
from eggrim.assets.factory import hero_frame, set_scarf_worn, tpose_frame
from eggrim.items import draw_scarf_sprite

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

_dither_map = None
_opened = False
_items = []
_equipped = {}
_drag_item = None
_drag_from = None

SLOT_ITEMS = {"fist_left": "scarf"}


def add_item(name):
    _items.append(name)


def has_item(name):
    return name in _items or name in _equipped.values()


def remove_item(name):
    if name in _items:
        _items.remove(name)
    else:
        for slot, item in list(_equipped.items()):
            if item == name:
                del _equipped[slot]
    _sync_scarf_worn()


def _sync_scarf_worn():
    set_scarf_worn(_equipped.get("fist_left") == "scarf")


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
    cursor.reset()


def close():
    global _opened
    _opened = False
    cursor.reset()


def is_open():
    return _opened


def tpose_origin():
    frame = tpose_frame("front")
    if frame is None:
        return None
    cx = MODAL_X + HALF_W // 2
    t = MODAL_Y + (MODAL_H - TPOSE_HEIGHT) // 2
    return cx - frame[3] // 2, t + (TPOSE_HEIGHT - frame[4]) // 2


def sphere_center(name):
    origin = tpose_origin()
    if origin is None:
        return None
    for sphere_name, ax, ay in TPOSE_SPHERES:
        if sphere_name == name:
            return origin[0] + ax, origin[1] + ay
    return None


def cell_at(mx, my):
    for index in range(GRID_COLS * GRID_ROWS):
        cell_x, cell_y = cell_top_left(index)
        if cell_x <= mx < cell_x + CELL_SIZE and cell_y <= my < cell_y + CELL_SIZE:
            return index
    return None


def sphere_at(mx, my):
    for name, _, _ in TPOSE_SPHERES:
        center = sphere_center(name)
        if center is None:
            continue
        dx = mx - center[0]
        dy = my - center[1]
        if dx * dx + dy * dy <= SPHERE_RADIUS * SPHERE_RADIUS:
            return name
    return None


def update():
    global _drag_item, _drag_from
    if _drag_item is not None and not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
        drop_dragged()
        return
    if _drag_item is None and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        target = cell_at(pyxel.mouse_x, pyxel.mouse_y)
        if target is not None and target < len(_items):
            _drag_item = _items.pop(target)
            _drag_from = target
            return
        sphere = sphere_at(pyxel.mouse_x, pyxel.mouse_y)
        if sphere is not None and sphere in _equipped:
            _drag_item = _equipped.pop(sphere)
            _drag_from = sphere


def drop_dragged():
    global _drag_item, _drag_from
    item, source = _drag_item, _drag_from
    _drag_item = None
    _drag_from = None
    mx = pyxel.mouse_x
    my = pyxel.mouse_y
    sphere = sphere_at(mx, my)
    if sphere is not None and SLOT_ITEMS.get(sphere) == item and sphere not in _equipped:
        _equipped[sphere] = item
        _sync_scarf_worn()
        return
    target = cell_at(mx, my)
    if target is not None:
        if target >= len(_items):
            _items.append(item)
        else:
            restore(item, source)
        _sync_scarf_worn()
        return
    restore(item, source)
    _sync_scarf_worn()


def restore(item, source):
    if source is None:
        _items.append(item)
    elif isinstance(source, int):
        _items.insert(min(source, len(_items)), item)
    else:
        _equipped[source] = item


def cursor_state():
    if _drag_item is not None:
        return "grab"
    target = cell_at(pyxel.mouse_x, pyxel.mouse_y)
    if target is not None and target < len(_items):
        return "open"
    sphere = sphere_at(pyxel.mouse_x, pyxel.mouse_y)
    if sphere is not None and sphere in _equipped:
        return "open"
    return "arrow"


TPOSE_HEIGHT = 56
OUTLINE_COLOR = 1
UNIFORM_MAIN_COLOR = 4
UNIFORM_SHADOW_COLOR = 3
UNIFORM_DARK_COLOR = 6
SKIN_COLOR = 11
SKIN_SHADOW_COLOR = 10
HAIR_COLOR = 12
HAIR_HIGHLIGHT_COLOR = 13
TRIM_COLOR = 9
SPHERE_COLOR = 12
SPHERE_RADIUS = 6
TPOSE_SPHERES = (
    ("head", 27, -6),
    ("fist_left", -2, 19),
    ("fist_right", 56, 19),
    ("foot_left", 20, 55),
    ("foot_right", 36, 55),
)


def draw_sphere(x, y, radius, color):
    pyxel.circb(x, y, radius, color)
    for yy in range(-radius + 1, radius):
        for xx in range(-radius + 1, radius):
            if xx * xx + yy * yy <= radius * radius and (x + xx + y + yy) % 2 == 0:
                pyxel.pset(x + xx, y + yy, color)


def draw_tpose_hero():
    cx = MODAL_X + HALF_W // 2
    t = MODAL_Y + (MODAL_H - TPOSE_HEIGHT) // 2
    frame = tpose_frame("front")
    if frame is not None:
        bank, u, v, w, h = frame
        ox = cx - w // 2
        oy = t + (TPOSE_HEIGHT - h) // 2
        pyxel.blt(ox, oy, bank, u, v, w, h, 0)
        hover = sphere_at(pyxel.mouse_x, pyxel.mouse_y) if _drag_item else None
        for name, ax, ay in TPOSE_SPHERES:
            sx = ox + ax
            sy = oy + ay
            if name == hover and SLOT_ITEMS.get(name) == _drag_item:
                draw_sphere(sx, sy, SPHERE_RADIUS, HAIR_HIGHLIGHT_COLOR)
            else:
                draw_sphere(sx, sy, SPHERE_RADIUS, SPHERE_COLOR)
            if name in _equipped:
                draw_scarf_sprite(sx, sy)
        return
    frame = hero_frame("idle", "front", 0)
    if frame is not None:
        bank, u, v, w, h = frame
        pyxel.blt(cx - w // 2, t + (TPOSE_HEIGHT - h) // 2, bank, u, v, w, h, 0)
        return
    pyxel.rect(cx - 2, t + 10, 4, 4, SKIN_SHADOW_COLOR)
    pyxel.rect(cx - 10, t + 12, 20, 6, OUTLINE_COLOR)
    pyxel.rect(cx - 9, t + 13, 18, 4, UNIFORM_MAIN_COLOR)
    pyxel.line(cx - 9, t + 16, cx + 8, t + 16, UNIFORM_SHADOW_COLOR)
    pyxel.rect(cx - 32, t + 12, 6, 7, OUTLINE_COLOR)
    pyxel.rect(cx - 31, t + 13, 4, 5, SKIN_COLOR)
    pyxel.rect(cx + 26, t + 12, 6, 7, OUTLINE_COLOR)
    pyxel.rect(cx + 27, t + 13, 4, 5, SKIN_COLOR)
    pyxel.rect(cx - 31, t + 12, 22, 6, OUTLINE_COLOR)
    pyxel.rect(cx - 30, t + 13, 20, 4, UNIFORM_MAIN_COLOR)
    pyxel.line(cx - 30, t + 13, cx - 11, t + 13, TRIM_COLOR)
    pyxel.line(cx - 30, t + 16, cx - 11, t + 16, UNIFORM_SHADOW_COLOR)
    pyxel.rect(cx + 9, t + 12, 22, 6, OUTLINE_COLOR)
    pyxel.rect(cx + 10, t + 13, 20, 4, UNIFORM_MAIN_COLOR)
    pyxel.line(cx + 11, t + 13, cx + 30, t + 13, TRIM_COLOR)
    pyxel.line(cx + 11, t + 16, cx + 30, t + 16, UNIFORM_SHADOW_COLOR)
    pyxel.rect(cx - 10, t + 16, 20, 16, OUTLINE_COLOR)
    pyxel.rect(cx - 9, t + 17, 18, 14, UNIFORM_MAIN_COLOR)
    pyxel.line(cx - 8, t + 21, cx - 3, t + 21, UNIFORM_SHADOW_COLOR)
    pyxel.line(cx + 3, t + 21, cx + 8, t + 21, UNIFORM_SHADOW_COLOR)
    pyxel.rect(cx - 10, t + 16, 4, 2, TRIM_COLOR)
    pyxel.rect(cx + 6, t + 16, 4, 2, TRIM_COLOR)
    pyxel.line(cx - 4, t + 16, cx, t + 19, TRIM_COLOR)
    pyxel.line(cx + 4, t + 16, cx, t + 19, TRIM_COLOR)
    pyxel.line(cx, t + 19, cx, t + 31, UNIFORM_SHADOW_COLOR)
    pyxel.pset(cx, t + 20, HAIR_HIGHLIGHT_COLOR)
    pyxel.pset(cx, t + 23, TRIM_COLOR)
    pyxel.pset(cx - 1, t + 24, TRIM_COLOR)
    pyxel.pset(cx + 1, t + 24, TRIM_COLOR)
    pyxel.pset(cx, t + 25, TRIM_COLOR)
    pyxel.rect(cx - 8, t + 31, 16, 3, UNIFORM_SHADOW_COLOR)
    pyxel.rect(cx - 2, t + 31, 4, 3, TRIM_COLOR)
    pyxel.rect(cx - 8, t + 34, 16, 2, UNIFORM_MAIN_COLOR)
    pyxel.rect(cx - 8, t + 36, 7, 14, OUTLINE_COLOR)
    pyxel.rect(cx - 7, t + 36, 5, 13, UNIFORM_MAIN_COLOR)
    pyxel.line(cx - 4, t + 38, cx - 4, t + 48, UNIFORM_SHADOW_COLOR)
    pyxel.rect(cx + 1, t + 36, 7, 14, OUTLINE_COLOR)
    pyxel.rect(cx + 2, t + 36, 5, 13, UNIFORM_MAIN_COLOR)
    pyxel.line(cx + 5, t + 38, cx + 5, t + 48, UNIFORM_SHADOW_COLOR)
    pyxel.rect(cx - 9, t + 49, 8, 6, OUTLINE_COLOR)
    pyxel.rect(cx - 8, t + 50, 6, 4, UNIFORM_DARK_COLOR)
    pyxel.rect(cx + 1, t + 49, 8, 6, OUTLINE_COLOR)
    pyxel.rect(cx + 2, t + 50, 6, 4, UNIFORM_DARK_COLOR)
    pyxel.line(cx - 8, t + 50, cx - 3, t + 50, TRIM_COLOR)
    pyxel.line(cx + 2, t + 50, cx + 7, t + 50, TRIM_COLOR)
    pyxel.circ(cx, t + 6, 5, SKIN_COLOR)
    pyxel.circb(cx, t + 6, 5, OUTLINE_COLOR)
    pyxel.rect(cx - 4, t + 1, 9, 3, HAIR_COLOR)
    pyxel.pset(cx - 5, t + 4, HAIR_COLOR)
    pyxel.pset(cx + 4, t + 4, HAIR_COLOR)
    pyxel.pset(cx + 1, t + 2, HAIR_HIGHLIGHT_COLOR)
    pyxel.pset(cx + 2, t + 3, HAIR_HIGHLIGHT_COLOR)
    pyxel.pset(cx - 2, t + 7, OUTLINE_COLOR)
    pyxel.pset(cx + 2, t + 7, OUTLINE_COLOR)
    pyxel.pset(cx - 3, t + 6, SKIN_SHADOW_COLOR)
    pyxel.pset(cx + 3, t + 6, SKIN_SHADOW_COLOR)


def grid_origin():
    grid_w = GRID_COLS * CELL_SIZE + (GRID_COLS - 1) * CELL_GAP
    grid_h = GRID_ROWS * CELL_SIZE + (GRID_ROWS - 1) * CELL_GAP
    x0 = MODAL_X + HALF_W + (MODAL_W - HALF_W - grid_w) // 2
    y0 = MODAL_Y + (MODAL_H - grid_h) // 2
    return x0, y0


def cell_top_left(index):
    x0, y0 = grid_origin()
    col = index % GRID_COLS
    row = index // GRID_COLS
    return x0 + col * (CELL_SIZE + CELL_GAP), y0 + row * (CELL_SIZE + CELL_GAP)


def draw_grid():
    for index in range(GRID_COLS * GRID_ROWS):
        cell_x, cell_y = cell_top_left(index)
        pyxel.rectb(cell_x, cell_y, CELL_SIZE, CELL_SIZE, BORDER_COLOR)
        if index >= len(_items):
            continue
        icon_cx = cell_x + CELL_SIZE // 2
        icon_cy = cell_y + CELL_SIZE // 2
        if _items[index] == "scarf":
            draw_scarf_sprite(icon_cx, icon_cy)


def draw():
    pyxel.bltm(0, 0, _dither_map, 0, 0, SCREEN_W, SCREEN_H, 0)
    pyxel.rect(MODAL_X, MODAL_Y, MODAL_W, MODAL_H, PANEL_COLOR)
    pyxel.rectb(MODAL_X, MODAL_Y, MODAL_W, MODAL_H, BORDER_COLOR)
    divider_x = MODAL_X + HALF_W
    pyxel.line(
        divider_x, MODAL_Y + 1, divider_x, MODAL_Y + MODAL_H - 2, BORDER_COLOR
    )
    draw_tpose_hero()
    draw_grid()
    if _drag_item is not None:
        draw_scarf_sprite(pyxel.mouse_x, pyxel.mouse_y)
    cursor.show(cursor_state())
    cursor.draw()