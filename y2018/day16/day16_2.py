import re
from sys import argv
from typing import List

from opcodes import OPS

LINES_PER_GROUP = 4


def find_values(raw_input: str) -> List[int]:
    return [int(d) for d in re.findall(r'\d+', raw_input)]


if __name__ == '__main__':
    f_name = argv[1]
    data = open(f_name, 'r').readlines()

    registers = [0, 0, 0, 0]

    for instr_line in data:
        instr = find_values(instr_line)
        op_code = instr[0]
        registers = OPS[op_code](registers, instr)

    print("REGISTERS:", registers)
