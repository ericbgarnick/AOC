from dance_master import DanceMaster
from simplifier import Simplifier

if __name__ == '__main__':
    data_file = '/Users/ericgarnick/PycharmProjects/AOC/day16/data16.txt'
    instructions = open(data_file, 'r').readline().strip()

    sfr = Simplifier(instructions)
    sfr.simplify()
    instructions = sfr.instructions

    dance_master = DanceMaster()
    dance_master.dance.call_dance(instructions, {'p'})

    post_pair_dancers = ''.join(dance_master.dance.dancers)

    dance_master = DanceMaster(post_pair_dancers)
    dance_master.dance.call_dance(instructions, {'s', 'x'})
    dance_master.find_conversion()

    print(''.join(dance_master.dance.dancers))

    # dance_master.find_repeat(instructions)
