import re
from sys import argv
from typing import Callable, Optional


def sum_lines(filename: str) -> int:
    return sum(evaluate(re.sub(r" ", "", line.strip())) for line in open(filename, "r"))


def evaluate(
        expression: str,
        operation: Optional[Callable] = None,
        total: Optional[int] = None,
) -> int:
    """Expression must contain only integers, parentheses and operators +,* (no whitespace)"""
    if not expression:
        return total

    next_symbol = expression[0]
    next_idx = 1

    if next_symbol == ")":
        pass
    elif next_symbol.isdecimal() and total is None:
        total = int(next_symbol)
    elif next_symbol in "+*":
        operation = int.__add__ if next_symbol == "+" else int.__mul__
    elif next_symbol.isdecimal():
        total = operation(total, int(next_symbol))
        operation = None
    elif next_symbol == "(":
        close = expression_end(expression)
        if operation and total is not None:
            total = operation(total, evaluate(expression[1:close]))
        else:
            total = evaluate(expression[1:close])
        next_idx = close

    return evaluate(expression[next_idx:], operation, total)


def expression_end(expression: str) -> int:
    """Return the index of the parenthesis that closes
    the first subexpression in expression"""
    idx = depth = 1  # first element of expression is ( for depth=1
    while depth:
        if expression[idx] == "(":
            depth += 1
        elif expression[idx] == ")":
            depth -= 1
        idx += 1
    return idx


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", sum_lines(input_file))
