import argparse
import re
from typing import List


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
        return -1


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

