import json
import os
import random

import pyxel
from PIL import Image

HERO_DIR = os.path.join(os.path.dirname(__file__), "drawn", "readmey_locked")
TPOSE_DIR = os.path.join(os.path.dirname(__file__), "drawn", "readmey_tpose")
HERO_STATES = {"idle": 4, "run": 4, "attack": 4, "defensive": 3, "dash": 8}
ENEMY_STATES = {"idle": 3, "attack": 4, "run": 4}
HERO_DIRECTIONS = ("right", "left", "front", "back")
STATE_DIRECTIONS = {"dash": ("left",)}
SCARF_DIRECTIONS = ("right", "front", "back")
BANK_PX = 256
CHARS = "0123456789abcdef"

USED_RECTS = {
    0: (
        (0, 128, 24, 8),
        (0, 136, 128, 64),
        (248, 248, 8, 8),
    ),
    1: (
        (0, 0, 64, 64),
        (64, 0, 64, 64),
        (128, 0, 64, 64),
        (192, 0, 64, 64),
        (0, 128, 64, 64),
    ),
    2: (
        (48, 16, 16, 16),
        (0, 32, 176, 16),
        (0, 48, 88, 24),
        (96, 64, 8, 8),
        (0, 96, 256, 128),
    ),
}

hero_frames = {}
tpose_frames = {}
plain_rows = {}
scarf_rows = {}
scarf_worn = False
hero_palette = ()
palette_chars = {}


def read_palette():
    global hero_palette, palette_chars
    manifest_path = os.path.join(HERO_DIR, "hero_palette.json")
    if not os.path.isfile(manifest_path):
        print("factory: hero_palette.json missing, palette unchanged")
        return False
    with open(manifest_path) as fh:
        slots = json.load(fh)["palette"]
    hero_palette = tuple(
        tuple(int(rgb[i : i + 2], 16) for i in (1, 3, 5)) for rgb in slots
    )
    palette_chars = {
        rgb: CHARS[index + 1] for index, rgb in enumerate(hero_palette)
    }
    for index, rgb in enumerate(hero_palette):
        pyxel.colors[index + 1] = (
            (rgb[0] << 16) | (rgb[1] << 8) | rgb[2]
        )
    return True


def reserve_rect(mask, x, y, w, h):
    win = (1 << w) - 1
    for py in range(y, y + h):
        mask[py] &= ~(win << x)


def free_mask(bank):
    full = (1 << BANK_PX) - 1
    mask = [full] * BANK_PX
    for x, y, w, h in USED_RECTS[bank]:
        reserve_rect(mask, x, y, w, h)
    return mask


def find_slot(mask, w, h):
    win = (1 << w) - 1
    for y in range(BANK_PX - h + 1):
        for x in range(BANK_PX - w + 1):
            if all(((mask[yy] >> x) & win) == win for yy in range(y, y + h)):
                for yy in range(y, y + h):
                    mask[yy] &= ~(win << x)
                return x, y
    return None


