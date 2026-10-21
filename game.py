import time

import raylib as rl

import config
from board import Board
from cli import Arguments
from player import Player, Token


class Game:
    def __init__(self, args: Arguments) -> None:
        self.players: list[Player] = [Player(i) for i in range(args.player_count)]
        self.board: Board = Board(args.seed)
        self.current_player_id: int = 0
        self.game_state: bool = False  # false: setup, true: play
        self.args = args
        self.round_count = 0

        self.selected_token: Token | None = None

        print("---")
        print(f"Board Seed  : {args.seed}")
        print(f"Player Count: {args.player_count}")
        print(f"Total Tokens: {args.player_token_count}")
        print("---")

    def _mouse_tile(self) -> tuple[int, int]:
        return (
            min(rl.GetMouseX() // config.CELL_SIZE, config.BOARD_SIZE - 1),
            min(rl.GetMouseY() // config.CELL_SIZE, config.BOARD_SIZE - 1),
        )

    def _is_occupied(self, x: int, y: int, ignore: Token | None = None) -> bool:
        for p in self.players:
            for t in p.tokens:
                if t is not ignore and (t.x, t.y) == (x, y):
                    return True
        return False

    def _setup_complete(self) -> bool:
        return all(len(p.tokens) >= self.args.player_token_count for p in self.players)

    def setup_mode(self) -> None:
        if not rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            return

        player_id: int = -1
        if rl.IsKeyDown(rl.KEY_ONE):
            player_id = 0
        elif rl.IsKeyDown(rl.KEY_TWO):
            player_id = 1
        elif rl.IsKeyDown(rl.KEY_THREE) and self.args.player_count > 2:
            player_id = 2
        elif rl.IsKeyDown(rl.KEY_FOUR) and self.args.player_count > 3:
            player_id = 3
        else:
            return

        if len(self.players[player_id].tokens) >= self.args.player_token_count:
            return

        tile_x, tile_y = self._mouse_tile()

        if self._is_occupied(tile_x, tile_y):
            return

        token = Token(tile_x, tile_y)
        print(f"SETUP: Player {player_id + 1} added {token}")
        self.players[player_id].tokens.append(token)

    def _remove_collision(self, x: int, y: int) -> list[Token]:
        captured: list[Token] = []
        for i in range(self.args.player_count):
            if i == self.current_player_id:
                continue
            remaining: list[Token] = []
            for t in self.players[i].tokens:
                if (t.x, t.y) == (x, y):
                    captured.append(t)
                else:
                    remaining.append(t)
            self.players[i].tokens = remaining
        return captured

    def play_mode(self) -> None:
        if not rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            return

        tile_x, tile_y = self._mouse_tile()

        # First click: select one of the current player's tokens.
        if self.selected_token is None:
            for token in self.players[self.current_player_id].tokens:
                if (token.x, token.y) == (tile_x, tile_y):
                    self.selected_token = token
                    return
            return

        # Second click: move there, capturing any opponents on the tile.
        captured = self._remove_collision(tile_x, tile_y)
        if captured:
            self.players[self.current_player_id].captured += len(captured)
            print(
                f"PLAY: Player {self.current_player_id + 1} captured "
                f"{len(captured)} token(s) from {[t for t in captured]}"
            )

        self.selected_token.x = tile_x
        self.selected_token.y = tile_y
        self.selected_token = None

    def update(self) -> None:
        if not self.game_state:
            self.game_state = self._setup_complete()
            if self.game_state == True:
                print(f"Time: {time.time()}")

        if self.game_state:
            self.play_mode()
        else:
            self.setup_mode()

        if rl.IsKeyPressed(rl.KEY_ENTER):
            self.current_player_id = (
                self.current_player_id + 1
            ) % self.args.player_count
            self.round_count += 1
            print(f"PLAY: Player {self.current_player_id + 1}'s turn")
            print(f"PLAY: Round {self.round_count}")

        if self.round_count > 36 or rl.IsKeyPressed(rl.KEY_ESCAPE):
            self.quit()

    def quit(self) -> None:
        rl.CloseWindow()

    def draw(self) -> None:
        self.board.draw()

        if self.selected_token is not None:
            rl.DrawRectangleLinesEx(
                (
                    self.selected_token.x * config.CELL_SIZE,
                    self.selected_token.y * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE,
                ),
                8,
                config.PLAYER_COLOR[self.current_player_id],
            )

        for player in self.players:
            player.draw()
