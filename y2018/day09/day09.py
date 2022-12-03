import re
from sys import argv
from typing import List

KEEPER = 23
BACKUP = 7


class Node:
    def __init__(self, value: int):
        self._value = value
        self._next_node = self
        self._prev_node = self

    def set_next(self, new_node):
        self._next_node = new_node

    def set_prev(self, new_node):
        self._prev_node = new_node

    @property
    def next_node(self):
        return self._next_node

    @property
    def prev_node(self):
        return self._prev_node

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class LinkedList:
    def __init__(self, cur_node: Node):
        self._cur_node = cur_node
        self._num_nodes = 1

    def add_node(self, next_node: Node):
        next_node.set_next(self._cur_node.next_node)
        next_node.set_prev(self._cur_node)

        cur_next = self._cur_node.next_node
        self._cur_node.set_next(next_node)
        cur_next.set_prev(next_node)

        self._cur_node = self._cur_node.next_node
        self._num_nodes += 1

    def pop(self) -> Node:
        next_node = self._cur_node.next_node
        prev_node = self._cur_node.prev_node
        prev_node.set_next(next_node)
        next_node.set_prev(prev_node)

        self._cur_node.set_next(None)
        self._cur_node.set_prev(None)

        saved_node = self._cur_node
        self._cur_node = next_node
        self._num_nodes -= 1

        return saved_node

    def forward(self, dist: int=1):
        for _ in range(dist):
            self._cur_node = self._cur_node.next_node

    def back(self, dist: int=1):
        for _ in range(dist):
            self._cur_node = self._cur_node.prev_node

    def __iter__(self):
        for _ in range(self._num_nodes):
            self._cur_node = self._cur_node.next_node
            yield self._cur_node.prev_node

    def __len__(self):
        return self._num_nodes


def play_marbles(data: List[int], part_num: int):
    num_players, *rest = data
    try:
        num_marbles, max_score = rest
    except ValueError:
        num_marbles = rest[0]
    if part_num == 2:
        num_marbles *= 100

    players = [0 for _ in range(num_players)]

    player_num = 0
    circle = LinkedList(Node(0))
    for marble_num in range(1, num_marbles + 1):
        new_marble = Node(marble_num)
        points = _inset_marble(new_marble, circle)
        player_num = (player_num + 1) % num_players
        players[player_num] += points

    print("MAX SCORE:", max(players))


def _inset_marble(new_marble: Node, circle: LinkedList) -> int:
    if _should_insert_marble(new_marble.value):
        circle.forward()
        circle.add_node(new_marble)
        points = 0
    else:
        circle.back(BACKUP)
        points = new_marble.value + circle.pop().value
    return points


def _should_insert_marble(marble_num: int) -> bool:
    """Return the new position in the circle and True if a marble should be
    inserted, otherwise False"""
    if marble_num and marble_num % KEEPER == 0:
        return False
    else:
        return True


if __name__ == '__main__':
    data_file = argv[1]
    for line in open(data_file, 'r'):
        input_nums = [int(val) for val in
                      re.findall(r'\d+', line.strip())]
        part = int(argv[2])
        kwargs = {'data': input_nums, 'part_num': part}

        play_marbles(**kwargs)
