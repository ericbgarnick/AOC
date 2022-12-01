import sys
from typing import List


def create_numbers_list(filename: str) -> List[int]:
    with open(filename) as f:
        read_data = f.read()

    return [int(str_num) for str_num in read_data.split()]


def count_increases(numbers_list: List[int]) -> int:
    new_list = []
    for i, item in enumerate(numbers_list[1:], 1):
        prev_idx = i - 1
        prev_item = numbers_list[prev_idx]
        if item > prev_item:
            new_list.append(item)
    list_length = len(new_list)
    return list_length


def main(filename: str):
    numbers_list = create_numbers_list(filename)
    result = count_increases(numbers_list)
    print("RESULT:", result)


if __name__ == "__main__":
    command_line_args = sys.argv
    if len(command_line_args) != 2:
        print("Please enter data file name")
    else:
        filename = sys.argv[1]
        main(filename)
