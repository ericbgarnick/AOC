from sys import argv
from typing import Tuple, List, Dict


# == SHARED == #
def record_foods(filename: str) -> Dict:
    food_record = associate_allergens_with_ingredients(filename)
    record_invalid_allergens(**food_record)
    return food_record


def associate_allergens_with_ingredients(filename: str) -> Dict[str, Dict]:
    """Return a dict:
    {
      'ingredients': {
        <ingredient>: {
          'count': <count>,
          'assoc_als': {<allergen>, ...},
          'invalid_als': {<allergen>, ...}
        }
      },
      'allergens': {
        <allergen>: {
          'count': <count>,
          <ingredient>: <count>,
          ...
        }
      }
    }
    """
    ingredient_record = {}
    allergen_record = {}
    for line in open(filename, "r"):
        ingredients, allergens = parse_line(line)
        for al in allergens:
            try:
                allergen_record[al]["count"] += 1
            except KeyError:
                allergen_record[al] = {"count": 1}
            for ingr in ingredients:
                try:
                    allergen_record[al][ingr] += 1
                except KeyError:
                    allergen_record[al][ingr] = 1
                try:
                    ingredient_record[ingr]["assoc_als"].add(al)
                except KeyError:
                    ingredient_record[ingr] = {"count": 0, "assoc_als": {al}, "invalid_als": set()}

        for ingr in ingredients:
            ingredient_record[ingr]["count"] += 1

    return {"ingredients": ingredient_record, "allergens": allergen_record}


def parse_line(line: str) -> Tuple[List[str], List[str]]:
    """Return a pair of lists: (ingredients, allergens)"""
    raw_ingredients, raw_allergens = line.strip("\n)").split(" (contains ")
    return raw_ingredients.split(), raw_allergens.split(", ")


def record_invalid_allergens(ingredients: Dict, allergens: Dict):
    """Update ingredients dict with allergens it cannot contain."""
    for al in allergens.keys():
        for key, count in allergens[al].items():
            if key != "count" and allergens[al][key] < allergens[al]["count"]:
                ingredients[key]["invalid_als"].add(al)


# == PART 1 == #
def count_inert_ingredients(ingredients: Dict) -> int:
    """Return the total number of occurrences of any ingredient that is not associated with an allergen."""
    count = 0
    for ingredient, ingredient_info in ingredients.items():
        if not ingredient_info["assoc_als"] - ingredient_info["invalid_als"]:
            count += ingredient_info["count"]
    return count


# == PART 2 == #
def cdil(ingredients: Dict, allergens: Dict) -> str:
    """Return a comma-separated list of ingredients, in alphabetical order of allergens they contain."""
    identified = identify_allergens(ingredients, allergens)
    return ",".join([identified[al] for al in sorted(identified)])


def identify_allergens(ingredients: Dict, allergens: Dict) -> Dict[str, str]:
    """Return a dict of each allergen mapped to the one ingredient containing that allergen."""
    remove_inert_ingredients(ingredients, allergens)
    known_ingrs = set()
    updated_allergens = {}
    while len(known_ingrs) < len(allergens):
        for al, al_data in allergens.items():
            if len(updated_allergens.get(al, set())) != 1:
                # Haven't identified the ingredient containing this allergen yet
                al_count = al_data["count"]
                candidates = set()
                for key, count in al_data.items():
                    if key != "count" and key not in known_ingrs and count == al_count:
                        candidates.add(key)
                updated_allergens[al] = candidates
                if len(candidates) == 1:
                    known_ingrs.add(min(candidates))
    return {al: ingrs.pop() for al, ingrs in updated_allergens.items()}


def remove_inert_ingredients(ingredients: Dict, allergens: Dict):
    """Update allergens dict, removing any ingredients that have been identified as inert
    (not associated with any allergens)."""
    for ingredient, ingredient_info in ingredients.items():
        if not ingredient_info["assoc_als"] - ingredient_info["invalid_als"]:
            for al_data in allergens.values():
                al_data.pop(ingredient, None)


if __name__ == "__main__":
    input_file = argv[1]
    record = record_foods(input_file)
    print("PART 1:", count_inert_ingredients(record["ingredients"]))
    print("PART 2:", cdil(**record))
