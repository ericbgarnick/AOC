import re
from sys import argv
from typing import Dict, Tuple, List, Set, Optional

Update = List[Tuple[int, int]]
Specification = Dict[str, Update]


def parse_input(filename: str) -> Specification:
    specification = {}
    mask = ""
    for line in open(filename, "r"):
        line = line.strip()
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
        else:
            address, value = [int(d) for d in re.findall(r"\d+", line)]
            try:
                specification[mask].append((address, value))
            except KeyError:
                specification[mask] = [(address, value)]
    return specification


# PART 1
def initialize(specification: Specification) -> int:
    computer = {}
    for mask, updates in specification.items():
        apply_specification_1(computer, mask, updates)
    return sum(computer.values())


def apply_specification_1(computer: Dict[int, int], mask: str, updates: Update):
    mask_0 = int(re.sub(r"[^0]", "1", mask), 2)
    mask_1 = int(re.sub(r"[^1]", "0", mask), 2)
    for address, value in updates:
        computer[address] = value & mask_0 | mask_1


# PART 2
def version_2(specification: Specification) -> int:
    print(f"PROCESSING {len(specification)} SPECIFICATIONS")
    computer = {}
    num_processed = 0
    for mask, updates in specification.items():
        apply_specification_2(computer, mask, updates)
        num_processed += 1
        print("PROCESSED:", num_processed)
    return sum(computer.values())


def apply_specification_2(computer: Dict[int, int], mask: str, updates: Update):
    x_indexes = tuple(i for i, val in enumerate(mask) if val == "X")

    for address, value in updates:
        # Remove X's
        masked_address = address | int(re.sub(r"X", "0", mask), 2)
        for combo in combinations(x_indexes):
            address_list = list(bin(masked_address))[2:]  # drop 0b prefix
            padding = ["0" for _ in range(len(mask) - len(address_list))]
            address_list = padding + address_list
            for i in combo:
                address_list[i] = "1"
            for i in set(x_indexes) - set(combo):
                address_list[i] = "0"
            updated_address_bin = "".join(address_list)
            updated_address_dec = int(updated_address_bin, 2)

            computer[updated_address_dec] = value


def combinations(original: Tuple[int], result: Optional[Set] = None) -> Set[Tuple[int]]:
    result = result or {tuple(o for o in original), ()}
    if len(original) <= 1:
        return result
    for o in original:
        next_combo = tuple(sorted(set(original) - {o}))
        result.add(next_combo)
        result = combinations(next_combo, result)
    return result


if __name__ == "__main__":
    input_file = argv[1]
    spec = parse_input(input_file)
    print("PART 1:", initialize(spec))
    print("PART 2:", version_2(spec))

