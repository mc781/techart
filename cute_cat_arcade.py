from turtle import color

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

class Backdrop:
    """A backdrop that fills the entire window with a color."""
    def __init__(self, type):
        self.sand_color = (194, 178, 128)
        self.grass_color = (34, 139, 34)
        self.ocean_color = (0, 105, 148)
        self.sky_color = (135, 206, 235)

        if type == "sand":
            self.color = self.sand_color
            self.bot = 0
            self.top = HEIGHT/2
            self.text = "Seashell"
        elif type == "ocean":
            self.color = self.ocean_color
            self.bot = HEIGHT/2
            self.top = 3 * HEIGHT/4
            self.text = "Boat"
        elif type == "sky":
            self.color = self.sky_color
            self.bot = 3 * HEIGHT/4
            self.top = HEIGHT
            self.text = "Seagull"

    def draw(self):
        arcade.draw_lbwh_rectangle_filled(0, self.bot, WIDTH, self.top, self.color)
        arcade.draw_text(self.text, WIDTH/2, self.top - 30, arcade.color.WHITE, 20, anchor_x="center")

class Animal:
    """A wandering animal that moves randomly on a 20x20 grid."""

    def __init__(self, type="cat"):
        self.row = random.randint(0, GRID_SIZE - 1)
        self.col = random.randint(0, GRID_SIZE - 1)
        self.dr = 0
        self.dc = 0 
        self.move_timer = 0
        self.type = type

        self.sound_hit = arcade.Sound("magic-teleport.wav")
        self.sound_step = arcade.Sound("step-grass.wav")

        if type == "me":
            self.texture = arcade.load_texture("me.png")
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
            if self.type != "me":
                self.dr, self.dc = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

            new_r = self.row + self.dr
            new_c = self.col + self.dc

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
        if self.type == "me":
            if self.dr != 0 or self.dc != 0:
                self.sound_step.play()

class PlayWindow(arcade.Window):
    """Main window showing the grid and the wandering cat."""
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade Grid")
        self.cat = Animal("cat")
        self.penguin = Animal("penguin")
        self.me = Animal("me")

        self.background_color = (30, 30, 30)

        self.backdrop_sand = Backdrop("sand")
        self.backdrop_ocean = Backdrop("ocean")
        self.backdrop_sky = Backdrop("sky")
         
        self.music = arcade.Sound("game_sound.mp3")
        self.music_player = self.music.play(volume=0.5, loop=True)

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
        self.backdrop_sand.draw()
        self.backdrop_ocean.draw()
        self.backdrop_sky.draw()
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

        if self.cat.row == self.me.row and self.cat.col == self.me.col:
            self.cat.sound_hit.play()
        if self.penguin.row == self.me.row and self.penguin.col == self.me.col:
            self.penguin.sound_hit.play()    


if __name__ == "__main__":
    PlayWindow()
    arcade.run()
