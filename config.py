from raylib import colors

BOARD_SIZE: tuple[int, int] = (8, 8)
assert BOARD_SIZE[0] == BOARD_SIZE[1]

TILE_COUNT: int = BOARD_SIZE[0] * BOARD_SIZE[1]
assert TILE_COUNT > 0

PLAYER_COUNT: int = 4
assert PLAYER_COUNT in range(2, 5)  # [2 | 3 | 4] players

PLAYER_COLOR: tuple = (
    colors.RED,  # player 1
    colors.BLUE,  # player 2
    colors.GREEN,  # player 3
    colors.YELLOW,  # player 4
)

TILE_TRAITS: dict[str, str] = {
    "speed-1": "+1 move per turn",
    "speed-2": "+2 move per turn",
    "speed-3": "+3 move per turn",
    "speed-4": "+4 move per turn",
    "attack-1": "+1 damage per turn",
    "attack-2": "+2 damage per turn",
    "attack-3": "+3 damage per turn",
    "attack-4": "+4 damage per turn",
}

# -- DO NOT CHANGE --

WINDOW_SIZE: int = 800
CELL_SIZE: int = WINDOW_SIZE // BOARD_SIZE[0]
