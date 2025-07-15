1. Abstract

Pathfinding is a fundamental requirement in autonomous robotics, and the A* algorithm remains one of the most efficient and widely adopted approaches for solving this problem. This paper explores the impact of heuristic selection on A* performance by comparing four heuristics: Manhattan, Euclidean, Diagonal (Chebyshev), and a custom Hybrid heuristic that combines Manhattan and Euclidean. These were tested across multiple map types—open arena, obstacle-dense random fields, room-like partitions, and maze-like corridors—representing realistic robotic navigation environments.

Performance was evaluated using key metrics including path length, computation time, node expansions, and deviation from optimal cost. Results demonstrate that Manhattan is the fastest but often leads to suboptimal paths, while Euclidean offers greater accuracy at higher computational cost. The Hybrid heuristic, weighted equally between Manhattan and Euclidean, achieves a balance by reducing path cost without significant increase in execution time. Visual path overlays further illustrate the trade-offs between heuristics. This study provides empirical insight into heuristic design for A* and proposes a direction for future work in adaptive or map-aware heuristics tailored to specific environments.

⸻

2. Introduction

Efficient path planning is a cornerstone of autonomous mobile robotics, enabling agents to navigate complex environments to reach target destinations. The A* algorithm is a widely used solution in both academia and industry due to its balance of optimality and efficiency. However, A*’s performance heavily depends on the choice of heuristic function, which estimates the remaining cost from a node to the goal. In real-world robotics—such as warehouse automation, delivery systems, or indoor navigation—the structure of the environment can significantly impact heuristic effectiveness.

While the Manhattan heuristic is well-suited for grid-based 4-directional movement and offers computational speed, it often produces longer paths when diagonal movement is allowed. Conversely, Euclidean and Diagonal heuristics offer greater accuracy in open or flexible spaces but require more node expansions and computation. This paper investigates the behavior of these heuristics across a range of map types and introduces a Hybrid heuristic that balances speed and optimality.

By treating each map as a simulated robot navigation task, we explore how each heuristic performs under different spatial constraints and propose empirical guidelines for heuristic selection in robotic applications.

⸻

3. Related Work

The A* algorithm was first introduced by Hart, Nilsson, and Raphael (1968) and remains a foundational technique for graph-based pathfinding. Its ability to guarantee optimality when using an admissible heuristic has made it a standard in fields such as robotics, video games, and AI planning. In robotic systems, A* is often employed for local and global navigation in grid-based maps, with its performance highly sensitive to the choice of heuristic function.

Manhattan and Euclidean heuristics are among the most commonly used. Manhattan distance is ideal for scenarios constrained to four-directional movement, while Euclidean distance approximates realistic motion more accurately in 8-directional or continuous spaces. Chebyshev distance (Diagonal heuristic) further accommodates diagonal movement with uniform cost assumptions.

Recent studies have explored ways to improve heuristic accuracy and adaptability. These include hybrid heuristics, weighted heuristics (e.g., weighted A*), and learning-based approaches that tailor the heuristic based on environment features. Notably, context-sensitive heuristics—which adjust based on map topology—have shown promise in dynamically improving A* performance without compromising completeness or admissibility. This paper builds on this foundation by implementing a simple hybrid heuristic and evaluating its impact across a variety of environmental structures.

4. Methodology

4.1 Heuristic Definitions

To evaluate the effect of different heuristics on A* pathfinding, the following four heuristics were implemented modularly in Python:
	•	Manhattan Distance:
h(n) = |x_1 - x_2| + |y_1 - y_2|
Suitable for 4-directional movement on a grid.
	•	Euclidean Distance:
h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}
Models realistic, continuous space traversal—ideal when diagonal movement is allowed.
	•	Diagonal (Chebyshev) Distance:
h(n) = \max(|x_1 - x_2|, |y_1 - y_2|)
Assumes uniform cost for diagonal movement.
	•	Hybrid Heuristic:
A linear combination of Manhattan and Euclidean distances:
h_{\text{hybrid}} = 0.5 \cdot h_{\text{Manhattan}} + 0.5 \cdot h_{\text{Euclidean}}
Designed to balance computational efficiency and path accuracy.

These heuristics were modularized via heuristics.py, allowing flexible integration into the core A* engine.

4.2 A* Pathfinding Implementation

The A* algorithm was implemented in astar.py, supporting both 4- and 8-directional movement. Key design components include:
	•	Open list: Maintained as a min-heap using Python’s heapq, prioritizing nodes by total cost f(n) = g(n) + h(n).
	•	Closed list: Stores visited nodes to prevent re-expansion.
	•	Movement Model: Dependent on heuristic—Manhattan restricts to 4 directions, while others allow diagonal traversal.
	•	Collision Handling: Obstacles were modeled as impassable cells in the binary map.
	•	Goal Termination: The search terminates upon reaching the goal node with minimum cost.

