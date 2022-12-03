from typing import List

import pytest

from .fish_number import explode, FishNumber, split, sum_fish_numbers, magnitude


@pytest.mark.parametrize(
    "original,exploded",
    [
        (
            [[[[[9, 8], 1], 2], 3], 4],
            [[[[0, 9], 2], 3], 4],
        ),
        (
            [7, [6, [5, [4, [3, 2]]]]],
            [7, [6, [5, [7, 0]]]],
        ),
        (
            [[6, [5, [4, [3, 2]]]], 1],
            [[6, [5, [7, 0]]], 3],
        ),
        (
            [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
        ),
        (
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        ),
    ],
)
def test_explode(original: FishNumber, exploded: FishNumber):
    result = explode(original)
    assert -1 not in result
    assert original == exploded


@pytest.mark.parametrize(
    "original,splitted",
    [
        (
            [[[[0, 7], 4], [15, [0, 13]]], [1, 1]],
            [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
        ),
        (
            [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
            [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]],
        ),
    ],
)
def test_split(original: FishNumber, splitted: FishNumber):
    result = split(original)
    assert -1 not in result
    assert original == splitted


@pytest.mark.parametrize(
    "addends,expected_result",
    [
        (
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
            ],
            [[[[1, 1], [2, 2]], [3, 3]], [4, 4]],
        ),
        (
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
                [5, 5],
            ],
            [[[[3, 0], [5, 3]], [4, 4]], [5, 5]],
        ),
        (
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
                [5, 5],
                [6, 6],
            ],
            [[[[5, 0], [7, 4]], [5, 5]], [6, 6]],
        ),
        (
            [
                [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
                [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
            ],
            [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]],
        ),
        (
            [
                [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]],
                [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
            ],
            [[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]],
        ),
        (
            [
                [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
                [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
                [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
                [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
                [7, [5, [[3, 8], [1, 4]]]],
                [[2, [2, 2]], [8, [8, 1]]],
                [2, 9],
                [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
                [[[5, [7, 4]], 7], 1],
                [[[[4, 2], 2], 6], [8, 7]],
            ],
            [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]],
        ),
    ],
)
def test_sum_fish_numbers(
        addends: List[FishNumber],
        expected_result: FishNumber
):
    result = sum_fish_numbers(addends[0], addends[1])
    for addend in addends[2:]:
        result = sum_fish_numbers(result, addend)
    assert result == expected_result


@pytest.mark.parametrize(
    "fish_number,expected_magnitude",
    [
        ([[1, 2], [[3, 4], 5]], 143),
        ([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]], 1384),
        ([[[[1, 1], [2, 2]], [3, 3]], [4, 4]], 445),
        ([[[[3, 0], [5, 3]], [4, 4]], [5, 5]], 791),
        ([[[[5, 0], [7, 4]], [5, 5]], [6, 6]], 1137),
        ([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]], 3488),
    ],
)
def test_magnitude(fish_number: FishNumber, expected_magnitude: int):
    assert magnitude(fish_number) == expected_magnitude
