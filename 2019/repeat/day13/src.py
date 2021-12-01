import argparse
import pathlib
import sys
from typing import List

sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))

from intcode.intcode5 import Computer
from simulation import GameScreen, Simulation


def solve(data: List[int], day_num: int) -> int:
    if day_num == 1:
        output_buffer = []
        computer = Computer(data, io_dest_type=Computer.MEMBUF_IO_DEST, custom_output_dest=output_buffer)
        computer.run()
        block_count = 0
        for value in output_buffer[2::3]:
            if value == GameScreen.VALUE_TYPE_BLOCK:
                block_count += 1
        return block_count
    else:
        # Create board
        # Record score
        # While blocks exist
        #   Stay under ball
        simulation = Simulation()
        simulation.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [int(val) for val in f_in.read().strip().split(",")]

    print("PART 1:", solve(data, day_num=1))
    solve(data, day_num=2)


if __name__ == "__main__":
    main()
