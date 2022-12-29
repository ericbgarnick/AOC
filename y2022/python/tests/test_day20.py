import pytest
from y2022.python.day20.day20 import Link, mix


@pytest.mark.parametrize(
    "original,mix_idx,expected_next,expected_prev",
    [
        pytest.param(
            [1, 2, 3, 4, 5],
            0,
            [3, 1, 4, 5, 2],
            [2, 5, 1, 3, 4],
            id="positive value, simple mix",
        ),
        pytest.param(
            [1, 2, 3, 4, 5],
            2,
            [3, 4, 2, 5, 1],
            [5, 3, 1, 2, 4],
            id="positive value, mix to end",
        ),
        pytest.param(
            [1, 3, 2, 4, 5],
            2,
            [3, 4, 1, 5, 2],
            [2, 1, 5, 3, 4],
            id="positive value, mix wrap",
        ),
        pytest.param(
            [1, 2, 3, -2, 5],
            3,
            [-2, 3, 5, 2, 1],
            [5, -2, 2, 1, 3],
            id="negative value, simple mix",
        ),
        pytest.param(
            [1, 2, 3, -3, 5],
            3,
            [2, 3, 5, 1, -3],
            [-3, 1, 2, 5, 3],
            id="negative value, mix to end",
        ),
        pytest.param(
            [1, 2, -3, 4, 5],
            2,
            [2, 4, 5, -3, 1],
            [5, 1, 4, 2, -3],
            id="negative value, mix wrap",
        ),
        pytest.param(
            [1, 2, 0, 4, 5],
            2,
            [2, 0, 4, 5, 1],
            [5, 1, 2, 0, 4],
            id="zero value",
        ),
        pytest.param(
            [1, 9, 0, 4, 5],
            1,
            [0, 4, 9, 5, 1],
            [5, 0, 1, 9, 4],
            id="value > len list",
        ),
        pytest.param(
            [1, -9, 0, 4, 5],
            1,
            [0, 1, 4, 5, -9],
            [-9, 5, 1, 0, 4],
            id="negative value > len list",
        ),
        pytest.param(
            [1, 2, 0, 4, 5],
            3,
            [2, 0, 4, 5, 1],
            [5, 1, 2, 0, 4],
            id="return to original position pos",
        ),
        pytest.param(
            [1, 2, 0, -4, 5],
            3,
            [2, 0, -4, 5, 1],
            [5, 1, 2, 0, -4],
            id="return to original position neg",
        ),
    ],
)
def test_mix(
    original: list[int],
    mix_idx: int,
    expected_next: list[int],
    expected_prev: list[int],
):
    nums = [Link(n) for n in original]
    for i in range(len(nums)):
        nums[i].next = nums[(i + 1) % len(nums)]
        nums[i].prev = nums[i - 1]

    mix(nums[mix_idx], len(nums))

    assert [link.next.value for link in nums] == expected_next
    assert [link.prev.value for link in nums] == expected_prev


def test_full_mix():
    original = [-3, 0, 4, -2, 2, 1, -2]
    # final: [0, -3, 4, 1, -2b, 2, -2a]
    nums = [Link(n) for n in original]
    for i in range(len(nums)):
        nums[i].next = nums[(i + 1) % len(nums)]
        nums[i].prev = nums[i - 1]

    expected_next = [4, -3, 1, 0, -2, -2, 2]
    expected_prev = [0, -2, -3, 2, -2, 4, 1]

    for link in nums:
        mix(link, len(nums))

    assert [link.next.value for link in nums] == expected_next
    assert [link.prev.value for link in nums] == expected_prev
