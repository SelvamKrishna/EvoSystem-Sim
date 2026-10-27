import raylib as rl

import cli
import config
from game import Game


def main() -> None:
    rl.InitWindow(config.WINDOW_SIZE, config.WINDOW_SIZE, b"EvoSystem-Sim")
    rl.SetTargetFPS(60)

    args = cli.get_cli_args()
    game = Game(args)

    while game.is_running():
        game.update()

        rl.BeginDrawing()
        rl.ClearBackground(rl.WHITE)

        game.draw()
        rl.EndDrawing()

        if rl.IsKeyPressed(rl.KEY_S):
            rl.TakeScreenshot(b"screenshot.png")

    rl.CloseWindow()

if __name__ == "__main__":
    main()
