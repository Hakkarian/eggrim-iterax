import math
import random

import pyxel

SCREEN_W = 256
SCREEN_H = 144
FPS = 60
MOVE_SPEED = 40.0
DASH_SPEED = 120.0
DASH_TOTAL_FRAMES = 24

from eggrim.assets import (
    ICON_CHARS,
    ICON_COLKEY,
    PORTRAIT_BLEND_POS,
    factory,
    load_banks,
)
from eggrim.assets.factory import enemy_frame, hero_frame
from eggrim.assets.floors import render_tiles
from eggrim.assets.portraits import PORTRAIT_THUMB_POS
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
from eggrim.creatures import (
    ENEMY_ATTACK_FRAMES,
    ENEMY_COOLDOWN_FRAMES,
    ENEMY_DAMAGE,
    ENEMY_HITBOX_SHRINK,
    ENEMY_SPRITE_W,
    PLAYER_SPRITE_W,
    ENEMY_VIEW_FRACTION,
    ENEMY_WALK_SPEED,
    ENEMY_WANDER_FRAMES,
    PILLAR_FLASH_FRAMES,
    spawn_pillars,
    spawn_test_enemy,
    spawn_walls,
)
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
from eggrim.items import (
    SCARF_PICKUP_RADIUS,
    draw_map_scarf,
    spawn_scarf,
)
from eggrim import cursor
from eggrim import inventory
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
scarf = None
enemy = None
fullscreen_on = True


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


def left_hand_banned():
    return factory.scarf_on() and player.view is Facing.LEFT


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
idle_phase = 0
dash_frames = 0


def portrait_key(view):
    if view in (Facing.LEFT, Facing.RIGHT):
        return "side"
    up = view is Facing.UP
    return "back" if up else "front"


def update():
    global portrait_to, portrait_from, portrait_fade, walls, player_on_door
    global fullscreen_on, idle_phase, dash_frames
    idle_phase += 1
    if pyxel.btnp(pyxel.KEY_RETURN) and pyxel.btn(pyxel.KEY_ALT) or pyxel.btnp(
        pyxel.KEY_ESCAPE
    ):
        fullscreen_on = not fullscreen_on
        pyxel.fullscreen(fullscreen_on)
    if pyxel.btnp(pyxel.KEY_I):
        inventory.toggle()
    if not fullscreen_on:
        inventory.close()
    if inventory.is_open():
        inventory.update()
        return
    if pyxel.btnp(pyxel.KEY_E):
        handle_scarf_hand()
    if dash_frames > 0:
        dash_frames -= 1
        new_x = player.x - DASH_SPEED / FPS
        if not feet_hits_wall(zone, new_x, player.y):
            player.x = new_x
        player.facing = (-1.0, 0.0)
        player.side = -1.0
        return
    if (
        pyxel.btnp(pyxel.KEY_SPACE)
        and factory.scarf_on()
        and player.view is Facing.LEFT
        and not player.blocking
    ):
        dash_frames = DASH_TOTAL_FRAMES
        player.blocking = False
        player.sprinting = False
        player.walk_phase = 0
        return
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
    if block_held and not left_hand_banned() and (
        player.stamina >= BLOCK_MIN_START or (player.blocking and player.stamina > 0)
    ):
        player.blocking = True
        player.block_anim += 1
        player.sprinting = False
        drained = True
        player.stamina = max(0.0, player.stamina - BLOCK_DRAIN / FPS)
    else:
        player.blocking = False
        player.block_anim = 0
    speed = MOVE_SPEED
    if not (dx or dy) or player.blocking:
        player.walk_phase = 0
    if (dx or dy) and not player.blocking:
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
        pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        and thrust.cooldown == 0
        and not player.blocking
    ):
        thrust.cooldown = THRUST_COOLDOWN_FRAMES
        thrust.anim = THRUST_ANIM_FRAMES
        thrust.facing = player.facing
        thrust.hit = False
        shoulder_x, shoulder_y = shoulder_point(player.view)
        shoulder_along = (
            (shoulder_x - player.x) * player.facing[0]
            + (shoulder_y - player.y) * player.facing[1]
        )
        target, target_contact = thrust_pillar_target(
            player, pillars, THRUST_REACH + shoulder_along
        )
        if target is not None:
            thrust.hit = True
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
                thrust.hit = True
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

    if enemy is not None:
        update_enemy(enemy)

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


