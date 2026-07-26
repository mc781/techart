import arcade
import random
from PIL import Image

# Setup
# > pip install arcade
# References
# - arcade documentation: https://api.arcade.academy/en/3.3.3/index.html
# - melody maker: https://musiclab.chromeexperiments.com/Melody-Maker/

# --- Grid settings ---
GRID_SIZE = 20
CELL_SIZE = 48
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE


class Animal:
    """A wandering animal that moves randomly on a 20x20 grid."""

    def __init__(self, type="cat"):
        self.row = random.randint(0, GRID_SIZE - 1)
        self.col = random.randint(0, GRID_SIZE - 1)
        self.move_timer = 0
        self.type = type

        if type == "me":
            self.texture = arcade.load_texture("me.png")
            self.dr = 0
            self.dc = 0 
        if type == "cat":
            self.texture = arcade.load_texture("cat_icon.png")
        elif type == "penguin":
            img = Image.open("cute_penguin.png")
            # Resize image smaller before creating the texture
            img = img.resize((CELL_SIZE, CELL_SIZE))
            self.texture = arcade.Texture(img)  

    def update(self):
        """Move every n frames, staying inside the grid."""
        n = 1
        if self.type == "cat":
            n = 2
        elif self.type == "penguin":
            n = 5
        elif self.type == "me":
            n = 1

        self.move_timer += 1

        if self.move_timer > n:
            self.move_timer = 0
            if self.type == "me":
                dr = self.dr
                dc = self.dc
            else:
                dr, dc = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

            new_r = self.row + dr
            new_c = self.col + dc

            if 0 <= new_r < GRID_SIZE:
                self.row = new_r
            if 0 <= new_c < GRID_SIZE:
                self.col = new_c

    def draw(self):
        """Draw the cat as a pink square initially in its current cell."""
        left = self.col * CELL_SIZE
        bottom = self.row * CELL_SIZE
        color = (255, 180, 200)  # Pink-color box for the cat
 #       arcade.draw_lbwh_rectangle_filled(left, bottom, CELL_SIZE, CELL_SIZE, color)

        rect = arcade.LBWH(left, bottom, CELL_SIZE, CELL_SIZE)
        arcade.draw_texture_rect(self.texture, rect, pixelated=True)

class PlayWindow(arcade.Window):
    """Main window showing the grid and the wandering cat."""
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade Grid")
        self.cat = Animal("cat")
        self.penguin = Animal("penguin")
        self.me = Animal("me")

        self.dr = 0
        self.dc = 0

        self.background_color = (30, 30, 30)
        self.music = arcade.Sound("game_sound.mp3")
        self.music_player = self.music.play(loop=True)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            self.music_player.volume = 0 if self.music_player.volume > 0 else 1

        if key == arcade.key.W:
            self.me.dr = 1     # up
        elif key == arcade.key.S:
            self.me.dr = -1    # down
        elif key == arcade.key.A:
            self.me.dc = -1    # left
        elif key == arcade.key.D:
            self.me.dc = 1     # right

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.me.dr = 0
        if key in (arcade.key.A, arcade.key.D):
            self.me.dc = 0

    def on_update(self, delta_time: float):
        self.cat.update()
        self.penguin.update()
        self.me.update()

    def on_draw(self):
        # Clear the screen (Arcade 3.3.3+ uses clear(), not start_render())
        self.clear(self.background_color)

        # Draw grid lines as rectagle shapes(slow)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                left = c * CELL_SIZE
                bottom = r * CELL_SIZE
                color = (60, 60, 60)  # Dark gray for grid lines
                arcade.draw_lbwh_rectangle_outline(left, bottom, CELL_SIZE, CELL_SIZE, color) #
 
        # Draw the cat
        self.cat.draw()
        self.penguin.draw()
        self.me.draw()


if __name__ == "__main__":
    PlayWindow()
    arcade.run()
