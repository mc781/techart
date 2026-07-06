import pygame
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

            # Stay inside the grid
            if 0 <= new_r < GRID_SIZE:
                self.row = new_r
            if 0 <= new_c < GRID_SIZE:
                self.col = new_c

    def draw(self, screen):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        pygame.draw.rect(screen, (255, 180, 200), (x, y, CELL_SIZE, CELL_SIZE))


# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cat = Cat()
running = True

# --- Main loop ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    cat.update()

    screen.fill((30, 30, 30))

    # Draw grid lines
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            pygame.draw.rect(screen, (60, 60, 60),
                             (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    cat.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