def handle_scarf_hand():
    global scarf
    if scarf is None:
        return
    feet_x = player.x
    feet_y = player.y + PLAYER_FEET_OFFSET_Y
    if scarf.on_map:
        dist = ((scarf.x - feet_x) ** 2 + (scarf.y - feet_y) ** 2) ** 0.5
        if dist <= SCARF_PICKUP_RADIUS:
            scarf.on_map = False
            inventory.add_item("scarf")
    elif inventory.has_item("scarf"):
        scarf.x = feet_x
        scarf.y = feet_y + 1.0
        scarf.on_map = True
        inventory.remove_item("scarf")


def shoulder_point(view):
    if view is Facing.RIGHT:
        return player.x + 5.0, player.y - 19.0
    if view is Facing.LEFT:
        return player.x - 5.0, player.y - 19.0
    if view is Facing.UP:
        return player.x + 1.0, player.y - 36.0
    return player.x + 1.0, player.y + 6.0


def enemy_feet_dist(enemy):
    return ((player.x - enemy.x) ** 2 + (player.y + PLAYER_FEET_OFFSET_Y - enemy.y) ** 2) ** 0.5


def enemy_attack_range():
    return (ENEMY_SPRITE_W + PLAYER_SPRITE_W) / 2 - ENEMY_HITBOX_SHRINK


def update_enemy(enemy):
    if enemy.cooldown > 0:
        enemy.cooldown -= 1
    if enemy.anim > 0:
        enemy.anim -= 1
        if enemy.anim == ENEMY_ATTACK_FRAMES // 2:
            if (
                enemy_feet_dist(enemy) <= enemy_attack_range()
                and not player.blocking
                and dash_frames == 0
            ):
                player.health = max(0.0, player.health - ENEMY_DAMAGE)
        return
    dist = enemy_feet_dist(enemy)
    if dist <= enemy_attack_range():
        if enemy.cooldown == 0:
            enemy.anim = ENEMY_ATTACK_FRAMES
            enemy.cooldown = ENEMY_COOLDOWN_FRAMES
        return
    view_radius = (zone.width_px + zone.height_px) / (2 * ENEMY_VIEW_FRACTION)
    if dist <= view_radius:
        enemy.heading_x = (player.x - enemy.x) / dist
        enemy.heading_y = (player.y + PLAYER_FEET_OFFSET_Y - enemy.y) / dist
    else:
        enemy.wander_timer -= 1
        if enemy.wander_timer <= 0:
            angle = random.uniform(0.0, 2 * math.pi)
            enemy.heading_x = math.cos(angle)
            enemy.heading_y = math.sin(angle)
            enemy.wander_timer = ENEMY_WANDER_FRAMES
    if dist > 1.0:
        new_x = enemy.x + enemy.heading_x * ENEMY_WALK_SPEED / FPS
        new_y = enemy.y + enemy.heading_y * ENEMY_WALK_SPEED / FPS
        if not feet_hits_wall(zone, new_x, enemy.y):
            enemy.x = new_x
        if not feet_hits_wall(zone, enemy.x, new_y):
            enemy.y = new_y
        enemy.walk_phase += 1


