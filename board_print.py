import raylib as rl

import cli
import config
from game import Game

WINDOW_DIMENSION: tuple[int, int] = (794, 1123)
TOKEN_SET_DIMENSION: tuple[int, int] = (WINDOW_DIMENSION[0] // 4, WINDOW_DIMENSION[1] - config.WINDOW_SIZE)

def main() -> None:
    rl.InitWindow(*WINDOW_DIMENSION, b"EvoSystem-Sim")
    rl.SetTargetFPS(60)

    args = cli.get_cli_args()
    game = Game(args)

    while not rl.WindowShouldClose():
        rl.BeginDrawing()
        rl.ClearBackground(rl.WHITE)

        game.draw()
        for i in range(4):
            rl.DrawRectangle(
                i * TOKEN_SET_DIMENSION[0],
                config.WINDOW_SIZE,
                *TOKEN_SET_DIMENSION,
                config.PLAYER_COLOR[i]
            )

        rl.EndDrawing()

        if rl.IsKeyPressed(rl.KEY_S):
            rl.TakeScreenshot(b"board_print.png")

    rl.CloseWindow()

if __name__ == "__main__":
    main()
