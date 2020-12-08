from sys import argv
from typing import List, Tuple, Optional, Dict


def parse_input(filename: str) -> List[Tuple[str, int]]:
    instructions = []
    for line in open(filename, "r"):
        op, arg = line.strip().split()
        instructions.append((op, int(arg)))
    return instructions


def run(instructions: List[Optional[Tuple[str, int]]]) -> Tuple[int, int]:
    """Replace visited instructions with None so repeat reads fail"""
    accumulator = current_pos = 0
    current_ins = instructions[current_pos]
    while current_ins:
        instructions[current_pos] = None
        op, arg = current_ins
        if op == "acc":
            accumulator += arg
            current_pos += 1
        elif op == "jmp":
            current_pos += arg
        elif op == "nop":
            current_pos += 1
        else:
            raise ValueError(f"Unknown operation: {op}")
        if current_pos == len(instructions):
            # Successfully reached the end of instructions
            current_ins = None
        else:
            # Advance to the next instruction
            current_ins = instructions[current_pos]
    return accumulator, current_pos


def find_changeable_ops(instructions: List[Tuple[str, int]]) -> Dict[str, List[int]]:
    """Return indexes of jmp and nop ops whose argument is not 1"""
    changes = {"nop": [], "jmp": []}
    for i, instr in enumerate(instructions):
        op, arg = instr
        if op in changes.keys() and arg != 1:
            changes[op].append(i)
    return changes


def try_alternatives(instructions: List[Tuple[str, int]], changes: Dict[str, List[int]]) -> int:
    """Run instructions repeatedly, exchanging one instance of 'nop' and 'jmp' for each run"""
    swap = {"nop": "jmp", "jmp": "nop"}
    for op in swap.keys():
        for change in changes[op]:
            op, arg = instructions[change]
            instructions[change] = (swap[op], arg)
            accumulator, final_pos = run([i for i in instructions])
            if final_pos == len(instructions):
                return accumulator
            else:
                instructions[change] = (op, arg)


if __name__ == "__main__":
    input_file = argv[1]
    instruction_set = parse_input(input_file)
    print("PART 1:", run([i for i in instruction_set])[0])
    possible_changes = find_changeable_ops(instruction_set)
    print("PART 2:", try_alternatives(instruction_set, possible_changes))
