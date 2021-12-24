from typing import List, Union

FishNumber = List[Union[List, int]]


def sum_fish_numbers(fish_number1: FishNumber, fish_number2: FishNumber) -> FishNumber:
    # Add copies, leaving original numbers unchanged
    added = eval(f"[{fish_number1},{fish_number2}]")
    return reduce(added)


def reduce(added: FishNumber) -> FishNumber:
    maybe_can_reduce = True
    while maybe_can_reduce:
        if -1 not in explode(added):
            continue
        if -1 not in split(added):
            continue
        maybe_can_reduce = False
    return added


def explode(fish_number: FishNumber, depth: int = 1) -> List[int]:
    """
    Update fish_number in place, exploding all numbers nested at a depth greater than 4.

    Return value of [-1, -1] indicates no explosion took place.
    """
    explosion_depth = 4
    result = [-1, -1]
    for i, num in enumerate(fish_number):
        if depth == explosion_depth and isinstance(num, list):
            fish_number[i] = 0
            if isinstance(fish_number[1 - i], list):
                update(fish_number[1 - i], i, num[1 - i])
            else:
                fish_number[1 - i] += num[1 - i]
            result = [0, 0]
            result[i] = num[i]
        elif isinstance(num, list):
            update_values = explode(num, depth + 1)
            if -1 not in update_values:
                if isinstance(fish_number[1 - i], list):
                    update(fish_number[1 - i], i, update_values[1 - i])
                else:
                    fish_number[1 - i] += update_values[1 - i]
                result[i] = update_values[i]
                result[1 - i] = 0
        if -1 not in result:
            break
    return result


def update(num: List, i: int, val: int):
    if isinstance(num[i], int):
        num[i] += val
    else:
        update(num[i], i, val)


def split(fish_number: FishNumber) -> List[int]:
    """
    Split the first number > 9.

    Return value of [-1, -1] indicates no split took place.
    """
    result = [-1, -1]
    for i, num in enumerate(fish_number):
        if isinstance(num, list):
            result = split(num)
        elif num > 9:
            fish_number[i] = [num // 2, (num + 1) // 2]
            result = [0, 0]
        if -1 not in result:
            break
    return result


def magnitude(fish_number: FishNumber) -> int:
    if isinstance(fish_number[0], list):
        left = 3 * magnitude(fish_number[0])
    else:
        left = 3 * fish_number[0]
    if isinstance(fish_number[1], list):
        right = 2 * magnitude(fish_number[1])
    else:
        right = 2 * fish_number[1]
    return left + right
