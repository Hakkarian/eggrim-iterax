from dataclasses import dataclass

THRUST_COOLDOWN_FRAMES = 15
THRUST_RANGE = 10.0
THRUST_DAMAGE = 1
THRUST_KNOCKBACK = 3.0
THRUST_ANIM_FRAMES = 4
THRUST_REACH = 13.0
THRUST_EXTEND_POINT = 0.4
THRUST_FIST_RADIUS = 2
PILLAR_HIT_RADIUS = 8.0


@dataclass
class ThrustState:
    cooldown: int = 0
    anim: int = 0
    facing: tuple = (1.0, 0.0)
    max_reach: float = THRUST_REACH


def thrust_target(player, pillars):
    best = None
    best_dist = None
    for pillar in pillars:
        to_x = pillar.x - player.x
        to_y = pillar.y - player.y
        dist = (to_x * to_x + to_y * to_y) ** 0.5
        if dist > THRUST_RANGE + PILLAR_HIT_RADIUS:
            continue
        if to_x * player.facing[0] + to_y * player.facing[1] <= 0:
            continue
        if best_dist is None or dist < best_dist:
            best, best_dist = pillar, dist
    return best