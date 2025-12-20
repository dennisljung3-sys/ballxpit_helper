# gui/app.py
import tkinter as tk
from PIL import Image, ImageTk
import os
from core.gamestate import GameState


HOVER_DELAY_MS = 500
IMG_SIZE = 80


class BallXPitApp:
    def __init__(self, root, state: GameState):
        self.root = root
        self.state = state
        self.root.title("Ball x Pit")

        # gui state
        self.buttons = {}              # ball_id -> list[Button]
        self.inventory_buttons = {}    # ball_id -> Button
        self.selected = set()
        self.images = {}
        self.hover_after_id = None
        self.hover_ball = None

        self._load_images()
        self._build_ui()
        self.refresh_all()

    # -------------------------------------------------
    # IMAGES
    # -------------------------------------------------
    def _load_images(self):
        for ball_id in self.state.get_all_balls():
            path = os.path.join("images", self.state.get_ball_image(ball_id))
            if not os.path.exists(path):
                continue
            img = Image.open(path).convert("RGBA")
            img = img.resize((IMG_SIZE, IMG_SIZE), Image.NEAREST)
            self.images[ball_id] = ImageTk.PhotoImage(img)

    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    def _build_ui(self):
        self.stage1_frame = tk.LabelFrame(self.root, text="Stage 1")
        self.stage23_frame = tk.LabelFrame(self.root, text="Stage 2 + 3")
        self.inventory_frame = tk.LabelFrame(self.root, text="Inventory")

        self.stage1_frame.pack(fill="x", padx=6, pady=4)
        self.stage23_frame.pack(fill="both", expand=True, padx=6, pady=4)
        self.inventory_frame.pack(fill="x", padx=6, pady=4)

        self.combine_btn = tk.Button(
            self.inventory_frame, text="Combine selected",
            command=self.combine_selected
        )
        self.combine_btn.pack(pady=4)

    # -------------------------------------------------
    # RENDER
    # -------------------------------------------------
    def refresh_all(self):
        self._clear_frames()
        self._render_stage1()
        self._render_stage23()
        self._render_inventory()
        self._update_selection_visuals()
        self._update_recipe_highlights()
        self.highlight_stage1_candidates()

    def _clear_frames(self):
        for frame in (self.stage1_frame, self.stage23_frame, self.inventory_frame):
            for w in frame.winfo_children():
                if w is not self.combine_btn:
                    w.destroy()
        self.buttons.clear()
        self.inventory_buttons.clear()

    def _render_stage1(self):
        balls = self.state.get_balls_by_stage("stage_1")
        self._render_grid(
            self.stage1_frame, balls, cols=9,
            left=self.add_to_inventory
        )

    def _render_stage23(self):
        balls = (
            self.state.get_balls_by_stage("stage_2")
            + self.state.get_balls_by_stage("stage_3")
        )
        self._render_grid(
            self.stage23_frame, balls, cols=11,
            hover=True
        )

    def _render_inventory(self):
        for ball_id in self.state.get_inventory():
            btn = self._make_button(
                self.inventory_frame,
                ball_id,
                left=lambda b=ball_id: self.toggle_select(b),
                right=lambda b=ball_id: self.remove_from_inventory(b),
            )
            btn.pack(side="left", padx=2, pady=2)
            self.inventory_buttons[ball_id] = btn

    def _render_grid(self, frame, balls, cols, left=None, hover=False):
        for i, ball_id in enumerate(balls):
            btn = self._make_button(
                frame,
                ball_id,
                left=(lambda b=ball_id: left(b)) if left else None,
                hover=hover
            )
            btn.grid(row=i // cols, column=i % cols, padx=2, pady=2)

    # -------------------------------------------------
    # BUTTONS
    # -------------------------------------------------
    def _make_button(self, parent, ball_id, left=None, right=None, hover=False):
        btn = tk.Button(
            parent,
            image=self.images.get(ball_id),
            width=IMG_SIZE,
            height=IMG_SIZE,
            relief="raised",
            bg="#dddddd",
            highlightthickness=6,
            highlightbackground="#dddddd"
        )

        if left:
            btn.config(command=left)
        if right:
            btn.bind("<Button-3>", lambda e: right())

        if hover:
            btn.bind("<Enter>", lambda e, b=ball_id: self._hover_start(b))
            btn.bind("<Leave>", lambda e: self._hover_cancel())

        self.buttons.setdefault(ball_id, []).append(btn)
        return btn

    # -------------------------------------------------
    # INVENTORY
    # -------------------------------------------------
    def add_to_inventory(self, ball_id):
        self.state.add_to_inventory(ball_id)
        self.refresh_all()

    def remove_from_inventory(self, ball_id):
        self.state.remove_ball(ball_id)
        self.selected.discard(ball_id)
        self.refresh_all()

    def toggle_select(self, ball_id):
        if ball_id in self.selected:
            self.selected.remove(ball_id)
        else:
            self.selected.add(ball_id)
        self.refresh_all()

    # -------------------------------------------------
    # COMBINE
    # -------------------------------------------------
    def combine_selected(self):
        if len(self.selected) < 2:
            return
        self.state.combine(list(self.selected))
        self.selected.clear()
        self.refresh_all()

    # -------------------------------------------------
    # VISUALS
    # -------------------------------------------------
    def _update_selection_visuals(self):
        for ball_id, btn in self.inventory_buttons.items():
            if ball_id in self.selected:
                btn.config(
                    bg="#88cfff",
                    highlightthickness=6,      # ← ÄNDRA HÄR
                    highlightbackground="#88cfff"
                )
            else:
                btn.config(
                    bg="#dddddd",
                    highlightthickness=1,      # ← ÄNDRA HÄR
                    highlightbackground="#888888"
                )

    def _reset_highlights(self):
        for btns in self.buttons.values():
            for btn in btns:
                btn.config(highlightbackground="#dddddd")

    def _update_recipe_highlights(self):
        inv = set(self.state.get_inventory())

        for target, btns in self.buttons.items():
            recipes = self.state.get_recipes_for_ball(target)

            has_complete = False
            has_partial = False

            for recipe in recipes:
                rset = set(recipe)

                if rset.issubset(inv):
                    has_complete = True
                    break  # GRÖN slår allt
                elif rset & inv:
                    has_partial = True

            if has_complete:
                color = "lightgreen"
            elif has_partial:
                color = "gold"
            else:
                continue

            for btn in btns:
                btn.config(highlightbackground=color)

    def highlight_stage1_candidates(self):
        inv = set(self.state.get_inventory())
        needed = set()

        for recipes in self.state.combinations.values():
            for recipe in recipes:
                rset = set(recipe)
                if rset & inv:
                    needed |= (rset - inv)

        for ball in needed:
            if self.state.get_ball_stage(ball) == 1:
                for btn in self.buttons.get(ball, []):
                    btn.config(highlightbackground="gold")

    # -------------------------------------------------
    # HOVER
    # -------------------------------------------------
    def _hover_start(self, ball_id):
        self._hover_cancel()
        self.hover_ball = ball_id
        self.hover_after_id = self.root.after(
            HOVER_DELAY_MS,
            lambda: self._apply_hover(ball_id)
        )

    def _hover_cancel(self):
        if self.hover_after_id:
            self.root.after_cancel(self.hover_after_id)
        self.hover_after_id = None
        self.hover_ball = None
        self._reset_highlights()
        self._update_recipe_highlights()
        self.highlight_stage1_candidates()

    def _apply_hover(self, ball_id):
        self._reset_highlights()
        recipes = self.state.get_recipes_for_ball(ball_id)
        inv = set(self.state.get_inventory())

        palette = ["#4fa3ff", "#ffd24f"]
        usage = {}

        for i, recipe in enumerate(recipes):
            color = palette[i % len(palette)]
            for b in recipe:
                usage.setdefault(b, set()).add(color)

        for b, colors in usage.items():
            if len(colors) > 1:
                final = "#b266ff"  # lila
            else:
                final = list(colors)[0]

            # prioritera inventory
            targets = []
            if b in self.inventory_buttons:
                targets = [self.inventory_buttons[b]]
            else:
                targets = self.buttons.get(b, [])

            for btn in targets:
                btn.config(highlightbackground=final)
