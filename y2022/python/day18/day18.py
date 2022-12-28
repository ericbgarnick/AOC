"""
Part 1 answer: 3432
Part 2 answer: 2042
"""
import re

from y2022.python.shared import get_data_file_path

extrema_list = list[list[tuple[float | int, float | int]]]


def main():
    max_x = float("-inf")
    max_y = float("-inf")
    max_z = float("-inf")
    points: list[tuple[int, int, int]] = []
    with open(get_data_file_path(__file__.split("/")[-1], sample=False), "r") as f_in:
        for line in f_in:
            # shift up 1 to create empty buffer around droplet
            x, y, z = (int(val) + 1 for val in re.findall(r"\d+", line))
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)
            points.append((x, y, z))
    # Add extra value to max for empty buffer around droplet
    droplet = [
        [[0 for _ in range(max_x + 2)] for _ in range(max_y + 2)]
        for _ in range(max_z + 2)
    ]
    x_extrema: extrema_list = [
        [(float("inf"), float("-inf")) for _ in range(max_y + 2)]
        for _ in range(max_z + 2)
    ]
    y_extrema: extrema_list = [
        [(float("inf"), float("-inf")) for _ in range(max_x + 2)]
        for _ in range(max_z + 2)
    ]
    z_extrema: extrema_list = [
        [(float("inf"), float("-inf")) for _ in range(max_x + 2)]
        for _ in range(max_y + 2)
    ]
    for x, y, z in points:
        droplet[z][y][x] = 1
        x_extrema[z][y] = (min(x, x_extrema[z][y][0]), max(x, x_extrema[z][y][1]))
        y_extrema[z][x] = (min(y, y_extrema[z][x][0]), max(y, y_extrema[z][x][1]))
        z_extrema[y][x] = (min(z, z_extrema[y][x][0]), max(z, z_extrema[y][x][1]))
    total_surface_area = 0
    exterior_surface_area = 0
    for x in range(max_x + 2):
        for y in range(max_y + 2):
            for z in range(max_z + 2):
                if not droplet[z][y][x]:
                    total_surface_area += neighbor_count(x, y, z, droplet)
                    exterior_surface_area += neighbor_count(
                        x,
                        y,
                        z,
                        droplet,
                        x_extrema,
                        y_extrema,
                        z_extrema,
                        include_interior=False,
                    )
    print("PART 1:", total_surface_area)
    print("PART 2:", exterior_surface_area)


def neighbor_count(
    x: int,
    y: int,
    z: int,
    droplet: list[list[list[int]]],
    x_extrema: extrema_list | None = None,
    y_extrema: extrema_list | None = None,
    z_extrema: extrema_list | None = None,
    include_interior: bool = True,
) -> int:
    def x_inc() -> int:
        return droplet[z][y][x + 1]

    def x_dec() -> int:
        return droplet[z][y][x - 1]

    def y_inc() -> int:
        return droplet[z][y + 1][x]

    def y_dec() -> int:
        return droplet[z][y - 1][x]

    def z_inc() -> int:
        return droplet[z + 1][y][x]

    def z_dec() -> int:
        return droplet[z - 1][y][x]

    def is_outside_extrema() -> bool:
        x_outside = x < x_extrema[z][y][0] or x > x_extrema[z][y][1]
        y_outside = y < y_extrema[z][x][0] or y > y_extrema[z][x][1]
        z_outside = z < z_extrema[y][x][0] or z > z_extrema[y][x][1]
        return x_outside or y_outside or z_outside

    num_neighbors = 0
    for fn in (x_inc, x_dec, y_inc, y_dec, z_inc, z_dec):
        try:
            neighbors = fn()
            if include_interior or is_outside_extrema():
                num_neighbors += neighbors
        except IndexError:
            pass
    return num_neighbors


if __name__ == "__main__":
    main()
