import re
from sys import argv
from typing import Dict, Tuple, List, Set

RulesType = Dict[str, List[str]]
ChartType = List[List[Set]]
VOCABULARY = "ab"


def read_input(filename: str) -> Tuple[Dict, List[str]]:
    raw_rules, raw_messages = open(filename, "r").read().split("\n\n")
    grammar = create_grammar(raw_rules)
    rev_grammar = create_rev_grammar(grammar)
    return rev_grammar, raw_messages.split()


def create_grammar(raw_rules: str) -> RulesType:
    rules = {}
    for line in raw_rules.split("\n"):
        input_val, output = line.split(": ")
        rules[input_val] = [
            ",".join(re.findall(r"\d+|[ab]", output_part))
            for output_part in output.split("|")
        ]
    return rules


def create_rev_grammar(grammar: Dict) -> Dict[str, Set[str]]:
    rev_grammar = {}
    for lhs, rhs_s in grammar.items():
        for rhs in rhs_s:
            try:
                rev_grammar[rhs].add(lhs)
            except KeyError:
                rev_grammar[rhs] = {lhs}
    return rev_grammar


def cyk(message: str, rev_grammar: Dict[str, Set[str]]) -> bool:
    n = len(message)
    chart = [[set() for _ in range(n + 1)] for _ in message]  # type: ChartType

    for i in range(n):
        letter = message[i]
        chart[i][i + 1] = rev_grammar[letter]

    for j in range(2, n + 1):
        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for b in chart[i][k]:
                    for c in chart[k][j]:
                        a = rev_grammar.get(",".join([b, c]))
                        if a:
                            chart[i][j] |= a

    return "0" in chart[0][n]


if __name__ == "__main__":
    input_file = argv[1]
    filepath1, ext = input_file.split(".")
    # PART 1
    input_file_1 = filepath1 + "_1." + ext
    rg1, msgs = read_input(input_file_1)
    print("PART 1:", sum(int(cyk(msg, rg1)) for msg in msgs))
    # PART 2
    input_file_2 = filepath1 + "_2." + ext
    rg2, msgs = read_input(input_file_2)
    print("PART 2:", sum(int(cyk(msg, rg2)) for msg in msgs))
