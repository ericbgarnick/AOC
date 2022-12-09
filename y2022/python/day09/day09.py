"""
Part 1 answer: 6314
Part 2 answer: 2504
"""
from y2022.python.shared import get_data_file_path


class Rope:
    ORIGIN = (0, 0)
    def __init__(self, length: int):
        self.knots = [Rope.ORIGIN for _ in range(length)]
        self.tail_history = {Rope.ORIGIN}

    def move(self, direction: str, distance: int):
        for step in range(distance):
            self.step(direction)
            self.tail_history.add(self.knots[-1])

    def step(self, direction: str):
        # Update head
        head = self.knots[0]
        if direction == "U":
            self.knots[0] = (head[0], head[1] + 1)
        elif direction == "D":
            self.knots[0] = (head[0], head[1] - 1)
        elif direction == "R":
            self.knots[0] = (head[0] + 1, head[1])
        else:
            self.knots[0] = (head[0] - 1, head[1])
        # Update the rest of the rope
        for i in range(len(self.knots) - 1):
            head = self.knots[i]
            tail = self.knots[i + 1]
            x_diff = abs(head[0] - tail[0])
            y_diff = abs(head[1] - tail[1])
            if y_diff > 1 or x_diff > 1:
                tail_change_y = y_diff if y_diff == 0 else (head[1] - tail[1]) // y_diff
                tail_change_x = x_diff if x_diff == 0 else (head[0] - tail[0]) // x_diff
                self.knots[i + 1] = (tail[0] + tail_change_x, tail[1] + tail_change_y)


def main():
    rope1 = Rope(length=2)
    rope2 = Rope(length=10)
    with open(get_data_file_path(__file__), "r") as f_in:
        for line in f_in:
            direction, distance = line.strip().split()
            rope1.move(direction, int(distance))
            rope2.move(direction, int(distance))
    print("PART 1:", len(rope1.tail_history))
    print("PART 2:", len(rope2.tail_history))


if __name__ == "__main__":
    main()
