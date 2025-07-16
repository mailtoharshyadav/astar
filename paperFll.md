1. Abstract

Pathfinding is a fundamental requirement in autonomous robotics, and the A* algorithm remains one of the most efficient and widely adopted approaches for this task. This paper investigates the impact of heuristic selection on A* performance by comparing four heuristic strategies: Manhattan, Euclidean, Diagonal (Chebyshev), and a custom Hybrid heuristic combining Manhattan and Euclidean with equal weight.

These heuristics were tested on a diverse set of map environments, including open fields, obstacle-dense layouts, indoor-like room partitions, maze-like corridors, and a weighted multi-terrain map (Map18 from the Moving AI benchmark) that simulates real-world cost variations. For each heuristic and map, we collected detailed metrics: path length, nodes expanded, execution time, and deviation from expected cost.

Results reveal that Manhattan is consistently the fastest, but often produces suboptimal paths, especially in open or diagonal-friendly maps. Euclidean and Diagonal improve path quality but at the cost of greater computational load. The Hybrid heuristic effectively balances both, offering near-optimal path length with reduced expansion overhead. In weighted terrain, it outperforms Manhattan in path quality while remaining significantly faster than Euclidean.

This study offers empirical insights into heuristic design and presents practical guidance for deploying A* in varied robotic contexts, especially where trade-offs between speed, accuracy, and terrain sensitivity are critical.

⸻

2. Introduction

Efficient and reliable path planning is a fundamental requirement in autonomous robotics, enabling agents to move from a start point to a destination while avoiding obstacles and minimizing travel cost. Among the various algorithms developed for this purpose, the A* search algorithm has become a cornerstone of modern pathfinding due to its balance between optimality and efficiency when guided by an admissible heuristic.

A*’s performance, however, is highly sensitive to the choice of heuristic function—a component that estimates the cost to reach the goal from any given node. In robotic navigation, this means the selected heuristic directly influences not only path optimality but also computational cost, node expansions, and responsiveness in real-time environments. While classic heuristics like Manhattan, Euclidean, and Chebyshev (Diagonal) have long been used in grid-based pathfinding, their effectiveness can vary widely across different map structures and terrain types.

To explore these dynamics, this study implements and evaluates multiple heuristics across a suite of test environments:
	•	Binary grid maps: including open arenas, dense random fields, partitioned room-like spaces, and tight mazes.
	•	Weighted multi-terrain maps: such as Map18 from the Moving AI benchmark, where terrain traversal cost varies by region, simulating roads, grass, or uneven terrain.

A novel Hybrid heuristic—a weighted combination of Manhattan and Euclidean functions—is also introduced, designed to bridge the gap between speed and accuracy.

The goal of this paper is to provide an empirical study of how different heuristics perform across diverse map structures, with a focus on robotic applicability. By analyzing metrics such as path length, nodes expanded, execution time, and cost deviation, the study offers guidance for selecting or designing heuristics tailored to specific robotic use cases—be it warehouse automation, terrain navigation, or real-time delivery.

⸻


⸻

3. Related Work

The A* algorithm was first introduced by Hart, Nilsson, and Raphael (1968) and remains a foundational technique for graph-based pathfinding. Its ability to guarantee optimality when using an admissible heuristic has made it a standard in fields such as robotics, video games, and AI planning. In robotic systems, A* is often employed for local and global navigation in grid-based maps, with its performance highly sensitive to the choice of heuristic function.

Manhattan and Euclidean heuristics are among the most commonly used. Manhattan distance is ideal for scenarios constrained to four-directional movement, while Euclidean distance approximates realistic motion more accurately in 8-directional or continuous spaces. Chebyshev distance (Diagonal heuristic) further accommodates diagonal movement with uniform cost assumptions.

Recent studies have explored ways to improve heuristic accuracy and adaptability. These include hybrid heuristics, weighted heuristics (e.g., weighted A*), and learning-based approaches that tailor the heuristic based on environment features. Notably, context-sensitive heuristics—which adjust based on map topology—have shown promise in dynamically improving A* performance without compromising completeness or admissibility. This paper builds on this foundation by implementing a simple hybrid heuristic and evaluating its impact across a variety of environmental structures.

4. Methodology

4.1 Heuristic Definitions

To evaluate the effect of different heuristics on A* pathfinding, four modular heuristic functions were implemented:
	•	Manhattan Distance:
Suitable for 4-directional movement on grids:
h(n) = |x_1 - x_2| + |y_1 - y_2|
	•	Euclidean Distance:
Approximates straight-line travel across open areas:
h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}
	•	Diagonal (Chebyshev) Distance:
Allows 8-directional uniform-cost movement:
h(n) = \max(|x_1 - x_2|, |y_1 - y_2|)
	•	Hybrid Heuristic:
