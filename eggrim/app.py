import pyxel

SCREEN_W = 256
SCREEN_H = 144
FPS = 60
MOVE_SPEED = 40.0

from eggrim.assets import ICON_CHARS, ICON_COLKEY, PORTRAIT_BLEND_POS, load_banks
from eggrim.combat import (
    PILLAR_HIT_RADIUS,
    THRUST_ANIM_FRAMES,
    THRUST_FIST_RADIUS,
    THRUST_COOLDOWN_FRAMES,
    THRUST_DAMAGE,
    THRUST_KNOCKBACK,
    THRUST_REACH,
    THRUST_EXTEND_POINT,
    ThrustState,
    thrust_target,
)
from eggrim.creatures import PILLAR_FLASH_FRAMES, spawn_pillars
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
from eggrim.zones import TILE, load_zone, render_tiles
from eggrim.world import (
    PLAYER_START_X,
    PLAYER_START_Y,
    outside_world,
    resolve_pillars,
)

load_banks()
render_pillar_tints()

player = Player(
    x=float(PLAYER_START_X),
    y=float(PLAYER_START_Y),
    facing=(1.0, 0.0),
    side=1.0,
)

pillars = spawn_pillars()
thrust = ThrustState()

zone = None


def camera_following_player():
    cam_x = max(0.0, min(player.x - SCREEN_W / 2, zone.width_px - SCREEN_W))
    cam_y = max(0.0, min(player.y - SCREEN_H / 2, zone.height_px - SCREEN_H))
    return cam_x, cam_y

portrait_to = "side"
portrait_from = None
portrait_fade = 0
PORTRAIT_FADE_FRAMES = 2


def portrait_key(view):
    if view in (Facing.LEFT, Facing.RIGHT):
        return "side"
    up = view is Facing.UP
    return "back" if up else "front"


def update():
    global portrait_to, portrait_from, portrait_fade
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
    if not (dx or dy):
        player.walk_phase = 0
    if dx or dy:
        length = (dx * dx + dy * dy) ** 0.5
        player.facing = (dx / length, dy / length)
        player.walk_phase += 2 if player.sprinting else 1
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

    if thrust.cooldown > 0:
        thrust.cooldown -= 1
    if thrust.anim > 0:
        thrust.anim -= 1
    if (
        pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
        and thrust.cooldown == 0
        and not player.blocking
    ):
        thrust.cooldown = THRUST_COOLDOWN_FRAMES
        thrust.anim = THRUST_ANIM_FRAMES
        thrust.facing = player.facing
        target = thrust_target(player, pillars)
        if target is not None:
            target_dist = ((target.x - player.x) ** 2 + (target.y - player.y) ** 2) ** 0.5
            thrust.max_reach = max(
                2.0, min(THRUST_REACH, target_dist - PILLAR_HIT_RADIUS - THRUST_FIST_RADIUS)
            )
            target.hp -= THRUST_DAMAGE
            target.flash = PILLAR_FLASH_FRAMES
            player.x -= player.facing[0] * THRUST_KNOCKBACK
            player.y -= player.facing[1] * THRUST_KNOCKBACK
        else:
            thrust.max_reach = THRUST_REACH
    for pillar in pillars:
        if pillar.flash > 0:
            pillar.flash -= 1

    resolve_pillars(player, pillars)

    key = portrait_key(player.view)
    if key != portrait_to:
        portrait_from = portrait_to
        portrait_to = key
        portrait_fade = PORTRAIT_FADE_FRAMES + 1
    if portrait_fade > 0:
        portrait_fade -= 1

    if outside_world(player.x, player.y):
        player.x = float(PLAYER_START_X)
        player.y = float(PLAYER_START_Y)


def draw_shield(view):
    px = int(player.x)
    py = int(player.y)
    if view in (Facing.LEFT, Facing.RIGHT):
        shield_x = px + (5 if view is Facing.RIGHT else -8)
        pyxel.rect(shield_x, py - 5, 3, 9, 12)
        pyxel.rectb(shield_x, py - 5, 3, 9, 0)
        pyxel.line(shield_x + 1, py - 3, shield_x + 1, py + 2, 7)
    elif view is Facing.UP:
        pyxel.rect(px - 2, py - 9, 4, 3, 12)
        pyxel.rectb(px - 2, py - 9, 4, 3, 0)
    else:
        pyxel.rect(px - 2, py - 3, 4, 5, 12)
        pyxel.rectb(px - 2, py - 3, 4, 5, 0)
        pyxel.pset(px, py - 1, 7)


