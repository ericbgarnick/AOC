from sys import argv
from typing import Tuple, List, Dict

SERIAL_NUMBER = 3628
RACK_ID_INCREMENT = 10
GRID_SIZE = 300


def find_best_power_coord(square_size: int) -> Tuple[Tuple[int, int], int]:
    best_p = 0
    best_power_coord = (0, 0)
    grid = []
    for y in range(GRID_SIZE):
        grid.append([])
        for x in range(GRID_SIZE):
            p = _power_level((x, y))
            vert_sum = _calc_vert_sum(x, y, grid, p, square_size)
            enough_cols = _enough_cols(x, square_size)

            grid[y].append({'power': p,
                            'vert_sum': vert_sum})

            if vert_sum and enough_cols:
                new_p = sum(grid[y][x_coord]['vert_sum'] for
                            x_coord in range(x - (square_size - 1), x + 1))
                if new_p > best_p:
                    best_p = new_p
                    best_power_coord = (x - (square_size - 2),
                                        y - (square_size - 2))
    return best_power_coord, best_p


def _calc_vert_sum(x: int, y: int, grid: List[List[Dict]],
                   current_power: int, square_size: int) -> int:
    if y < square_size - 1:
        return 0
    else:
        return sum(grid[y_coord][x]['power'] for y_coord in
                   range(y - (square_size - 1), y)) + current_power


def _enough_cols(x: int, square_size: int) -> bool:
    if x < square_size - 1:
        return False
    else:
        return True


def _power_level(coord: Tuple[int, int]) -> int:
    # power level calculated using 1-indexing
    x, y = [c + 1 for c in coord]
    rack_id = x + RACK_ID_INCREMENT
    power_str = str((y * rack_id + SERIAL_NUMBER) * rack_id)
    try:
        p = int(str(power_str)[-3])
    except IndexError:
        p = 0
    return p - 5


if __name__ == '__main__':
    size = int(argv[1])
    if size:
        best_coord, best_power = find_best_power_coord(size)
        best_size = size
    else:
        best_coord = (0, 0)
        best_size = 0
        best_power = 0
        for s in range(1, GRID_SIZE + 1):
            new_coord, new_power = find_best_power_coord(s)
            if new_power > best_power:
                best_coord = new_coord
                best_power = new_power
                best_size = s
            elif new_power < best_size:
                break

            print("BEST COORD: {} HAS POWER: {} AT SIZE: {}".format(best_coord,
                                                                    best_power,
                                                                    best_size))
