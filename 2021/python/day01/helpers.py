print("My name is:", __name__)


def my_add(val1: int, val2: int) -> int:
    return val1 + val2


my_sum = my_add(1, 2)


def my_subtract():
    pass


my_diff = my_subtract(my_sum, 7)


def my_multiply():
    pass


if __name__ == "__main__":
    print(my_add(5, 7))
