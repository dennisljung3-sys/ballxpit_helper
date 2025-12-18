from collections import Counter
from typing import List, Dict


class GameState:
    def __init__(self, balls: list[dict], combinations: dict):
        self.balls: dict[str, dict] = {}

        for ball in balls:
            ball_id = ball["id"]
            stage_num = int(ball["stage"].split("_")[1])

            self.balls[ball_id] = {
                "stage": stage_num,
                "image": ball["image"],
            }

        self.combinations = combinations
        self.inventory: list[str] = []
        self.history: list[str] = []

    # -------------------------
    # INVENTORY
    # -------------------------

    def add_ball(self, ball: str):
        self.inventory.append(ball)
        self.history.append(f"+ {ball}")

    def remove_ball(self, ball: str):
        if ball in self.inventory:
            self.inventory.remove(ball)
            self.history.append(f"- {ball}")

    def get_inventory(self) -> list[str]:
        return list(self.inventory)

    # -------------------------
    # BALL INFO
    # -------------------------

    def get_all_balls(self) -> list[str]:
        return list(self.balls.keys())

    def get_ball_stage(self, ball: str) -> int:
        return self.balls[ball]["stage"]

    def get_ball_image(self, ball: str) -> str:
        return self.balls[ball]["image"]

    # -------------------------
    # RECIPES
    # -------------------------

    def get_recipes_for_ball(self, target_ball: str) -> List[List[str]]:
        return self.combinations.get(target_ball, [])

    # -------------------------
    # ANALYSIS
    # -------------------------

    def can_build(self, recipe: List[str]) -> bool:
        inv = Counter(self.inventory)
        req = Counter(recipe)
        return all(inv[b] >= req[b] for b in req)

    # -------------------------
    # COMBINE (FIXED)
    # -------------------------

    def combine(self, recipe: List[str]) -> str | None:
        recipe_counter = Counter(recipe)

        if not self.can_build(recipe):
            return None

        for evolved, recipes in self.combinations.items():
            for r in recipes:
                if Counter(r) == recipe_counter:
                    # Ta bort använda bollar
                    for ball in recipe:
                        self.inventory.remove(ball)

                    self.add_ball(evolved)
                    self.history.append(f"COMBINE {recipe} -> {evolved}")
                    return evolved

        return None

    # -------------------------
    # STAGE HELPERS (GUI)
    # -------------------------

    def get_balls_by_stage(self, stage: str) -> list[str]:
        stage_num = int(stage.split("_")[1])
        return [
            ball_id
            for ball_id, data in self.balls.items()
            if data["stage"] == stage_num
        ]

    # Alias för GUI
    def add_to_inventory(self, ball: str):
        self.add_ball(ball)
