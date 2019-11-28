import argparse

from duet import NaiveDuet, RealDuet


def parse_duet_args() -> argparse.Namespace:
    """Parse args for 'naive' ('n') or 'real' ('n') Duet."""
    parser = argparse.ArgumentParser()

    parser.add_argument('--type', choices={'n', 'naive', 'r', 'real'},
                        required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--input')

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_duet_args()

    data = open(args.source, 'r').read().split('\n')

    if args.type in {'n', 'naive'}:
        duet = NaiveDuet(data)
        duet.run()
    else:
        duet0 = RealDuet(data, 0)
        duet1 = RealDuet(data, 1, partner=duet0)
        duet0.set_partner(duet1)

        counter = 0
        send_count = 0
        while not (duet0.done and duet1.done) and counter < 3:
            for duet in [duet0, duet1]:
                # print("BEFORE")
                # print("registers: {}".format(duet._registers))
                # print("BUFFER:", duet._buffer)
                duet.run()
                # print("\nAFTER")
                # print("registers: {}".format(duet._registers))
                # print("BUFFER:", duet._buffer)
                # print("\n----------------\n")
            # print("================\n")
            # print("1 send count:", duet1.send_count)
            # print("1 send diff:", duet1.send_count - send_count)
            # send_count = duet1.send_count
            counter += 1
            if not counter % 1:
                print("-----------\n{} CYCLES".format(counter))
                for d in [duet0, duet1]:
                    print("-----------\nPID {} at {} registers: {}\nbuffer: {}"
                          .format(d._pid, d._instruction_index, d._registers,
                                  d._buffer))

        print("Ended at {}".format(duet1._instruction_index))
        print("Duet 1 sent {}".format(duet1.send_count))
