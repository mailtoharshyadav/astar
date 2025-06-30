import time
import numpy as np
import pandas as pd
import argparse
import os

from astar import a_star
from heuristics import manhattan, euclidean, diagonal, hybrid
from map_generator import (
    generate_open_field,
    generate_obstacle_field,
    generate_maze,
    add_borders,
    load_map_file,
    load_scen_file
)

# Apply terrain weight if enabled (cost = 5 on cell value 2, 10 on 3, etc.)
def apply_weights(grid, weight_map=None):
    if weight_map:
        weighted = grid.copy()
        for (x, y), cost in weight_map.items():
            if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
                weighted[x][y] = cost
        return weighted
    return grid

def run_experiment(map_name, grid, start, goal, apply_weight=False, optimal_cost=None):
    heuristics = {
        "manhattan": manhattan,
        "euclidean": euclidean,
        "diagonal": diagonal,
        "hybrid": lambda p1, p2: hybrid(p1, p2, w1=0.3, w2=0.7)
    }

    results = []

    for h_name, h_func in heuristics.items():
        g = grid.copy()

        if apply_weight:
            g[start[0]][start[1]] = 0
            g[goal[0]][goal[1]] = 0

        start_time = time.time()
        path, visited = a_star(start, goal, g, h_func)
        duration = time.time() - start_time

        actual_cost = len(path)
        optimality_ratio = actual_cost / optimal_cost if optimal_cost else None

        results.append({
            "map": map_name,
            "heuristic": h_name,
            "path_length": actual_cost,
            "nodes_visited": len(visited),
            "time_seconds": round(duration, 5),
            "optimal_cost": round(optimal_cost, 5) if optimal_cost else None,
            "optimality_ratio": round(optimality_ratio, 5) if optimality_ratio else None
        })

        print(f"[{map_name}] {h_name} - Path: {actual_cost}, Nodes: {len(visited)}, Time: {duration:.5f}s, Optimal: {optimal_cost}, Ratio: {optimality_ratio}")

    df = pd.DataFrame(results)
    os.makedirs("results", exist_ok=True)
    df.to_csv(f"results/metrics_{map_name}.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run A* with various heuristics.")
    parser.add_argument('--source', choices=['custom', 'ai'], default='ai', help='Map source')
    parser.add_argument('--weights', action='store_true', help='Apply terrain weights')
    args = parser.parse_args()

    if args.source == 'custom':
        print("Running on custom maps")
        width, height = 20, 20
        start, goal = (1, 1), (1, 18)

        maps = {
            "open_field": add_borders(generate_open_field(width, height)),
            "obstacle_dense": add_borders(generate_obstacle_field(width, height, 0.3)),
            "maze": generate_maze(width, height)
        }

        for name, grid in maps.items():
            grid[start[0]][start[1]] = 0
            grid[goal[0]][goal[1]] = 0
            run_experiment(name, grid, start, goal, args.weights)

    elif args.source == 'ai':
        mapNames = ("16room_002" , "Map18", "Maze512-1-0", "random512-10-0")
        print("Running on Moving AI benchmark map")
        for name in mapNames:
            print("map", name)
            mapPath = "maps/"+ name + ".map"
            scenPath = "maps/"+ name + ".map.scen"
            grid = load_map_file(mapPath)
            scenarios = load_scen_file(scenPath)
            for i, (start, goal, optimal_cost) in enumerate(scenarios[:10]):
                run_experiment(f"{name}_{i+1}", grid, start, goal, args.weights, optimal_cost)