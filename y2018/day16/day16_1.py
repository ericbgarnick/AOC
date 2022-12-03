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

    num_ambiguous = 0

    code_map = {}

    for offset in range(0, len(data), LINES_PER_GROUP):
        before_raw, instr_raw, after_raw, *blank = data[offset: offset + LINES_PER_GROUP]
        before = find_values(before_raw)
        instr = find_values(instr_raw)
        after = find_values(after_raw)

        code = instr[0]
        code_map[code] = code_map.get(code, set())

        match_count = 0
        for op in OPS.values():
            copy = [r for r in before]
            operated = op(copy, instr)
            if operated == after:
                code_map[code].add(op.__name__)
                match_count += 1

        if match_count > 2:
            num_ambiguous += 1

    print("{} SAMPLES ARE AMBIGUOUS".format(num_ambiguous))
    for code, names in code_map.items():
        print("{}: {}".format(code, names))
