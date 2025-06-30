import time
import numpy as np
import pandas as pd

from astar import a_star
from heuristics import manhattan, euclidean, diagonal, hybrid
from map_generator import generate_open_field, generate_obstacle_field, generate_maze, add_borders

# Setup experiments
def run_tests():
    width, height = 20, 20
    start, goal = (1, 1), (18, 18)

    maps = {
        "open_field": add_borders(generate_open_field(width, height)),
        "obstacle_dense": add_borders(generate_obstacle_field(width, height, obstacle_prob=0.3)),
        "maze": generate_maze(width, height)
    }

    heuristics = {
        "manhattan": manhattan,
        "euclidean": euclidean,
        "diagonal": diagonal,
        "hybrid": lambda p1, p2: hybrid(p1, p2, w1=0.3, w2=0.7)
    }

    results = []

    for map_name, grid in maps.items():
        for h_name, h_func in heuristics.items():
            start_time = time.time()
            path, visited = a_star(start, goal, grid, h_func)
            duration = time.time() - start_time

            results.append({
                "map": map_name,
                "heuristic": h_name,
                "path_length": len(path),
                "nodes_visited": len(visited),
                "time_seconds": round(duration, 5)
            })

            print(f"[{map_name}] {h_name} - Path Length: {len(path)}, Nodes: {len(visited)}, Time: {duration:.5f}s")

    # Save results to CSV
    import os
    os.makedirs("results", exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv("results/metrics.csv", index=False)

if __name__ == "__main__":
    run_tests()