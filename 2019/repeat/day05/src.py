"""
Defaults to using data_test.txt for input data.
Use flag --live-run to use 'real' data.
"""
import argparse
import pathlib
import sys
from typing import List

sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))

from intcode.intcode2 import Computer


def solve(data: List[int], day_num: int, live_run: bool = True):
    computer = Computer(data, debug=False)
    computer.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [int(val) for val in f_in.read().strip().split(",")]

    print("PART 1:")
    solve(data, day_num=1, live_run=args.live_run)
    # print(f"PART 2: {solve(data, day_num=2, live_run=args.live_run)}")


if __name__ == "__main__":
    main()
    # data = [1002, 4, 3, 4, 33]
    # computer = Computer(data, debug=True)
    # computer.run()
    # print("MEMORY DUMP:", computer.dump())
