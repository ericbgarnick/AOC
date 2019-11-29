import re
import sys
from collections import namedtuple
from typing import List, Dict

SPLIT = '|'
OPEN = '('
CLOSE = ')'
GROUPING = ''.join([OPEN, CLOSE])
START = '^'
END = '$'
BOOKENDS = ''.join([START, END])
SYMBOLS = ''.join([GROUPING, BOOKENDS])


######################
# ----- PART I ----- #
######################
# Recursively find the longest segment in the input
def find_longest_route(regex_route: str) -> str:
    regex_route = regex_route.strip(SYMBOLS)
    regex_route = drop_dead_ends(regex_route)
    return longer_route(regex_route)


def longer_route(regex_route: str) -> str:
    if SPLIT not in regex_route:
        return regex_route
    elif OPEN not in regex_route:
        return longest_string(*regex_route.split('|'))
    else:
        prefix, suffix = regex_route.split(OPEN, maxsplit=1)

    splits = get_splits(suffix)
    split1 = splits[0]

    first = longer_route(suffix[:split1].strip(SYMBOLS))
    if len(splits) > 1:
        split2 = splits[1]
        second = longer_route(suffix[split1 + 1:split2].strip(SYMBOLS))
        third = longer_route(suffix[split2 + 1:].strip(SYMBOLS))
    else:
        second = longer_route(suffix[split1 + 1:].strip(SYMBOLS))
        third = ""

    return prefix + longest_string(first, second, third)


def drop_dead_ends(regex_route: str) -> str:
    escaped = [re.escape(s) for s in [OPEN, SPLIT, CLOSE]]
    return re.sub(r'{}[NSEW]+{}{}'.format(*escaped), '', regex_route)


def get_splits(route_segment: str) -> List[int]:
    nesting = 0
    splits = []
    for i, symbol in enumerate(route_segment):
        if symbol == SPLIT and not nesting:
            splits.append(i)
        elif symbol == OPEN:
            nesting += 1
        elif symbol == CLOSE:
            nesting -= 1
        else:
            pass
    return splits


def longest_string(*paths: str) -> str:
    return sorted(paths, key=lambda s: len(s))[-1]


#######################
# ----- PART II ----- #
#######################
# Follow all paths and record distances of each room from start
Position = namedtuple("Position", 'row col')


class Explorer:
    def __init__(self):
        self._cur_pos = Position(0, 0)  # increases to S, E
        self._journal = {self._cur_pos: 0}  # {<coords>: dist}

    @property
    def journal(self) -> Dict[Position, int]:
        return self._journal

    @property
    def max_distance(self) -> int:
        return max(self._journal.values())

    def explore_cave(self, directions: str):
        """Clean off BOOKENDS and explore cave by following directions"""
        self._explore(directions.strip(BOOKENDS))

    def _explore(self, directions: str):
        """Follow all paths in directions"""
        start = self._cur_pos
        if SPLIT not in directions:
            self._follow_path(directions)
        else:
            if OPEN in directions:
                open_idx = directions.find(OPEN)
                prefix = directions[:open_idx]
                directions = directions[open_idx:]
                self._follow_path(prefix)
            for path in self._find_sections(directions):
                self._explore(path)
        self._cur_pos = start

    @staticmethod
    def _find_sections(directions: str) -> List[str]:
        directions = directions.strip(SYMBOLS)
        sections = []
        section_start = 0
        parens_count = 0
        for i, d in enumerate(directions):
            if d == OPEN:
                parens_count += 1
            elif d == CLOSE:
                parens_count -= 1
            elif not parens_count and d == SPLIT:
                sections.append(directions[section_start:i])
                section_start = i + 1
            else:
                # Direction symbol
                pass
        if directions[section_start] not in SYMBOLS:
            sections.append(directions[section_start:])
        return sections

    def _follow_path(self, path: str):
        """Make a move for each step in path"""
        for step in path:
            self.move(step)

    def move(self, direction: str):
        """Update self._cur_pos for moving in the given direction.
        Also update self._journal with distance for new position."""
        cur_dist = self._journal[self._cur_pos]
        cur_row, cur_col = self._cur_pos
        if direction == 'N':
            self._cur_pos = Position(cur_row - 1, cur_col)
        elif direction == 'S':
            self._cur_pos = Position(cur_row + 1, cur_col)
        elif direction == 'W':
            self._cur_pos = Position(cur_row, cur_col - 1)
        elif direction == 'E':
            self._cur_pos = Position(cur_row, cur_col + 1)
        if self._cur_pos not in self._journal:
            self._journal[self._cur_pos] = cur_dist + 1


if __name__ == '__main__':
    # part 1: find the length of the longest path
    # data_file = sys.argv[1]
    # data = open(data_file, 'r').readline().strip()
    # longer = find_longest_route(data)
    # print(longer)
    # print(len(longer))

    # part 2: how many paths with len >= 1000?
    e = Explorer()
    e.explore_cave('(NESEW|EEESEN|ENSWW)')
    print(e.journal)
