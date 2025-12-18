def can_build(recipe, inventory):
    return all(inventory.count(b) >= recipe.count(b) for b in recipe)


def missing_ingredients(recipe, inventory):
    missing = []
    for b in recipe:
        if inventory.count(b) < recipe.count(b):
            missing.append(b)
    return missing
