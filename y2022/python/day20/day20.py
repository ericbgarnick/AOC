"""
Part 1 answer: 10831
Part 2 answer: 6420481789383
"""
from y2022.python.shared import get_data_file_path

DISTANCES = [1000, 2000, 3000]
DECRYPTION_KEY = 811589153
MIX_COUNT = 10


class Link:
    def __init__(self, value: int):
        self.value = value
        self.next: "Link" = self
        self.prev: "Link" = self


def main():
    with open(get_data_file_path(__file__.split("/")[-1], sample=False), "r") as f_in:
        original_vals = [int(line.strip()) for line in f_in]
    # PART 1
    nums = create_loop(original_vals)
    zero = next(link for link in nums if link.value == 0)
    for link in nums:
        mix(link, len(nums))
    print("PART 1:", sum(value_at(zero, d) for d in DISTANCES))
    # PART 2
    nums = create_loop(original_vals, DECRYPTION_KEY)
    zero = next(link for link in nums if link.value == 0)
    for _ in range(MIX_COUNT):
        for link in nums:
            mix(link, len(nums))
    print("PART 2:", sum(value_at(zero, d) for d in DISTANCES))


def create_loop(original_vals: list[int], multiplier: int = 1) -> list[Link]:
    nums = [Link(v * multiplier) for v in original_vals]
    for i in range(len(nums)):
        nums[i].next = nums[(i + 1) % len(nums)]
        nums[i].prev = nums[i - 1]
    return nums


def mix(link: Link, length: int):
    dest = link
    dist = (
        link.value % (length - 1)
        if link.value >= 0
        else abs(link.value) % (length - 1) + 1
    )
    if not dist:
        return
    for _ in range(dist):
        if link.value < 0:
            dest = dest.prev
        else:
            dest = dest.next
    # Repair original location
    link.prev.next, link.next.prev = link.next, link.prev
    # Update shifted link
    link.next, link.prev = dest.next, dest
    # Update new location
    link.next.prev = link
    link.prev.next = link


def value_at(start_link: Link, distance: int) -> int:
    cur_link = start_link
    for _ in range(distance):
        cur_link = cur_link.next
    return cur_link.value


if __name__ == "__main__":
    main()