⸻

4.3 Experimental Environment

All experiments were conducted using Python 3 on a standard CPU laptop (no GPU). Visualizations were created with Matplotlib. The automation script gen_csv_astar.py was developed to run batches of tests and log performance metrics.

4.4 Map Types and Scenarios

Four types of 2D grid maps were used to simulate common navigation environments:
	1.	Arena – Sparse obstacles, mimicking open warehouse spaces.
	2.	Random – High obstacle density, resembling urban or cluttered layouts.
	3.	Room – Partitioned indoor-like layout with room structures.
	4.	Maze – Narrow, winding corridors with limited valid paths.

Each map is represented as a binary image:
	•	Black: obstacles
	•	White: free space
	•	Blue: start point
	•	Red: goal point
	•	Green: final path (for visual inspection)

Start and goal locations were manually placed to ensure solvability across all maps.

⸻

4.5 Evaluation Metrics

The following metrics were recorded for every heuristic on every map:
	•	Path Length: Total number of steps from start to goal.
	•	Visited Nodes: Number of nodes expanded during search.
	•	Execution Time: Measured using wall-clock timing per run.
	•	Cost Deviation: Difference between expected and actual path cost.
	•	Error Bars: For time metrics, multiple runs were used to compute variance.

All results were logged to CSV files and later visualized as bar graphs and overlays.

5. Results

The performance of each heuristic was evaluated across four distinct map types: arena, random, room, and maze. For each, five key metrics were collected: average path length, nodes expanded, execution time, cost deviation, and time variance (with error bars). The results highlight how heuristic choice significantly impacts A*’s behavior in different environments.

⸻

5.1 Arena Map

The arena map represents a sparsely obstructed field with wide open movement areas.
	•	Execution Time: Manhattan was the fastest, followed by Hybrid and Euclidean. Diagonal took slightly longer.
	•	Path Length: Euclidean produced the shortest path; Manhattan’s was notably longer due to 4-direction limitation.
	•	Visited Nodes: Manhattan expanded the fewest nodes, while Euclidean and Hybrid visited more due to diagonal reachability.
	•	Error Bars: Minimal variance across heuristics—arena offered predictable performance.
	•	Cost Deviation: Manhattan had the largest gap from expected cost, while Euclidean and Hybrid stayed closer.

Interpretation: In open spaces, diagonal-capable heuristics are advantageous for accuracy. Manhattan is efficient but suboptimal.

⸻

5.2 Random Map

This map simulates high obstacle density, with irregularly scattered blockers.
	•	Execution Time: All heuristics performed similarly; Hybrid was slightly slower due to blended computation.
	•	Path Length: Euclidean again offered the shortest paths. Hybrid closely matched, with Diagonal lagging slightly.
	•	Visited Nodes: All heuristics visited a high number of nodes, reflecting map complexity. Hybrid reduced this modestly.
	•	Cost Deviation: Hybrid and Euclidean had minimal error, while Manhattan showed higher deviation.

Interpretation: In dense environments, Hybrid offers a good balance—retaining Manhattan’s speed while gaining Euclidean’s optimality.

⸻

5.3 Room Map

This partitioned layout features corridors and room-like structures.
	•	Execution Time: Manhattan remained fastest; Hybrid close behind.
	•	Path Length: Hybrid and Euclidean produced near-optimal paths. Manhattan was longer due to orthogonal bias.
	•	Visited Nodes: Diagonal expanded the most; Hybrid reduced node expansions effectively.
	•	Error Bars: Time variance increased due to corridor routing complexity.

Interpretation: Hybrid heuristics help in semi-structured environments by minimizing both path cost and node expansions.

⸻

5.4 Maze Map

A challenging narrow-corridor map requiring tight navigation.
	•	Execution Time: Manhattan again outperformed others in speed.
	•	Path Length: All heuristics converged to similar values—limited path options in maze make direction less impactful.
	•	Visited Nodes: Manhattan expanded fewer nodes due to its greedy orthogonal search.
	•	Cost Deviation: Minimal across all heuristics—maze structure constrained route choices.

Interpretation: In mazes, heuristic impact is reduced. Even basic heuristics perform comparably due to tight constraints.

⸻

5.5 Path Overlay Comparison

To highlight qualitative differences, visual overlays were generated for Arena map:
	•	Manhattan produced zig-zag, stair-stepped paths, extending path length in open areas.
	•	Euclidean followed a smoother, straight-line trajectory with diagonal moves.
	•	Hybrid tracked closely with Euclidean while maintaining faster execution.