A linear blend of Manhattan and Euclidean heuristics:
h_{\text{hybrid}} = 0.5 \cdot h_{\text{Manhattan}} + 0.5 \cdot h_{\text{Euclidean}}
Designed to balance fast computation and realistic path quality.

⸻

4.2 A* Pathfinding Implementation

The pathfinding logic was implemented in astar.py and supports both 4- and 8-directional movement models. Key features include:
	•	Open list: A priority queue implemented with heapq, ordered by total cost f(n) = g(n) + h(n).
	•	Closed list: Prevents revisiting expanded nodes.
	•	Collision detection: Obstacles are treated as impassable cells.
	•	Path tracking: Backtracking from goal to start constructs the final path.
	•	Cost modeling: Weighted grids allow cost accumulation across variable terrain types.

⸻

4.3 Metric Logging and Evaluation Tools

All experiments were automated using gen_csv_astar.py, which:
	•	Runs A* with each heuristic across all map types.
	•	Logs results into structured CSV files.
	•	Tracks performance metrics:
	•	Path length
	•	Visited nodes
	•	Execution time
	•	Expected vs. actual cost
	•	Time variance (error bars)

⸻

4.4 Experimental Setup and Tools
	•	Language: Python 3.x
	•	Libraries: NumPy, Matplotlib, heapq
	•	Hardware: Experiments were executed on a standard MacBook M2 Pro.
	•	Map format: All maps were grid-based; black pixels represent obstacles, white pixels are traversable, and color overlays represent paths.

⸻

4.5 Map Types

The following maps were used to simulate distinct navigation environments:
	1.	Arena – Open grid with minimal obstacles.
	2.	Random – High obstacle density.
	3.	Room – Partitioned space resembling indoor layouts.
	4.	Maze – Tight corridors and winding paths.
	5.	(Visualized mlue, goal as red, and path as green)

⸻

4.6 Weighted Terrain Maps (Map18 - Moving AI Benchmark)

To assess performance in a realistic, large-scale, cost-sensitive environment, we incorporated Map18 from the Moving AI Benchmark. This map includes:
	•	Variable terrain costs: Each cell has a traversal cost based on terrain type (e.g., roads, grass, forest).
	•	High-resolution grid: Representing thousands of nodes with non-uniform cost distribution.
	•	Real-world inspired layouts: Includes both open spaces and natural chokepoints.

This map reflects more authentic robotic navigation challenges, where not all paths are equally “cheap” despite being similar in distance. While the implemented heuristics remain unaware of exact terrain weights, their structural assumptions directly impact how effectively they navigate cost variations. This setup allowed us to test generalizability beyond uniform-cost grids.

All results were logged to CSV files and later visualized as bar graphs and overlays.

5. Results

This section presents the empirical outcomes of running A* search with each heuristic across all map types. Results are broken down by environment type, and include execution time, path length, and nodes expanded. All metrics were averaged over multiple runs.

⸻

5.1 Arena Map

A sparse map with minimal obstacles and large open space.
	•	Manhattan was the fastest but produced longer paths due to limited directional movement.
	•	Euclidean and Hybrid produced shorter, more direct paths.
	•	Diagonal was slightly slower and expanded more nodes.
	•	Hybrid offered a good balance between speed and accuracy.

⸻

5.2 Random Map

A cluttered map with high obstacle density.
	•	Manhattan remained fastest but showed inefficiencies in path optimality.
	•	Hybrid closely followed in time while achieving shorter paths.
	•	Euclidean and Diagonal expanded more nodes and were slower.
	•	Hybrid minimized both path cost and node expansions compared to pure heuristics.

⸻

5.3 Room Map

A map simulating indoor room partitions and corridors.
	•	Hybrid and Euclidean produced the most efficient paths.
	•	Manhattan performed well on time but at the cost of longer paths.
	•	Diagonal continued to be the most expensive in node expansions.
	•	Hybrid reduced node overhead without sacrificing quality.

⸻

5.4 Maze Map

A tightly constrained grid of winding corridors.
	•	All heuristics performed similarly in path length due to limited options.
	•	Manhattan was fastest due to minimal expansions.
	•	Euclidean and Diagonal had higher overhead without gain in path quality.
	•	Heuristic impact was minimal in such constrained spaces.

⸻

5.5 Path Overlay Visualization

Overlay images (provided for arena map) demonstrated:
	•	Manhattan created stair-step patterns and inefficient routing.
	•	Euclidean followed smoother, direct paths.
	•	Hybrid closely mimicked Euclidean with improved speed.

⸻

5.6 Map18 – Weighted Multi-Terrain (Moving AI Benchmark)

