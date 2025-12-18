import json
from collections import Counter
from pathlib import Path


class GameState:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

        self.balls = self._load_json("balls.json")
        self.combinations = self._load_json("combinations.json")

        self.inventory = Counter()

    def _load_json(self, filename):
        with open(self.data_dir / filename, "r", encoding="utf-8") as f:
            return json.load(f)

    # ------------------------
    # Inventory management
    # ------------------------

    def add_ball(self, ball_name, amount=1):
        self.inventory[ball_name] += amount

    def remove_ball(self, ball_name, amount=1):
        if self.inventory[ball_name] >= amount:
            self.inventory[ball_name] -= amount
            if self.inventory[ball_name] == 0:
                del self.inventory[ball_name]

    def has_ball(self, ball_name, amount=1):
        return self.inventory.get(ball_name, 0) >= amount

    # ------------------------
    # Combination logic
    # ------------------------

    def can_build(self, recipe):
        needed = Counter(recipe)
        return all(self.inventory[b] >= c for b, c in needed.items())

    def missing_for_recipe(self, recipe):
        needed = Counter(recipe)
        missing = {}
        for ball, count in needed.items():
            have = self.inventory.get(ball, 0)
            if have < count:
                missing[ball] = count - have
        return missing

    def possible_combinations(self):
        """Return all buildable results"""
        results = []
        for result, recipes in self.combinations.items():
            for recipe in recipes:
                if self.can_build(recipe):
                    results.append((result, recipe))
        return results

    def near_combinations(self, max_missing=1):
        """Return combinations missing N balls"""
        near = []
        for result, recipes in self.combinations.items():
            for recipe in recipes:
                missing = self.missing_for_recipe(recipe)
                if 0 < sum(missing.values()) <= max_missing:
                    near.append((result, recipe, missing))
        return near

    # ------------------------
    # Execute combination
    # ------------------------

    def combine(self, recipe, result):
        if not self.can_build(recipe):
            return False

        for ball in recipe:
            self.remove_ball(ball)

        self.add_ball(result)
        return True
