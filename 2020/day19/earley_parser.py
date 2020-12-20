import re
from sys import argv
from typing import List, Dict, Tuple, Optional

Grammar = Dict[str, List[str]]

TERMINALS = "ab"


def read_input(filename: str) -> Tuple[Grammar, List[str]]:
    rules, messages = open(filename, "r").read().split("\n\n")
    return build_grammar(rules), messages.split()


def build_grammar(raw_rules: str) -> Grammar:
    grammar = {}
    for line in raw_rules.split("\n"):
        input_val, output = line.split(": ")
        grammar[input_val] = [
            ",".join(re.findall(r"\d+|[ab]", output_part))
            for output_part in output.split("|")
        ]
    return grammar


def earley_parse(message: str, grammar: Dict):
    msg_len = len(message)

    chart = [[] for _ in range(msg_len + 1)]
    add_to_chart({"$": ".0"}, (0, 0), chart[0])

    for i in range(msg_len):
        for rule, indices in chart[i]:
            initial = re.search(r"\.\d+", list(rule.values())[0])
            if initial and grammar[initial.group()] not in TERMINALS:
                predictor(grammar, rule, indices, chart)


def predictor(grammar: Dict, rule: Dict, indices: Tuple, chart: List):
    next_symbol = re.search(r"\.\d+", list(rule.values())[0])
    for production in grammar[next_symbol]:



def add_to_chart(rule: Dict, indices: Tuple, state_list: List):
    if (rule, indices)not in state_list:
        state_list.append((rule, indices))


def get_initial_symbol(rule: Dict) -> Optional[str]:
    maybe_symbol = re.search(r"\.\d+", list(rule.values())[0])


if __name__ == "__main__":
    input_file = argv[1]
    grammar_rules, message_list = read_input(input_file)
    print(earley_parse(message_list[0], grammar_rules))
