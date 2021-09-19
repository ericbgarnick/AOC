import sys

from paint_robot import PaintRobot


if __name__ == '__main__':
    data_file = sys.argv[1]
    data = [int(x) for x in open(data_file, 'r').read().strip().split(',')]

    robot = PaintRobot()
    robot.paint(data)
    num_painted = len(robot.painted)

    print(f"PART 1:\n{num_painted} spaces painted")
    robot.display()
