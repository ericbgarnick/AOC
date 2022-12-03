from sys import argv
from typing import Set, List


ADJUST_SIZE = 300


def get_positive_conditions(data: List[str]) -> Set[str]:
    return {c[:5] for c in data if c.endswith('#')}


def apply_conditions(plants_row: str, positive_conditions: Set[str]) -> str:
    new_row = ['.', '.']
    for i in range(2, len(plants_row) - 2):
        section = plants_row[i - 2:i + 3]
        if section in positive_conditions:
            new_row.append('#')
        else:
            new_row.append('.')

    return ''.join(new_row + ['.', '.'])


def count_plants(plants_row: str, start_idx: int) -> int:
    total = 0
    for idx, plant in enumerate(plants_row):
        if plant == '#':
            total += idx + start_idx
    return total


if __name__ == '__main__':
    data_file = argv[1]
    iterations = int(argv[2])

    with open(data_file, 'r') as f_in:
        plants = (('.' * ADJUST_SIZE) +
                  f_in.readline().strip().split()[-1] +
                  ('.' * ADJUST_SIZE))
        next(f_in)
        raw_conditions = [c.strip() for c in f_in.readlines()]

        conditions = get_positive_conditions(raw_conditions)

    last_count = count_plants(plants, -1 * ADJUST_SIZE)
    print("PLANT COUNT:", last_count)

    for i in range(iterations):
        plants = apply_conditions(plants, conditions)
        plant_count = count_plants(plants, -1 * ADJUST_SIZE)
        print("PLANT COUNT DIFF {} AT {}".format(plant_count - last_count, i))
        last_count = plant_count

    # plant_count = count_plants(plants, -1 * ADJUST_SIZE)
    # print("PLANT COUNT:", plant_count)
