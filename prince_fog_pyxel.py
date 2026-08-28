"""Eggrim's Iterax -- MVP single-file Pyxel game.

Coordinate system: the internal 256x144 screen IS the world.
Every coordinate, speed and distance below uses these internal pixels.
"""

import pyxel

# ---------------------------------------------------------------------------
# Screen / timing constants (internal 256x144 coordinate system)
# ---------------------------------------------------------------------------
SCREEN_W = 256
SCREEN_H = 144
FPS = 60

# ---------------------------------------------------------------------------
# Palette reference (Pyxel default 16-color palette, index: name)
#   0 black    1 navy      2 purple    3 light blue-gray  <- FLOOR
#   4 brown    5 dark blue 6 light gray 7 white
#   8 peach    9 orange   10 red      11 cyan
#  12 dark blue 13 magenta 14 dark gray 15 (unused)
# ---------------------------------------------------------------------------

def update():
    """All input + game state changes happen here, once per frame."""
    pass


def draw():
    """All rendering happens here, once per frame."""
    # Floor: light bluish-gray fills the internal screen.
    pyxel.cls(3)


# ---------------------------------------------------------------------------
# Boot
# ---------------------------------------------------------------------------
# NOTE: modern Pyxel renamed 'caption'->'title' and 'scale'->'display_scale'
pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
pyxel.run(update, draw)