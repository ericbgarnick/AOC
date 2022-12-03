import argparse
import pathlib
import sys
from typing import List, Optional, Deque

sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))

from intcode.intcode3 import Computer, EmptyInput

SIMPLE_PHASE_VALUES = {0, 1, 2, 3, 4}
FEEDBACK_PHASE_VALUES = {5, 6, 7, 8, 9}


def solve(data: List[int], day_num: int) -> int:
    best_signal = 0
    phase_values = SIMPLE_PHASE_VALUES if day_num == 1 else FEEDBACK_PHASE_VALUES
    for phase_a in phase_values:
        for phase_b in phase_values - {phase_a}:
            for phase_c in phase_values - {phase_a, phase_b}:
                for phase_d in phase_values - {phase_a, phase_b, phase_c}:
                    for phase_e in phase_values - {phase_a, phase_b, phase_c, phase_d}:
                        computer_a = setup_computer(data, "A")
                        computer_b = setup_computer(data, "B", phase_b, input_buffer=computer_a.get_output_buffer())
                        computer_c = setup_computer(data, "C", phase_c, input_buffer=computer_b.get_output_buffer())
                        computer_d = setup_computer(data, "D", phase_d, input_buffer=computer_c.get_output_buffer())
                        computer_e = setup_computer(data, "E", phase_e, input_buffer=computer_d.get_output_buffer())
                        if day_num == 2:
                            computer_a.set_input_buffer(computer_e.get_output_buffer())
                        computer_a.add_input(phase_a)
                        computer_a.add_input(0)
                        run_computers([computer_a, computer_b, computer_c, computer_d, computer_e], loop=day_num == 2)
                        new_signal = computer_e.output_history[-1]
                        if new_signal > best_signal:
                            best_signal = new_signal

    return best_signal


def setup_computer(
        data: List[int],
        identifier: str,
        phase_setting: Optional[int] = None,
        input_signal: Optional[int] = None,
        input_buffer: Optional[Deque] = None,
        output_buffer: Optional[Deque] = None,
) -> Computer:
    computer = Computer(
        code=data,
        identifier=identifier,
        io_src=Computer.MEMBUF_IO_SRC,
        io_dest=Computer.MEMBUF_IO_DEST,
        custom_input_buffer=input_buffer,
        custom_output_buffer=output_buffer,
    )
    if phase_setting is not None:
        computer.add_input(phase_setting)
    if input_signal is not None:
        computer.add_input(input_signal)
    return computer


def run_computers(computers: List[Computer], loop: bool):
    # Computers return 0 on successful termination
    results = [1 for _ in range(len(computers))]
    cur_computer_idx = 0
    while any(results):
        try:
            results[cur_computer_idx] = computers[cur_computer_idx].run()
        except EmptyInput:
            if loop:
                pass
            else:
                # Only need output, not terminal state
                results[cur_computer_idx] = 0
        cur_computer_idx = (cur_computer_idx + 1) % len(computers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = [int(val) for val in f_in.read().strip().split(",")]

    print("PART 1:", solve(data, day_num=1))
    print("PART 2:", solve(data, day_num=2))


if __name__ == "__main__":
    main()