These visuals demonstrate why Manhattan, while faster, can result in inefficient navigation—especially in domains allowing free movement.

6. Analysis

This section provides a detailed examination of how each heuristic influenced A*’s performance across different map types and what the results imply for real-world robotic navigation. The analysis draws on both quantitative metrics and visual evidence.

⸻

6.1 Heuristic Trade-offs

The Manhattan heuristic consistently delivered the fastest execution times due to its restricted 4-directional movement model and simpler arithmetic. However, this speed came at the cost of path optimality, especially in maps like arena or room, where diagonal movement could significantly reduce path length. Visual overlays clearly show zig-zag trajectories and detours when using Manhattan in open maps.

In contrast, Euclidean produced smoother and shorter paths across all map types. Its diagonal movement capability makes it ideal for navigating open fields or rooms. However, this improvement comes at the expense of increased node expansions and processing time, as seen in the random and maze maps where search space complexity is high.

The Diagonal (Chebyshev) heuristic, although theoretically ideal for 8-direction movement with equal cost, often underperformed in terms of node efficiency. Its aggressive expansion in all directions led to larger search areas, making it less effective in tightly constrained environments.

⸻

6.2 Hybrid Heuristic Performance

The Hybrid heuristic, designed as a weighted blend h = 0.5 \cdot h_{\text{Manhattan}} + 0.5 \cdot h_{\text{Euclidean}}, successfully mitigated the limitations of its parent heuristics:
	•	It retained Manhattan’s computational simplicity while benefiting from Euclidean’s accuracy.
	•	It showed moderate execution times across all maps, never the slowest nor the fastest.
	•	Path length and cost deviation were consistently close to optimal.
	•	In maps like room and random, it reduced node expansions more effectively than either parent heuristic.

The hybrid’s balanced behavior suggests that blending heuristics can lead to general-purpose planning strategies suitable for a wide range of environments, especially when environmental structure is unknown or dynamic.

⸻

6.3 Environment-Specific Insights
	•	In open spaces (arena), diagonal movement is critical. Manhattan performs poorly here, while Euclidean and Hybrid excel.
	•	In obstacle-dense fields (random), heuristic performance converges, but Hybrid offers a slight edge by avoiding over-expansion.
	•	In structured indoor maps (room), Hybrid reduces detours common in Manhattan without adding computational load.
	•	In mazes, all heuristics converge in performance; constrained paths negate directional advantages, reducing the impact of heuristic design.

These findings suggest that no single heuristic is best in all environments—the map structure plays a decisive role in determining which heuristic performs optimally.

⸻

6.4 Visual Comparison as Justification

The included path overlay images clearly demonstrate that:
	•	Manhattan can take unnecessary detours around diagonal corridors or open areas.
	•	Euclidean and Hybrid follow more natural, straight-line paths.
	•	In environments where every movement decision matters (e.g., delivery robots or warehouse bots), even small differences in path length can impact total task efficiency.

7. Conclusion and Future Work

This study evaluated the impact of heuristic selection on the performance of A* pathfinding across diverse map environments. Through extensive testing using Manhattan, Euclidean, Diagonal (Chebyshev), and a Hybrid heuristic, it was demonstrated that no single heuristic dominates across all scenarios. The Manhattan heuristic, while computationally fast, produced longer and less efficient paths in environments where diagonal movement was beneficial. The Euclidean heuristic consistently delivered more optimal paths but incurred higher computational costs.

The Hybrid heuristic, combining Manhattan and Euclidean with equal weights, emerged as a strong general-purpose solution. It balanced the speed of Manhattan with the directional flexibility of Euclidean, yielding near-optimal paths with only moderate increases in node expansions and runtime. Particularly in semi-structured or cluttered environments such as room and random, the hybrid approach provided a favorable compromise between efficiency and path quality.

In the future, the research can be extended in multiple directions:
	•	Adaptive Heuristics: Dynamically altering heuristic weights based on local map context (e.g., open vs. constrained space).
	•	Environment-Aware Tuning: Learning the best heuristic per map type or even per region within a map.
	•	Larger-scale and Dynamic Environments: Including moving obstacles, larger maps, or real-time re-planning scenarios.
	•	Hardware Evaluation: Testing on embedded or mobile platforms to assess real-world execution time and resource constraints.

These extensions can further bridge the gap between theoretical pathfinding and practical robotic deployment, making navigation systems more robust, efficient, and context-aware.





***The authors used OpenAI’s ChatGPT to assist with language refinement, grammar correction, and formatting suggestions during the preparation of this manuscript.***