def draw_test_enemy(enemy):
    if enemy.anim > 0:
        state = "attack"
        index = min(3, (ENEMY_ATTACK_FRAMES - enemy.anim) * 4 // ENEMY_ATTACK_FRAMES)
    elif enemy.walk_phase:
        state = "run"
        index = (enemy.walk_phase % 16) // 4
    else:
        state = "idle"
        index = (idle_phase // 15) % 3
    frame = enemy_frame(state, index)
    if frame is None:
        return
    bank, u, v, w, h = frame
    pyxel.blt(int(enemy.x) - w // 2, int(enemy.y) - h, bank, u, v, w, h, 0)


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
    if view in (Facing.UP, Facing.DOWN):
        if thrust.hit:
            pyxel.rect(int(fist_x) - 1, int(fist_y) - 1, 2, 2, 7)
        return
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
    draw_map_scarf(scarf)
    if enemy is not None and enemy.y <= player.y + PLAYER_FEET_OFFSET_Y:
        draw_test_enemy(enemy)
    if dash_frames > 0:
        state, frame_index = "dash", min(
            7, (DASH_TOTAL_FRAMES - 1 - dash_frames) * 8 // DASH_TOTAL_FRAMES
        )
    elif thrust.anim > 0:
        state, frame_index = "attack", min(
            3, int((1 - thrust.anim / THRUST_ANIM_FRAMES) * 4)
        )
    elif player.blocking:
        state, frame_index = "defensive", min(2, player.block_anim // 8)
    elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
        state, frame_index = "attack", 3
    elif player.walk_phase:
        state, frame_index = "run", (player.walk_phase % 16) // 4
    else:
        state, frame_index = "idle", (idle_phase // 15) % 4
    attacking = thrust.anim > 0
    bob = 1 if not attacking and player.sprinting and state == "run" and frame_index == 1 else 0
    if view is Facing.UP:
        direction = "back"
    elif view is Facing.DOWN:
        direction = "front"
    elif view is Facing.RIGHT:
        direction = "right"
    else:
        direction = "left"
    frame = hero_frame(state, direction, frame_index)
    if frame is not None:
        bank, u, v, w, h = frame
        pyxel.blt(
            int(player.x) - w // 2,
            int(player.y) + 8 - h - bob,
            bank,
            u,
            v,
            w,
            h,
            0,
        )
    elif view in (Facing.LEFT, Facing.RIGHT):
        walk_frame = (0, 1, 2, 1)[player.walk_phase % 20 // 5]
        if attacking:
            if thrust.anim == THRUST_ANIM_FRAMES or thrust.anim == 1:
                pose = 3
            elif thrust.anim == THRUST_ANIM_FRAMES - 1 or thrust.anim == 2:
                pose = 4
            else:
                pose = 5
        else:
            pose = walk_frame
        frames = ((0, 0), (48, 32), (0, 32), (96, 32), (144, 32), (0, 48))
        sprite_u, sprite_v = frames[pose]
        sprite_w = -16 if view is Facing.LEFT else 16
        pyxel.blt(
            int(player.x) - 8,
            int(player.y) - 8 - bob,
            0,
            sprite_u,
            sprite_v,
            sprite_w,
            16,
            0,
        )
    else:
        front = direction == "front"
        sprite_u, sprite_v = (16, 0) if front else (0, 16)
        pyxel.blt(
            int(player.x) - 8,
            int(player.y) - 8 - bob,
            0,
            sprite_u,
            sprite_v,
            16,
            16,
            0,
        )
    if attacking:
        draw_strike(view)
    for pillar in pillars:
        if pillar.y > player.y:
            draw_pillar(pillar)
    if enemy is not None and enemy.y > player.y + PLAYER_FEET_OFFSET_Y:
        draw_test_enemy(enemy)
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
        bank, u, v = PORTRAIT_BLEND_POS[(portrait_from, portrait_to, step)]
        pyxel.blt(0, 0, bank, u, v, 64, 64, 15)
    else:
        thumb_u, thumb_v = PORTRAIT_THUMB_POS[portrait_key(view)]
        portrait_w = -64 if view is Facing.LEFT else 64
        pyxel.blt(0, 0, 0, thumb_u, thumb_v, portrait_w, 64, 15)
    if inventory.is_open():
        inventory.draw()


def run():
    global zone, pillars, walls, scarf, enemy
    pyxel.init(
        SCREEN_W,
        SCREEN_H,
        title="Eggrim's Iterax",
        display_scale=5,
        fps=FPS,
        quit_key=pyxel.KEY_NONE,
    )
    pyxel.fullscreen(True)
    pyxel.icon(ICON_CHARS, 1, ICON_COLKEY)
    cursor.reset()
    inventory.render_backdrop()
    render_tiles()
    render_tile_tints()
    zone = load_zone("arena")
    player.x, player.y = zone.player_start
    pillars = spawn_pillars(zone)
    walls = spawn_walls(zone)
    scarf = spawn_scarf(zone, player.x, player.y)
    enemy = spawn_test_enemy(zone)
    pyxel.run(update, draw)