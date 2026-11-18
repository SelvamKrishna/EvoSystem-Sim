import time

import raylib as rl
from colorama import Fore

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
        self._is_running = True
        self._start_time: float

        self.LAST_ROUND = self.args.player_count * config.MAX_ROUND
        self.selected_token: Token | None = None

        print("---")
        print(f"Board Seed  : {args.seed}")
        print(f"Player Count: {args.player_count}")
        print(f"Total Tokens: {args.player_token_count}")
        print("---")

    def is_running(self) -> bool:
        return not rl.WindowShouldClose() and self._is_running

    def _get_mouse_tile(self) -> tuple[int, int]:
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

        tile_x, tile_y = self._get_mouse_tile()

        if self._is_occupied(tile_x, tile_y):
            return

        token = Token(tile_x, tile_y)
        print(f"{Fore.MAGENTA}SETUP:{Fore.RESET} Player {player_id + 1} added {token}")
        self.players[player_id].tokens.append(token)

    def _take_colliding_token(self, x: int, y: int) -> Token | None:
        for i in range(self.args.player_count):
            if i == self.current_player_id:
                continue

            for t in self.players[i].tokens:
                if (t.x, t.y) != (x, y):
                    continue

                self.players[i].tokens.remove(t)
                return t

        return None

    def play_mode(self) -> None:
        if not rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            return

        tile_x, tile_y = self._get_mouse_tile()
        player: Player = self.players[self.current_player_id]

        if not player.has_energy():
            return

        # 1st click: get the token selected by the player
        if self.selected_token is None:
            self.selected_token = player.get_selection(tile_x, tile_y)
            return

        # 2nd click: move the token to clicked position, resolve combat
        if (self.selected_token.x == tile_x) and (self.selected_token.y == tile_y):
            self.selected_token = None
            return

        captured = self._take_colliding_token(tile_x, tile_y)
        if captured:
            player.captured += 1
            player.energy += 10
            print(f"PLAY: Player {self.current_player_id + 1} captured {captured}")

        player.energy -= 1
        print(f"-> Energy: {player.energy}")
        self.selected_token.x = tile_x
        self.selected_token.y = tile_y
        self.selected_token = None

    def _setup_round(self):
        player = self.players[self.current_player_id]
        print(f"PLAY: Round {self.round_count}")
        print(f"PLAY: Player {self.current_player_id + 1}")
        player.add_energy()
        player.consume_energy()
        print(f"-> Energy: {player.energy}")

    def _next_round(self) -> None:
        self.current_player_id = (self.current_player_id + 1) % self.args.player_count
        self.round_count += 1
        self._setup_round()

    def update(self) -> None:
        if not self.game_state:
            self.game_state = self._setup_complete()
            if self.game_state == True:
                self._start_time = time.time()
                self._setup_round()

        if self.game_state:
            self.play_mode()
        else:
            self.setup_mode()

        if rl.IsKeyPressed(rl.KEY_ENTER):
            self._next_round()

        if self.round_count >= self.args.player_count * 12 or rl.IsKeyPressed(
            rl.KEY_ESCAPE
        ):
            self.quit()

    def quit(self) -> None:
        self._is_running = False
        total_time = time.time() - self._start_time
        print(f"Time Played: {total_time:4}s")

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
