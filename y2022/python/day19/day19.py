"""
Part 1 answer:
Part 2 answer:
"""
import re
from collections import defaultdict
from enum import Enum

from y2022.python.shared import get_data_file_path


class MaterialType(Enum):
    geode = "geode"
    obsidian = "obsidian"
    clay = "clay"
    ore = "ore"


class RobotFactory:
    def __init__(self, raw_blueprint: str):
        self.blueprint = self.parse_blueprint(raw_blueprint)

    def __str__(self) -> str:
        return "\n".join(f"{k}: {v}" for k, v in self.blueprint.items())

    @staticmethod
    def parse_blueprint(
        raw_blueprint: str,
    ) -> dict[MaterialType, dict[MaterialType, int]]:
        robot_specs = re.findall(r"Each.+?\.", raw_blueprint)
        blueprint = {}
        for spec in robot_specs:
            robot_cost = {}
            robot_type = MaterialType[spec.split()[1]]
            raw_cost_factors = re.findall(r"\d+ [a-z]+", spec)
            for cost_factor in raw_cost_factors:
                amount_str, material_name = cost_factor.split()
                robot_cost[MaterialType[material_name]] = int(amount_str)
            blueprint[robot_type] = robot_cost
        return blueprint

    def robot_is_affordable(
        self, robot_type: MaterialType, stockpile: dict[MaterialType, int]
    ) -> bool:
        """Return True if stockpile has enough resources to build robot_type."""
        cost = self.blueprint[robot_type]
        for material, amount in cost.items():
            if stockpile.get(material, 0) < amount:
                return False
        return True


def main():
    with open(get_data_file_path(__file__.split("/")[-1], sample=True), "r") as f_in:
        for line in f_in:
            rf = RobotFactory(line)
            # Create initial ore robot
            # run minutes:
            # - check for materials available to make a robot
            # - queue creation of 0 or 1 of each robot possible to make
            # - collect materials for all robots available
            # - add queued robots to available collectors
            print(rf)
            print("")
    workforce = defaultdict(int)
    workforce[MaterialType.ore] = 1
    stockpile = defaultdict(int)
    result = run_simulation(rf, workforce, stockpile, 24)
    print("PART 1:", result)


def run_simulation(
    robot_factory: RobotFactory,
    workforce: dict[MaterialType, int],
    stockpile: dict[MaterialType, int],
    time_left: int,
) -> int:
    if not time_left:
        result = stockpile[MaterialType.geode]
        if result > 8:
            print("RESULT:", result)
        return result
    build_options = get_build_options(robot_factory, stockpile)
    for material_type, robot_count in workforce.items():
        stockpile[material_type] += robot_count
    sim_results = []
    # if MaterialType.geode in build_options:
    #     breakpoint()
    for option in build_options:
        new_workforce = clone_dict(workforce)
        new_workforce[option] += 1
        new_stockpile = clone_dict(stockpile)
        for material_type, amount in robot_factory.blueprint[option].items():
            new_stockpile[material_type] -= amount
        sim_results.append(
            run_simulation(robot_factory, new_workforce, new_stockpile, time_left - 1)
        )
    sim_results.append(
        run_simulation(
            robot_factory, clone_dict(workforce), clone_dict(stockpile), time_left - 1
        )
    )
    return max(sim_results)


def clone_dict(d: dict) -> dict:
    new_d = defaultdict(int)
    for k, v in d.items():
        new_d[k] = v
    return new_d


def get_build_options(
    robot_factory: RobotFactory, stockpile: dict[MaterialType, int]
) -> list[MaterialType]:
    return [t for t in MaterialType if robot_factory.robot_is_affordable(t, stockpile)]


if __name__ == "__main__":
    main()
