import re
from collections import defaultdict
from sys import argv
from typing import Dict

InsertionRule = Dict[str, str]


class PolymerFormula:
    def __init__(self, template: str, insertion_rules: InsertionRule):
        self.template = template
        self.polymer = self.count_pairs()
        self.insertion_rules = insertion_rules

    def count_pairs(self) -> Dict[str, int]:
        """Return counts of pairs of values in self.template"""
        counts = defaultdict(int)
        for i in range(1, len(self.template)):
            counts[self.template[i - 1: i + 1]] += 1
        return counts

    def step(self):
        self.apply_insertions()

    def apply_insertions(self):
        new_polymer = defaultdict(int)
        for pair, count in self.polymer.items():
            insert = self.insertion_rules[pair]
            new_pair1 = f"{pair[0]}{insert}"
            new_pair2 = f"{insert}{pair[1]}"
            new_polymer[new_pair1] += count
            new_polymer[new_pair2] += count
        self.polymer = new_polymer

    @property
    def counts(self) -> Dict[str, int]:
        individual_counts = defaultdict(int)
        for pair, count in self.polymer.items():
            individual_counts[pair[0]] += count
        individual_counts[self.template[-1]] += 1
        return individual_counts


def parse_input(filename: str) -> PolymerFormula:
    with open(filename, "r") as f_in:
        template = next(f_in).strip()
        _ = next(f_in)
        insertion_rules = dict([tuple(re.findall(r"[A-Z]+", line)) for line in f_in])
    return PolymerFormula(template, insertion_rules)


def part1(formula: PolymerFormula) -> int:
    """
    Return the difference between the most common
    and least common element after 10 steps.
    """
    return synthesize_polymer(formula, 10)


def part2(formula: PolymerFormula) -> int:
    """
    Return the difference between the most common
    and least common element after 40 steps.
    """
    return synthesize_polymer(formula, 40)


def synthesize_polymer(formula: PolymerFormula, num_steps: int) -> int:
    """
    Return the difference between the most common
    and least common element after num_steps steps.
    """
    for _ in range(num_steps):
        formula.step()
    sorted_counts = sorted(formula.counts.values())
    return sorted_counts[-1] - sorted_counts[0]


def main():
    try:
        input_file = argv[1]
        formula = parse_input(input_file)
        print(f"PART 1: {part1(formula)}")
        formula = parse_input(input_file)
        print(f"PART 2: {part2(formula)}")
    except IndexError:
        print("Enter path to data file!")


if __name__ == "__main__":
    main()
