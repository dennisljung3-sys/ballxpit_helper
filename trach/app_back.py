import tkinter as tk
import json
from pathlib import Path
from core.gamestate import GameState


class BallXPitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ball X Pit – Prototype")
        self.root.geometry("1000x700")

        # ---------- Load data ----------
        data_dir = Path("data")

        with open(data_dir / "balls.json", "r", encoding="utf-8") as f:
            balls = json.load(f)

        with open(data_dir / "evolved_combinations_normalized.json", "r", encoding="utf-8") as f:
            combos = json.load(f)

        self.state = GameState(balls, combos)

        # ---------- Test inventory ----------
        self.state.add_ball("iron_ball")
        self.state.add_ball("ghost_ball")

        self.build_ui()

    # ---------- UI ----------
    def build_ui(self):
        container = tk.Frame(self.root, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        # ---------- Stage 1 ----------
        stage1_frame = tk.LabelFrame(container, text="Stage 1", padx=5, pady=5)
        stage1_frame.pack(fill="x", pady=5)

        stage1_balls = self.state.get_balls_by_stage("stage_1")
        self._render_ball_grid(stage1_frame, stage1_balls, cols=6)

        # ---------- Stage 2 + 3 ----------
        stage23_frame = tk.LabelFrame(
            container, text="Stage 2 & 3", padx=5, pady=5
        )
        stage23_frame.pack(fill="both", pady=5)

        stage23_balls = (
            self.state.get_balls_by_stage("stage_2")
            + self.state.get_balls_by_stage("stage_3")
        )
        self._render_ball_grid(stage23_frame, stage23_balls, cols=6)

        # ---------- Inventory ----------
        inventory_frame = tk.LabelFrame(
            container, text="Inventory", padx=5, pady=5
        )
        inventory_frame.pack(fill="x", pady=5)

        inventory = self.state.get_inventory()
        self._render_ball_grid(inventory_frame, inventory, cols=6)

    # ---------- Helpers ----------
    def _render_ball_grid(self, parent, ball_ids, cols=6):
        for idx, ball_id in enumerate(ball_ids):
            row = idx // cols
            col = idx % cols

            btn = tk.Button(
                parent,
                text=ball_id,
                width=20,
                command=lambda b=ball_id: self.on_ball_clicked(b)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="w")

    def on_ball_clicked(self, ball_id: str):
        print(f"[CLICK] {ball_id}")
