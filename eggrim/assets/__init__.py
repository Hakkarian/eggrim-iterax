import pyxel

from eggrim.assets.floors import render_tiles
from eggrim.assets.icon import ICON_CHARS, ICON_COLKEY
from eggrim.assets.pillar import (
    PILLAR_CHARS,
    render_pillar_flash,
)
from eggrim.assets.player_sprites import (
    BACK_ATTACK_CHARS,
    BACK_BLEND_CHARS,
    BACK_FADE_CHARS,
    BACK_HALF_CHARS,
    BACK_CHARS,
    BACK_ROWS,
    BACK_WALK_CHARS,
    FRONT_ATTACK_CHARS,
    FRONT_BLEND_CHARS,
    FRONT_CHARS,
    FRONT_FADE_CHARS,
    FRONT_HALF_CHARS,
    FRONT_ROWS,
    FRONT_WALK_CHARS,
    SIDE_ATTACK_CHARS,
    SIDE_BLEND_CHARS,
    SIDE_FADE_CHARS,
    SIDE_HALF_CHARS,
    SIDE_WALK_CHARS,
    SPRITE_CHARS,
)
from eggrim.assets.portraits import (
    PORTRAIT_BACK_CHARS,
    PORTRAIT_CHARS,
    PORTRAIT_FRONT_CHARS,
    PORTRAIT_BLEND_POS,
    render_portrait_blends,
)


def load_banks():
    pyxel.images[0].set(0, 0, SPRITE_CHARS)
    pyxel.images[0].set(16, 0, FRONT_CHARS)
    pyxel.images[0].set(0, 16, BACK_CHARS)
    pyxel.images[0].set(32, 0, PORTRAIT_CHARS)
    pyxel.images[0].set(64, 0, PORTRAIT_FRONT_CHARS)
    pyxel.images[0].set(96, 0, PORTRAIT_BACK_CHARS)
    pyxel.images[0].set(128, 0, PILLAR_CHARS)
    pyxel.images[0].set(0, 48, SIDE_ATTACK_CHARS)
    pyxel.images[0].set(16, 48, FRONT_ATTACK_CHARS)
    pyxel.images[0].set(32, 48, BACK_ATTACK_CHARS)
    pyxel.images[0].set(0, 32, SIDE_WALK_CHARS)
    pyxel.images[0].set(16, 32, FRONT_WALK_CHARS)
    pyxel.images[0].set(32, 32, BACK_WALK_CHARS)
    pyxel.images[0].set(48, 32, SIDE_HALF_CHARS)
    pyxel.images[0].set(64, 32, FRONT_HALF_CHARS)
    pyxel.images[0].set(80, 32, BACK_HALF_CHARS)
    pyxel.images[0].set(96, 32, SIDE_BLEND_CHARS)
    pyxel.images[0].set(112, 32, FRONT_BLEND_CHARS)
    pyxel.images[0].set(128, 32, BACK_BLEND_CHARS)
    pyxel.images[0].set(144, 32, SIDE_FADE_CHARS)
    pyxel.images[0].set(160, 32, FRONT_FADE_CHARS)
    pyxel.images[0].set(176, 32, BACK_FADE_CHARS)
    render_pillar_flash()
    render_portrait_blends()