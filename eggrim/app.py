import pyxel

SCREEN_W = 256
SCREEN_H = 144
FPS = 60
MOVE_SPEED = 40.0

from eggrim.assets import ICON_CHARS, ICON_COLKEY, PORTRAIT_BLEND_POS, load_banks
from eggrim.assets.floors import render_tiles
from eggrim.combat import (
    THRUST_ANIM_FRAMES,
    THRUST_FIST_RADIUS,
    THRUST_COOLDOWN_FRAMES,
    THRUST_DAMAGE,
    THRUST_KNOCKBACK,
    THRUST_REACH,
    THRUST_EXTEND_POINT,
    ThrustState,
    thrust_pillar_target,
    thrust_wall_target,
)
from eggrim.creatures import PILLAR_FLASH_FRAMES, spawn_pillars, spawn_walls
from eggrim.fog import (
    FOG_COLOR,
    TILE_TINT_V,
    WALL_FLASH_U,
    WALL_FLASH_V,
    pillar_tint_level,
    render_pillar_tints,
    render_tile_tints,
)
from eggrim.hud import (
    HEALTH_BAR_Y,
    HEALTH_COLOR,
    HUD_BAR_H,
    HUD_BAR_W,
    HUD_BAR_X,
    STAMINA_BAR_Y,
    STAMINA_COLOR,
    draw_bar,
    draw_minimap,
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
from eggrim.zones import (
    TILE,
    TILE_TYPE_INDEX,
    ZONE_LINKS,
    load_zone,
)
from eggrim.world import (
    PLAYER_FEET_OFFSET_Y,
    PLAYER_FEET_RADIUS,
    PLAYER_ZONE_MARGIN,
    PLAYER_START_X,
    PLAYER_START_Y,
    feet_hits_wall,
    outside_zone,
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

pillars = []
walls = {}
thrust = ThrustState()

zone = None
player_on_door = False


def door_at(zone, feet_x, feet_y):
    for index, (door_x, door_y) in enumerate(zone.doors):
        if not door_x * TILE <= feet_x < (door_x + 1) * TILE:
            continue
        below_open = door_y + 1 < zone.height_tiles and zone.grid[door_y + 1][door_x] != "#"
        above_open = door_y > 0 and zone.grid[door_y - 1][door_x] != "#"
        if below_open:
            if (
                feet_y <= (door_y + 1) * TILE + PLAYER_FEET_RADIUS + 1.0
                and player.facing[1] < 0
            ):
                return index
        elif above_open:
            if door_y * TILE <= feet_y < (door_y + 1) * TILE:
                return index
    return None


def move_to_zone(target_name, door_index, feet):
    global zone, pillars, walls
    src_x, _ = zone.doors[door_index]
    src_width = feet[0] - src_x * TILE
    zone = load_zone(target_name)
    pillars = spawn_pillars(zone)
    walls = spawn_walls(zone)
    dst_x, dst_y = zone.doors[door_index]
    below_open = dst_y + 1 < zone.height_tiles and zone.grid[dst_y + 1][dst_x] != "#"
    if below_open:
        exit_feet_y = (dst_y + 1) * TILE + PLAYER_FEET_RADIUS + 0.5
    else:
        exit_feet_y = dst_y * TILE - PLAYER_FEET_RADIUS - 0.5
    player.x = dst_x * TILE + src_width
    player.y = exit_feet_y - PLAYER_FEET_OFFSET_Y


def camera_following_player():
    cam_x = max(0, min(int(player.x) - SCREEN_W // 2, zone.width_px - SCREEN_W))
    cam_y = max(0, min(int(player.y) - SCREEN_H // 2, zone.height_px - SCREEN_H))
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
    global portrait_to, portrait_from, portrait_fade, walls, player_on_door
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
        new_x = player.x + player.facing[0] * speed / FPS
        new_y = player.y + player.facing[1] * speed / FPS
        if not feet_hits_wall(zone, new_x, player.y):
            player.x = new_x
        if not feet_hits_wall(zone, player.x, new_y):
            player.y = new_y
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
        shoulder_x, shoulder_y = shoulder_point(player.view)
        shoulder_along = (
            (shoulder_x - player.x) * player.facing[0]
            + (shoulder_y - player.y) * player.facing[1]
        )
        target, target_contact = thrust_pillar_target(
            player, pillars, THRUST_REACH + shoulder_along
        )
        if target is not None:
            thrust.max_reach = max(2.0, min(THRUST_REACH, target_contact - shoulder_along + 1.0))
            target.hp -= THRUST_DAMAGE
            target.flash = PILLAR_FLASH_FRAMES
            knockback_x = player.x - player.facing[0] * THRUST_KNOCKBACK
            knockback_y = player.y - player.facing[1] * THRUST_KNOCKBACK
            if not feet_hits_wall(zone, knockback_x, knockback_y):
                player.x = knockback_x
                player.y = knockback_y
        else:
            wall_target, wall_dist = thrust_wall_target(
                player, zone, walls, THRUST_REACH + shoulder_along
            )
            if wall_target is not None:
                thrust.max_reach = max(2.0, min(THRUST_REACH, wall_dist - shoulder_along + 1.0))
                wall_target.hp -= THRUST_DAMAGE
                wall_target.flash = PILLAR_FLASH_FRAMES
                knockback_x = player.x - player.facing[0] * THRUST_KNOCKBACK
                knockback_y = player.y - player.facing[1] * THRUST_KNOCKBACK
                if not feet_hits_wall(zone, knockback_x, knockback_y):
                    player.x = knockback_x
                    player.y = knockback_y
                if wall_target.hp <= 0:
                    tile_x = wall_target.tile_x
                    tile_y = wall_target.tile_y
                    row = zone.grid[tile_y]
                    zone.grid[tile_y] = row[:tile_x] + "." + row[tile_x + 1 :]
                    del walls[(tile_x, tile_y)]
            else:
                thrust.max_reach = THRUST_REACH
    for pillar in pillars:
        if pillar.flash > 0:
            pillar.flash -= 1
    for wall in walls.values():
        if wall.flash > 0:
            wall.flash -= 1

    resolve_pillars(player, pillars)

    key = portrait_key(player.view)
    if key != portrait_to:
        portrait_from = portrait_to
        portrait_to = key
        portrait_fade = PORTRAIT_FADE_FRAMES + 1
    if portrait_fade > 0:
        portrait_fade -= 1

    if outside_zone(zone, player.x, player.y):
        margin = PLAYER_ZONE_MARGIN
        player.x = max(margin, min(player.x, zone.width_px - margin))
        player.y = max(margin, min(player.y, zone.height_px - margin))

    feet_x = player.x
    feet_y = player.y + PLAYER_FEET_OFFSET_Y
    door_index = door_at(zone, feet_x, feet_y)
    on_door = door_index is not None
    if on_door and not player_on_door:
        link = ZONE_LINKS.get((zone.name, door_index))
        if link is not None:
            move_to_zone(link[0], link[1], (feet_x, feet_y))
    player_on_door = on_door


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


def shoulder_point(view):
    if view in (Facing.LEFT, Facing.RIGHT):
        return player.x + (3.0 if view is Facing.RIGHT else -3.0), player.y - 3.0
    if view is Facing.UP:
        return player.x + 1.0, player.y - 2.0
    return player.x + 1.0, player.y + 2.0


def draw_strike(view):
    progress = 1 - thrust.anim / THRUST_ANIM_FRAMES
    if progress < THRUST_EXTEND_POINT:
        strike = progress / THRUST_EXTEND_POINT
    else:
        strike = 1 - (progress - THRUST_EXTEND_POINT) / (1 - THRUST_EXTEND_POINT)
    reach = thrust.max_reach * strike
    shoulder_x, shoulder_y = shoulder_point(view)
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


def draw_world_tiles(cam_x, cam_y):
    px = int(player.x)
    py = int(player.y)
    tile_x0 = cam_x // TILE
    tile_y0 = cam_y // TILE
    tile_x1 = min((cam_x + SCREEN_W) // TILE, zone.width_tiles - 1)
    tile_y1 = min((cam_y + SCREEN_H) // TILE, zone.height_tiles - 1)
    for tile_y in range(tile_y0, tile_y1 + 1):
        row = zone.grid[tile_y]
        for tile_x in range(tile_x0, tile_x1 + 1):
            offset_x = tile_x * TILE + TILE // 2 - px
            offset_y = tile_y * TILE + TILE // 2 - py
            dist = (offset_x * offset_x + offset_y * offset_y) ** 0.5
            level = pillar_tint_level(dist)
            if level is None:
                continue
            kind = TILE_TYPE_INDEX[row[tile_x]]
            src_u = level * TILE
            src_v = TILE_TINT_V + kind * TILE
            if kind == 2 and (tile_x, tile_y) in walls and walls[(tile_x, tile_y)].flash > 0:
                src_u, src_v = WALL_FLASH_U, WALL_FLASH_V
            pyxel.blt(
                tile_x * TILE,
                tile_y * TILE,
                2,
                src_u,
                src_v,
                TILE,
                TILE,
                0,
            )


def draw():
    pyxel.cls(FOG_COLOR)
    cam_x, cam_y = camera_following_player()
    pyxel.camera(cam_x, cam_y)
    draw_world_tiles(cam_x, cam_y)
    view = player.view
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
    draw_minimap(zone, player, pillars, cam_x, cam_y)
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
    global zone, pillars, walls
    pyxel.init(SCREEN_W, SCREEN_H, title="Eggrim's Iterax", display_scale=5, fps=FPS)
    pyxel.fullscreen(True)
    pyxel.icon(ICON_CHARS, 1, ICON_COLKEY)
    render_tiles()
    render_tile_tints()
    zone = load_zone("arena")
    player.x, player.y = zone.player_start
    pillars = spawn_pillars(zone)
    walls = spawn_walls(zone)
    pyxel.run(update, draw)