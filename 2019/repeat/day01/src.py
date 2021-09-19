"""
Defaults to using data_test.txt for input data.
Use flag --live-run to use 'real' data.
"""
import argparse
from typing import List


def calculate_total_fuel(modules: List[str], day_num: int) -> int:
    calculation = (
        calculate_fuel_for_module_simple if day_num == 1
        else calculate_fuel_for_module_with_fuel
    )
    return sum(calculation(int(module_mass)) for module_mass in modules)


def calculate_fuel_for_module_simple(module_mass: int) -> int:
    return module_mass // 3 - 2


def calculate_fuel_for_module_with_fuel(mass: int, fuel: int = 0) -> int:
    """Recursively calculate fuel for fuel until additional fuel is 0"""
    fuel_for_mass = max(0, mass // 3 - 2)
    if fuel_for_mass:
        fuel += calculate_fuel_for_module_with_fuel(fuel_for_mass, fuel_for_mass)
    return fuel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-run", action="store_true")
    args = parser.parse_args()
    data_file = "data.txt" if args.live_run else "data_test.txt"

    with open(data_file, "r") as f_in:
        data = f_in.readlines()

    print(f"PART 1: {calculate_total_fuel(data, day_num=1)}")
    print(f"PART 2: {calculate_total_fuel(data, day_num=2)}")


if __name__ == "__main__":
    main()
