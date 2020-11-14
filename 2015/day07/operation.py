MASK = (1 << 16) - 1


def op_not(val: int) -> int:
    return MASK & ~val


def op_and(a: int, b: int) -> int:
    return MASK & (a & b)


def op_or(a: int, b: int) -> int:
    return MASK & (a | b)


def op_lshift(val: int, offset: int) -> int:
    return MASK & (val << offset)


def op_rshift(val: int, offset: int) -> int:
    return MASK & (val >> offset)
