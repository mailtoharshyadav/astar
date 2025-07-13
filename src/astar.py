import math
import heapq

# Terrain cost definitions (default weight = 1)
terrain_costs = {
    '.': 1.0,   # Flat ground
    'B': float('inf'),
    'C': 3.0,
    'D': 4.0,
    'E': 2.0,
    'F': 3.5,
    'G': 1.5,
    'H': 2.5,
    'I': 2.0,
    'J': 4.5,
    'K': 5.0,
    'L': 10.0,
    'M': 6.0,
    'N': 1.0,
    'O': 1.0,
    '@': float('inf'),
    'T': float('inf')
}

def get_cell_cost(cell):
    return terrain_costs.get(cell, 1)

def cost(a, b, grid):
    base = math.sqrt(2) if a[0] != b[0] and a[1] != b[1] else 1
    cell_cost = get_cell_cost(grid[b[0]][b[1]])
    return base * cell_cost

# Reconstruct path from goal to start using the came_from dictionary
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star(start, goal, grid, heuristic):
    if get_cell_cost(grid[start[0]][start[1]]) == float('inf') or get_cell_cost(grid[goal[0]][goal[1]]) == float('inf'):
        return [], set()  # Start or goal is blocked

    open_set = []  # Priority queue of (f_score, tie_breaker, node)
    heapq.heappush(open_set, (0, heuristic(start, goal), start))

    came_from = {}  # For path reconstruction
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    visited_nodes = set()  # For analysis/visualization
    closed_set = set()     # Optional: to avoid reprocessing

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in closed_set:
            continue

        closed_set.add(current)
        visited_nodes.add(current)

        if current == goal:
            return reconstruct_path(came_from, current), visited_nodes

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                if get_cell_cost(grid[neighbor[0]][neighbor[1]]) == float('inf'):
                    continue

                if dx != 0 and dy != 0:
                    if (get_cell_cost(grid[current[0] + dx][current[1]]) == float('inf') or
                        get_cell_cost(grid[current[0]][current[1] + dy]) == float('inf')):
                        continue

                move_cost = cost(current, neighbor, grid)
                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], heuristic(neighbor, goal), neighbor))

    return [], visited_nodes
