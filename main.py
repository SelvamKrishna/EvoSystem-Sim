import raylib as rl

import config


def main() -> None:
    rl.InitWindow(config.WINDOW_SIZE, config.WINDOW_SIZE, b"EvoSystem-Sim")
    rl.SetTargetFPS(60)

    while not rl.WindowShouldClose():
        rl.BeginDrawing()
        rl.ClearBackground(rl.BLACK)
        rl.EndDrawing()

    rl.CloseWindow()

if __name__ == "__main__":
    main()
