import sys
import opcodes6
from typing import Tuple, List


Instruction = Tuple[str, int, int, int]


def parse_file(data_file_name: str) -> Tuple[int, List[Instruction]]:
    instructions = []
    with open(data_file_name, 'r') as f_in:
        i_ptr = int(f_in.readline().strip().split()[-1])
        for row in f_in:
            instr, a, b, c = row.strip().split()
            instructions.append((instr, int(a), int(b), int(c)))
    return i_ptr, instructions


if __name__ == '__main__':
    file_name = sys.argv[1]
    ip_reg, instr_list = parse_file(file_name)
    idx2 = 10551276
    registers = [0, 1, idx2, 0, 2, 10551276]
    ip = 3
    last_counter = counter = 0
    last_3 = [0, 1, idx2, 0, 2, 10551276]
    while 0 <= ip < len(instr_list):
        instr_line = instr_list[ip]
        fn_name, a, b, c = instr_line
        fn = getattr(opcodes6, fn_name)
        registers[ip_reg] = ip
        registers = fn(registers, [a, b, c])
        ip = registers[ip_reg] + 1
        counter += 1
        if ip == 3:
            idx2 += 1
            if registers != [0, 1, idx2, 0, 2, 10551276]:
                print("RAN {} ITERATIONS. REGISTER 0: {}. POINTER AT: {}, REGISTERS: {}"
                      .format(counter, registers[0], ip, registers))

        # if ip == 4 and counter >= last_counter + 10000000:
        #     last_counter = counter
        # print("RAN {} ITERATIONS. REGISTER 0: {}. POINTER AT: {}, REGISTERS: {}"
        #       .format(counter, registers[0], ip, registers))
        if counter == 16:
            print("RAN {} ITERATIONS. REGISTER 0: {}. POINTER AT: {}, REGISTERS: {}"
                  .format(counter, registers[0], ip, registers))
        # if registers[3] == registers[5]:
        #     print("3 and 5 are equal at loop", counter)
        # if counter == 100000100:
            break
    print(registers[0])
