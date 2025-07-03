import math
import heapq

# Function to reconstruct the path from start to goal using the came_from dictionary
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()  # Reverse the path to get it from start to goal
    return path

# A* pathfinding algorithm implementation
def a_star(start, goal, grid, heuristic):
    open_set = []  # Priority queue of (f_score, node)
    heapq.heappush(open_set, (0, start))
    came_from = {}  # Tracks the most efficient previous step

    g_score = {start: 0}  # Cost from start to the current node
    f_score = {start: heuristic(start, goal)}  # Estimated cost from start to goal through current node

    visited_nodes = set()  # Track visited nodes for analysis

    while open_set:
        _, current = heapq.heappop(open_set)  # Node with lowest f_score
        visited_nodes.add(current)

        if current == goal:
            # Goal reached; reconstruct and return the path
            return reconstruct_path(came_from, current), visited_nodes

        # Explore neighbors (including diagonals)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue

                # Prevent cutting corners through walls on diagonals
                if dx != 0 and dy != 0:
                    if grid[current[0] + dx][current[1]] == 1 or grid[current[0]][current[1] + dy] == 1:
                        continue

                movement_cost = math.sqrt(2) if dx != 0 and dy != 0 else 1
                tentative_g = g_score[current] + movement_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # If the goal is unreachable, return empty path and visited nodes
    return [], visited_nodes