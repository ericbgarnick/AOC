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


def solve(data: List[int], day_num: int, live_run: bool = True) -> str:
    computer = Computer(data)
    if day_num == 1:
        if live_run:
            computer.initialize({1: 12, 2: 2})
        computer.run()
        if live_run:
            return str(computer.dump()[0])
        else:
            return str(computer.dump())
    else:
        if live_run:
            goal = 19690720
            init_value_range = (0, 100)
            for noun in range(*init_value_range):
                for verb in range(*init_value_range):
                    computer.initialize({1: noun, 2: verb})
                    computer.run()
                    if computer.dump()[0] == goal:
                        return str(100 * noun + verb)
        else:
            return "No test run available"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [int(val) for val in f_in.read().strip().split(",")]

    print(f"PART 1: {solve(data, day_num=1, live_run=args.live_run)}")
    print(f"PART 2: {solve(data, day_num=2, live_run=args.live_run)}")


if __name__ == "__main__":
    main()
