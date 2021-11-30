import re
from sys import argv
from typing import List, Dict, Tuple

Rules = Dict[str, List[str]]

MESSAGE_IDX = 0


def parse_input(filename: str) -> Tuple[Rules, List[str]]:
    rules, messages = open(filename, "r").read().split("\n\n")
    return parse_rules(rules), messages.split()


def parse_rules(raw_rules: str) -> Rules:
    rules = {}
    for line in raw_rules.split("\n"):
        input_val, output = line.split(": ")
        rules[input_val] = [
            ",".join(re.findall(r"\d+|[ab]", output_part))
            for output_part in output.split("|")
        ]
    return rules


def parse_message(message: str, rules: Rules, node: str) -> bool:
    """Return True parse succeeded, otherwise return False."""
    global MESSAGE_IDX
    cur_idx = MESSAGE_IDX
    success = False
    if MESSAGE_IDX < len(message):
        for option in rules[node]:
            if option in "ab":
                if message[MESSAGE_IDX] == option:
                    MESSAGE_IDX += 1
                    success = True
            else:
                for symbol in option.split(","):
                    success = parse_message(message, rules, symbol)
                    if not success:
                        MESSAGE_IDX = cur_idx
                        break
            if success:
                return True
    return success


if __name__ == "__main__":
    input_file = argv[1]
    rule_dict, msg_list = parse_input(input_file)
    match_count = 0
    for msg in msg_list:
        MESSAGE_IDX = 0
        good_msg = parse_message(msg, rule_dict, "0") and MESSAGE_IDX == len(msg)
        match_count += int(good_msg)
    print("PART 1:", match_count)
