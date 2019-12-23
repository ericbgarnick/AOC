import sys

from ascii_system import AsciiSystem

if __name__ == '__main__':
    data_file = sys.argv[1]
    data1 = [int(x) for x in open(data_file, 'r').read().strip().split(',')]
    ascii_sys = AsciiSystem()
    ascii_sys.run(data1, record_image=True)
    print(f"PART 1:\n{ascii_sys.alignment_parameters_sum()}")
    data2 = [2] + [x for x in data1[1:]]
    ascii_sys.run(data2, record_image=False)
