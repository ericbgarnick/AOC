import re
from sys import argv
from typing import List, Tuple


InsertionRule = List[Tuple[str, str]]


class PolymerFormula:
    def __init__(self, template: str, insertion_rules: InsertionRule):
        self.template = template
        self.insertion_rules = insertion_rules


def parse_input(filename: str) -> PolymerFormula:
    with open(filename, "r") as f_in:
        template = next(f_in).strip()
        _ = next(f_in)
        insertion_rules = [tuple(re.findall(r"[A-Z]+", line)) for line in f_in]
    return PolymerFormula(template, insertion_rules)


def part1(formula: PolymerFormula) -> int:
    """
    """

    return -1


def part2(formula: PolymerFormula) -> int:
    """
    """
    return -1


def main():
    try:
        input_file = argv[1]
        formula = parse_input(input_file)
        print(f"PART 1: {part1(formula)}")
        print(f"PART 2: {part2(formula)}")
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()
