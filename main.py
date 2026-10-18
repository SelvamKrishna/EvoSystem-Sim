import time

import raylib as rl

import config
from board import Board

SEED = time.time_ns()
SEED = 1792297318392815100

def main() -> None:
    rl.InitWindow(config.WINDOW_SIZE, config.WINDOW_SIZE, b"EvoSystem-Sim")
    rl.SetTargetFPS(60)

    board = Board(SEED)

    while not rl.WindowShouldClose():
        rl.BeginDrawing()
        rl.ClearBackground(rl.WHITE)

        board.draw()
        rl.EndDrawing()

        if rl.IsKeyPressed(rl.KEY_S):
            rl.TakeScreenshot(b"screenshot.png")


    rl.CloseWindow()

if __name__ == "__main__":
    main()
