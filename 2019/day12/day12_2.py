import re
import sys
from itertools import combinations
from typing import List, Tuple


class OneDObject:
    def __init__(self, pos: int):
        self.pos = pos
        self.vel = 0

    @property
    def data(self) -> Tuple[int, int]:
        return self.pos, self.vel

    def apply_gravity(self, other: 'OneDObject'):
        if other.pos > self.pos:
            self.vel += 1
        elif other.pos < self.pos:
            self.vel -= 1

    def apply_velocity(self):
        self.pos += self.vel


def find_repeat_time(coords: List[int]) -> Tuple[int, int]:
    """Return repeat_offset, repeat_span"""
    objects = [OneDObject(p) for p in coords]
    idx_pairs = list(combinations(range(len(objects)), 2))
    cur_time = 0
    cur_data = tuple(o.data for o in objects)
    data_for_time = {cur_data: cur_time}
    while True:
        for pair in idx_pairs:
            obj1, obj2 = objects[pair[0]], objects[pair[1]]
            obj1.apply_gravity(obj2)
            obj2.apply_gravity(obj1)
        for obj in objects:
            obj.apply_velocity()
        cur_data = tuple(o.data for o in objects)
        cur_time += 1
        try:
            earlier_time = data_for_time[cur_data]
            repeat_span = cur_time - earlier_time
            repeat_offset = earlier_time
            return repeat_offset, repeat_span
        except KeyError:
            data_for_time[cur_data] = cur_time


def lcm(nums: List[int]) -> int:
    factors = [get_factors(n) for n in nums]
    unique_factors = set()
    for f_list in factors:
        unique_factors |= set(f_list)
    to_keep = []
    for f in unique_factors:
        max_count = 0
        for f_list in factors:
            max_count = max(max_count, f_list.count(f))
        to_keep.append(f ** max_count)
    total = 1
    for kept in to_keep:
        total *= kept
    return total


def get_factors(n: int) -> List[int]:
    factors = []
    while n > 1:
        cand = 2
        div, mod = divmod(n, cand)
        while mod:
            cand += 1
            div, mod = divmod(n, cand)
        factors.append(cand)
        n = div
    return factors


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [line.strip() for line in open(data_file, 'r').readlines()]
    input_coords = [tuple(int(c) for c in re.findall(r'-?\d+', line)) for line in data]
    xs = [t[0] for t in input_coords]
    ys = [t[1] for t in input_coords]
    zs = [t[2] for t in input_coords]
    print("X vals:", xs)
    print("y vals:", ys)
    print("z vals:", zs)
    offset_x, span_x = find_repeat_time(xs)
    print(f"X repeats from offset {offset_x} after {span_x} ticks")

    offset_y, span_y = find_repeat_time(ys)
    print(f"Y repeats from offset {offset_y} after {span_y} ticks")

    offset_z, span_z = find_repeat_time(zs)
    print(f"Z repeats from offset {offset_z} after {span_z} ticks")

    test = [span_x, span_y, span_z]
    print(f"LCM of {test}", lcm(test))
