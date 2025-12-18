import json
from itertools import combinations

# ---------- Load data ----------

with open("balls.json", "r") as f:
    BALLS = json.load(f)

with open("evolved_combinations_final.json", "r") as f:
    COMBINATIONS = json.load(f)


# ---------- Core logic ----------

def can_build(recipe, inventory):
    """Return True if all balls in recipe exist in inventory"""
    return all(ball in inventory for ball in recipe)


def missing_balls(recipe, inventory):
    """Return list of balls missing from inventory"""
    return [ball for ball in recipe if ball not in inventory]


def find_buildable(inventory):
    """All balls that can be built now"""
    result = []

    for result_ball, recipes in COMBINATIONS.items():
        for recipe in recipes:
            if can_build(recipe, inventory):
                result.append((result_ball, recipe))

    return result


def find_near_buildable(inventory, missing_count=1):
    """Balls that are close to being built"""
    result = []

    for result_ball, recipes in COMBINATIONS.items():
        for recipe in recipes:
            missing = missing_balls(recipe, inventory)
            if len(missing) == missing_count:
                result.append((result_ball, recipe, missing))

    return result


def combine(result_ball, recipe, inventory):
    """Simulate combining balls"""
    new_inventory = set(inventory)

    for ball in recipe:
        new_inventory.remove(ball)

    new_inventory.add(result_ball)
    return new_inventory


# ---------- Demo / Test ----------

def main():
    inventory = {
        "iron_ball",
        "ghost_ball",
        "burn_ball",
    }

    print("Inventory:")
    for b in sorted(inventory):
        print(" ", b)

    print("\nCan build now:")
    for result, recipe in find_buildable(inventory):
        print(f" - {result}  <=  {recipe}")

    print("\nNear to build (1 missing):")
    for result, recipe, missing in find_near_buildable(inventory):
        print(f" - {result}  missing {missing}")

    # simulate combine
    buildable = find_buildable(inventory)
    if buildable:
        result, recipe = buildable[0]
        inventory = combine(result, recipe, inventory)
        print("\nAfter combining:")
        print(sorted(inventory))


if __name__ == "__main__":
    main()
