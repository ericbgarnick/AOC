from sys import argv
from typing import List, Tuple


def read_license(license_data: List[int], part_num: int):
    if part_num == 1:
        count, end = simple_recurse(license_data)
        print("COUNT:", count)
    elif part_num == 2:
        count, end = complex_recurse(license_data)
        print("COUNT:", count)


def simple_recurse(data: List[int], end: int=-1) -> Tuple[int, int]:
    num_children, meta_len, *body = data[end + 1:]
    end += 2

    count = 0
    for _ in range(num_children):
        sub_count, end = simple_recurse(data, end)
        count += sub_count

    start = end + 1

    count += sum(data[start: start + meta_len])
    end = end + meta_len

    return count, end


def complex_recurse(data: List[int], end: int=-1) -> Tuple[int, int]:
    num_children, meta_len, *body = data[end + 1:]
    end += 2

    child_totals = []
    for _ in range(num_children):
        sub_count, end = complex_recurse(data, end)
        child_totals.append(sub_count)

    start = end + 1

    children = data[start: start + meta_len]

    if not num_children:
        count = sum(children)
    else:
        children_to_add = [child_num - 1 for child_num in children
                           if child_num and child_num <= num_children]
        count = sum(child_totals[ch] for ch in children_to_add)

    end += meta_len

    return count, end


if __name__ == '__main__':
    data_file = argv[1]
    data_lines = [int(n) for n in open(data_file, 'r').read().strip().split()]
    part = int(argv[2])
    kwargs = {'license_data': data_lines, 'part_num': part}

    read_license(**kwargs)

