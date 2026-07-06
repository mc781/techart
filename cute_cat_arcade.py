import arcade
import random

# --- Grid settings ---
GRID_SIZE = 20
CELL_SIZE = 32
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# --- Cat object ---
class Cat:
    def __init__(self):
        self.row = random.randint(0, GRID_SIZE - 1)
        self.col = random.randint(0, GRID_SIZE - 1)
        self.move_timer = 0

    def update(self):
        self.move_timer += 1

        # Move every 15 frames
        if self.move_timer > 15:
            self.move_timer = 0
            dr, dc = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

            new_r = self.row + dr
            new_c = self.col + dc

            if 0 <= new_r < GRID_SIZE:
                self.row = new_r
            if 0 <= new_c < GRID_SIZE:
                self.col = new_c

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        arcade.draw_rectangle_filled(
            x + CELL_SIZE/2,
            y + CELL_SIZE/2,
            CELL_SIZE,
            CELL_SIZE,
            (255, 180, 200)
        )

# --- Arcade Window ---
class CatWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade Cat Grid")
        arcade.set_background_color((30, 30, 30))
        self.cat = Cat()

    def on_update(self, delta_time):
        self.cat.update()

    def on_draw(self):
        arcade.start_render()

        # Draw grid lines
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                arcade.draw_rectangle_outline(
                    x + CELL_SIZE/2,
                    y + CELL_SIZE/2,
                    CELL_SIZE,
                    CELL_SIZE,
                    (60, 60, 60)
                )

        self.cat.draw()

# --- Run the game ---
CatWindow()
arcade.run()
