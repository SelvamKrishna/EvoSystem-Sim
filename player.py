import random

import raylib as rl

import config


class Token:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def draw(self, color: tuple[int, int, int, int]) -> None:
        PADDING: int = -3
        HALF_CELL_SIZE: int = config.CELL_SIZE // 2

        new_color = list(color)
        new_color[3] = 50

        rl.DrawCircle(
            self.x * config.CELL_SIZE + HALF_CELL_SIZE,
            self.y * config.CELL_SIZE + HALF_CELL_SIZE,
            HALF_CELL_SIZE + PADDING,
            new_color,
        )


class Player:
    def __init__(self, player_id: int) -> None:
        self.id = player_id
        self.tokens: list[Token] = []
        self.captured: int = 0
        self.energy: int = 25

    def add_energy(self) -> None:
        add_val = random.randrange(1, 6)
        self.energy += add_val
        print(f"-> Rolled: {add_val}")

    def has_energy(self) -> bool:
        return self.energy > 0

    def consume_energy(self) -> None:
        self.energy -= len(self.tokens)

    def get_selection(self, tile_x, tile_y) -> Token | None:
        for token in self.tokens:
            if (token.x, token.y) == (tile_x, tile_y):
                return token
        return None

    def draw(self) -> None:
        for token in self.tokens:
            token.draw(config.PLAYER_COLOR[self.id])

    def __repr__(self) -> str:
        return f"Player {self.id}"


# each players start with a total of 25 energy points;
# each turn: player-energy - no. of tokens they have;
# each move: player-energy -= 1;
# attacking another player's token gives + 10 energy;
