"""
Part 1 answer: 65556
Part 2 answer: CB779
"""
from y2016.python.shared import get_data_file_path


SIMPLE_MOVES = {
    "1": {"U": "1", "R": "2", "D": "4", "L": "1"},
    "2": {"U": "2", "R": "3", "D": "5", "L": "1"},
    "3": {"U": "3", "R": "3", "D": "6", "L": "2"},
    "4": {"U": "1", "R": "5", "D": "7", "L": "4"},
    "5": {"U": "2", "R": "6", "D": "8", "L": "4"},
    "6": {"U": "3", "R": "6", "D": "9", "L": "5"},
    "7": {"U": "4", "R": "8", "D": "7", "L": "7"},
    "8": {"U": "5", "R": "9", "D": "8", "L": "7"},
    "9": {"U": "6", "R": "9", "D": "9", "L": "8"},
}
COMPLEX_MOVES = {
    "1": {"U": "1", "R": "1", "D": "3", "L": "1"},
    "2": {"U": "2", "R": "3", "D": "6", "L": "2"},
    "3": {"U": "1", "R": "4", "D": "7", "L": "2"},
    "4": {"U": "4", "R": "4", "D": "8", "L": "3"},
    "5": {"U": "5", "R": "6", "D": "5", "L": "5"},
    "6": {"U": "2", "R": "7", "D": "A", "L": "5"},
    "7": {"U": "3", "R": "8", "D": "B", "L": "6"},
    "8": {"U": "4", "R": "9", "D": "C", "L": "7"},
    "9": {"U": "9", "R": "9", "D": "9", "L": "8"},
    "A": {"U": "6", "R": "B", "D": "A", "L": "A"},
    "B": {"U": "7", "R": "C", "D": "D", "L": "A"},
    "C": {"U": "8", "R": "C", "D": "C", "L": "B"},
    "D": {"U": "B", "R": "D", "D": "D", "L": "D"},
}


def load_instructions() -> list[str]:
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        return [line.strip() for line in f_in]


def follow_instructions(pos: int, instruction: str, moves_map: dict[str, dict[str, str]]) -> int:
    for move in instruction:
        pos = moves_map[pos][move]
    return pos


def main():
    instructions = load_instructions()
    simple_pos = "5"
    complex_pos = "5"
    simple_code = []
    complex_code = []
    for instr in instructions:
        simple_pos = follow_instructions(simple_pos, instr, SIMPLE_MOVES)
        simple_code.append(simple_pos)
        complex_pos = follow_instructions(complex_pos, instr, COMPLEX_MOVES)
        complex_code.append(complex_pos)
    print("PART 1:", "".join(str(val) for val in simple_code))
    print("PART 1:", "".join(str(val) for val in complex_code))


if __name__ == "__main__":
    main()
