"""
Part 1 answer: 11720
Part 2 answer: ERCREPCJ
"""
from y2022.python.shared import get_data_file_path

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 6

SCREEN = []


def draw_screen():
    print("\n".join("".join(row) for row in SCREEN))


def find_signal_strength(instructions: list[str], check_cycles: list[int]) -> int:
    register_x = 1
    cycle = 1
    signal_strength = 0
    for line in instructions:
        if not check_cycles:
            break
        instruction = line.strip().split()
        if instruction[0] == "noop":
            new_register_val = register_x
            ticks = 1
        else:
            new_register_val = register_x + int(instruction[1])
            ticks = 2
        if cycle == check_cycles[-1] or cycle + 1 == check_cycles[-1]:
            signal_strength += check_cycles.pop() * register_x
        register_x = new_register_val
        cycle += ticks
    return signal_strength


def draw_image(instructions: list[str]):
    global SCREEN
    register_x = 1
    cycle = 1
    sprite_pos = {register_x - 1, register_x, register_x + 1}
    screen_row = [" " for _ in range(SCREEN_WIDTH)]
    for line in instructions:
        instruction = line.strip().split()
        if cycle - 1 in sprite_pos:
            screen_row[cycle - 1] = "#"
        if instruction[0] == "noop":
            cycle += 1
        else:
            if cycle in sprite_pos:
                screen_row[cycle] = "#"
            register_x += int(instruction[1])
            cycle += 2
            sprite_pos = {register_x - 1, register_x, register_x + 1}
        if cycle >= SCREEN_WIDTH:
            SCREEN.append(screen_row)
            screen_row = [" " for _ in range(SCREEN_WIDTH)]
            cycle = cycle % SCREEN_WIDTH


def main():
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        instructions = f_in.readlines()
        signal_strength = find_signal_strength(
            instructions, [220, 180, 140, 100, 60, 20]
        )
        draw_image(instructions)
    print("PART 1:", signal_strength)
    print("PART 2:")
    draw_screen()


if __name__ == "__main__":
    main()
