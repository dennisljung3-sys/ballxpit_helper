import tkinter as tk
from core.gamestate import GameState


HOVER_DELAY_MS = 500

RECIPE_COLORS = [
    "#4aa3ff",  # blå
    "#ffd84a",  # gul
    "#c77dff",  # lila
    "#4aff9c",  # grön
]


class BallXPitApp:
    def __init__(self, root, state: GameState):
        self.root = root
        self.root.title("Ball x Pit")

        self.state = state

        self.buttons = {}              # ball_id -> list[Button]
        self.inventory_buttons = {}    # ball_id -> Button
        self.selected = set()

        # hover state
        self.hover_after_id = None
        self.hover_target = None

        self.build_ui()
        self.refresh_all()

    # -------------------------------------------------
    # UI BUILD
    # -------------------------------------------------
    def build_ui(self):
        self.stage1_frame = self._make_section("Stage 1")
        self.stage23_frame = self._make_section("Stage 2 + 3")
        self.inventory_frame = self._make_section("Inventory")

        self.stage1_frame.pack(fill="x", padx=10, pady=5)
        self.stage23_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.inventory_frame.pack(fill="x", padx=10, pady=5)

        self.combine_btn = tk.Button(
            self.inventory_frame,
            text="Combine selected",
            command=self.combine_selected
        )
        self.combine_btn.pack(pady=5)

    def _make_section(self, title):
        return tk.LabelFrame(self.root, text=title, padx=5, pady=5)

    # -------------------------------------------------
    # RENDER
    # -------------------------------------------------
    def refresh_all(self):
        self._clear_frames()
        self._render_stage1()
        self._render_stage23()
        self._render_inventory()
        self._update_selection_visuals()

    def _clear_frames(self):
        for frame in (self.stage1_frame, self.stage23_frame, self.inventory_frame):
            for widget in frame.winfo_children():
                if widget != self.combine_btn:
                    widget.destroy()

        self.buttons.clear()
        self.inventory_buttons.clear()

    def _render_stage1(self):
        balls = self.state.get_balls_by_stage("stage_1")
        self._render_ball_grid(
            self.stage1_frame,
            balls,
            cols=6,
            click_action=self.add_to_inventory
        )

    def _render_stage23(self):
        balls = (
            self.state.get_balls_by_stage("stage_2")
            + self.state.get_balls_by_stage("stage_3")
        )

        self._render_ball_grid(
            self.stage23_frame,
            balls,
            cols=6,
            click_action=None,
            hover=True
        )

    def _render_inventory(self):
        for ball_id in self.state.get_inventory():
            btn = self._make_ball_button(
                self.inventory_frame,
                ball_id,
                left=lambda b=ball_id: self.toggle_select(b),
                right=lambda b=ball_id: self.remove_from_inventory(b)
            )
            self.inventory_buttons[ball_id] = btn
            btn.pack(side="left", padx=2, pady=2)

    def _render_ball_grid(self, frame, balls, cols, click_action=None, hover=False):
        for i, ball_id in enumerate(balls):
            btn = self._make_ball_button(
                frame,
                ball_id,
                left=(lambda b=ball_id: click_action(
                    b)) if click_action else None
            )

            if hover:
                btn.bind("<Enter>", lambda e,
                         b=ball_id: self.on_hover_enter(b))
                btn.bind("<Leave>", lambda e: self.on_hover_leave())

            btn.grid(row=i // cols, column=i % cols, padx=2, pady=2)

    # -------------------------------------------------
    # BUTTON FACTORY
    # -------------------------------------------------
    def _make_ball_button(self, parent, ball_id, left=None, right=None):
        btn = tk.Button(
            parent,
            text=ball_id,
            width=16,
            relief="raised",
            bg="lightgray",
            highlightthickness=1,
            highlightbackground="black"
        )

        if left:
            btn.config(command=left)
        if right:
            btn.bind("<Button-3>", lambda e: right())

        self.buttons.setdefault(ball_id, []).append(btn)
        return btn

    # -------------------------------------------------
    # INVENTORY ACTIONS
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
        self._update_selection_visuals()

    # -------------------------------------------------
    # COMBINE
    # -------------------------------------------------
    def combine_selected(self):
        if len(self.selected) < 2:
            return

        result = self.state.combine(list(self.selected))
        self.selected.clear()
        self.refresh_all()

    # -------------------------------------------------
    # SELECTION VISUALS
    # -------------------------------------------------
    def _update_selection_visuals(self):
        for ball_id, btn in self.inventory_buttons.items():
            if ball_id in self.selected:
                btn.config(bg="skyblue")
            else:
                btn.config(bg="lightgray")

    # -------------------------------------------------
    # HOVER LOGIC
    # -------------------------------------------------
    def on_hover_enter(self, ball_id):
        self.hover_target = ball_id
        self.hover_after_id = self.root.after(
            HOVER_DELAY_MS,
            lambda: self._apply_hover_highlights(ball_id)
        )

    def on_hover_leave(self):
        if self.hover_after_id:
            self.root.after_cancel(self.hover_after_id)
            self.hover_after_id = None

        self.hover_target = None
        self._clear_hover_highlights()

    def _clear_hover_highlights(self):
        for btns in self.buttons.values():
            for btn in btns:
                btn.config(highlightbackground="black", highlightthickness=1)

    def _apply_hover_highlights(self, target_ball):
        self._clear_hover_highlights()

        recipes = self.state.get_recipes_for_ball(target_ball)
        inventory = set(self.state.get_inventory())

        usage_count = {}

        for idx, recipe in enumerate(recipes):
            color = RECIPE_COLORS[idx % len(RECIPE_COLORS)]

            for ball in recipe:
                usage_count[ball] = usage_count.get(ball, 0) + 1

                # inventory först
                targets = []
                if ball in self.inventory_buttons:
                    targets = [self.inventory_buttons[ball]]
                else:
                    targets = self.buttons.get(ball, [])

                for btn in targets:
                    btn.config(
                        highlightbackground=color,
                        highlightthickness=3
                    )

        # randig effekt (simulerad)
        for ball, count in usage_count.items():
            if count > 1:
                for btn in self.buttons.get(ball, []) + [self.inventory_buttons.get(ball)]:
                    if btn:
                        btn.config(highlightthickness=5)
