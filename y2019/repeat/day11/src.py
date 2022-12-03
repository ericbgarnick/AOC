import argparse
import pathlib
import sys
from typing import List

sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))

from day11.robot import Robot
from intcode.intcode5 import Computer


def solve(data: List[int], day_num: int) -> int:
    if day_num == 1:
        robot = Robot(calibrate=True)
    else:
        robot = Robot()
    computer = Computer(
        data,
        io_src_type=Computer.OBJECT_IO_SRC,
        io_dest_type=Computer.OBJECT_IO_DEST,
        custom_input_src=robot,
        custom_output_dest=robot,
    )
    result = computer.run()

    if result:
        return -1
    else:
        if day_num == 1:
            return robot.canvas_size
        else:
            robot.display_painting()
            return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [int(val) for val in f_in.read().strip().split(",")]

    print("PART 1:", solve(data, day_num=1))
    print("PART 2:")
    solve(data, day_num=2)


if __name__ == "__main__":
    main()
