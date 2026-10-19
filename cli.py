import sys
import time
from dataclasses import dataclass


@dataclass
class Arguments:
    seed: int
    player_count: int
    player_token_count: int


def get_cli_args() -> Arguments:
    seed: int = time.time_ns()
    player_count: int = 2
    player_token_count: int = 5

    args = sys.argv
    for arg in args:
        if arg.startswith("s="):
            seed = int(arg.strip("s="))

        if arg.startswith("p="):
            player_count = int(arg.strip("p="))

        if arg.startswith("n="):
            player_token_count = int(arg.strip("n="))

    return Arguments(seed, player_count, player_token_count)
