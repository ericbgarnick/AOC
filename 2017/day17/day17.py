from spinlock import Spinlock

if __name__ == '__main__':
    data_file = '/Users/ericgarnick/PycharmProjects/AOC/day16/data16.txt'
    instructions = open(data_file, 'r').readline().strip()

    sl = Spinlock(363, 50000000, remember_first=True)
    sl.consume()

    nearby = sl.buffer[sl.cur_position - 3: sl.cur_position + 4]

    # print("At {} in {}".format(sl.cur_position, nearby))
    print("First value:", sl.first_val)
