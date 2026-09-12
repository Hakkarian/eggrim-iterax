import pyxel

from eggrim.assets.factory import (
    load_hero_asset,
    load_scarf_asset,
    load_tpose_asset,
    read_palette,
)
from eggrim.assets.floors import render_tiles
from eggrim.assets.icon import ICON_CHARS, ICON_COLKEY
from eggrim.assets.pillar import (
    PILLAR_CHARS,
    render_pillar_flash,
)
from eggrim.assets.portraits import (
    PORTRAIT_BLEND_POS,
    PORTRAIT_THUMB_POS,
    render_portrait_blends,
    render_thumbs,
)


def load_banks():
    palette_ready = read_palette()
    pyxel.images[0].set(128, 0, PILLAR_CHARS)
    render_pillar_flash()
    render_thumbs()
    render_portrait_blends()
    if palette_ready:
        load_hero_asset()
        load_scarf_asset()
        load_tpose_asset()