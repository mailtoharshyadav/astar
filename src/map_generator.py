import numpy as np
import random

# Generate an empty grid with no obstacles
def generate_open_field(width, height):
    return np.zeros((height, width), dtype=int)

# Generate a grid with random obstacles (1 = wall, 0 = free)
def generate_obstacle_field(width, height, obstacle_prob=0.2):
    grid = np.zeros((height, width), dtype=int)
    for i in range(height):
        for j in range(width):
            if random.random() < obstacle_prob:
                grid[i][j] = 1
    return grid

# Add border walls to a grid
def add_borders(grid):
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    return grid

# Print the grid in a readable format for debugging
def print_grid(grid, path=None):
    display = grid.copy()
    if path:
        for x, y in path:
            if display[x][y] == 0:
                display[x][y] = 8  # Mark the path with 8
    for row in display:
        print(' '.join(str(cell) for cell in row))

# Generate a very simple horizontal/vertical tunnel-based maze
def generate_maze(width, height):
    grid = np.ones((height, width), dtype=int)  # start with all walls
    grid[1:-1, 1] = 0  # vertical tunnel
    grid[1, 1:-1] = 0  # horizontal tunnel
    return add_borders(grid)

# Visualize all map types side by side
def test_map_types():
    import matplotlib.pyplot as plt

    maps = {
        "Open Field": generate_open_field(20, 20),
        "Obstacle Dense": generate_obstacle_field(20, 20, 0.3),
        "Maze": generate_maze(20, 20)
    }

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (title, grid) in zip(axes, maps.items()):
        ax.imshow(grid, cmap='Greys', origin='upper')
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# Load a Moving AI .map file and convert to a grid
def load_map_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    header_skipped = False
    grid_lines = []

    for line in lines:
        if not header_skipped:
            if line.strip().lower() == 'map':
                header_skipped = True
            continue
        grid_lines.append(line.strip())

    height = len(grid_lines)
    width = len(grid_lines[0])
    grid = np.zeros((height, width), dtype=int)

    for i in range(height):
        for j in range(width):
            if grid_lines[i][j] in ['@', 'O', 'W', 'T']:  # Wall/blocked terrain
                grid[i][j] = 1  # Obstacle
            else:
                grid[i][j] = 0  # Free cell

    return grid

# Load Moving AI .scen file and return start-goal pairs and optimal costs
def load_scen_file(filepath):
    scenarios = []
    with open(filepath, 'r') as f:
        lines = f.readlines()[1:]  # skip header
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 9:
                continue
            start = (int(parts[5]), int(parts[4]))  # (y, x)
            goal = (int(parts[7]), int(parts[6]))  # (y, x)
            optimal = float(parts[8])
            scenarios.append((start, goal, optimal))
    return scenarios