from dataclasses import dataclass

from eggrim.world import circle_touches_rect, circle_wall_tile
from eggrim.zones import TILE

THRUST_COOLDOWN_FRAMES = 15
THRUST_RANGE = 10.0
THRUST_DAMAGE = 1
THRUST_KNOCKBACK = 3.0
THRUST_ANIM_FRAMES = 7
THRUST_REACH = 13.0
THRUST_EXTEND_POINT = 0.4
THRUST_FIST_RADIUS = 2

PILLAR_HIT_X0 = -4.0
PILLAR_HIT_Y0 = 5.0
PILLAR_HIT_X1 = 5.0
PILLAR_HIT_Y1 = 8.0


@dataclass
class ThrustState:
    cooldown: int = 0
    anim: int = 0
    facing: tuple = (1.0, 0.0)
    max_reach: float = THRUST_REACH


def ray_contact(player, reach_from_center, touching):
    def overlaps(probe):
        probe_x = player.x + player.facing[0] * probe
        probe_y = player.y + player.facing[1] * probe
        return touching(probe_x, probe_y)

    hit_step = None
    for step in range(1, int(reach_from_center) + 2):
        if overlaps(step):
            hit_step = step
            break
    if hit_step is None:
        return None
    low = float(hit_step)
    while low > 0.5 and overlaps(low - 0.5):
        low -= 0.5
    contact = low
    for refine in range(1, 21):
        candidate = low - 0.5 + refine * (0.5 / 20)
        if overlaps(candidate):
            contact = candidate
            break
    return contact


def thrust_pillar_target(player, pillars, reach_from_center):
    def touching(probe_x, probe_y):
        for pillar in pillars:
            if circle_touches_rect(
                probe_x,
                probe_y,
                THRUST_FIST_RADIUS,
                pillar.x + PILLAR_HIT_X0,
                pillar.y + PILLAR_HIT_Y0,
                pillar.x + PILLAR_HIT_X1,
                pillar.y + PILLAR_HIT_Y1,
            ):
                return pillar
        return None

    contact = ray_contact(player, reach_from_center, touching)
    if contact is None:
        return None, None
    probe_x = player.x + player.facing[0] * contact
    probe_y = player.y + player.facing[1] * contact
    return touching(probe_x, probe_y), contact


def thrust_wall_target(player, zone, walls, reach_from_center):
    def touching(probe_x, probe_y):
        tile = circle_wall_tile(zone, probe_x, probe_y, THRUST_FIST_RADIUS)
        if tile is not None and tile in walls:
            return tile
        return None

    contact = ray_contact(player, reach_from_center, touching)
    if contact is None:
        return None, None
    probe_x = player.x + player.facing[0] * contact
    probe_y = player.y + player.facing[1] * contact
    return walls[touching(probe_x, probe_y)], contact