"""
Part 1 answer: 332
Part 2 answer: 166
"""
from y2016.python.shared import get_data_file_path


def load_directions() -> list[str]:
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        return f_in.read().strip().split(", ")


def travel(directions: list[str]):
    turns = {
        "N": {"R": "E", "L": "W"},
        "E": {"R": "S", "L": "N"},
        "S": {"R": "W", "L": "E"},
        "W": {"R": "N", "L": "S"},
    }
    twice_visited_dist = -1
    cur_x = 0
    cur_y = 0
    history = {(cur_x, cur_y)}
    facing = "N"
    for step in directions:
        facing = turns[facing][step[0]]
        dist = int(step[1:])
        for _ in range(dist):
            if facing == "N":
                cur_y += 1
            elif facing == "E":
                cur_x += 1
            elif facing == "S":
                cur_y -= 1
            else:
                cur_x -= 1
            if twice_visited_dist < 0:
                if (cur_x, cur_y) in history:
                    twice_visited_dist = abs(cur_x) + abs(cur_y)
                else:
                    history.add((cur_x, cur_y))
    print("PART 1:", abs(cur_x) + abs(cur_y))
    print("PART 2:", twice_visited_dist)


def main():
    directions = load_directions()
    travel(directions)


if __name__ == "__main__":
    main()

