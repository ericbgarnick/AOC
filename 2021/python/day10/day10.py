from sys import argv
from typing import List


SYMBOLS = {
    ")": {"syntax_score": 3, "completion_score": 1},
    "]": {"syntax_score": 57, "completion_score": 2},
    "}": {"syntax_score": 1197, "completion_score": 3},
    ">": {"syntax_score": 25137, "completion_score": 4},
}
PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}


def parse_input(filename: str) -> List[str]:
    return [line.strip() for line in open(filename, "r")]


def part1(nav_subsystem: List[str]) -> int:
    """Return the syntax error score for the received navigation subsystem."""
    return sum(syntax_error_score(line) for line in nav_subsystem)


def part2(nav_subsystem: List[str]) -> int:
    """Return the middle completion score for incomplete navigation subsystem lines."""
    scores = [
        completion_score(line) for line in nav_subsystem
        if not syntax_error_score(line)
    ]
    mid_idx = len(scores) // 2
    return sorted(scores)[mid_idx]


def syntax_error_score(subsystem_line: str) -> int:
    stack = []
    for symbol in subsystem_line:
        if symbol in PAIRS.keys():
            stack.append(symbol)
        elif PAIRS[stack[-1]] != symbol:
            return SYMBOLS[symbol]["syntax_score"]
        else:
            stack.pop()
    return 0


def completion_score(subsystem_line: str) -> int:
    score = 0
    stack = []
    for symbol in subsystem_line:
        if symbol in PAIRS.keys():
            stack.append(symbol)
        elif PAIRS[stack[-1]] == symbol:
            stack.pop()
        else:
            print(f"FOUND UNMATCHED CLOSER: {symbol}")
            return 0

    for opener in stack[::-1]:
        score *= 5
        closer = PAIRS[opener]
        score += SYMBOLS[closer]["completion_score"]

    return score


def main():
    try:
        input_file = argv[1]
        nav_subsystem = parse_input(input_file)
        print("PART 1:", part1(nav_subsystem))
        print("PART 2:", part2(nav_subsystem))
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()
