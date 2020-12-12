import pytest

from day12 import teleport, rotate


@pytest.mark.parametrize(
    "h_wp, v_wp, direction, degrees, h_expected, v_expected",
    [
        # Q1 - R
        (1, 4, "R", 90, 4, -1),
        (1, 4, "R", 180, -1, -4),
        (1, 4, "R", 270, -4, 1),
        # Q2 - R
        (4, -1, "R", 90, -1, -4),
        (4, -1, "R", 180, -4, 1),
        (4, -1, "R", 270, 1, 4),
        # Q3 - R
        (-1, -4, "R", 90, -4, 1),
        (-1, -4, "R", 180, 1, 4),
        (-1, -4, "R", 270, 4, -1),
        # Q4 - R
        (-4, 1, "R", 90, 1, 4),
        (-4, 1, "R", 180, 4, -1),
        (-4, 1, "R", 270, -1, -4),
        # Q1 - L
        (1, 4, "L", 90, -4, 1),
        (1, 4, "L", 180, -1, -4),
        (1, 4, "L", 270, 4, -1),
        # Q2 - L
        (4, -1, "L", 90, 1, 4),
        (4, -1, "L", 180, -4, 1),
        (4, -1, "L", 270, -1, -4),
        # Q3 - L
        (-1, -4, "L", 90, 4, -1),
        (-1, -4, "L", 180, 1, 4),
        (-1, -4, "L", 270, -4, 1),
        # Q4 - L
        (-4, 1, "L", 90, -1, -4),
        (-4, 1, "L", 180, 4, -1),
        (-4, 1, "L", 270, 1, 4),
    ],
)
def test_rotate(h_wp, v_wp, direction, degrees, h_expected, v_expected):
    assert rotate(h_wp, v_wp, direction, degrees) == (h_expected, v_expected)


@pytest.mark.parametrize(
    "h_wp, v_wp, multiplier, h_expected, v_expected",
    [
        (3, 2, 5, 15, 10),
        (-3, 2, 5, -15, 10),
        (3, -2, 5, 15, -10),
        (-3, -2, 5, -15, -10),
    ],
)
def test_teleport(h_wp, v_wp, multiplier, h_expected, v_expected):
    assert teleport(h_wp, v_wp, multiplier) == (h_expected, v_expected)
