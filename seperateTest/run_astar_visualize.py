
import argparse
import math
import importlib.util
import os
import sys
from html import escape

import os


# Dynamically load astar.py
spec_astar = importlib.util.spec_from_file_location("astar", "seperateTest/astar.py")
astar_module = importlib.util.module_from_spec(spec_astar)
spec_astar.loader.exec_module(astar_module)

# Dynamically load heuristics.py
spec_heur = importlib.util.spec_from_file_location("heuristics", "seperateTest/heuristics.py")
heur_module = importlib.util.module_from_spec(spec_heur)
spec_heur.loader.exec_module(heur_module)

def parse_map(map_path):
    with open(map_path, 'r') as f:
        lines = f.readlines()
    header_idx = next(i for i, line in enumerate(lines) if line.strip().lower() == 'map')
    grid = [list(line.strip()) for line in lines[header_idx+1:]]
    return grid

def parse_scenario(scen_path):
    with open(scen_path, 'r') as f:
        lines = f.readlines()[1:]  # Skip header
    cases = []
    for line in lines:
        parts = line.strip().split()
        sx, sy, gx, gy = int(parts[4]), int(parts[5]), int(parts[6]), int(parts[7])
        cases.append(((sy, sx), (gy, gx)))  # row,col format
    return cases

# Get valid neighbors (8 directions, no corner cutting)
def get_neighbors(pos, grid):
    directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    r, c = pos
    rows, cols = len(grid), len(grid[0])
    result = []

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < rows and 0 <= nc < cols): continue
        if grid[nr][nc] != '.': continue
        if abs(dr) + abs(dc) == 2:
            if grid[r][nc] != '.' or grid[nr][c] != '.':
                continue  # corner cutting
        result.append((nr, nc))
    return result

def cost(a, b):
    return math.sqrt(2) if a[0] != b[0] and a[1] != b[1] else 1

def a_star_wrapped(start, goal, grid, heuristic):
    def h(a, b=goal): return heuristic(a, b)
    def wrapped_heur(pos1, pos2): return h(pos1, pos2)
    return astar_module.a_star(start, goal, grid, wrapped_heur)

def render_html(grid, path, visited, start, goal, out_file):
    cell_classes = {}  # Map positions to CSS classes

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) == start:
                cell_classes[(r, c)] = 'start'
            elif (r, c) == goal:
                cell_classes[(r, c)] = 'goal'
            elif grid[r][c] == '@':
                cell_classes[(r, c)] = 'wall'
            elif (r, c) in path:
                cell_classes[(r, c)] = 'path'
            elif (r, c) in visited:
                cell_classes[(r, c)] = 'visited'
            else:
                cell_classes[(r, c)] = 'empty'

    with open(out_file, 'w') as f:
        f.write(f'''
<html>
<head>
<style>
  .grid {{
    display: grid;
    grid-template-columns: repeat({len(grid[0])}, 10px);
    width: fit-content;
  }}
  .cell {{
    width: 10px;
    aspect-ratio: 1;
    border: 1px solid #ccc;
  }}
  .empty {{ background: white; }}
  .wall {{ background: black; }}
  .visited {{ background: lightblue; }}
  .path {{ background: green; }}
  .start {{ background: blue; }}
  .goal {{ background: red; }}
</style>
</head>
<body>
<div class="grid">
''')

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                cls = cell_classes.get((r, c), 'empty')
                f.write(f'<div class="cell {cls}"></div>')
        
        f.write('</div></body></html>')

    print(f"HTML saved to {out_file}")

def main():

    # map= "./seperateTest/random512-10-0.map"
    # scen= "./seperateTest/random512-10-0.map.scen"
    mapName = "testMap"
    case= 1
    # heuristic="euclidean"
    heuristic="manhattan"
    # heuristic="diagonal"
    # heuristic="hybrid"



    map= f"./seperateTest/{mapName}.map"
    scen= f"./seperateTest/{mapName}.map.scen"

    grid = parse_map(map)
    scenarios = parse_scenario(scen)

    if case >= len(scenarios):
        print(f"Invalid case index: {case}")
        return

    start, goal = scenarios[case]

    heuristic_func = getattr(heur_module, heuristic, None)
    if not heuristic_func:
        print(f"Heuristic '{heuristic}' not found in heuristics.py")
        return

    print(f"▶ Running A* from {start} to {goal} using '{heuristic}' heuristic...")
    converted_grid = [[1 if cell == '@' else 0 for cell in row] for row in grid]
    path, visited = astar_module.a_star(start, goal, converted_grid, heuristic_func)
    print(f"Path length: {len(path)}  |  Visited: {len(visited)}")

    out_html = f"./seperateTest/results/{mapName}_{case}_{heuristic}.html"
    render_html(grid, path, visited, start, goal, out_html)

if __name__ == "__main__":
    main()
