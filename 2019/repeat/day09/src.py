import argparse
import pathlib
import sys
from typing import List

sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))

from intcode.intcode4 import Computer


def solve(data: List[int], day_num: int) -> int:
    if day_num == 1:
        computer = Computer(
            data,
            io_src=Computer.MEMBUF_IO_SRC,
            io_dest=Computer.MEMBUF_IO_DEST,
        )
        computer.add_input(1)
        result = computer.run()

        output_buffer = computer.get_output_buffer()
        next_output = output_buffer.popleft()
        while output_buffer:
            print(next_output)
            next_output = output_buffer.popleft()

        if result:
            return -1
        else:
            return next_output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [int(val) for val in f_in.read().strip().split(",")]

    print("PART 1:", solve(data, day_num=1))
    # print("PART 2:", solve(data, day_num=2))


if __name__ == "__main__":
    main()
