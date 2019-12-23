import sys

from ascii_system import AsciiSystem

if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]
    ascii_sys = AsciiSystem()
    ascii_sys.run(data)
    print(f"PART 1:\n{ascii_sys.alignment_parameters_sum()}")
