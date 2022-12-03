from functools import partial
from typing import List, Tuple, Callable, Any


def keep_ith(i: int, *args: List[Any]) -> Any:
    return args[i]


###################
# - GENERIC OPS - #
###################
def opr(registers: List[int],
        instructions: Tuple[int, int, int, int],
        op: Callable) -> List[int]:
    r1, r2, r3 = instructions[1:]
    registers[r3] = int(op(registers[r1], registers[r2]))
    return registers


def opi(registers: List[int],
        instructions: Tuple[int, int, int, int],
        op: Callable) -> List[int]:
    r1, v1, r2 = instructions[1:]
    registers[r2] = int(op(registers[r1], v1))
    return registers


################
# - ADDITION - #
################
def addr(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opr(registers, instructions, int.__add__)


def addi(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opi(registers, instructions, int.__add__)


######################
# - MULTIPLICATION - #
######################
def mulr(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opr(registers, instructions, int.__mul__)


def muli(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opi(registers, instructions, int.__mul__)


###################
# - BITWISE AND - #
###################
def banr(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opr(registers, instructions, int.__and__)


def bani(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opi(registers, instructions, int.__and__)


##################
# - BITWISE OR - #
##################
def borr(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opr(registers, instructions, int.__or__)


def bori(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opi(registers, instructions, int.__or__)


##################
# - ASSIGNMENT - #
##################
def setr(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opr(registers, instructions, partial(keep_ith, 0))


def seti(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    reordered = tuple(instructions[i] for i in [0, 2, 1, 3])
    return opi(registers, reordered, partial(keep_ith, 1))


####################
# - GREATER THAN - #
####################
def gtrr(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opr(registers, instructions, int.__gt__)


def gtri(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opi(registers, instructions, int.__gt__)


def gtir(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    reordered = tuple(instructions[i] for i in [0, 2, 1, 3])
    return opi(registers, reordered, int.__lt__)


################
# - EQUALITY - #
################
def eqrr(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opr(registers, instructions, int.__eq__)


def eqri(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    return opi(registers, instructions, int.__eq__)


def eqir(registers: List[int],
         instructions: Tuple[int, int, int, int]) -> List[int]:
    reordered = tuple(instructions[i] for i in [0, 2, 1, 3])
    return opi(registers, reordered, int.__eq__)


OPS = {15: addr, 4: addi, 6: mulr, 5: muli,
       11: banr, 8: bani, 12: borr, 10: bori,
       2: setr, 0: seti, 7: gtrr, 9: gtri,
       3: gtir, 14: eqrr, 13: eqri, 1: eqir}
