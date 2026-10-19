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

TILE_TRAITS: dict[str, tuple[str, int]] = {
    "": ("no effect", 30),
    "speed-1": ("+1 move per turn", 15),
    "speed-2": ("+2 move per turn", 10),
    "speed-3": ("+3 move per turn", 4),
    "speed-4": ("+4 move per turn", 1),
    "attack-1": ("+1 damage per turn", 15),
    "attack-2": ("+2 damage per turn", 10),
    "attack-3": ("+3 damage per turn", 4),
    "attack-4": ("+4 damage per turn", 1),
    "health-1": ("-1 damage per turn", 15),
    "health-2": ("-2 damage per turn", 10),
    "health-3": ("-3 damage per turn", 4),
    "health-4": ("-4 damage per turn", 1),
}

# -- DO NOT CHANGE --

WINDOW_SIZE: int = 800
CELL_SIZE: int = WINDOW_SIZE // BOARD_SIZE
