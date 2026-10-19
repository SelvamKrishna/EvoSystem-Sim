import raylib as rl

from board import Board
from cli import *
from player import *


class Game:
    def __init__(self, args: Arguments) -> None:
        self.players: list[Player] = [
            Player(args.player_token_count, i) for i in range(args.player_count)
        ]
        self.board: Board = Board(args.seed)
        self.current_player: int = 0
        self.game_state: bool = False  # false: setup, true: play
        self.args = args

        print("---")
        print(f"Board Seed  : {args.seed}")
        print(f"Player Count: {args.player_count}")
        print(f"Total Tokens: {args.player_token_count}")
        print("---")

    def setup_mode(self) -> None:
        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            player_id: int = 0
            if rl.IsKeyDown(rl.KEY_ONE):
                player_id = 0
            elif rl.IsKeyDown(rl.KEY_TWO):
                player_id = 1
            elif rl.IsKeyDown(rl.KEY_THREE):
                player_id = 2
            elif rl.IsKeyDown(rl.KEY_FOUR):
                player_id = 3
            else:
                return

            if len(self.players[player_id].tokens) >= self.args.player_token_count:
                return

            token = Token(
                int(rl.GetMouseX() // config.CELL_SIZE),
                int(rl.GetMouseY() // config.CELL_SIZE),
            )
            print(f"SETUP: Player {player_id + 1} added {token}")
            self.players[player_id].tokens.append(token)

    def play_mode(self) -> None:
        pass

    def update(self) -> None:
        self.game_state = True
        for player in self.players:
            if len(player.tokens) < self.args.player_token_count:
                self.game_state = False
                break

        self.play_mode() if self.game_state else self.setup_mode()

    def draw(self) -> None:
        self.board.draw()

        for player in self.players:
            player.draw()
