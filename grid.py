import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Define constants
GRID_WIDTH = 50
GRID_HEIGHT = 8
SQUARE_SIZE = 20
BACKGROUND_COLOR = (30, 30, 30)  # Dark grey for background
GRID_COLOR = (50, 50, 50)  # Darker grey for grid lines
GREEN = (0, 200, 0)  # Dark green
RED = (200, 0, 0)  # Dark red
WHITE = (255, 255, 255)
SAVE_FILE = "grid_state.txt"

# Calculate screen dimensions based on grid size and square size
SCREEN_WIDTH = GRID_WIDTH * SQUARE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * SQUARE_SIZE

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Coloring")

# Function to save grid state to file
def save_grid_state(grid):
    with open(SAVE_FILE, "w") as file:
        for row in grid:
            for color in row:
                if color == GREEN:
                    file.write("1")
                elif color == RED:
                    file.write("2")
                else:
                    file.write("0")
            file.write("\n")

# Function to load grid state from file
def load_grid_state():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            lines = file.readlines()
            loaded_grid = []
            for line in lines:
                row = []
                for char in line.strip():
                    if char == "1":
                        row.append(GREEN)
                    elif char == "2":
                        row.append(RED)
                    else:
                        row.append(WHITE)
                loaded_grid.append(row)
            return loaded_grid
    else:
        return [[WHITE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Initialize grid with loaded state or create new grid
grid = load_grid_state()

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = grid[y][x]
            pygame.draw.rect(screen, color, (x * SQUARE_SIZE + 1, y * SQUARE_SIZE + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2), border_radius=4)
            pygame.draw.rect(screen, GRID_COLOR, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2, border_radius=4)

def get_grid_position(pos):
    x, y = pos
    grid_x = x // SQUARE_SIZE
    grid_y = y // SQUARE_SIZE
    return grid_x, grid_y

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save grid state before exiting
            save_grid_state(grid)
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                grid_x, grid_y = get_grid_position((x, y))
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    current_color = grid[grid_y][grid_x]
                    if current_color == WHITE:
                        grid[grid_y][grid_x] = GREEN
                    elif current_color == GREEN:
                        grid[grid_y][grid_x] = RED
                    elif current_color == RED:
                        grid[grid_y][grid_x] = WHITE

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    pygame.display.flip()

pygame.quit()
sys.exit()
