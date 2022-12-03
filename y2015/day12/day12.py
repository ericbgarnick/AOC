import json
from sys import argv
from typing import Dict, List


def sum_nums(filename: str, skip_red: bool = False) -> int:
    content = json.load(open(filename, "r"))
    return sum_object(content, skip_red)


def sum_object(json_object: Dict, skip_red: bool) -> int:
    object_total = 0
    for k, v in json_object.items():
        if skip_red and v == "red":
            return 0
        elif isinstance(v, int):
            object_total += v
        elif isinstance(v, list):
            object_total += sum_list(v, skip_red)
        elif isinstance(v, dict):
            object_total += sum_object(v, skip_red)
    return object_total


def sum_list(json_list: List, skip_red: bool) -> int:
    list_total = 0
    for el in json_list:
        if isinstance(el, int):
            list_total += el
        elif isinstance(el, list):
            list_total += sum_list(el, skip_red)
        elif isinstance(el, dict):
            list_total += sum_object(el, skip_red)
    return list_total


if __name__ == "__main__":
    try:
        input_file = argv[1]
        print("PART 1:", sum_nums(input_file))
        print("PART 2:", sum_nums(input_file, skip_red=True))
    except IndexError:
        print("Enter path to data file!")
