import re
from typing import List

from y2022.python.shared import get_data_file_path


def main():
    with open(get_data_file_path(day_number=5), "r") as f_in:
        raw_stacks = []
        line = next(f_in).strip("\n")
        while line:
            raw_stacks.append(line)
            line = next(f_in).strip("\n")
        stacks_1 = process_stacks(raw_stacks)
        stacks_2 = [[crate for crate in stack] for stack in stacks_1]
        for instruction in f_in:
            process_instruction_9000(stacks_1, instruction)
            process_instruction_9001(stacks_2, instruction)
    print("PART 1:", "".join(stack[-1] for stack in stacks_1))
    print("PART 2:", "".join(stack[-1] for stack in stacks_2))


def process_stacks(raw_stacks: List[str]):
    stacks = []
    rotated = _rotate_90_deg(raw_stacks)
    for row in rotated:
        if re.match(r"\d+", row[0]):
            stacks.append(re.findall(r"[A-Z]", row))
    return stacks


def _rotate_90_deg(raw: List[str]) -> List[str]:
    result = [[] for _ in range(len(raw[-2]))]
    for raw_row in raw[-1::-1]:
        for i in range(len(raw_row)):
            result[i].append(raw_row[i])
    return ["".join(row) for row in result]


def process_instruction_9000(stacks: List[List[str]], instruction: str):
    amount, origin, destination = re.findall(r"\d+", instruction)
    for _ in range(int(amount)):
        stacks[int(destination) - 1].append(stacks[int(origin) - 1].pop())


def process_instruction_9001(stacks: List[List[str]], instruction: str):
    amount, origin, destination = re.findall(r"\d+", instruction)
    crane = []
    for _ in range(int(amount)):
        crane.append(stacks[int(origin) - 1].pop())
    for _ in range(int(amount)):
        stacks[int(destination) - 1].append(crane.pop())


if __name__ == "__main__":
    main()
