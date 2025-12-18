import json
from collections import Counter

BALLS_FILE = "balls.json"
COMBOS_FILE = "evolved_combinations_normalized.json"


def load_data():
    with open(BALLS_FILE, "r", encoding="utf-8") as f:
        balls = json.load(f)

    with open(COMBOS_FILE, "r", encoding="utf-8") as f:
        combos = json.load(f)

    return balls, combos


def inventory_counter(inventory):
    """
    Räknar hur många av varje boll vi har
    """
    return Counter(inventory)


# -----------------------------
# 🔍 A. Vad kan byggas NU?
# -----------------------------
def buildable_now(inventory, combos):
    inv = inventory_counter(inventory)
    result = []

    for result_ball, recipes in combos.items():
        for recipe in recipes:
            recipe_count = Counter(recipe)

            if all(inv[b] >= recipe_count[b] for b in recipe_count):
                result.append((result_ball, recipe))

    return result


# -----------------------------
# 🔍 B. Vad är nära att byggas?
# (exakt 1 sak saknas)
# -----------------------------
def almost_buildable(inventory, combos):
    inv = inventory_counter(inventory)
    result = []

    for result_ball, recipes in combos.items():
        for recipe in recipes:
            recipe_count = Counter(recipe)

            missing = []
            for ball, needed in recipe_count.items():
                have = inv.get(ball, 0)
                if have < needed:
                    missing.extend([ball] * (needed - have))

            if len(missing) == 1:
                result.append((result_ball, recipe, missing[0]))

    return result


# -----------------------------
# 🔁 C. Kombinera
# -----------------------------
def combine(inventory, result_ball, recipe):
    inv = inventory_counter(inventory)
    recipe_count = Counter(recipe)

    # kontroll
    for ball, count in recipe_count.items():
        if inv[ball] < count:
            raise ValueError("Receptet kan inte byggas")

    # ta bort ingredienser
    for ball, count in recipe_count.items():
        for _ in range(count):
            inventory.remove(ball)

    # lägg till resultat
    inventory.append(result_ball)

    return inventory


# -----------------------------
# 🧪 DEMO / TEST
# -----------------------------
def main():
    balls, combos = load_data()

    inventory = [
        "iron_ball",
        "ghost_ball",
        "dark_ball",
    ]

    print("\n📦 INVENTORY:")
    print(inventory)

    print("\n✅ KAN BYGGAS NU:")
    for ball, recipe in buildable_now(inventory, combos):
        print(f"  → {ball}  via {recipe}")

    print("\n🟡 NÄRA ATT BYGGAS (1 sak saknas):")
    for ball, recipe, missing in almost_buildable(inventory, combos):
        print(f"  → {ball} via {recipe} (saknar {missing})")

    print("\n🔁 TESTAR KOMBINERING:")
    buildable = buildable_now(inventory, combos)
    if buildable:
        ball, recipe = buildable[0]
        inventory = combine(inventory, ball, recipe)
        print(f"Byggde {ball}")
        print("Nytt inventory:", inventory)


if __name__ == "__main__":
    main()
