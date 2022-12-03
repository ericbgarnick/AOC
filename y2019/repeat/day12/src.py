import argparse
import re
from collections import defaultdict
from typing import List, Dict, Optional, Tuple

STEPS = 1000


class Moon:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0

    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}, Z: {self.z}"

    @property
    def potential_energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self) -> int:
        return abs(self.x_vel) + abs(self.y_vel) + abs(self.z_vel)

    @property
    def total_energy(self) -> int:
        return self.potential_energy * self.kinetic_energy

    def get_coords(self, dimension: Optional[str] = None):
        if dimension:
            return getattr(self, dimension), getattr(self, f"{dimension}_vel")
        else:
            return self.x, self.y, self.z, self.x_vel, self.y_vel, self.z_vel

    def apply_velocity(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.z += self.z_vel


def solve(moons_data: List[str], day_num: int) -> int:
    if day_num == 1:
        moons = [create_moon(row) for row in moons_data]
        for _ in range(STEPS):
            for i in range(len(moons)):
                for j in range(i + 1, len(moons)):
                    moon1 = moons[i]
                    moon2 = moons[j]
                    apply_gravity(moon1, moon2)
            for moon in moons:
                moon.apply_velocity()
        return sum([moon.total_energy for moon in moons])
    else:
        periods = find_periods(moons_data)
        return lcm(list(periods.values()))


def find_periods(moons_data: List[str]) -> Dict:
    moons = [create_moon(row) for row in moons_data]
    history = create_moon_history_point(moons)
    step = 0
    while True:
        step += 1
        for i in range(len(moons)):
            for j in range(i + 1, len(moons)):
                moon1 = moons[i]
                moon2 = moons[j]
                apply_gravity(moon1, moon2)
        for i, moon in enumerate(moons):
            moon.apply_velocity()
        update_history_for_dimensions(history, moons, step)
        if all(v["period"] for v in history.values()):
            return {k: v["period"] for k, v in history.items()}


def update_history_for_dimensions(history: Dict, moons: List[Moon], step: int):
    """
    If moons are at new coords, record step for these coords for each dimension.
    Otherwise, calculate and record period.
    """
    for dimension in "xyz":
        coords = create_coords(moons, dimension)
        if coords in history[dimension]["coords"] and history[dimension]["period"] is None:
            history[dimension]["period"] = step - history[dimension]["coords"][coords]
        else:
            history[dimension]["coords"][coords] = step


def create_moon_history_point(moons: List[Moon]) -> Dict:
    return {
        dimension: {
            "coords": {create_coords(moons, dimension): 0},
            "period": None,
            "first": None,
        } for dimension in "xyz"
    }


def create_coords(moons: List[Moon], dimension: str) -> Tuple:
    return tuple(moon.get_coords(dimension) for moon in moons)


def lcm(nums: List[int]) -> int:
    combined_factors = defaultdict(int)
    for num in nums:
        factors = get_factors(num)
        for f, count in factors.items():
            combined_factors[f] = max(combined_factors[f], count)
    result = 1
    for f, count in combined_factors.items():
        result *= f ** count
    return result


def get_factors(num: int) -> Dict[int, int]:
    factors = defaultdict(int)
    f = 2
    while f <= int(num ** 0.5):
        div, mod = divmod(num, f)
        if mod == 0:
            factors[f] += 1
            num = div
            f = 2
        else:
            f += 1
    factors[num] += 1
    return factors


def apply_gravity(moon1: Moon, moon2: Moon):
    for axis in "xyz":
        pos1, pos2 = getattr(moon1, axis), getattr(moon2, axis)
        mag1, mag2 = getattr(moon1, f"{axis}_vel"), getattr(moon2, f"{axis}_vel")
        if pos1 > pos2:
            setattr(moon1, f"{axis}_vel", mag1 - 1)
            setattr(moon2, f"{axis}_vel", mag2 + 1)
        elif pos1 < pos2:
            setattr(moon1, f"{axis}_vel", mag1 + 1)
            setattr(moon2, f"{axis}_vel", mag2 - 1)
        else:
            pass  # same magnitudes, no change


def create_moon(moon_data: str) -> Moon:
    x, y, z = re.findall(r"-?\d+", moon_data)
    return Moon(int(x), int(y), int(z))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    data = [row.strip() for row in open(data_file, "r")]

    print(f"PART 1: {solve(data, day_num=1)}")
    print(f"PART 2: {solve(data, day_num=2)}")


if __name__ == "__main__":
    main()
