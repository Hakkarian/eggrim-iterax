import pyxel

SCREEN_W = 256
SCREEN_H = 144
FPS = 60
MOVE_SPEED = 40.0

from eggrim.assets import load_banks
from eggrim.creatures import spawn_pillars
from eggrim.fog import FOG_HALF, FOG_SIZE, pillar_tint_level, render_pillar_tints
from eggrim.hud import (
    HEALTH_BAR_Y,
    HEALTH_COLOR,
    HUD_BAR_H,
    HUD_BAR_W,
    HUD_BAR_X,
    STAMINA_BAR_Y,
    STAMINA_COLOR,
    draw_bar,
)
from eggrim.player import (
    BLOCK_DRAIN,
    BLOCK_MIN_START,
    Facing,
    Player,
    SPRINT_DRAIN,
    SPRINT_MIN_START,
    SPRINT_MULTIPLIER,
    STAMINA_REGEN,
    STAT_MAX,
)
from eggrim.states import announce_progress
from eggrim.world import PLAYER_START_X, PLAYER_START_Y, outside_world

load_banks()
render_pillar_tints()

player = Player(
    x=float(PLAYER_START_X),
    y=float(PLAYER_START_Y),
    facing=(1.0, 0.0),
    side=1.0,
)

pillars = spawn_pillars()


def update():
    dx = (
        (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT))
        - (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT))
    )
    dy = (
        (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN))
        - (pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP))
    )
    sprint_held = (
        pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.KEY_LSHIFT) or pyxel.btn(pyxel.KEY_RSHIFT)
    )
    block_held = pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT)
    drained = False
    if block_held and (
        player.stamina >= BLOCK_MIN_START or (player.blocking and player.stamina > 0)
    ):
        player.blocking = True
        player.sprinting = False
        drained = True
        player.stamina = max(0.0, player.stamina - BLOCK_DRAIN / FPS)
    else:
        player.blocking = False
    speed = MOVE_SPEED
    if dx or dy:
        length = (dx * dx + dy * dy) ** 0.5
        player.facing = (dx / length, dy / length)
        if player.facing[0]:
            player.side = 1.0 if player.facing[0] > 0 else -1.0
        if not player.blocking and sprint_held and (
            player.stamina >= SPRINT_MIN_START or (player.sprinting and player.stamina > 0)
        ):
            player.sprinting = True
            drained = True
            speed = MOVE_SPEED * SPRINT_MULTIPLIER
            player.stamina = max(0.0, player.stamina - SPRINT_DRAIN / FPS)
        else:
            player.sprinting = False
        player.x += player.facing[0] * speed / FPS
        player.y += player.facing[1] * speed / FPS
    if not drained:
        player.sprinting = False
        player.stamina = min(STAT_MAX, player.stamina + STAMINA_REGEN / FPS)

    if outside_world(player.x, player.y):
        player.x = float(PLAYER_START_X)
        player.y = float(PLAYER_START_Y)


def draw():
    pyxel.cls(3)
    view = player.view
    pyxel.blt(
        int(player.x) - FOG_HALF,
        int(player.y) - FOG_HALF,
        1,
        0,
        0,
        FOG_SIZE,
        FOG_SIZE,
        0,
    )
    for pillar in pillars:
        dist = ((pillar.x - player.x) ** 2 + (pillar.y - player.y) ** 2) ** 0.5
        level = pillar_tint_level(dist)
        if level < 0:
            pyxel.blt(int(pillar.x) - 8, int(pillar.y) - 8, 0, 96, 16, 16, 16, 0)
        else:
            pyxel.blt(int(pillar.x) - 8, int(pillar.y) - 8, 2, 16 * level, 16, 16, 16, 0)
    sprite_x = int(player.x) - 8
    sprite_y = int(player.y) - 8
    if view in (Facing.LEFT, Facing.RIGHT):
        sprite_w = -16 if view is Facing.LEFT else 16
        pyxel.blt(sprite_x, sprite_y, 0, 0, 0, sprite_w, 16, 0)
    elif view is Facing.UP:
        pyxel.blt(sprite_x, sprite_y, 0, 0, 16, 16, 16, 0)
    else:
        pyxel.blt(sprite_x, sprite_y, 0, 16, 0, 16, 16, 0)
    draw_bar(
        HUD_BAR_X,
        HEALTH_BAR_Y,
        HUD_BAR_W,
        HUD_BAR_H,
        HEALTH_COLOR,
        player.health,
        STAT_MAX,
    )
    draw_bar(
        HUD_BAR_X,
        STAMINA_BAR_Y,
        HUD_BAR_W,
        HUD_BAR_H,
        STAMINA_COLOR,
        player.stamina,
        STAT_MAX,
    )
    if view in (Facing.LEFT, Facing.RIGHT):
        px_src, portrait_w = 32, -32 if view is Facing.LEFT else 32
    elif view is Facing.UP:
        px_src, portrait_w = 96, 32
    else:
        px_src, portrait_w = 64, 32
    pyxel.blt(0, 0, 0, px_src, 0, portrait_w, 32, 3)


def run():
    pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
    announce_progress()
    pyxel.run(update, draw)