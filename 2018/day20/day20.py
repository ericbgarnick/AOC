import re
import sys
from typing import List

SPLIT = '|'
OPEN = '('
CLOSE = ')'
GROUPING = ''.join([OPEN, CLOSE])
START = '^'
END = '$'
SYMBOLS = ''.join([GROUPING, START, END])


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


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = open(data_file, 'r').readline().strip()
    longer = find_longest_route(data)
    print(longer)
    print(len(longer))

    # part 2: how many paths with len >= 1000?
