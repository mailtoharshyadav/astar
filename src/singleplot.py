import matplotlib.pyplot as plt
import numpy as np
import math
from astar import a_star
from heuristics import manhattan, euclidean, diagonal, hybrid
from map_generator import load_map_file, load_scen_file

import plotly.graph_objects as go
import numpy as np
import webbrowser
import os
import json

import pygame
import time

def plot_map_with_paths(grid, start, goal, paths_dict, cell_size=10, delay=0):
    pygame.init()

    rows, cols = len(grid), len(grid[0])
    width, height = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A* Pathfinding Visualizer - Pygame")

    # Define colors
    COLORS = {
        'free': (238, 238, 238),
        'wall': (0, 0, 0),
        'start': (0, 200, 0),
        'goal': (200, 0, 0),
        'Manhattan': (30, 144, 255),
        'Euclidean': (255, 165, 0),
        'Diagonal': (128, 0, 128),
        'Hybrid': (0, 255, 255)
    }

    def draw_grid():
        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                color = COLORS['wall'] if grid[y][x] == 1 else COLORS['free']
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # light border

    def draw_circle(pos, color):
        x, y = pos[1], pos[0]
        center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
        pygame.draw.circle(screen, color, center, cell_size // 2)

    draw_grid()
    draw_circle(start, COLORS['start'])
    draw_circle(goal, COLORS['goal'])

    for name, path in paths_dict.items():
        for i in range(1, len(path)):
            y1, x1 = path[i-1]
            y2, x2 = path[i]
            pygame.draw.line(
                screen,
                COLORS.get(name, (100, 100, 100)),
                (x1 * cell_size + cell_size // 2, y1 * cell_size + cell_size // 2),
                (x2 * cell_size + cell_size // 2, y2 * cell_size + cell_size // 2),
                2
            )
            if delay:
                pygame.display.flip()
                time.sleep(delay)

    pygame.display.flip()

    # Wait until user closes the window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


# def plot_map_with_paths(grid, start, goal, paths_dict, output_file="outputs/astar_paths_table.html"):
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
#     scale = 0
#     # Convert grid and paths to serializable types
#     grid = grid.tolist() if hasattr(grid, "tolist") else grid
#     start = list(start.tolist()) if hasattr(start, "tolist") else list(start)
#     goal = list(goal.tolist()) if hasattr(goal, "tolist") else list(goal)

#     # Build cell-to-color mapping
#     color_map = {}
#     for name, path in paths_dict.items():
#         color = {
#             "Manhattan": "blue",
#             "Euclidean": "orange",
#             "Diagonal": "purple",
#             "Hybrid": "cyan"
#         }.get(name, "gray")

#         for y, x in path:
#             color_map[(y, x)] = color

#     # Mark start and goal specially
#     color_map[tuple(start)] = "green"
#     color_map[tuple(goal)] = "red"

#     # Build the table HTML
#     table_rows = []
#     for y in range(len(grid)):
#         row = []
#         for x in range(len(grid[0])):
#             cell_class = "wall" if grid[y][x] == 1 else "free"
#             color = color_map.get((y, x), "")
#             style = f"background-color: {color};" if color else ""
#             row.append(f'<td class="{cell_class}" style="{style}"></td>')
#         table_rows.append("<tr>" + "".join(row) + "</tr>")

#     table_html = "\n".join(table_rows)

#     html = f"""
# <!DOCTYPE html>
# <html lang=\"en\">
# <head>
#     <meta charset=\"UTF-8\">
#     <title>A* Pathfinding Visualizer (Table)</title>
#     <style>
#         table {{
#             border-collapse: collapse;
#             transform: scale(1);
#             transform-origin: top left;
#         }}
#         td {{
#             width: 12px;
#             height: 12px;
#             border: 1px solid #ddd;
#         }}
#         .wall {{
#             background-color: black;
#         }}
#         .free {{
#             background-color: #eee;
#         }}
#     </style>
# </head>
# <body>
#     <h3>A* Pathfinding Visualizer (Table View)</h3>
#     <div id=\"controls\">
#         <button onclick=\"zoom(1.2)\">Zoom In</button>
#         <button onclick=\"zoom(0.8)\">Zoom Out</button>
#     </div>
#     <div id=\"table-wrapper\">
#         <table id=\"grid\">
#             {table_html}
#         </table>
#     </div>

#     <script>
#         let scale = 1;
#         function zoom(factor) {{
#             scale *= factor;
#             document.getElementById('grid').style.transform = `scale(${scale})`;
#         }}
#     </script>
# </body>
# </html>
# """

#     with open(output_file, "w") as f:
#         f.write(html)

#     webbrowser.open('file://' + os.path.realpath(output_file))

# Actual cost computation from path
def compute_path_cost(path):
    return sum(
        math.sqrt(2) if abs(path[i][0] - path[i-1][0]) == 1 and abs(path[i][1] - path[i-1][1]) == 1 else 1
        for i in range(1, len(path))
    ) if path else float('inf')

# Main execution for a single case from .scen
def run_single_case_from_scenario(scen_path, index=0, map_name = ""):
    scenarios = load_scen_file(scen_path)
    if index >= len(scenarios):
        print(f"Index {index} out of range. Scenario file contains {len(scenarios)} entries.")
        return
    start, goal, optimal = scenarios[index]
    map_file = f"maps/{map_name}.map"

    print(f"Map: {map_file}")
    print(f"Start: {start}, Goal: {goal}, Optimal Cost: {optimal}")

    grid = load_map_file(map_file)
    heuristics = {
        "Manhattan": manhattan,
        "Euclidean": euclidean,
        "Diagonal": diagonal,
        "Hybrid": lambda p1, p2: hybrid(p1, p2, w1=0.3, w2=0.7)
    }

    paths = {}
    for name, heuristic in heuristics.items():
        path, visited = a_star(start, goal, grid, heuristic)
        cost = compute_path_cost(path)
        print(f"{name} → Steps: {len(path)}, Cost: {round(cost, 5)}, Visited: {len(visited)}")
        paths[name] = path

    plot_map_with_paths(grid, start, goal, paths)

# Example usage
if __name__ == "__main__":
    scenario_file = "maps/16room_002.map.scen"  # Update as needed
    scenario_index = 3  # Change the index to select a different test case
    run_single_case_from_scenario(scenario_file, scenario_index, "16room_002")