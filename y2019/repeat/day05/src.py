"""
Defaults to using data_test.txt for input data.
Use flag --live-run to use 'real' data.
"""
import argparse
import pathlib
import sys
from typing import List

sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))

from intcode.intcode3 import Computer


def solve(data: List[int]):
    computer = Computer(data)
    computer.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [int(val) for val in f_in.read().strip().split(",")]

    print("** ENTER 1 FOR PART 1, ENTER 5 FOR PART 2 **")
    solve(data)


if __name__ == "__main__":
    main()
