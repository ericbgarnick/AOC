"""
Part 1 answer: 66802
Part 2 answer: 21800916620 (with help from Reddit)
"""
import re
from collections import deque
from typing import Callable

from y2022.python.shared import get_data_file_path

PART_1_NUM_ROUNDS = 20
PART_2_NUM_ROUNDS = 10_000


class Monkey:
    def __init__(
        self,
        items: list[int],
        inspect_op: Callable,
        inspect_val: int,
        test_val: int,
        test_t_dest: int,
        test_f_dest: int,
    ):
        self.items = deque(items)
        self.inspect_op = inspect_op
        self.inspect_val = inspect_val
        self.test_val = test_val
        self.test_t_dest = test_t_dest
        self.test_f_dest = test_f_dest
        self.relief_factor = 1
        self.inspections = 0

    def __str__(self):
        return f"Monkey: {self.test_val}"

    def misbehave(self, monkeys: list['Monkey'], custom_relief: bool):
        while len(self.items):
            self._inspect_item(custom_relief)
            self._test_item(monkeys)

    def _inspect_item(self, custom_relief: bool):
        try:
            item = self.items[0]
            self.inspections += 1
            item = self.inspect_op(item, self.inspect_val)
            if custom_relief:
                item %= self.relief_factor
            else:
                item //= 3
            self.items[0] = item
        except IndexError:
            pass

    def _test_item(self, monkeys: list['Monkey']):
        try:
            item = self.items.popleft()
            if item % self.test_val == 0:
                monkeys[self.test_t_dest].receive(item)
            else:
                monkeys[self.test_f_dest].receive(item)
        except IndexError:
            pass

    def receive(self, item: int):
        self.items.append(item)


def create_monkey(characteristics: list[str]) -> Monkey:
    items = [int(item) for item in re.findall(r"\d+", characteristics[1])]
    inspect_op, inspect_val = characteristics[2].split()[-2:]
    try:
        inspect_val = int(inspect_val)
        if inspect_op == "+":
            inspect_op = int.__add__
        else:
            inspect_op = int.__mul__
    except ValueError:
        inspect_val = 2
        inspect_op = int.__pow__
    test_val = int(characteristics[3].split()[-1])
    test_t_dest = int(characteristics[4].split()[-1])
    test_f_dest = int(characteristics[5].split()[-1])
    return Monkey(items, inspect_op, inspect_val, test_val, test_t_dest, test_f_dest)


def main():
    monkeys_rd_1 = []
    monkeys_rd_2 = []
    relief_factor = 1
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        monkey_characteristics = []
        for line in f_in:
            if line == "\n":
                monkeys_rd_1.append(create_monkey(monkey_characteristics))
                monkeys_rd_2.append(create_monkey(monkey_characteristics))
                relief_factor *= monkeys_rd_1[-1].test_val
                monkey_characteristics = []
            else:
                monkey_characteristics.append(line.strip())
        monkeys_rd_1.append(create_monkey(monkey_characteristics))
        monkeys_rd_2.append(create_monkey(monkey_characteristics))
        relief_factor *= monkeys_rd_1[-1].test_val
    for monkey in monkeys_rd_1:
        monkey.relief_factor = relief_factor
    for monkey in monkeys_rd_2:
        monkey.relief_factor = relief_factor

    # PART 1
    for _ in range(PART_1_NUM_ROUNDS):
        for i, monkey in enumerate(monkeys_rd_1):
            monkey.misbehave(monkeys_rd_1, custom_relief=False)
    # PART 2
    for _ in range(PART_2_NUM_ROUNDS):
        for i, monkey in enumerate(monkeys_rd_2):
            monkey.misbehave(monkeys_rd_2, custom_relief=True)
    print("PART 1:", get_monkey_business_level(monkeys_rd_1))
    print("PART 2:", get_monkey_business_level(monkeys_rd_2))


def get_monkey_business_level(monkeys: list[Monkey]) -> int:
    inspections = sorted([m.inspections for m in monkeys], reverse=True)
    return inspections[0] * inspections[1]


if __name__ == "__main__":
    main()
