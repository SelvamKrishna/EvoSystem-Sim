import random

import raylib as rl
from raylib import colors

import config


class Board:
    def __init__(self, seed: int) -> None:
        self.board: list[list[str]] = Board._make_board(seed)

    @staticmethod
    def _make_board(seed: int) -> list[list[str]]:
        rng = random.Random(seed)
        print(f"Board Seed: {seed}")

        CENTER = config.BOARD_SIZE / 2
        trait_keys = list(config.TILE_CONFIG.keys())
        trait_weights = [attrib.weight for attrib in config.TILE_CONFIG.values()]
        board: list[list[str]] = []
        weight_board: list[list[float]] = []

        for y in range(config.BOARD_SIZE):
            row: list[str] = []
            weight_row: list[float] = []

            for x in range(config.BOARD_SIZE):
                tile_trait = rng.choices(trait_keys, trait_weights)[0]

                tier_weight = config.TILE_CONFIG[tile_trait].tier_weight
                magnitude = config.CENTER_BIAS * ((x - CENTER + 0.5) ** 2 + (y - CENTER + 0.5) ** 2) + 1
                weight_row.append(magnitude)

                if tier_weight is None:
                    row.append(tile_trait)
                    continue

                tile_tier = rng.choices([1, 2, 3], [weight / magnitude for weight in tier_weight])[0]
                row.append(f"{tile_trait}-{tile_tier}")

            weight_board.append(weight_row)
            board.append(row)

        for r in weight_board:
            for x in r:
                print(f"{int(x)}, ", end="")
            print()

        return board

    @staticmethod
    def _get_text_color(text: str) -> tuple[int, int, int, int]:
        if text.startswith("speed"):
            return (0, 0, 200, 255)

        if text.startswith("attack"):
            return (200, 0, 0, 255)

        if text.startswith("health"):
            return (0, 200, 0, 255)

        if text.startswith("split"):
            return (150, 0, 200, 255)

        return (100, 100, 100, 255)

    def __getitem__(self, row: int) -> list[str]:
        return self.board[row]

    def __repr__(self) -> str:
        return "\n".join(" ".join(row) for row in self.board)

    def draw(self) -> None:
        TEXT_PADDING = 5
        for y in range(config.BOARD_SIZE):
            for x in range(config.BOARD_SIZE):
                text = self.board[y][x]
                text_color = Board._get_text_color(text)
                rl.DrawRectangleLines(
                    x * config.CELL_SIZE,
                    y * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE,
                    colors.BLACK,
                )
                rl.DrawText(
                    text.encode(),
                    x * config.CELL_SIZE + TEXT_PADDING,
                    y * config.CELL_SIZE + TEXT_PADDING,
                    20,
                    text_color,
                )
