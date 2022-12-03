from functools import reduce
from sys import argv
from typing import Dict

TEASPOON_LIMIT = 101


def parse_input(filename: str) -> Dict[str, Dict[str, int]]:
    ingredient_properties = {}
    for line in open(filename, "r"):
        ingredient, properties = line.strip().split(": ")
        prop_values = {
            prop: int(val) for prop, val
            in [pair.split() for pair in properties.split(", ")]
        }
        ingredient_properties[ingredient.lower()] = prop_values
    return ingredient_properties


def find_best_recipe(
        ingredient_properties: Dict[str, Dict[str, int]],
        max_calories: int = 0,
) -> int:
    best_score = 0
    for f in range(1, TEASPOON_LIMIT - 3):
        for c in range(1, TEASPOON_LIMIT - f - 2):
            for b in range(1, TEASPOON_LIMIT - (f + c) - 1):
                s = TEASPOON_LIMIT - 1 - (f + c + b)
                recipe = {"frosting": f, "candy": c, "butterscotch": b, "sugar": s}
                if max_calories:
                    possible_recipe = total_calories(ingredient_properties, recipe) == max_calories
                else:
                    possible_recipe = True
                if possible_recipe:
                    best_score = max(best_score, score_recipe(ingredient_properties, recipe))
    return best_score


def total_calories(
        ingredient_properties: Dict[str, Dict[str, int]],
        recipe: Dict[str, int],
) -> int:
    return sum(
        ingredient_properties[ingredient]["calories"] * amt
        for ingredient, amt
        in recipe.items()
    )


def score_recipe(
        ingredient_properties: Dict[str, Dict[str, int]],
        recipe: Dict[str, int],
) -> int:
    property_totals = {
        "capacity": 0,
        "durability": 0,
        "flavor": 0,
        "texture": 0,
    }
    for ingredient, amount in recipe.items():
        for prop in property_totals.keys():
            property_totals[prop] += ingredient_properties[ingredient][prop] * amount

    for prop, val in property_totals.items():
        property_totals[prop] = max(val, 0)

    return reduce(lambda x, y: x * y, property_totals.values())


if __name__ == "__main__":
    try:
        input_file = argv[1]
        parsed = parse_input(input_file)
        print("PART 1:", find_best_recipe(parsed))
        print("PART 2:", find_best_recipe(parsed, 500))
    except IndexError:
        print("Enter path to data file!")
