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

        rl.DrawCircle(
            self.x * config.CELL_SIZE + HALF_CELL_SIZE,
            self.y * config.CELL_SIZE + HALF_CELL_SIZE,
            HALF_CELL_SIZE + PADDING,
            color,
        )


class Player:
    def __init__(self, player_id: int) -> None:
        self.id = player_id
        self.tokens: list[Token] = []

    def draw(self) -> None:
        for token in self.tokens:
            token.draw(config.PLAYER_COLOR[self.id])
