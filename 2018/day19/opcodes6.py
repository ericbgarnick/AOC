from typing import List, Tuple, Callable


Instruction = Tuple[int, int, int]


###################
# - GENERIC OPS - #
###################
def opr(registers: List[int],
        instructions: Instruction,
        op: Callable) -> List[int]:
    r1, r2, r3 = instructions
    registers[r3] = int(op(registers[r1], registers[r2]))
    return registers


def opi(registers: List[int],
        instructions: Instruction,
        op: Callable) -> List[int]:
    r1, v1, r2 = instructions
    registers[r2] = int(op(registers[r1], v1))
    return registers


################
# - ADDITION - #
################
def addr(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = registers[a] + registers[b]
    return registers


def addi(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = registers[a] + b
    return registers


######################
# - MULTIPLICATION - #
######################
def mulr(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = registers[a] * registers[b]
    return registers


def muli(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = registers[a] * b
    return registers


###################
# - BITWISE AND - #
###################
def banr(registers: List[int],
         instructions: Instruction) -> List[int]:
    return opr(registers, instructions, int.__and__)


def bani(registers: List[int],
         instructions: Instruction) -> List[int]:
    return opi(registers, instructions, int.__and__)


##################
# - BITWISE OR - #
##################
def borr(registers: List[int],
         instructions: Instruction) -> List[int]:
    return opr(registers, instructions, int.__or__)


def bori(registers: List[int],
         instructions: Instruction) -> List[int]:
    return opi(registers, instructions, int.__or__)


##################
# - ASSIGNMENT - #
##################
def setr(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = registers[a]
    return registers


def seti(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = a
    return registers


####################
# - GREATER THAN - #
####################
def gtrr(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = int(registers[a] > registers[b])
    return registers


def gtri(registers: List[int],
         instructions: Instruction) -> List[int]:
    return opi(registers, instructions, int.__gt__)


def gtir(registers: List[int],
         instructions: Instruction) -> List[int]:
    reordered = tuple(instructions[i] for i in [1, 0, 2])
    return opi(registers, reordered, int.__lt__)


################
# - EQUALITY - #
################
def eqrr(registers: List[int],
         instructions: Instruction) -> List[int]:
    a, b, c = instructions
    registers[c] = int(registers[a] == registers[b])
    return registers


def eqri(registers: List[int],
         instructions: Instruction) -> List[int]:
    return opi(registers, instructions, int.__eq__)


def eqir(registers: List[int],
         instructions: Instruction) -> List[int]:
    reordered = tuple(instructions[i] for i in [1, 0, 2])
    return opi(registers, reordered, int.__eq__)
