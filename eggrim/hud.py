import math

import pyxel

ORB_X = 44
ORB_Y = 104
ORB_OUTER_R = 24
ORB_HOLE_R = 12
ORB_MARK_R = 4
ORB_MARK_OFFSET = 17
HOOK_R = 30
HOOK_COLOR_HP = 11
HOOK_COLOR_SP = 5
HOOK_SWEEP = 150.0
HUD_BORDER_COLOR = 0
BLOCK_TEXT_COLOR = 12
BLOCK_BLOB_ANGLES = (100.0, 170.0)

MINIMAP_X = 190
MINIMAP_Y = 2
MINIMAP_BORDER_COLOR = 5
MINIMAP_VIEW_COLOR = 6
MINIMAP_PILLAR_COLOR = 12
MINIMAP_PLAYER_COLOR = 8


def draw_minimap(zone, player, pillars, cam_x, cam_y):
    pyxel.rect(MINIMAP_X - 1, MINIMAP_Y - 1, zone.width_tiles + 2, zone.height_tiles + 2, HUD_BORDER_COLOR)
    pyxel.rectb(MINIMAP_X - 1, MINIMAP_Y - 1, zone.width_tiles + 2, zone.height_tiles + 2, MINIMAP_BORDER_COLOR)
    pyxel.rectb(
        MINIMAP_X + cam_x // 8,
        MINIMAP_Y + cam_y // 8,
        32,
        18,
        MINIMAP_VIEW_COLOR,
    )
    for pillar in pillars:
        pyxel.pset(MINIMAP_X + int(pillar.x) // 8, MINIMAP_Y + int(pillar.y) // 8, MINIMAP_PILLAR_COLOR)
    player_px = min(zone.width_tiles - 2, max(0, int(player.x) // 8 - 1))
    player_py = min(zone.height_tiles - 2, max(0, int(player.y) // 8 - 1))
    pyxel.rect(MINIMAP_X + player_px, MINIMAP_Y + player_py, 2, 2, MINIMAP_PLAYER_COLOR)


def draw_orb(blocking):
    for py in range(-ORB_OUTER_R, ORB_OUTER_R + 1):
        for px in range(-ORB_OUTER_R, ORB_OUTER_R + 1):
            dist = (px * px + py * py) ** 0.5
            if ORB_HOLE_R <= dist <= ORB_OUTER_R:
                pyxel.pset(ORB_X + px, ORB_Y + py, 1)
    if blocking:
        for py in range(-ORB_OUTER_R, ORB_OUTER_R + 1):
            for px in range(-ORB_OUTER_R, ORB_OUTER_R + 1):
                dist = (px * px + py * py) ** 0.5
                if not ORB_HOLE_R <= dist <= ORB_OUTER_R:
                    continue
                angle = math.degrees(math.atan2(py, px)) % 360
                if BLOCK_BLOB_ANGLES[0] <= angle <= BLOCK_BLOB_ANGLES[1] and (px + py) % 2 == 0:
                    pyxel.pset(ORB_X + px, ORB_Y + py, 13)
        pyxel.line(ORB_X + 6, ORB_Y - 22, ORB_X + 9, ORB_Y - 25, 13)
        pyxel.line(ORB_X + 9, ORB_Y - 20, ORB_X + 13, ORB_Y - 22, 13)
        pyxel.line(ORB_X + 11, ORB_Y - 17, ORB_X + 16, ORB_Y - 18, 13)
        pyxel.text(ORB_X - 11, ORB_Y - 38, "block", BLOCK_TEXT_COLOR)
    pyxel.circb(ORB_X, ORB_Y - ORB_MARK_OFFSET, ORB_MARK_R, 1)
    pyxel.circ(ORB_X, ORB_Y - ORB_MARK_OFFSET, ORB_MARK_R - 1, 13)


def draw_hook(color, fraction, mirror):
    steps = 72
    for step in range(steps + 1):
        t = step / steps
        if t > fraction:
            break
        angle = math.radians(90.0 - HOOK_SWEEP * t if mirror else 90.0 + HOOK_SWEEP * t)
        for radius in range(HOOK_R - 1, HOOK_R + 2):
            px = ORB_X + radius * math.cos(angle)
            py = ORB_Y + radius * math.sin(angle)
            pyxel.pset(int(px), int(py), color)
        for radius in (HOOK_R - 2, HOOK_R + 2):
            px = ORB_X + radius * math.cos(angle)
            py = ORB_Y + radius * math.sin(angle)
            pyxel.pset(int(px), int(py), 1)


def draw_orb_hud(blocking, health, stamina):
    draw_hook(HOOK_COLOR_HP, health, False)
    draw_hook(HOOK_COLOR_SP, stamina, True)
    draw_orb(blocking)