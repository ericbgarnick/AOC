from typing import List, Tuple, Optional, Union

Point = Tuple[int, int]


class CaveSpot:
    WALL = "#"
    FLOOR = "."

    def __init__(self, spot_type: str):
        # Units may be on top of a FLOOR type spot
        self._type = spot_type if spot_type == self.WALL else self.FLOOR

        self._u = None              # type: Optional['CaveSpot']
        self._l = None              # type: Optional['CaveSpot']
        self._r = None              # type: Optional['CaveSpot']
        self._d = None              # type: Optional['CaveSpot']

    def __str__(self):
        return self._type

    def __repr__(self):
        return self.__str__()

    @property
    def spot_type(self) -> str:
        return self._type

    @property
    def u(self):
        return self._u

    @property
    def l(self):
        return self._l

    @property
    def r(self):
        return self._r

    @property
    def d(self):
        return self._d

    def set_u(self, spot: Optional['CaveSpot']):
        self._u = spot

    def set_l(self, spot: Optional['CaveSpot']):
        self._l = spot

    def set_r(self, spot: Optional['CaveSpot']):
        self._r = spot

    def set_d(self, spot: Optional['CaveSpot']):
        self._d = spot


class Cave:

    def __init__(self, width: int, full_map: List[CaveSpot] = None):
        self._cave_map = full_map or []
        self._width = width
        if self._cave_map:
            self.link_spots()

    @staticmethod
    def cave_string(cave_map: List[Union[CaveSpot, str]],
                    cave_width: int) -> str:
        """
        Return a string representation of cave_map. E.g.

        Input: ['#', '#', '#', '#', '.', '#', '#', '#', '#']
        Output:
        '###
         #.#
         ###'
        """
        cave_rows = []
        for start in range(0, len(cave_map), cave_width):
            cave_rows.append(cave_map[start: start + cave_width])
        return '\n'.join(''.join([str(spot) for spot in row])
                         for row in cave_rows)

    @property
    def width(self) -> int:
        return self._width

    @property
    def cave_map(self) -> List[CaveSpot]:
        return self._cave_map

    def add_row(self, row: List[CaveSpot]):
        self._cave_map.extend(row)

    def link_spots(self):
        assert self._width != 0
        assert len(self._cave_map) % self._width == 0

        for row_start in range(0, len(self._cave_map), self._width):
            for i in range(row_start, row_start + self._width):
                self._set_spot_neighbors(row_start, i)

    def copy_map(self) -> 'Cave':
        new_cave_spots = [CaveSpot(spot.spot_type) for spot in self._cave_map]
        new_map = Cave(self._width, new_cave_spots)
        new_map.link_spots()
        return new_map

    def _set_spot_neighbors(self, row_start: int, i: int):
        spot = self._cave_map[i]
        if row_start > 0:
            spot.set_u(self._cave_map[i - self._width])
        if row_start < len(self._cave_map) - self._width:
            spot.set_d(self._cave_map[i + self._width])
        if i % self._width != 0:
            spot.set_l(self._cave_map[i - 1])
        if (i + 1) % self._width != 0:
            spot.set_r(self._cave_map[i + 1])

    def __str__(self):
        return self.cave_string(self._cave_map, self._width)

    def __repr__(self):
        return self.__str__()
