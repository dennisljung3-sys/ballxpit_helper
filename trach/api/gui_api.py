from core.state import GameState
from core.logic import can_build, missing_ingredients
from data_loader import load_balls, load_recipes


class BallXPitAPI:
    def __init__(self):
        self.state = GameState()
        self.balls = load_balls()
        self.recipes = load_recipes()

    # ---- inventory ----

    def add_ball(self, ball):
        self.state.add_ball(ball)
        return self._snapshot()

    def remove_ball(self, ball):
        self.state.remove_ball(ball)
        return self._snapshot()

    def toggle_select(self, ball):
        self.state.toggle_select(ball)
        return self._snapshot()

    # ---- combination ----

    def combine_selected(self):
        if len(self.state.selected) < 2:
            return None

        selected = list(self.state.selected)

        for result, recipes in self.recipes.items():
            for r in recipes:
                if sorted(r) == sorted(selected):
                    # consume
                    for b in selected:
                        self.state.remove_ball(b)
                    self.state.add_ball(result)
                    self.state.selected.clear()
                    return self._snapshot()

        return None

    # ---- analysis ----

    def analyze(self):
        inventory = self.state.inventory
        buildable = {}
        almost = {}

        for result, recipes in self.recipes.items():
            for r in recipes:
                if can_build(r, inventory):
                    buildable.setdefault(result, []).append(r)
                elif len(missing_ingredients(r, inventory)) == 1:
                    almost.setdefault(result, []).append(
                        missing_ingredients(r, inventory)
                    )

        return {
            "buildable": buildable,
            "almost": almost
        }

    # ---- snapshot ----

    def _snapshot(self):
        return {
            "inventory": list(self.state.inventory),
            "selected": list(self.state.selected),
            **self.analyze()
        }