def draw_strike(view):
    progress = 1 - thrust.anim / THRUST_ANIM_FRAMES
    if progress < THRUST_EXTEND_POINT:
        strike = progress / THRUST_EXTEND_POINT
    else:
        strike = 1 - (progress - THRUST_EXTEND_POINT) / (1 - THRUST_EXTEND_POINT)
    reach = thrust.max_reach * strike
    if view in (Facing.LEFT, Facing.RIGHT):
        shoulder_x = player.x + (3.0 if view is Facing.RIGHT else -3.0)
        shoulder_y = player.y - 3.0
    elif view is Facing.UP:
        shoulder_x, shoulder_y = player.x + 1.0, player.y - 2.0
    else:
        shoulder_x, shoulder_y = player.x + 1.0, player.y + 2.0
    fist_x = shoulder_x + thrust.facing[0] * reach
    fist_y = shoulder_y + thrust.facing[1] * reach
    pyxel.line(int(shoulder_x), int(shoulder_y), int(fist_x), int(fist_y), 6)
    if abs(thrust.facing[0]) >= abs(thrust.facing[1]):
        pyxel.line(int(shoulder_x), int(shoulder_y) + 1, int(fist_x), int(fist_y) + 1, 6)
    else:
        pyxel.line(int(shoulder_x) + 1, int(shoulder_y), int(fist_x) + 1, int(fist_y), 6)
    pyxel.rect(int(fist_x) - 1, int(fist_y) - 1, 2, 2, 7)


def draw_pillar(pillar):
    dist = ((pillar.x - player.x) ** 2 + (pillar.y - player.y) ** 2) ** 0.5
    level = pillar_tint_level(dist)
    if pillar.flash > 0:
        pyxel.blt(int(pillar.x) - 8, int(pillar.y) - 8, 2, 48, 16, 16, 16, 0)
    elif level is None:
        return
    else:
        pyxel.blt(int(pillar.x) - 8, int(pillar.y) - 8, 2, 16 * level, 32, 16, 16, 0)


def draw():
    pyxel.cls(3)
    cam_x, cam_y = camera_following_player()
    pyxel.camera(cam_x, cam_y)
    pyxel.bltm(
        0,
        0,
        zone.tilemap,
        int(cam_x),
        int(cam_y),
        SCREEN_W,
        SCREEN_H,
        0,
    )
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
        if pillar.y <= player.y:
            draw_pillar(pillar)
    sprite_x = int(player.x) - 8
    sprite_y = int(player.y) - 8
    attacking = thrust.anim > 0
    walk_frame = (0, 1, 2, 1)[player.walk_phase % 20 // 5]
    if not attacking and player.sprinting and walk_frame == 1:
        sprite_y -= 1
    if attacking:
        if thrust.anim == THRUST_ANIM_FRAMES or thrust.anim == 1:
            pose = 3
        elif thrust.anim == THRUST_ANIM_FRAMES - 1 or thrust.anim == 2:
            pose = 4
        else:
            pose = 5
    else:
        pose = walk_frame
    if view in (Facing.LEFT, Facing.RIGHT):
        frames = ((0, 0), (48, 32), (0, 32), (96, 32), (144, 32), (0, 48))
    elif view is Facing.UP:
        frames = ((0, 16), (80, 32), (32, 32), (128, 32), (176, 32), (32, 48))
    else:
        frames = ((16, 0), (64, 32), (16, 32), (112, 32), (160, 32), (16, 48))
    sprite_u, sprite_v = frames[pose]
    if attacking and view is Facing.UP:
        draw_strike(view)
    if view in (Facing.LEFT, Facing.RIGHT):
        sprite_w = -16 if view is Facing.LEFT else 16
        pyxel.blt(sprite_x, sprite_y, 0, sprite_u, sprite_v, sprite_w, 16, 0)
    else:
        pyxel.blt(sprite_x, sprite_y, 0, sprite_u, sprite_v, 16, 16, 0)
    if attacking and view is not Facing.UP:
        draw_strike(view)
    if player.blocking:
        draw_shield(view)
    for pillar in pillars:
        if pillar.y > player.y:
            draw_pillar(pillar)
    pyxel.camera(0, 0)
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
    if portrait_fade > 0 and portrait_from is not None:
        step = PORTRAIT_FADE_FRAMES - portrait_fade + 1
        u, v = PORTRAIT_BLEND_POS[(portrait_from, portrait_to, step)]
        pyxel.blt(0, 0, 0, u, v, 32, 32, 3)
    else:
        if view in (Facing.LEFT, Facing.RIGHT):
            px_src, portrait_w = 32, -32 if view is Facing.LEFT else 32
        elif view is Facing.UP:
            px_src, portrait_w = 96, 32
        else:
            px_src, portrait_w = 64, 32
        pyxel.blt(0, 0, 0, px_src, 0, portrait_w, 32, 3)


def run():
    global zone
    pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
    pyxel.icon(ICON_CHARS, 1, ICON_COLKEY)
    render_tiles()
    zone = load_zone("arena")
    announce_progress()
    pyxel.run(update, draw)