import math
import sys
from typing import List, Dict, Tuple


ORE_COLLECTED = 1000000000000
OPERATIONS = {'add': int.__add__, 'sub': int.__sub__}
OPERATION_LOOP = {'add': 'sub', 'sub': 'add'}

COMPARISONS = {'gt': int.__gt__, 'lt': int.__lt__}
COMPARISON_LOOP = {'gt': 'lt', 'lt': 'gt'}


class Nanofactory:
    def __init__(self, reactions: List[str], fuel_needed: int = 1):
        # {
        #     <resource>: {
        #         "num": <int>,
        #         "cost": [
        #             {
        #                 "resource": <resource>,
        #                 "num": <int>
        #             }
        #         ]
        #     }
        # }
        self._reactions = self._parse_reactions(reactions)
        # {<resource>: <int>}
        self._need = {"FUEL": fuel_needed}
        # {<resource>: <int>}
        self._extra = {}

    def fuel_cost(self) -> int:
        """Return the minimum number of ORE needed to produce 1 FUEL"""
        while set(self._need.keys()) != {"ORE"}:
            needed = {r for r in self._need.keys() if r != "ORE"}
            resource_to_buy = needed.pop()
            self._make_purchase(resource_to_buy, self._need[resource_to_buy])
        return self._need["ORE"]

    def _parse_reactions(self, raw_reactions: List[str]) -> Dict:
        reactions = {}
        for row in raw_reactions:
            raw_cost, raw_resource = [val.strip() for val in row.split('=>')]
            cost_data = self._parse_cost(raw_cost)
            resource_name, resource_num = self._parse_resource(raw_resource)
            reactions[resource_name] = {'num': resource_num, 'cost': cost_data}
        return reactions

    @staticmethod
    def _parse_cost(raw_cost: str) -> List[Dict]:
        inputs = [c.strip().split() for c in raw_cost.split(',')]
        return [{'resource': r, 'num': int(n)} for n, r in inputs]

    @staticmethod
    def _parse_resource(raw_resource: str) -> Tuple[str, int]:
        n, r = raw_resource.strip().split()
        return r, int(n)

    def _make_purchase(self, resource: str, num_needed: int):
        resource_data = self._reactions[resource]
        num_available, cost_data = resource_data["num"], resource_data["cost"]
        purchase_multiple = self._log_purchase(resource, num_needed, num_available)
        self._log_cost(cost_data, purchase_multiple)

    def _log_purchase(self, resource: str, num_needed: int,
                      num_available: int) -> int:
        purchase_multiple = math.ceil(num_needed / num_available)
        num_bought = num_available * purchase_multiple
        extra = num_bought - num_needed
        try:
            self._extra[resource] += extra
        except KeyError:
            self._extra[resource] = extra
        self._need.pop(resource)
        return purchase_multiple

    def _log_cost(self, cost_data: List[Dict], purchase_multiple: int):
        for cost_item in cost_data:
            r = cost_item["resource"]
            n = cost_item["num"] * purchase_multiple
            have = self._extra.get(r, 0)
            n -= have
            try:
                self._need[r] += n
            except KeyError:
                self._need[r] = n
            try:
                self._extra[r] -= have
            except KeyError:
                self._extra[r] = have


def fuel_available() -> int:
    """Make a guess as the square root of ORE_COLLECTED, then alternatively
    increase and decrease the guess by decreasing amounts until the largest
    value below ORE_COLLECTED is found."""
    guess = int(ORE_COLLECTED ** .5)
    factory = Nanofactory(data, guess)
    needed = factory.fuel_cost()

    increase = 0
    factor = 100000
    reduction = 10

    operation_name = 'add'
    comparison_name = 'lt'
    comparison = COMPARISONS[comparison_name]
    operation = OPERATIONS[operation_name]

    while factor:
        while comparison(needed, ORE_COLLECTED):
            increase = operation(increase, factor)
            factory = Nanofactory(data, int(guess + increase))
            needed = factory.fuel_cost()

        factor = factor // reduction

        comparison_name = COMPARISON_LOOP[comparison_name]
        comparison = COMPARISONS[comparison_name]

        operation_name = OPERATION_LOOP[operation_name]
        operation = OPERATIONS[operation_name]

    return guess + increase


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [line.strip() for line in open(data_file, 'r').readlines()]

    nanofactory = Nanofactory(data)
    ore_needed = nanofactory.fuel_cost()

    print(f"PART 1:\nNeed {ore_needed} ORE")
    print(f"PART 2:\nCan create {fuel_available()} FUEL")
