from typing import List, Dict, Set
from sys import argv


Board = List[List[int]]


class BingoPlayer:
    def __init__(self, board: Board):
        self.board = board
        self.needed = self.determine_needed()
        self.already_bingoed = False

    def determine_needed(self) -> Dict[str, Set[int]]:
        """Return a dictionary of sets of numbers needed to win
        where keys are row numbers and column numbers,
        prefixed by 'r' and 'c' respectively."""
        needed = {}
        for r, row in enumerate(self.board):
            for c, val in enumerate(row):
                try:
                    needed[f"r{r}"].add(val)
                except KeyError:
                    needed[f"r{r}"] = {val}
                try:
                    needed[f"c{c}"].add(val)
                except KeyError:
                    needed[f"c{c}"] = {val}
        return needed

    def has_bingo(self, num: int) -> bool:
        """
        Return True if num causes this player to get BINGO.

        Side effect: update self.already_bingoed
        """
        result = False
        for key, nums in self.needed.items():
            if num in nums:
                nums.remove(num)
                if not len(nums):
                    # BINGO: return winning number
                    self.already_bingoed = True
                    result = True
        return result

    def calculate_score(self, last_number: int) -> int:
        remaining = set()
        for n in self.needed.values():
            remaining |= n
        return sum(remaining) * last_number


class BingoGame:
    def __init__(self, numbers: List[int], boards: List[Board]):
        self.numbers = numbers
        self.boards = boards
        self.players = [BingoPlayer(board) for board in self.boards]


def parse_input(filename: str) -> BingoGame:
    boards = []
    with open(filename, "r") as f_in:
        numbers = [int(num) for num in next(f_in).strip().split(",")]
        cur_board = []
        for line in f_in:
            line = line.strip()
            if line == "" and len(cur_board):
                boards.append(copy_board(cur_board))
                cur_board = []
            elif len(line):
                cur_board.append([int(n) for n in line.strip().split()])
            else:
                # Empty row before any board has been read
                continue
        boards.append(copy_board(cur_board))
    return BingoGame(numbers, boards)


def copy_board(original: Board) -> Board:
    new_board = []
    for row in original:
        new_board.append([n for n in row])
    return new_board


def part1(bingo_game: BingoGame) -> int:
    """Return the score for the first player to get BINGO."""
    for number in bingo_game.numbers:
        for player in bingo_game.players:
            if player.has_bingo(number):
                return player.calculate_score(number)
    return -1


def part2(bingo_game: BingoGame) -> int:
    """Return the score for the last player to get BINGO."""
    win_count = 0
    score = -1
    for number in bingo_game.numbers:
        for player in bingo_game.players:
            if not player.already_bingoed and player.has_bingo(number):
                win_count += 1
                score = player.calculate_score(number)
                if win_count == len(bingo_game.players):
                    return score
    return score


def main():
    try:
        input_file = argv[1]
        bingo_game = parse_input(input_file)
        print("PART 1:", part1(bingo_game))
        bingo_game = parse_input(input_file)
        print("PART 2:", part2(bingo_game))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()
