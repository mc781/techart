import arcade
import random

# --- Grid settings ---
GRID_SIZE = 20
CELL_SIZE = 32
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE


class Cat:
    """A wandering cat that moves randomly on a 20x20 grid."""

    def __init__(self):
        self.row = random.randint(0, GRID_SIZE - 1)
        self.col = random.randint(0, GRID_SIZE - 1)
        self.move_timer = 0

    def update(self):
        """Move every 5 frames, staying inside the grid."""
        self.move_timer += 1

        if self.move_timer > 5:
            self.move_timer = 0
            dr, dc = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

            new_r = self.row + dr
            new_c = self.col + dc

            if 0 <= new_r < GRID_SIZE:
                self.row = new_r
            if 0 <= new_c < GRID_SIZE:
                self.col = new_c

    def draw(self):
        """Draw the cat as a pink square in its current cell."""
        left = self.col * CELL_SIZE
        bottom = self.row * CELL_SIZE

        arcade.draw_lbwh_rectangle_filled(
            left,
            bottom,
            CELL_SIZE,
            CELL_SIZE,
            (255, 180, 200),
        )


class CatWindow(arcade.Window):
    """Main window showing the grid and the wandering cat."""

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade Cat Grid")
        self.cat = Cat()
        self.background_color = (30, 30, 30)

    def on_update(self, delta_time: float):
        self.cat.update()

    def on_draw(self):
        # Clear the screen (Arcade 3.3.3+ uses clear(), not start_render())
        self.clear(self.background_color)

        # Draw grid lines
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                left = c * CELL_SIZE
                bottom = r * CELL_SIZE

                arcade.draw_lbwh_rectangle_outline(
                    left,
                    bottom,
                    CELL_SIZE,
                    CELL_SIZE,
                    (60, 60, 60),
                )

        # Draw the cat
        self.cat.draw()


if __name__ == "__main__":
    CatWindow()
    arcade.run()
