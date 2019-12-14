import re
import sys
from itertools import combinations
from typing import Tuple, List, Optional

ThreeDPos = Tuple[int, int, int]
RUNTIME = 1000


class Moon:
    def __init__(self, x_pos: int, y_pos: int, z_poz: int):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._z_pos = z_poz
        self._x_vel = 0
        self._y_vel = 0
        self._z_vel = 0

    @property
    def coords(self) -> ThreeDPos:
        return self._x_pos, self._y_pos, self._z_pos

    @property
    def total_energy(self) -> int:
        return self._potential * self._kinetic

    @property
    def _potential(self) -> int:
        return abs(self._x_pos) + abs(self._y_pos) + abs(self._z_pos)

    @property
    def _kinetic(self) -> int:
        return abs(self._x_vel) + abs(self._y_vel) + abs(self._z_vel)

    def apply_gravity(self, other: 'Moon'):
        other_x, other_y, other_z = other.coords
        self._adjust_cooord(self._x_pos, other_x, '_x_vel')
        self._adjust_cooord(self._y_pos, other_y, '_y_vel')
        self._adjust_cooord(self._z_pos, other_z, '_z_vel')

    def apply_velocity(self):
        self._x_pos += self._x_vel
        self._y_pos += self._y_vel
        self._z_pos += self._z_vel

    def _adjust_cooord(self, my_pos: int, other_pos: int, vel_name: str):
        if other_pos > my_pos:
            self.__dict__[vel_name] += 1
        elif other_pos < my_pos:
            self.__dict__[vel_name] -= 1

    def __str__(self) -> str:
        pos_str = f"pos=<x={self._x_pos}, y={self._y_pos}, z={self._z_pos}>"
        vel_str = f"vel=<x={self._x_vel}, y={self._y_vel}, z={self._z_vel}>"
        return f"{pos_str}, {vel_str}"

    __repr__ = __str__


def day12_part1(puzzle_data: List[str], num_secs: Optional[int]) -> int:
    global RUNTIME
    num_secs = num_secs or RUNTIME
    moon_coords = _parse_coords(puzzle_data)
    moons = [Moon(*coords) for coords in moon_coords]
    idx_pairs = combinations(range(len(moons)), 2)
    for _ in range(num_secs):
        _update_gravity(moons, idx_pairs)
        _update_velocity(moons)
    return sum(moon.total_energy for moon in moons)


def _parse_coords(coord_data: List[str]) -> List[ThreeDPos]:
    result = []
    for row in coord_data:
        result.append(tuple(int(pos) for pos in re.findall(r'-?\d+', row)))
    return result


def _update_gravity(moons: List[Moon], idx_pairs: List[Tuple[int, int]]):
    for pair in idx_pairs:
        moon1, moon2 = moons[pair[0]], moons[pair[1]]
        moon1.apply_gravity(moon2)
        moon2.apply_gravity(moon1)


def _update_velocity(moons: List[Moon]):
    for moon in moons:
        moon.apply_velocity()


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [line.strip() for line in open(data_file, 'r').readlines()]
    if len(sys.argv) > 2:
        runtime = int(sys.argv[2])
    else:
        runtime = None
    print(f"PART 1:\n{day12_part1(data, runtime)}")
    # print(f"PART 2:\n{day12_part2(data)}")

