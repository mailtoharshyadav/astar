1. Abstract

Pathfinding is a fundamental requirement in autonomous robotics, and the A* algorithm remains one of the most efficient and widely adopted approaches for this task. This paper investigates the impact of heuristic selection on A* performance by comparing four heuristic strategies: Manhattan, Euclidean, Diagonal (Chebyshev), and a custom Hybrid heuristic combining Manhattan and Euclidean with equal weight.

These heuristics were tested on a diverse set of map environments, including open fields, obstacle-dense layouts, indoor-like room partitions, maze-like corridors, and a weighted multi-terrain map (Map18 from the Moving AI benchmark) that simulates real-world cost variations. For each heuristic and map, we collected detailed metrics: path length, nodes expanded, execution time, and deviation from expected cost.

Results reveal that Manhattan is consistently the fastest, but often produces suboptimal paths, especially in open or diagonal-friendly maps. Euclidean and Diagonal improve path quality but at the cost of greater computational load. The Hybrid heuristic effectively balances both, offering near-optimal path length with reduced expansion overhead. In weighted terrain, it outperforms Manhattan in path quality while remaining significantly faster than Euclidean.

This study offers empirical insights into heuristic design and presents practical guidance for deploying A* in varied robotic contexts, especially where trade-offs between speed, accuracy, and terrain sensitivity are critical.

⸻

Introduction

Efficient path planning is essential in autonomous robotics, allowing agents to navigate from a start point to a goal while avoiding obstacles and minimizing travel cost. The A* search algorithm is widely used for this purpose due to its balance between optimality and efficiency when guided by a suitable heuristic.

However, A*’s performance depends heavily on the heuristic function used, which estimates the cost from a given node to the goal. The choice of heuristic impacts not only path quality but also computational cost and speed—key concerns in real-time robotic systems. Common heuristics like Manhattan, Euclidean, and Chebyshev are popular in grid-based environments, but their effectiveness can vary across different map types and terrain conditions.

This study evaluates these heuristics on two types of maps:
	•	Binary grid maps: including open spaces, random obstacles, and maze-like structures, based on standard Moving AI Lab maps.
	•	Weighted multi-terrain maps: such as Map18, where movement costs vary to simulate real-world terrain.

A custom Hybrid heuristic, combining Manhattan and Euclidean distances, is also introduced to balance speed and accuracy.

The paper aims to analyze how these heuristics perform across diverse environments, using metrics like path length, execution time, and nodes expanded. The findings offer practical guidance for choosing effective heuristics in real-world robotic applications.


3. Related Work

Related Work

The A* algorithm was first introduced by Hart, Nilsson, and Raphael (1968) and remains a foundational technique for graph-based pathfinding. Its ability to guarantee optimality when using an admissible heuristic has made it a standard in fields such as robotics, video games, and AI planning. In robotic systems, A* is often employed for both local and global navigation in grid-based maps, with its performance being highly dependent on the choice of heuristic function.

Manhattan and Euclidean heuristics are among the most commonly used. Manhattan distance is suited for four-directional movement, while Euclidean distance better models continuous or diagonal motion. Chebyshev distance (also known as the Diagonal heuristic) further supports diagonal movement with uniform cost assumptions. These heuristics are widely used in grid-based robotic navigation, but their effectiveness can vary significantly depending on the environment.

Recent research has explored improved heuristic strategies, such as hybrid heuristics, weighted A*, and learning-based methods. These include techniques that adapt heuristics based on map features or pre-training on known environments to speed up planning. While effective, such methods can require significant setup or lack flexibility in unknown or dynamic environments. In contrast, this study focuses on on-the-fly heuristic evaluation, aiming for real-time use without relying on prior map-specific training.

We propose a lightweight Hybrid heuristic, combining Manhattan and Euclidean distances, and evaluate it across varied map types to provide practical insights for robotic path planning.

4. Methodology

4.1 Heuristic Definitions

To evaluate the effect of different heuristics on A* pathfinding, four modular heuristic functions were implemented:
	•	Manhattan Distance
Suitable for 4-directional movement on grids:
h(n) = |x_1 - x_2| + |y_1 - y_2|
	•	Euclidean Distance
Approximates straight-line travel across open areas:
h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}
	•	Diagonal (Chebyshev) Distance
Allows 8-directional uniform-cost movement:
h(n) = \max(|x_1 - x_2|, |y_1 - y_2|)
	•	Hybrid Heuristic
A linear combination of Manhattan and Euclidean distances:
h_{\text{hybrid}} = 0.5 \cdot h_{\text{Manhattan}} + 0.5 \cdot h_{\text{Euclidean}}
Designed to balance fast computation with realistic path quality.

⸻

4.2 A Pathfinding Implementation*

The A* pathfinding algorithm was implemented in Python and supports 8-directional movement. A priority queue manages the open list, ordered by total cost f(n) = g(n) + h(n), while a closed list avoids revisiting expanded nodes. Obstacles are modeled as impassable cells. Once the goal is reached, the path is reconstructed by backtracking from the goal to the start node. In weighted environments, the algorithm accumulates terrain-specific costs for more realistic evaluation.

⸻

4.3 Metric Logging and Evaluation Tools

A script was developed to run A* with each heuristic across various map types, using SCEN files from the Moving AI Benchmark to define start and goal test cases. Performance data was recorded in structured CSV files. The following metrics were tracked:
	•	Path length
	•	Number of visited nodes (open + closed)
	•	Execution time
	•	Expected vs. actual path cost (benchmarked against SCEN solutions)
	•	Time variance across multiple runs

To aid analysis, HTML-based visualizations were generated for each run:
	•	Blue: Visited nodes
	•	Red: Goal
	•	Green: Final path
	•	Black: Obstacles

These visuals help explain why certain heuristics perform differently in terms of speed and path quality.

⸻

4.4 Experimental Setup and Tools
	•	Language: Python 3.x
	•	Libraries: NumPy, Matplotlib, heapq
	•	Hardware: MacBook M2 Pro (standard desktop use)
	•	Map Format: All maps were grid-based and sourced from the Moving AI Lab dataset, which includes diverse environments with varying obstacle density and terrain cost. Each map type presents distinct pathfinding challenges.

⸻

4.5 Map Types

The following maps from the Moving AI Benchmark were used to simulate diverse navigation environments:
	1.	Arena – Open grid with minimal obstacles
	2.	Random – High-density, randomly placed obstacles
	3.	Room – Partitioned space resembling indoor layouts
	4.	Maze – Tight corridors and constrained paths
	5.	Map18 – A large, weighted map with varying terrain costs, designed to simulate real-world navigation challenges

All results were logged to CSV files and visualized using graphs and map overlays.

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


6.x Path Overlay Visualization

Overlay images (provided for arena map) demonstrated:
	•	Manhattan created stair-step patterns and inefficient routing.
	•	Euclidean followed smoother, direct paths.
	•	Hybrid closely mimicked Euclidean with improved speed.


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

7. Conclusion and Future Work 

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

Redblob games??



***The authors used OpenAI’s ChatGPT to assist with language refinement, grammar correction, and formatting suggestions during the preparation of this manuscript.***
