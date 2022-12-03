from sys import argv
from typing import Tuple

TURNS = ("E", "S", "W", "N")


def move_ship(filename: str) -> int:
    """Destination holds still, ship turns and moves along its course"""
    direction = "E"
    h_dist = v_dist = 0
    for line in open(filename, "r"):
        h_change = v_change = 0
        action = line[0]
        value = int(line[1:])
        if action in TURNS:
            h_change, v_change = advance(action, value)
        elif action in {"R", "L"}:
            direction = turn(direction, action, value)
        elif action == "F":
            h_change, v_change = advance(direction, value)
        else:
            raise ValueError("Unknown direction:", direction)
        h_dist += h_change
        v_dist += v_change
    return abs(h_dist) + abs(v_dist)


def turn(cur_dir: str, turn_dir: str, turn_deg: int) -> str:
    """Return he direction the ship should be facing
    after turning turn_deg in direction turn_dir"""
    cur_idx = TURNS.index(cur_dir)
    op = int.__add__ if turn_dir == "R" else int.__sub__
    next_idx = op(cur_idx, turn_deg // 90) % len(TURNS)
    return TURNS[next_idx]


def move_everything(filename: str) -> int:
    """Destination rotates around ship and moves in cardinal directions,
    ship jumps around relative to destination"""
    direction = "E"
    h_ship = v_ship = 0
    h_wp = 10
    v_wp = 1
    for line in open(filename, "r"):
        h_change_ship = v_change_ship = h_change_wp = v_change_wp = 0
        action = line[0]
        value = int(line[1:])
        if action in TURNS:
            h_change_wp, v_change_wp = advance(action, value)
        elif action in {"R", "L"}:
            h_wp, v_wp = rotate(h_wp, v_wp, action, value)
        elif action == "F":
            h_change_ship, v_change_ship = teleport(h_wp, v_wp, value)
        else:
            raise ValueError("Unknown direction:", direction)
        h_wp += h_change_wp
        v_wp += v_change_wp
        h_ship += h_change_ship
        v_ship += v_change_ship
    return abs(h_ship) + abs(v_ship)


def advance(direction: str, distance: int) -> Tuple[int, int]:
    """Return the change in horizontal and vertical coordinate values
    after moving direction for distance"""
    h_dist = v_dist = 0
    if direction == "N":
        v_dist += distance
    elif direction == "S":
        v_dist -= distance
    elif direction == "E":
        h_dist += distance
    elif direction == "W":
        h_dist -= distance
    else:
        raise ValueError("Unknown direction:", direction)
    return h_dist, v_dist


def rotate(h_wp: int, v_wp: int, rot_dir: str, rot_deg: int) -> Tuple[int, int]:
    """Return the change in horizontal and vertical coordinate values
    after rotating the waypoint around the ship"""
    if rot_dir == "L":
        # Convert to clockwise rotation
        rot_deg = 360 - rot_deg
    h_neg = h_wp < 0
    v_neg = v_wp < 0
    if rot_deg == 180:
        h_wp *= -1
        v_wp *= -1
    elif rot_deg == 90:
        if h_neg == v_neg:
            h_wp, v_wp = v_wp, h_wp
            v_wp *= -1
        else:
            h_wp *= -1
            h_wp, v_wp = v_wp, h_wp
    elif rot_deg == 270:
        if h_neg == v_neg:
            h_wp, v_wp = v_wp, h_wp
            h_wp *= -1
        else:
            v_wp *= -1
            h_wp, v_wp = v_wp, h_wp
    else:
        h_wp *= -1
        h_wp, v_wp = v_wp, h_wp
    return h_wp, v_wp


def teleport(h_wp: int, v_wp: int, multiplier: int) -> Tuple[int, int]:
    """Return the change in horizontal and vertical coordinates
    after jumping the ship based on waypoint location"""
    return h_wp * multiplier, v_wp * multiplier


if __name__ == "__main__":
    input_file = argv[1]
    print("PART 1:", move_ship(input_file))
    print("PART 2:", move_everything(input_file))
