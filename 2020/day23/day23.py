from typing import List

CUP_LABELS = [3, 1, 8, 9, 4, 6, 5, 7, 2]


def play(num_moves, max_cup: int) -> str:
    history = {}
    cups = [cup for cup in CUP_LABELS + list(range(10, max_cup + 1))]
    cur_idx = 0
    for i in range(num_moves):
        cur_cup = cups[cur_idx]
        cups = move_cups(cups, cur_idx)
        cur_idx = (cups.index(cur_cup) + 1) % len(cups)

        # one_idx = cups.index(1)
        # as_str = "-".join([str(cup) for cup in cups[one_idx + 1:] + cups[:one_idx]][:2])
        # if as_str in history:
        #     if i > -1:
        #         print(f"repeat at {i} from {history[as_str]}: {as_str}")
        #     history[as_str].add(i)
        # else:
        #     history[as_str] = {i}

    return after_1(cups)


def move_cups(cups: List[int], cur_idx: int) -> List[int]:
    cur_cup = cups[cur_idx]

    pick1 = cups[(cur_idx + 1) % len(cups)]
    pick2 = cups[(cur_idx + 2) % len(cups)]
    pick3 = cups[(cur_idx + 3) % len(cups)]

    destination = cur_cup - 1 or 9
    while destination in [pick1, pick2, pick3]:
        destination = destination - 1 or 9

    reduced_cups = [cup for cup in cups if cup not in [pick1, pick2, pick3]]
    dest_idx = reduced_cups.index(destination)
    cups = reduced_cups[:dest_idx + 1] + [pick1, pick2, pick3] + reduced_cups[dest_idx + 1:]

    return cups


def after_1(cups: List[int], cutoff: int = 2) -> str:
    one_idx = cups.index(1)
    return "-".join([str(cup) for cup in cups[one_idx + 1:] + cups[:one_idx]][:cutoff])


if __name__ == "__main__":
    from time import time
    start = time()
    print(play(200, 1_000_000))
    print("RUNTIME:", time() - start)
