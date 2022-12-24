"""
Part 1 answer: 14375
Part 2 answer: 10274
"""
from y2022.python.shared import get_data_file_path

SELF_SHAPES = "XYZ"
OPPONENT_SHAPES = "ABC"

WIN_SCORE = 6
DRAW_SCORE = 3
LOSE_SCORE = 0


def main():
    wrong_score = 0
    right_score = 0
    with open(get_data_file_path(__file__.split("/")[-1]), "r") as f_in:
        for line in f_in:
            opponent_shape, other_value = line.strip().split()
            wrong_score += score_round_wrong(opponent_shape, other_value)
            right_score += score_round_right(opponent_shape, other_value)
    print("PART 1:", wrong_score)
    print("PART 2:", right_score)


def score_round_wrong(opponent_shape: str, self_shape: str) -> int:
    opponent_idx = OPPONENT_SHAPES.index(opponent_shape)
    self_idx = SELF_SHAPES.index(self_shape)

    score = self_idx + 1
    if (opponent_idx + 1) % len(SELF_SHAPES) == self_idx:
        score += WIN_SCORE
    elif opponent_idx == self_idx:
        score += DRAW_SCORE

    return score


def score_round_right(opponent_shape: str, outcome: str) -> int:
    opponent_idx = OPPONENT_SHAPES.index(opponent_shape)

    if outcome == "X":
        self_idx = (opponent_idx - 1) % len(SELF_SHAPES)
        score = LOSE_SCORE
    elif outcome == "Y":
        self_idx = opponent_idx
        score = DRAW_SCORE
    else:
        self_idx = (opponent_idx + 1) % len(SELF_SHAPES)
        score = WIN_SCORE

    score += self_idx + 1

    return score


if __name__ == "__main__":
    main()