Map18 is a high-resolution map with terrain-based cost variation.
	•	Manhattan had the lowest execution time (~7.5s) but the longest path (~854 units).
	•	Euclidean and Diagonal produced shorter paths (~848 units) but took longer (9–10s) and expanded ~850k–900k nodes.
	•	Hybrid struck a middle ground:
	•	Path length (~849 units)
	•	Time (~8.9s)
	•	Nodes expanded (~779k)

Conclusion: In complex cost-based maps, the Hybrid heuristic achieved a strong balance, improving over Manhattan without suffering the computational cost of Diagonal.


6. Analysis

This section interprets performance differences across map types, focusing on the trade-offs between speed, optimality, and computational cost.

⸻

6.1 Manhattan Heuristic
	•	Fastest execution in every test case.
	•	Performed well in constrained spaces (e.g., maze), but poorly in open or diagonal-friendly areas.
	•	Struggled with terrain variation in Map18, taking longer, costlier paths.
	•	Suitable for fast approximation where exact path quality is less critical.

⸻

6.2 Euclidean and Diagonal Heuristics
	•	Euclidean consistently produced the shortest paths, especially in arena, room, and Map18.
	•	Diagonal expanded the most nodes and was computationally expensive.
	•	These heuristics excel when optimality is essential, but are costly in terms of CPU and memory usage.

⸻

6.3 Hybrid Heuristic
	•	Blending Manhattan and Euclidean allowed adaptive behavior:
	•	Speed comparable to Manhattan.
	•	Path quality comparable to Euclidean.
	•	Outperformed pure heuristics in random and room environments.
	•	In Map18, it achieved a solid balance between cost and speed.

⸻

6.4 Environment-Specific Heuristic Suitability

Map Type	Best Heuristic	Reason
Arena	Hybrid / Euclidean	Optimal paths with fast execution
Random	Hybrid	Reduced expansions and cost
Room	Hybrid	Balanced corridor navigation
Maze	Manhattan	Limited routing space favors simplicity
Map18	Hybrid	Best compromise in cost-aware terrain

6.5 Analysis of Map18 (Weighted Terrain)
	•	Realistic terrain costs created a challenge for simple heuristics.
	•	Manhattan ignored cost granularity and followed inefficient routes.
	•	Euclidean found optimal paths but expanded too widely.
	•	Hybrid adapted best, staying close to optimal while keeping computational cost low.
	•	Demonstrated that heuristic blending can generalize well to large-scale, terrain-sensitive environments.

7. Conclusion and Future Work (Updated)

This study systematically evaluated the impact of heuristic choice on the performance of the A* pathfinding algorithm across a diverse set of environments. Four heuristics—Manhattan, Euclidean, Diagonal (Chebyshev), and a custom Hybrid heuristic—were tested on various map types, including open fields, dense obstacle layouts, maze-like grids, indoor room structures, and a realistic weighted terrain map (Map18) from the Moving AI benchmark.

The results showed that Manhattan consistently delivered the fastest execution times but often produced suboptimal paths, especially in open and terrain-variable environments. Euclidean and Diagonal heuristics generated more accurate and shorter paths but came at the cost of significantly higher node expansions and computational overhead. The Hybrid heuristic, blending Manhattan and Euclidean with equal weighting, proved to be a highly effective compromise—achieving near-optimal path quality while maintaining acceptable execution times across all map types.

The inclusion of Map18 demonstrated the Hybrid heuristic’s generalizability to large-scale, cost-sensitive terrain. In this setting, it maintained competitive speed while avoiding the excessive expansion seen with Euclidean and Diagonal. This insight is critical for real-world applications where robots must operate in dynamic, high-cost environments such as delivery zones, rough terrain, or mixed urban spaces.

⸻

Future Work

This project opens the door to several promising research directions:
	•	Adaptive Heuristics: Future implementations could dynamically adjust heuristic weights based on local map structure (e.g., shifting from Manhattan in corridors to Euclidean in open areas).
	•	Learning-Based Heuristics: Incorporating machine learning to predict optimal heuristic weightings or generate context-aware heuristics could significantly enhance planning performance.
	•	Dynamic Environments: Testing heuristic performance in maps with moving obstacles or time-dependent cost changes would further simulate real-world conditions.
	•	Hardware-Targeted Optimization: Evaluating performance on actual robotic hardware or embedded systems will help assess energy consumption and practical feasibility.
	•	Terrain-Aware Heuristics: Designing heuristics that explicitly account for known terrain costs (e.g., preferring paved paths over grass) could further optimize routes in weighted graphs.

Ultimately, the findings suggest that hybrid or adaptive heuristics offer strong potential for improving A* search performance in both structured and unstructured environments. As robotics systems move toward greater autonomy and contextual awareness, intelligent heuristic selection will become a key driver of navigation efficiency.

Refrences ???????




***The authors used OpenAI’s ChatGPT to assist with language refinement, grammar correction, and formatting suggestions during the preparation of this manuscript.***
