import sys

from repair_droid import RepairDroid

if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]

    droid = RepairDroid()
    droid.run(data)
