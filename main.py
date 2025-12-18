import json
import tkinter as tk
from gui.app import BallXPitApp
from core.gamestate import GameState


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    balls = load_json("data/balls.json")
    combos = load_json("data/evolved_combinations_normalized.json")

    state = GameState(balls, combos)

    root = tk.Tk()
    app = BallXPitApp(root, state)
    root.mainloop()


if __name__ == "__main__":
    main()
