import abc
import sys
from typing import Dict

ROLLS_PER_TURN = 3
BOARD_SIZE = 10

# Real input
P1_START = 8
P2_START = 2

# Test input
P1_START_TEST = 4
P2_START_TEST = 8


class Die(abc.ABC):
    MAX_VALUE: int

    @property
    def roll(self) -> int:
        raise NotImplementedError


class D100(Die):
    """
    A die that always produces 1 greater than the previous value.
    Wraps around to 1 after 100.
    """
    MAX_VALUE = 100

    def __init__(self):
        self.last_value = self.MAX_VALUE
        self.roll_count = 0

    @property
    def roll(self) -> int:
        self.last_value = (self.last_value + 1) % self.MAX_VALUE
        self.roll_count += 1
        return self.last_value


class Player:
    def __init__(self, position: int):
        self.position = position
        self.score = 0

    def take_turn(self, move_distance: int):
        # No 0 position: multiple of 10 -> 10
        self.position = (self.position + move_distance) % BOARD_SIZE or 10
        self.score += self.position


def part1(test: bool = False) -> int:
    winning_score = 1000
    die = D100()
    p1 = Player(P1_START_TEST) if test else Player(P1_START)
    p2 = Player(P2_START_TEST) if test else Player(P2_START)
    players = (p1, p2)
    cur_player_idx = 0
    while p1.score < winning_score and p2.score < winning_score:
        cur_player = players[cur_player_idx]
        move_distance = sum(die.roll for _ in range(ROLLS_PER_TURN))
        cur_player.take_turn(move_distance)
        cur_player_idx = 1 - cur_player_idx
    return min(p1.score, p2.score) * die.roll_count


def part2(test: bool = False) -> int:
    p1 = Player(P1_START_TEST) if test else Player(P1_START)
    p2 = Player(P2_START_TEST) if test else Player(P2_START)
    players = {0: {"player": p1, "win_count": 0}, 1: {"player": p2, "win_count": 0}}
    simulate(0, players)
    return max(players[0]["win_count"], players[1]["win_count"])


def simulate(player_num: int, players: Dict):
    winning_score = 21
    player = players[player_num]["player"]
    for possible_roll in [3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9]:
        player.take_turn(possible_roll)
        if player.score >= winning_score:
            players[player_num]["win_count"] += 1
        else:
            simulate(1 - player_num, players)


def main():
    is_test = len(sys.argv) > 1 and sys.argv[1].lower() in {"t", "test"}
    print("PART 1:", part1(test=is_test))
    print("PART 2:", part2(test=is_test))


if __name__ == "__main__":
    main()
