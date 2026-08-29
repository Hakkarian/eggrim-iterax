from enum import Enum, auto


class GameState(Enum):
    FOUNDATION = auto()
    FOG = auto()
    HUD = auto()
    COMBAT = auto()


PHASES_REACHED = GameState.COMBAT


def announce_progress():
    for state in GameState:
        if state.value <= PHASES_REACHED.value:
            print(f"Phase {state.value} complete")