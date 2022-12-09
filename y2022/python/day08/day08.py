"""Note: Solution assumes a square grid for the forest."""
from typing import List, Any

from y2022.python.shared import get_data_file_path


def main():
    with open(get_data_file_path(__file__), "r") as f_in:
        forest = []
        for row in f_in:
            forest.append([int(tree) for tree in row.strip()])
    print("PART 1:", count_visible_trees(forest))
    print("PART 2:", calculate_scenic_score(forest))


def count_visible_trees(forest: List[List[int]]) -> int:
    visibility = create_visibility_map(forest, middle_value=0, edge_value=1)

    for i in range(1, len(forest) - 1):
        # scan forward
        f_row_max_hor = forest[i][0]
        f_row_max_ver = forest[0][i]
        for f in range(1, len(forest[i]) - 1):
            f_row_max_hor = update_visibility(forest, visibility, i, f, f_row_max_hor)
            f_row_max_ver = update_visibility(forest, visibility, f, i, f_row_max_ver)
        # scan in reverse
        r_row_max_hor = forest[i][-1]
        r_row_max_ver = forest[-1][i]
        for r in range(len(forest[i]) - 2, 0, -1):
            r_row_max_hor = update_visibility(forest, visibility, i, r, r_row_max_hor)
            r_row_max_ver = update_visibility(forest, visibility, r, i, r_row_max_ver)
    return sum(sum(row) for row in visibility)


def calculate_scenic_score(forest: List[List[int]]) -> int:
    scenic_scores = create_visibility_map(forest, middle_value=1, edge_value=0)

    for i in range(len(forest)):
        # scan forward
        # the last index in the forest row having a tree at least as tall as index in tree_heights
        # i.e. [6, 6, 6, 6, 4. 4. -1. -1. -1, -1]
        #  tree at index 6 is the last tree seen with height 3,
        #  tree at index 4 is the last tree seen with height 5,
        #  no tree has yet been seen with height > 5
        tree_heights_hor = [-1 for _ in range(10)]
        tree_heights_ver = [-1 for _ in range(10)]
        visibility_range_hor = [0 for _ in range(len(forest))]
        visibility_range_ver = [0 for _ in range(len(forest))]
        for f in range(len(forest)):
            update_sight_distance(tree_heights_hor, visibility_range_hor, forest[i][f], f)
            update_sight_distance(tree_heights_ver, visibility_range_ver, forest[f][i], f)
        for h, d in enumerate(visibility_range_hor):
            scenic_scores[i][h] *= d
        for v, d in enumerate(visibility_range_ver):
            scenic_scores[v][i] *= d

        tree_heights_hor = [-1 for _ in range(10)]
        tree_heights_ver = [-1 for _ in range(10)]
        visibility_range_hor = [0 for _ in range(len(forest))]
        visibility_range_ver = [0 for _ in range(len(forest))]
        for r in range(len(forest) - 1, -1, -1):
            tree_height_hor = forest[i][r]
            if tree_heights_hor[tree_height_hor] == -1:
                visibility_range_hor[r] = len(forest) - 1 - r
            else:
                visibility_range_hor[r] = tree_heights_hor[tree_height_hor] - r
            for height in range(tree_height_hor + 1):
                tree_heights_hor[height] = r

            tree_height_ver = forest[r][i]
            if tree_heights_ver[tree_height_ver] == -1:
                visibility_range_ver[r] = len(forest) - 1 - r
            else:
                visibility_range_ver[r] = tree_heights_ver[tree_height_ver] - r
            for height in range(tree_height_ver + 1):
                tree_heights_ver[height] = r
        for h, d in enumerate(visibility_range_hor):
            scenic_scores[i][h] *= d
        for v, d in enumerate(visibility_range_ver):
            scenic_scores[v][i] *= d
    return max(max(row) for row in scenic_scores)


def create_visibility_map(
    forest: List[List[int]], middle_value: int, edge_value: int
) -> List[List[int]]:
    visibility = [[middle_value for _ in range(len(forest))] for _ in range(len(forest))]
    # Update edges
    for i in range(len(visibility)):
        if i == 0 or i + 1 == len(visibility):
            visibility[i] = [edge_value for _ in range(len(visibility))]
        else:
            visibility[i][0] = edge_value
            visibility[i][-1] = edge_value
    return visibility


def update_visibility(
    forest: List[List[int]],
    visibility: List[List[int]],
    row_idx: int,
    col_idx: int,
    max_height: int,
) -> int:
    """
    Return (possibly new) max height and update visibility map if tree is visible.
    """
    tree_height = forest[row_idx][col_idx]
    if tree_height > max_height:
        visibility[row_idx][col_idx] = 1
        max_height = tree_height
    return max_height


def update_sight_distance(
    tree_heights: List[int],
    visibility_range: List[int],
    tree_height: int,
    col_idx: int,
):
    if tree_heights[tree_height] == -1:
        visibility_range[col_idx] = col_idx
    else:
        visibility_range[col_idx] = col_idx - tree_heights[tree_height]
    for height in range(tree_height + 1):
        tree_heights[height] = col_idx

def print_map(forest_map: List[List[Any]]):
    print("\n".join([" ".join([str(tree) for tree in row]) for row in forest_map]))


if __name__ == "__main__":
    main()
