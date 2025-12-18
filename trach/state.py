class GameState:
    def __init__(self):
        self.inventory = []          # list[str]
        self.selected = set()         # max 2 i GUI

    def add_ball(self, ball: str):
        self.inventory.append(ball)

    def remove_ball(self, ball: str):
        if ball in self.inventory:
            self.inventory.remove(ball)

    def toggle_select(self, ball: str):
        if ball in self.selected:
            self.selected.remove(ball)
        elif len(self.selected) < 2:
            self.selected.add(ball)
