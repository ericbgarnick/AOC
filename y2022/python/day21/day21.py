"""
Part 1 answer: 121868120894282
Part 2 answer: 3582317956029
"""
import re

from y2022.python.shared import get_data_file_path

OPERATIONS = {
    "+": int.__add__,
    "-": int.__sub__,
    "*": int.__mul__,
    "/": lambda a, b: a // b,
}
INVERSE = {
    "+": "-",
    "-": "+",
    "*": "/",
    "/": "*",
}


class Monkey:
    def __init__(
        self,
        name: str,
        value: int | None,
        inputs: list[str] | None = None,
        operation: str | None = None,
    ):
        self.name = name
        self.value = value
        self.inputs = inputs
        self.operation = operation

    def yell(self, directory: dict[str, "Monkey"]) -> int:
        if self.value is None and self.operation is not None:
            input_values = [directory[i].yell(directory) for i in self.inputs]
            self.value = OPERATIONS[self.operation](*input_values)
        if self.value is not None:
            return self.value
        raise ValueError("Monkey has no value yet")

    def is_human_ancestor(self, directory: dict[str, "Monkey"]) -> bool:
        if self.name == "humn":
            return True
        if self.inputs is None:
            return False
        return any([directory[i].is_human_ancestor(directory) for i in self.inputs])


def main():
    monkey_directory = {}
    with open(get_data_file_path(__file__.split("/")[-1], sample=False), "r") as f_in:
        for line in f_in:
            monkey = parse_monkey(line)
            monkey_directory[monkey.name] = monkey
    root = monkey_directory["root"]

    # PART 1
    print("PART 1:", root.yell(monkey_directory))

    # PART 2
    ancestor = next(
        name
        for name in root.inputs
        if monkey_directory[name].is_human_ancestor(monkey_directory)
    )
    non_ancestor = next(
        name
        for name in root.inputs
        if not monkey_directory[name].is_human_ancestor(monkey_directory)
    )
    goal = monkey_directory[non_ancestor].yell(monkey_directory)
    print("PART 2:", calc_value(goal, monkey_directory[ancestor], monkey_directory))


def parse_monkey(monkey_spec: str) -> Monkey:
    name, spec = monkey_spec.split(":")
    value_search = re.search(r"\d+", spec)
    if value_search is not None:
        value = int(value_search.group())
        return Monkey(name, value)
    else:
        input_a, operation, input_b = spec.strip().split()
        return Monkey(name, None, [input_a, input_b], operation)


def calc_value(goal: int, cur_monkey: Monkey, directory: dict[str, Monkey]) -> int:
    if cur_monkey.name == "humn":
        return goal
    a, b = cur_monkey.inputs
    monkey_a = directory[a]
    monkey_b = directory[b]
    inverse_op = INVERSE[cur_monkey.operation]
    if monkey_a.is_human_ancestor(directory):
        new_goal = OPERATIONS[inverse_op](goal, monkey_b.yell(directory))
        return calc_value(new_goal, monkey_a, directory)
    else:
        if inverse_op in {"-", "/"}:
            new_goal = OPERATIONS[inverse_op](goal, monkey_a.yell(directory))
        else:
            new_goal = OPERATIONS[INVERSE[inverse_op]](monkey_a.yell(directory), goal)
        return calc_value(new_goal, monkey_b, directory)


if __name__ == "__main__":
    main()
