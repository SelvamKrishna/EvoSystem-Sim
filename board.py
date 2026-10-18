import random

import raylib as rl

import config


class Board:
    def __init__(self, seed: int) -> None:
        self.board: list[list[str]] = Board._make_board(seed)

    @staticmethod
    def _make_board(seed: int) -> list[list[str]]:
        random.seed(seed)
        print(f"Board Seed: {seed}")

        trait_keys = list(config.TILE_TRAITS.keys())
        trait_weights = [weight for _, weight in config.TILE_TRAITS.values()]

        board = [
            random.choices(trait_keys, weights=trait_weights, k=config.BOARD_SIZE)
            for _ in range(config.BOARD_SIZE)
        ]

        return board

    @staticmethod
    def _get_text_color(text: str) -> tuple[int, int, int, int]:
        if text.startswith("speed"):
            return (0, 0, 200, 255)

        if text.startswith("attack"):
            return (200, 0, 0, 255)

        if text.startswith("health"):
            return (0, 200, 0, 255)

        return (100, 100, 100, 255)

    def __getitem__(self, row: int) -> list[str]:
        return self.board[row]

    def __repr__(self) -> str:
        return "\n".join(" ".join(row) for row in self.board)

    def draw(self) -> None:
        TEXT_PADDING: int = 5

        for y in range(config.BOARD_SIZE):
            for x in range(config.BOARD_SIZE):
                text = self.board[y][x]
                text_color = Board._get_text_color(text)

                rl.DrawRectangleLines(
                    x * config.CELL_SIZE,
                    y * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE,
                    rl.BLACK,
                )
                rl.DrawText(
                    text.encode(),
                    x * config.CELL_SIZE + TEXT_PADDING,
                    y * config.CELL_SIZE + TEXT_PADDING,
                    20,
                    text_color
                )
