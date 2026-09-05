import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

BASE_COLORS = {
    "white": (255, 255, 255),
    "skin": (172, 50, 50),
    "uniform": (74, 90, 191),
    "cyan": (95, 205, 228),
    "steel": (48, 96, 130),
    "navy": (23, 23, 41),
}

SLOT_BUDGET = {
    "navy": 1,
    "uniform": 3,
    "steel": 2,
    "cyan": 2,
    "skin": 2,
    "white": 2,
}

FAMILY_ORDER = ["navy", "uniform", "steel", "cyan", "skin", "white"]

OUTLINE_INDEX = 0
OUTLINE_COLOR = (26, 7, 10)

LAB_MATRIX = np.array(
    [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ]
)
D65_WHITE = np.array([0.95047, 1.0, 1.08883])
MAX_RUNG_SLOTS = 12


def srgb_to_lab(colors):
    normalized = np.asarray(colors, dtype=float) / 255.0
    linear = np.where(
        normalized <= 0.04045, normalized / 12.92, ((normalized + 0.055) / 1.055) ** 2.4
    )
    xyz = linear @ LAB_MATRIX.T / D65_WHITE
    folded = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16.0 / 116.0)
    lab = np.empty_like(folded)
    lab[..., 0] = 116.0 * folded[..., 1] - 16.0
    lab[..., 1] = 500.0 * (folded[..., 0] - folded[..., 1])
    lab[..., 2] = 200.0 * (folded[..., 1] - folded[..., 2])
    return lab


def classify_families(unique_colors, counts):
    labs = srgb_to_lab(unique_colors)
    hue = np.degrees(np.arctan2(labs[:, 2], labs[:, 1])) % 360.0
    chroma = np.hypot(labs[:, 1], labs[:, 2])
    lightness = labs[:, 0]
    families = {name: [] for name in BASE_COLORS}
    for i, color in enumerate(unique_colors):
        if (chroma[i] < 22.0 and lightness[i] > 55.0) or (chroma[i] < 14.0 and lightness[i] >= 40.0):
            name = "white"
        elif chroma[i] < 14.0:
            name = "navy"
        elif hue[i] <= 60.0 or hue[i] >= 345.0:
            name = "skin"
        elif 150.0 <= hue[i] < 245.0:
            name = "cyan" if lightness[i] >= 55.0 else "steel"
        elif 245.0 <= hue[i] < 262.0:
            name = "steel"
        else:
            name = "navy" if lightness[i] < 26.0 else "uniform"
        families[name].append((tuple(int(v) for v in color), int(counts[i])))
    return families


def weighted_median_l(values, weights):
    order = np.argsort(values)
    total = weights[order].sum()
    cutoff = total / 2.0
    running = 0.0
    for idx in order:
        running += weights[idx]
        if running >= cutoff:
            return values[idx]
    return values[order[-1]]


def pick_family_rungs(shades, budget, family):
    if budget >= len(shades):
        return [color for color, _ in shades]
    lightness = srgb_to_lab([color for color, _ in shades])[:, 0]
    weights = np.array([count for _, count in shades], dtype=float)
    centers = []
    for j in range(budget):
        target = (j + 0.5) / budget
        running = 0.0
        for i in range(len(shades)):
            running += weights[i]
            if running >= target * weights.sum():
                break
        centers.append(lightness[i])
    centers = np.array(centers, dtype=float)
    for _ in range(32):
        assign = np.array([int(np.argmin(np.abs(centers - value))) for value in lightness])
        for j in range(budget):
            members = assign == j
            if members.any():
                centers[j] = np.average(lightness[members], weights=weights[members])
    chosen = []
    for j in range(budget):
        members = [i for i in np.where(assign == j)[0] if i not in chosen]
        if not members:
            members = [i for i in np.argsort(np.abs(lightness - centers[j])) if i not in chosen][:1]
        chosen.append(int(members[int(np.argmax(weights[members]))]))
    anchor_rgb = BASE_COLORS[family]
    member_rgbs = [color for color, _ in shades]
    chosen_colors = [shades[i][0] for i in chosen]
    if anchor_rgb in member_rgbs and anchor_rgb not in chosen_colors:
        anchor_lab = srgb_to_lab([anchor_rgb])[0]
        rung_labs = srgb_to_lab([shades[i][0] for i in chosen])
        closest = int(np.argmin(np.linalg.norm(rung_labs - anchor_lab, axis=1)))
        chosen[closest] = member_rgbs.index(anchor_rgb)
    return [shades[i][0] for i in chosen]


def build_all_ladders(families):
    ladders = {}
    for name in FAMILY_ORDER:
        shades = sorted(families[name], key=lambda item: srgb_to_lab([item[0]])[0][0])
        if not shades:
            continue
        rungs = pick_family_rungs(shades, SLOT_BUDGET[name], name)
        ladders[name] = sorted(rungs, key=lambda color: srgb_to_lab([color])[0][0])
    return ladders


def build_palette(ladders):
    palette = [OUTLINE_COLOR]
    slot_names = {}
    for name in FAMILY_ORDER:
        for color in ladders.get(name, []):
            if color in palette:
                raise SystemExit(f"duplicate rung {color} in family {name}")
            slot_names[len(palette)] = (name, color)
            palette.append(color)
    if len(palette) > MAX_RUNG_SLOTS + 1:
        raise SystemExit(f"palette overflow: {len(palette)} slots > 13")
    return palette, slot_names


