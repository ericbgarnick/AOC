# from sys import argv
#
#
# class Elf:
#     def __init__(self, recipe: int, position: int):
#         self._recipe_number = recipe
#         self._position = position
#
#     @property
#     def recipe_number(self):
#         return self._recipe_number
#
#     @property
#     def position(self):
#         return self._position
#
#     def set_recipe(self, recipe_number: int):
#         self._recipe_number = recipe_number
#
#     def set_position(self, position: int):
#         self._position = position
#
#
# ELVES = [Elf(3, 0), Elf(7, 1)]
#
# NUM_RECIPES = 793061
# NUM_EXTRAS = 10
#
# RECIPES = [e.recipe_number for e in ELVES]
#
#
# def advance_elf(elf: Elf):
#     elf.set_position((elf.position + elf.recipe_number + 1) % len(RECIPES))
#     elf.set_recipe(int(RECIPES[elf.position]))
#
#
# if __name__ == '__main__':
#     part = argv[1]
#
#     if part == '1':
#         while len(RECIPES) < NUM_RECIPES + NUM_EXTRAS:
#             new_recipes = [int(r_num) for r_num in
#                            str(sum(e.recipe_number for e in ELVES))]
#             for r in new_recipes:
#                 RECIPES.append(r)
#             for e in ELVES:
#                 advance_elf(e)
#         print("RECIPES:", RECIPES[NUM_RECIPES:NUM_RECIPES + NUM_EXTRAS])
#
#     elif part == '2':
#         RECIPES = ''.join(str(r) for r in RECIPES)
#         NUM_REC_STR = str(NUM_RECIPES)
#         while RECIPES[-len(NUM_REC_STR):] != NUM_REC_STR:
#             for e in ELVES:
#                 advance_elf(e)
#             to_append = str(sum(e.recipe_number for e in ELVES))
#             RECIPES += to_append
#         print("RECIPES:", len(RECIPES))

# Copied from shared solution on Reddit:
# https://www.reddit.com/r/adventofcode/comments/a61ojp/2018_day_14_solutions/

recipes = '793061'

score = '37'
elf1 = 0
elf2 = 1
while recipes not in score[-7:]:
    score += str(int(score[elf1]) + int(score[elf2]))
    elf1 = (elf1 + int(score[elf1]) + 1) % len(score)
    elf2 = (elf2 + int(score[elf2]) + 1) % len(score)

print('Part 1:', score[int(recipes):int(recipes)+10])
print('Part 2:', score.index(recipes))
