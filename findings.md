1. manhattan- is best for 4 dir not 8 thats why bigger path
2. we need to add medain also to all graphs


findings

-- 
arena

1. average cost expected vs actual
 - everyone is giving same results 
 - manhattan is givig slightly more value because of 4 dir behavoiur
 - hybrid use 50% value of manhattan so little deviation is seen

 2. average path length, aprat from manhattan every one seeing same, manhattan seeing slightly highter

 3. average time per huristic


 🔹 From Average Time per Heuristic:
	•	Fastest: Manhattan and Hybrid (≈ 0.0002s)
	•	Slowest: Diagonal (≈ 0.0016s)
	•	Euclidean: Moderate (≈ 0.0008s)

🔹 From Average Visited Nodes:
	•	Fewest Expansions: Manhattan (26) and Hybrid (28)
	•	Most Expansions: Diagonal (254) > Euclidean (132)

🔹 From Average Path Length:
	•	All heuristics are very close (22.64–22.98)
	•	Manhattan produced slightly longer paths on average

🔹 From Expected vs Actual Cost per Heuristic:
	•	Expected Cost is constant across heuristics (≈ 26.086)
	•	Actual Cost:
	•	Manhattan overshot most (≈ 26.32 → error ~0.24)
	•	Hybrid ≈ 26.16, Diagonal ≈ 26.086, Euclidean ≈ 26.086 (very close)


2. randomMap

