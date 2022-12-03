from sys import argv
from typing import List, Dict, Tuple, Set


class TrackMap:
    """A class for representing a cart map."""
    def __init__(self, mapfile_name: str):
        self._mapfile_name = mapfile_name
        self._map = []    # type: List[List[str]]
        self._max_width = 0

    def load_map(self):
        for line in open(self._mapfile_name, 'r').readlines():
            line = line.strip('\n')
            self._max_width = max(self._max_width, len(line))
            self._map.append(list(line))
        self._pad_rows()

    def _pad_rows(self):
        for row in self._map:
            row += [' ' for _ in range(self._max_width - len(row))]

    def draw(self, coords: Tuple[int, int], direction_symbol: str):
        x, y = coords
        if self._map[y][x] in '^v<>':
            self._map[y][x] = 'x'
        else:
            self._map[y][x] = direction_symbol

    @property
    def map(self):
        return self._map

    def __str__(self):
        return '\n'.join([''.join(line) for line in self._map])


class Cart:
    """
    A class for representing cart that has x, y coordinates and a direction of:
    '^' (up), 'V' (down), '<' (left), '>' (right)
    """
    TURN_ORDER = {None: "l", "l": "s", "s": "r", "r": "l"}
    CORNER_TURNS = {'^': {'/': '>', '\\': '<'},
                    'v': {'/': '<', '\\': '>'},
                    '<': {'/': 'v', '\\': '^'},
                    '>': {'/': '^', '\\': 'v'}}
    JUNCTION_TURNS = {'^': {'l': '<', 'r': '>', 's': '^'},
                      'v': {'l': '>', 'r': '<', 's': 'v'},
                      '<': {'l': 'v', 'r': '^', 's': '<'},
                      '>': {'l': '^', 'r': 'v', 's': '>'}}

    def __init__(self, x_coord: int, y_coord: int, direction: str):
        self._x = x_coord
        self._y = y_coord
        self._direction = direction
        self._next_turn = None

    @property
    def coords(self) -> Tuple[int, int]:
        return self._x, self._y

    @property
    def direction(self) -> str:
        return self._direction

    def move(self, neighbors: Dict[str, str]):
        """neighbors is a Dict with keys "^", ">", "v", "<" and
        values of None or str (for the symbol in the trackmap)."""
        dest = neighbors[self._direction]
        self._update_coords()
        self._update_direction(dest)

    def _update_coords(self):
        if self._direction == '^':
            self._y -= 1
        elif self._direction == 'v':
            self._y += 1
        elif self._direction == '<':
            self._x -= 1
        elif self._direction == '>':
            self._x += 1

    def _update_direction(self, destination_symbol: str):
        if destination_symbol in '-|':
            # Going in a straight line
            pass
        elif destination_symbol in '\/':
            self._turn_corner(destination_symbol)
        elif destination_symbol == '+':
            self._turn_junction()

    def _turn_corner(self, symbol: str):
        self._direction = self.CORNER_TURNS[self._direction][symbol]

    def _turn_junction(self):
        self._set_next_turn()
        self._make_turn()

    def _set_next_turn(self):
        self._next_turn = self.TURN_ORDER[self._next_turn]

    def _make_turn(self):
        self._direction = self.JUNCTION_TURNS[self._direction][self._next_turn]

    def __str__(self) -> str:
        return "({}, {}) {}".format(self._x, self._y, self._direction)


class Simulation:
    def __init__(self, trackmap: TrackMap):
        self._trackmap = trackmap
        self._carts = []    # type: List[Cart]
        self._collision = False

    def run(self, part_num: int):
        self._set_carts()
        count = 0
        while not self._collision:
            self._carts.sort(key=lambda c: c.coords)
            for cart in self._carts:
                cart_neighbors = self._get_cart_neighbors(cart)
                cart.move(cart_neighbors)
                self._check_collisions()
                if self._collision and self._done_from_collision(part_num):
                    break
            count += 1
        print("Cycles:", count)

    def _set_carts(self):
        for y, line in enumerate(self._trackmap.map):
            for x, symbol in enumerate(line):
                if symbol in '^v<>':
                    self._carts.append(Cart(x, y, symbol))

    def _get_cart_neighbors(self, cart: Cart) -> Dict[str, str]:
        x, y = cart.coords
        neighbors = {'^': None, 'v': None, '<': None, '>': None}
        if x:
            neighbors['<'] = self._trackmap.map[y][x - 1]
        if x < len(self._trackmap.map[0]) - 1:
            neighbors['>'] = self._trackmap.map[y][x + 1]
        if y:
            neighbors['^'] = self._trackmap.map[y - 1][x]
        if y < len(self._trackmap.map) - 1:
            neighbors['v'] = self._trackmap.map[y + 1][x]
        return neighbors

    def _check_collisions(self):
        occupied = {c.coords for c in self._carts}
        self._collision = len(occupied) < len(self._carts)

    def _done_from_collision(self, part_num: int) -> bool:
        if part_num == 1:
            return True
        else:
            self._remove_collisions()
            if len(self._carts) > 1:
                self._collision = False
            else:
                print("1 cart!")
            return len(self._carts) == 1

    def _remove_collisions(self):
        crash_locations = self._find_crash_locations()
        self._carts = [c for c in self._carts if
                       c.coords not in crash_locations]

    def _find_crash_locations(self) -> Set[Tuple[int, int]]:
        location_counts = {}
        for c in self._carts:
            coords = c.coords
            try:
                location_counts[coords] += 1
            except KeyError:
                location_counts[coords] = 1
        return {loc for loc, ct in location_counts.items() if ct > 1}

    def __str__(self) -> str:
        self._draw_carts()
        return "{}\n{}".format([str(c) for c in self._carts],
                               str(self._trackmap))

    def _draw_carts(self):
        for c in self._carts:
            self._trackmap.draw(c.coords, c.direction)


if __name__ == '__main__':
    filename = argv[1]
    part = int(argv[2])

    tm = TrackMap(filename)
    tm.load_map()

    sim = Simulation(tm)
    sim.run(part)
    print(sim)

