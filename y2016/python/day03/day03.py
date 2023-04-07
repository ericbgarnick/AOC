"""
Part 1 answer: 917
Part 2 answer: 1649
"""
from y2016.python.shared import get_data_file_path


def load_data_h() -> list[list[int]]:
    input_data = []
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        for row in f_in:
            input_data.append([int(val) for val in row.strip().split()])
    return input_data


def load_data_v() -> list[list[int]]:
    input_data = [[], [], []]
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        for row in f_in:
            if len(input_data[-1]) == 3:
                input_data.extend([[], [], []])
            t1, t2, t3 = [int(val) for val in row.strip().split()]
            input_data[-3].append(t1)
            input_data[-2].append(t2)
            input_data[-1].append(t3)
    return input_data


def is_possible_triangle(a: int, b: int, c: int) -> bool:
    return a + b > c and b + c > a and c + a > b


def main():
    h_data = load_data_h()
    triangle_count = sum(1 for row in h_data if is_possible_triangle(*row))
    print("PART 1:", triangle_count)
    v_data = load_data_v()
    triangle_count = sum(1 for row in v_data if is_possible_triangle(*row))
    print("PART 2:", triangle_count)


if __name__ == "__main__":
    main()
