from sys import argv
from typing import Callable, List


def sum_lines(filename: str) -> int:
    total = 0
    for line in open(filename, "r"):
        symbols = list(filter(lambda x: x != " ", line.strip()))
        total += int(evaluate(symbols)[0])
    return total


def evaluate(expression: List[str]) -> List[str]:
    """Expression must contain only integers, parentheses and operators +,* (no whitespace)"""
    expression = resolve_parentheses(expression)
    expression = resolve_calculation(expression, "+", int.__add__)
    expression = resolve_calculation(expression, "*", int.__mul__)
    return expression


def resolve_parentheses(expression: List[str]) -> List[str]:
    for i in range(len(expression)):
        if expression[i] == "(":
            end = expression_end(expression[i:], i)
            subexpression = evaluate(expression[i + 1: end - 1])
            return evaluate(expression[:i] + subexpression + expression[end:])
    return expression


def resolve_calculation(expression: List[str], symbol: str, operation: Callable) -> List[str]:
    for i in range(len(expression)):
        if expression[i] == symbol:
            total = operation(int(expression[i - 1]), int(expression[i + 1]))
            return evaluate(expression[:i - 1] + [str(total)] + expression[i + 2:])
    return expression


def expression_end(expression: List[str], start: int) -> int:
    """Return the index of the parenthesis that closes
    the first subexpression in expression"""
    idx = depth = 1  # first element of expression is ( for depth=1
    while depth:
        if expression[idx] == "(":
            depth += 1
        elif expression[idx] == ")":
            depth -= 1
        idx += 1
    return idx + start


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 2:", sum_lines(input_file))
