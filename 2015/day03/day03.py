from sys import argv
from typing import Tuple, Set, Iterable


def solution(filename: str):
    raw_path = open(filename, "r").read()
    print("PART 1:", len(deliver(raw_path)))
    paths = {1: [2, []], 2: [1, []]}
    cur_path = 1
    for c in raw_path:
        paths[cur_path][1].append(c)
        cur_path = paths[cur_path][0]
    print("PART 2:", len(deliver(paths[1][1]) | deliver(paths[2][1])))


def deliver(path: Iterable[str]) -> Set[Tuple[int, int]]:
    x = y = 0
    coords = {(x, y)}
    for c in path:
        if c == "^":
            y += 1
        elif c == "v":
            y -= 1
        elif c == ">":
            x += 1
        else:
            x -= 1
        coords.add((x, y))
    return coords


if __name__ == "__main__":
    try:
        input_file = argv[1]
        solution(input_file)
    except IndexError:
        print("Enter path to data file!")
