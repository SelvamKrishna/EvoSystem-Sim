import raylib as rl

from board import Board
from cli import *
from player import *


class Game:
    def __init__(self, args: Arguments) -> None:
        self.players: list[Player] = [Player(i) for i in range(args.player_count)]
        self.board: Board = Board(args.seed)
        self.current_player: int = 0
        self.game_state: bool = False  # false: setup, true: play
        self.args = args

        self.selected_token: Token | None = None

        print("---")
        print(f"Board Seed  : {args.seed}")
        print(f"Player Count: {args.player_count}")
        print(f"Total Tokens: {args.player_token_count}")
        print("---")

    def _is_occupied(self, x: int, y: int, ignore: Token | None = None) -> bool:
        for p in self.players:
            for t in p.tokens:
                if t is not ignore and (t.x, t.y) == (x, y):
                    return True
        return False

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

            token_x = int(rl.GetMouseX() // config.CELL_SIZE)
            token_y = int(rl.GetMouseY() // config.CELL_SIZE)

            if self._is_occupied(token_x, token_y):
                return

            token = Token(token_x, token_y)
            print(f"SETUP: Player {player_id + 1} added {token}")
            self.players[player_id].tokens.append(token)

    def play_mode(self) -> None:
        if not rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            return

        tile_x = min(rl.GetMouseX() // config.CELL_SIZE, config.BOARD_SIZE - 1)
        tile_y = min(rl.GetMouseY() // config.CELL_SIZE, config.BOARD_SIZE - 1)

        if self.selected_token is None:
            for token in self.players[self.current_player].tokens:
                if (token.x, token.y) == (tile_x, tile_y):
                    self.selected_token = token
                    return
            return

        if self._is_occupied(tile_x, tile_y, ignore=self.selected_token):
            self.selected_token = None
            return

        self.selected_token.x = tile_x
        self.selected_token.y = tile_y
        self.selected_token = None
        self.current_player = (self.current_player + 1) % self.args.player_count

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
