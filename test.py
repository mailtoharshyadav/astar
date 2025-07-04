import math
import heapq
import time


def parse_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    header_index = lines.index('map\n')
    return [list(row.strip()) for row in lines[header_index+1:]]


def parse_scen(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]  # skip header
    scenarios = []
    for line in lines:
        parts = line.strip().split()
        sx, sy, gx, gy = map(int, parts[4:8])
        benchmark = float(parts[8])
        scenarios.append(((sy, sx), (gy, gx), benchmark))  # (row, col) format
    return scenarios


def get_neighbors(pos, grid):
    dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    r, c = pos
    neighbors = []
    for dr, dc in dirs:
        nr, nc = r+dr, c+dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] != '.': continue
            if abs(dr) + abs(dc) == 2:
                if grid[r][nc] != '.' or grid[nr][c] != '.':
                    continue  # corner-cut prevention
            neighbors.append((nr, nc))
    return neighbors


def heuristic(a, b):
    # Euclidean
    return math.hypot(b[0] - a[0], b[1] - a[1])


def movement_cost(a, b):
    return math.sqrt(2) if a[0] != b[0] and a[1] != b[1] else 1


def a_star(start, goal, grid):
    open_set = [(0 + heuristic(start, goal), 0, start, None)]
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, g, current, parent = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            path.reverse()
            return path

        came_from[current] = parent

        for neighbor in get_neighbors(current, grid):
            new_cost = g + movement_cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, new_cost, neighbor, current))

    return []  # No path


def compute_cost(path):
    return sum(movement_cost(path[i], path[i+1]) for i in range(len(path)-1))


def main():
    map_file = input("Enter path to .map file: ").strip()
    scen_file = input("Enter path to .scen file: ").strip()
    case_index = int(input("Enter scenario index (e.g., 0): ").strip())

    grid = parse_map(map_file)
    scenarios = parse_scen(scen_file)

    if case_index >= len(scenarios):
        print("Invalid case index")
        return

    start, goal, expected_cost = scenarios[case_index]
    print(f"Start: {start}, Goal: {goal}, Expected Optimal Cost: {expected_cost}")

    start_time = time.time()
    path = a_star(start, goal, grid)
    end_time = time.time()

    if not path:
        print("❌ No path found")
        return

    total_cost = compute_cost(path)
    print(f"✅ Path found! Length: {len(path)}")
    print(f"⏱ Time taken: {end_time - start_time:.4f} sec")
    print(f"📍 Path cost: {total_cost:.4f}")
    print(f"📊 Error vs expected: {abs(total_cost - expected_cost):.4f}")


if __name__ == "__main__":
    main()