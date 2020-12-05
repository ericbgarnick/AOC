import pytest

from day05 import boarding_pass_helper


@pytest.mark.parametrize(
    "code, row_min, row_max, expected_result",
    [
        ("F", 1, 2, 0),
        ("B", 1, 2, 1),
        ("FF", 1, 4, 0),
        ("FB", 1, 4, 1),
        ("BF", 1, 4, 2),
        ("BB", 1, 4, 3),
        ("FBFBBFF", 1, 128, 44),
        ("FBFBBFB", 1, 128, 45),
    ]
)
def test_helper_rows(code, row_min, row_max, expected_result):
    assert boarding_pass_helper(code, row_min, row_max, "F") == expected_result


@pytest.mark.parametrize(
    "code, col_min, col_max, expected_result",
    [
        ("L", 1, 2, 0),
        ("R", 1, 2, 1),
        ("LL", 1, 4, 0),
        ("LR", 1, 4, 1),
        ("RL", 1, 4, 2),
        ("RR", 1, 4, 3),
        ("RLR", 1, 8, 5),
        ("LLR", 1, 8, 1),
    ]
)
def test_helper_cols(code, col_min, col_max, expected_result):
    assert boarding_pass_helper(code, col_min, col_max, "L") == expected_result