def nearest_slot(rgb):
    r, g, b = rgb
    best = min(
        palette_chars,
        key=lambda c: (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2,
    )
    return palette_chars[best]


def frame_rows(img):
    w, h = img.size
    pixels = img.load()
    rows = []
    mismatches = 0
    for y in range(h):
        chars = []
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                chars.append("0")
            else:
                if (r, g, b) not in palette_chars:
                    mismatches += 1
                chars.append(nearest_slot((r, g, b)))
        rows.append("".join(chars))
    return rows, mismatches


def load_hero_asset():
    global hero_frames
    if not palette_chars:
        print("factory: palette not installed, hero stays procedural")
        return
    masks = {bank: free_mask(bank) for bank in (0, 1, 2)}
    free_px = sum(
        bin(row).count("1") for mask in masks.values() for row in mask
    )
    wanted = []
    for state, count in HERO_STATES.items():
        for direction in hero_directions(state):
            for index in range(count):
                wanted.append((state, direction, index))
    for state, count in ENEMY_STATES.items():
        for index in range(count):
            wanted.append(("enemy", state, index))
    images = {}
    missing = []
    for state, direction, index in wanted:
        if state == "enemy":
            path = os.path.join(HERO_DIR, f"{direction}_front_scarf_{index}.png")
            name = f"enemy_{direction}_{index}"
        else:
            path = os.path.join(HERO_DIR, f"{state}_{direction}_{index}.png")
            name = f"{state}_{direction}_{index}"
        if not os.path.isfile(path):
            missing.append(name)
            continue
        images[(state, direction, index)] = Image.open(path).convert("RGBA")
    needed_px = sum(img.size[0] * img.size[1] for img in images.values())
    if needed_px > free_px:
        print(
            f"factory: hero does not fit ({needed_px} px needed, {free_px} px free),"
            " hero stays procedural"
        )
        return
    if missing:
        print(f"factory: missing hero frames: {', '.join(missing)}")
    area_order = sorted(images, key=lambda key: -images[key].size[0] * images[key].size[1])
    orders = [area_order] + [
        random.Random(seed).sample(area_order, len(area_order)) for seed in range(8)
    ]

    def pack():
        for order in orders:
            masks = {
                bank: free_mask(bank)
                for bank in (0, 1, 2)
            }
            placed = {}
            total_mismatches = 0
            unplaced = []
            for key in order:
                img = images[key]
                w, h = img.size
                for bank in (0, 1, 2):
                    slot = find_slot(masks[bank], w, h)
                    if slot is not None:
                        break
                if slot is None:
                    unplaced.append(key)
                    continue
                placed[key] = (bank, slot[0], slot[1], w, h)
                rows, mismatches = frame_rows(img)
                total_mismatches += mismatches
            if not unplaced:
                break
        return placed, total_mismatches, unplaced

    placed, total_mismatches, unplaced = pack()
    for key, (bank, x, y, w, h) in placed.items():
        rows, _ = frame_rows(images[key])
        pyxel.images[bank].set(x, y, rows)
        hero_frames[key] = (bank, x, y, w, h)
        plain_rows[key] = rows
    loaded = len(hero_frames)
    if loaded == 0:
        print("factory: no hero frames placed, hero stays procedural")
        return
    if unplaced:
        print(f"factory: unplaced frames: {', '.join(f'{k[0]}_{k[1]}_{k[2]}' for k in unplaced)}")
    per_state = ", ".join(
        f"{state} {len([1 for k in hero_frames if k[0] == state])}"
        for state in HERO_STATES
    )
    print(
        f"factory: hero {loaded}/{len(wanted)} frames ({per_state}),"
        f" palette {len(hero_palette)} slots, {total_mismatches} off-palette px"
    )


def load_tpose_asset():
    global tpose_frames
    tpose_frames = {}
    if not palette_chars:
        return
    path = os.path.join(TPOSE_DIR, "tpose_front_0.png")
    if not os.path.isfile(path):
        print("factory: tpose frame missing, inventory falls back to front idle")
        return
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    masks = {
        bank: free_mask(bank)
        for bank in (0, 1, 2)
    }
    for bank, x, y, fw, fh in hero_frames.values():
        win = (1 << fw) - 1
        for yy in range(y, y + fh):
            masks[bank][yy] &= ~(win << x)
    slot = None
    for bank in (0, 1, 2):
        slot = find_slot(masks[bank], w, h)
        if slot is not None:
            break
    if slot is None:
        print("factory: tpose frame does not fit, inventory falls back to front idle")
        return
    rows, mismatches = frame_rows(img)
    pyxel.images[bank].set(slot[0], slot[1], rows)
    tpose_frames["front"] = (bank, slot[0], slot[1], w, h)
    print(
        f"factory: tpose frame placed bank {bank} at ({slot[0]},{slot[1]}),"
        f" {mismatches} off-palette px"
    )


def tpose_frame(direction):
    return tpose_frames.get(direction)


def hero_directions(state):
    return STATE_DIRECTIONS.get(state, HERO_DIRECTIONS)


def scarf_directions(state):
    if state in ("idle", "run", "defensive"):
        return HERO_DIRECTIONS
    return STATE_DIRECTIONS.get(state, SCARF_DIRECTIONS)


def scarf_behind_rows(plain, twin):
    return [
        "".join(t if p == "0" else p for p, t in zip(prow, trow))
        for prow, trow in zip(plain, twin)
    ]


def load_scarf_asset():
    global scarf_rows
    scarf_rows = {}
    if not hero_frames:
        return
    wanted = [
        (state, direction, index)
        for state in HERO_STATES
        for direction in hero_directions(state)
        for index in range(HERO_STATES[state])
    ]
    for key in wanted:
        slot = hero_frames.get(key)
        if slot is None:
            continue
        state, direction, index = key
        path = os.path.join(HERO_DIR, f"{state}_{direction}_scarf_{index}.png")
        if not os.path.isfile(path):
            continue
        img = Image.open(path).convert("RGBA")
        if img.size != (slot[3], slot[4]):
            print(
                f"factory: scarf frame {state}_{direction}_{index} size"
                f" {img.size} != slot {slot[3]}x{slot[4]}, skipped"
            )
            continue
        rows, mismatches = frame_rows(img)
        if state in ("idle", "run") and direction == "right":
            rows = scarf_behind_rows(plain_rows[key], rows)
        scarf_rows[key] = rows
    for state in HERO_STATES:
        for direction in scarf_directions(state):
            available = [
                index
                for index in range(HERO_STATES[state])
                if (state, direction, index) in scarf_rows
            ]
            if not available or len(available) == HERO_STATES[state]:
                continue
            for index in range(HERO_STATES[state]):
                if (state, direction, index) in scarf_rows:
                    continue
                nearest = min(available, key=lambda i: abs(i - index))
                scarf_rows[(state, direction, index)] = scarf_rows[
                    (state, direction, nearest)
                ]
    print(
        f"factory: scarf {len(scarf_rows)}/{len(wanted)} frames"
        " reusable in plain slots"
    )


def set_scarf_worn(worn):
    global scarf_worn
    if worn == scarf_worn:
        return
    variant = scarf_rows if worn else plain_rows
    for key, rows in variant.items():
        bank, x, y, _, _ = hero_frames[key]
        pyxel.images[bank].set(x, y, rows)
    scarf_worn = worn


def hero_frame(state, direction, index):
    return hero_frames.get((state, direction, index))


def scarf_on():
    return scarf_worn


def enemy_frame(state, index):
    return hero_frames.get(("enemy", state, index))