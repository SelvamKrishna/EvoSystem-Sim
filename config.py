from dataclasses import dataclass

from raylib import colors

BOARD_SIZE = 8
assert BOARD_SIZE > 0

TILE_COUNT: int = BOARD_SIZE * BOARD_SIZE
assert TILE_COUNT > 0

PLAYER_COLOR: tuple = (
    colors.RED,  # player 1
    colors.BLUE,  # player 2
    colors.GREEN,  # player 3
    colors.YELLOW,  # player 4
)


@dataclass
class TraitAttribute:
    weight: int
    tier_weight: None | tuple[int, int, int] = None


CENTER_BIAS: float = 10.0
TILE_CONFIG: dict[str, TraitAttribute] = {
    "": TraitAttribute(5),
    "attack": TraitAttribute(10, (30, 20, 10)),
    "health": TraitAttribute(5, (30, 20, 5)),
    "speed": TraitAttribute(10, (30, 20, 10)),
    "split": TraitAttribute(1),
}

# -- DO NOT CHANGE --

WINDOW_SIZE: int = 794
CELL_SIZE: int = WINDOW_SIZE // BOARD_SIZE
