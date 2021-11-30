from sys import argv
from typing import List


def play_game(starting_nums: List[int], final_turn: int) -> int:
    memory = {num: idx + 1 for idx, num in enumerate(starting_nums)}
    current_turn = len(starting_nums) + 1
    current_num = 0  # Last of starting_nums was never said before
    while current_turn < final_turn:
        next_num = current_turn - memory.get(current_num, current_turn)
        memory[current_num] = current_turn
        current_num = next_num
        current_turn += 1
    return current_num


if __name__ == "__main__":
    version = argv[1]
    if version == "test":
        input_nums_set = ([0, 3, 6], [1, 3, 2], [2, 1, 3], [1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2])
        for ins in input_nums_set[:1]:
            print(play_game(ins, 2020))
    else:
        input_nums = [2, 0, 1, 9, 5, 19]
        print("PART 1:", play_game(input_nums, 2020))
        print("PART 2:", play_game(input_nums, 30000000))