def fs_dither_frame(rgb_float, opaque, palette_rgb):
    height, width = opaque.shape
    err = np.zeros_like(rgb_float)
    for y in range(height):
        x = 0
        while x < width:
            if not opaque[y, x]:
                x += 1
                continue
            old = rgb_float[y, x] + err[y, x]
            dists = np.sum((palette_rgb - old) ** 2, axis=1)
            chosen = palette_rgb[int(np.argmin(dists))]
            diff = old - chosen
            if x + 1 < width:
                err[y, x + 1] += diff * (7.0 / 16.0)
            if y + 1 < height:
                if x > 0:
                    err[y + 1, x - 1] += diff * (3.0 / 16.0)
                err[y + 1, x] += diff * (5.0 / 16.0)
                if x + 1 < width:
                    err[y + 1, x + 1] += diff * (1.0 / 16.0)
            rgb_float[y, x] = chosen
            err[y, x] = 0.0
            x += 1
    return rgb_float


def snap_to_rungs(rgb_float, opaque, palette_rgb):
    flat = rgb_float[opaque]
    dists = np.sum((flat[:, None, :] - palette_rgb[None, :, :]) ** 2, axis=2)
    chosen = palette_rgb[np.argmin(dists, axis=1)]
    out = rgb_float.copy()
    out[opaque] = chosen
    return out


def process_frame(path, output_path, palette_rgb):
    image = Image.open(path).convert("RGBA")
    arr = np.array(image)
    opaque = arr[..., 3] > 0
    rgb_float = fs_dither_frame(arr[..., :3].astype(float), opaque, palette_rgb)
    locked = np.rint(snap_to_rungs(rgb_float, opaque, palette_rgb)).astype(np.uint8)
    out_arr = np.zeros_like(arr)
    out_arr[..., :3] = locked
    out_arr[..., 3] = arr[..., 3]
    out_arr[..., :3][~opaque] = 0
    Image.fromarray(out_arr).save(output_path)
    flat = locked[opaque].astype(int)
    slot_ids = np.argmin(
        np.sum((flat[:, None, :] - palette_rgb[None, :, :].astype(int)) ** 2, axis=2),
        axis=1,
    )
    return slot_ids, int(opaque.sum())


def main():
    input_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "eggrim/assets/drawn/readmey")
    output_dir = Path(sys.argv[2] if len(sys.argv) > 2 else str(input_dir) + "_locked")
    files = sorted(
        p
        for p in input_dir.glob("*.png")
        if "sheet" not in p.stem.lower() and "palette" not in p.stem.lower()
    )
    if not files:
        raise SystemExit(f"no frames found in {input_dir}")
    if output_dir.resolve() == input_dir.resolve():
        raise SystemExit("output_dir must differ from input_dir")
    output_dir.mkdir(parents=True, exist_ok=True)
    source_names = {p.name for p in files}
    for stale in output_dir.glob("*.png"):
        if stale.name not in source_names:
            stale.unlink()
    families = gather_families(files)
    ladders = build_all_ladders(families)
    palette, slot_names = build_palette(ladders)
    print("hero palette ladder:")
    for index, color in enumerate(palette):
        if index == OUTLINE_INDEX:
            print(f"  {index:2d}  #{color[0]:02x}{color[1]:02x}{color[2]:02x}  outline/transparency")
        else:
            family, color = slot_names[index]
            print(f"  {index:2d}  #{color[0]:02x}{color[1]:02x}{color[2]:02x}  {family}")
    palette_rgb = np.array(palette, dtype=float)
    slot_totals = np.zeros(len(palette), dtype=int)
    for path in files:
        slot_ids, pixel_count = process_frame(path, output_dir / path.name, palette_rgb)
        slot_totals += np.bincount(slot_ids, minlength=len(palette))
        print(f"  locked {path.name} ({pixel_count} px)")
    print("slot pixel totals:")
    for index, total in enumerate(slot_totals):
        color = palette[index]
        print(f"  {index:2d}  #{color[0]:02x}{color[1]:02x}{color[2]:02x}  {int(total)}")
    unused = [i for i, t in enumerate(slot_totals) if t == 0]
    if unused:
        print(f"unused slots: {unused}")
    json_path = output_dir / "hero_palette.json"
    json_path.write_text(
        json.dumps(
            {
                "palette": [
                    "#%02x%02x%02x" % tuple(color) for color in palette
                ],
                "ladders": {
                    name: [
                        "#%02x%02x%02x" % tuple(color) for color in colors
                    ]
                    for name, colors in ladders.items()
                },
            },
            indent=2,
        )
    )
    print(f"wrote {json_path}")


def gather_families(files):
    combined = {}
    for path in files:
        arr = np.array(Image.open(path).convert("RGBA"))
        opaque_colors = arr[arr[..., 3] > 0][:, :3]
        colors, counts = np.unique(opaque_colors.reshape(-1, 3), axis=0, return_counts=True)
        for color, count in zip(colors.tolist(), counts.tolist()):
            key = tuple(color)
            combined[key] = combined.get(key, 0) + count
    unique_colors = np.array(list(combined), dtype=np.uint8)
    counts = np.array(list(combined.values()), dtype=np.int64)
    print(f"source shades: {len(unique_colors)} across {len(files)} frames")
    return classify_families(unique_colors, counts)


if __name__ == "__main__":
    main()