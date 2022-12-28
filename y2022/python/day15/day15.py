"""
Part 1 answer: 4827924
Part 2 answer: 12977110973564
"""
import re
from bisect import insort
from typing import Tuple

from y2022.python.shared import get_data_file_path

"""
PART 1
For each sensor
    - determine its sight range and if it can see the target row
    - compile the set of visible points (x-values) in the target row
    - sum visible points in target row minus number of beacons in target row
    
PART 2 (this takes ~19 seconds to run)
For each row
    - determine which sensors can see that row
    - order sight ranges by range start for each sensor from above
    - for each range
        - keeping track of the farthest range end, find a range whose start leaves a gap
"""

TARGET_ROW = 2_000_000
# TARGET_ROW = 10  # Sample run value

MAX_RANGE = 4_000_000
# MAX_RANGE = 20  # Sample run value
TUNING_FREQ_FACTOR = 4_000_000


class Sensor:
    def __init__(self, x_coord: int, y_coord: int, beacon_x: int, beacon_y: int):
        self.x = x_coord
        self.y = y_coord
        self.bx = beacon_x
        self.by = beacon_y
        self.sight_range = self._calculate_sight_range()
        self.min_visible_row = self.y - self.sight_range
        self.max_visible_row = self.y + self.sight_range

    def _calculate_sight_range(self) -> int:
        return abs(self.x - self.bx) + abs(self.y - self.by)

    def can_see_row(self, y_val: int) -> bool:
        return self.min_visible_row <= y_val <= self.max_visible_row

    def visible_x_range(self, y_val: int) -> Tuple[int, int]:
        sensor_dist = abs(self.y - y_val)
        sight_radius = self.sight_range - sensor_dist
        return self.x - sight_radius, self.x + sight_radius


def main():
    visible_x_vals = set()
    beacons_in_target_row = set()
    sensors = []
    with open(get_data_file_path(__file__.split("/")[-1], sample=False), "r") as f_in:
        for line in f_in:
            sx, sy, bx, by = [int(val) for val in re.findall(r"-?\d+", line)]
            sensor = Sensor(sx, sy, bx, by)
            sensors.append(sensor)
            if sensor.can_see_row(TARGET_ROW):
                min_x, max_x = sensor.visible_x_range(TARGET_ROW)
                for x_val in range(min_x, max_x + 1):
                    visible_x_vals.add(x_val)
            if sensor.by == TARGET_ROW:
                beacons_in_target_row.add((bx, by))
    print("PART 1:", len(visible_x_vals) - len(beacons_in_target_row))

    # PART 2
    for row in range(MAX_RANGE):
        sight_ranges = []
        for sensor in sensors:
            if sensor.can_see_row(row):
                insort(
                    sight_ranges,
                    sensor.visible_x_range(row),
                    key=lambda pair: pair[0],
                )
        max_range_end = 0
        for r in sight_ranges:
            if r[0] > max_range_end + 1:
                print("PART 2:", (r[0] - 1) * TUNING_FREQ_FACTOR + row)
                return
            else:
                max_range_end = max(max_range_end, r[1])


if __name__ == "__main__":
    main()
