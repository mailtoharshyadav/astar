import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load CSV data
# graph_name = "arena"
# graph_name = "maze512-1-0"
# graph_name = "16room_002"
# graph_name = "16room_002"
graph_name = "Map18"


csv_path = f"./results/csv/{graph_name}_evaluation.csv"
save_path = f"./results/img/{graph_name}/"

# Ensure output directory exists
os.makedirs(save_path, exist_ok=True)

# Read CSV
df = pd.read_csv(csv_path)

# Set plot style
sns.set(style="whitegrid")

# Normalize column names
df.columns = [col.lower() for col in df.columns]

# -------------------------------
# A. Average Time per Heuristic
# -------------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="time_sec", ci=None, estimator="mean", palette="muted")
plt.title("Average Time per Heuristic")
plt.ylabel("Time (seconds)")
plt.xlabel("Heuristic")
for container in plt.gca().containers:
    plt.bar_label(container, fmt="%.4f", padding=3)
plt.tight_layout()
plt.savefig(save_path + "avg_time_per_heuristic.png")
plt.close()

# ----------------------------------
# B. Average Nodes Visited per Heuristic
# ----------------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="visited_nodes", ci=None, estimator="mean", palette="pastel")
plt.title("Average Visited Nodes per Heuristic")
plt.ylabel("Visited Nodes")
plt.xlabel("Heuristic")
for container in plt.gca().containers:
    plt.bar_label(container, fmt="%.0f", padding=3)
plt.tight_layout()
plt.savefig(save_path + "avg_visited_nodes.png")
plt.close()

# -----------------------------
# C. Average Path Length
# -----------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="path_length", ci=None, estimator="mean", palette="deep")
plt.title("Average Path Length per Heuristic")
plt.ylabel("Path Length")
plt.xlabel("Heuristic")
for container in plt.gca().containers:
    plt.bar_label(container, fmt="%.2f", padding=3)
plt.tight_layout()
plt.savefig(save_path + "avg_path_length.png")
plt.close()

# -----------------------------
# D. Total Cost vs. Expected Cost (Bar Chart Version)
# -----------------------------
df_cost = df.dropna(subset=["expected_cost", "actual_cost"])
df_cost_melted = pd.melt(
    df_cost,
    id_vars=["case_id", "heuristic"],
    value_vars=["expected_cost", "actual_cost"],
    var_name="cost_type",
    value_name="cost"
)

plt.figure(figsize=(14, 6))
sns.barplot(
    data=df_cost_melted,
    x="case_id",
    y="cost",
    hue="cost_type",
    palette="Set2",
    ci=None
)

# Skip every 3rd x-tick for readability
xticks = plt.gca().get_xticks()
xticklabels = plt.gca().get_xticklabels()
plt.xticks(ticks=xticks[::3], labels=[label.get_text() for label in xticklabels[::3]], rotation=45)

plt.title("Expected vs Actual Cost by Case (Bar Chart)")
plt.ylabel("Cost")
plt.xlabel("Case ID")
plt.legend(title="Cost Type")
# for container in plt.gca().containers:
#     plt.bar_label(container, fmt="%.2f", padding=3)
plt.tight_layout()
plt.savefig(save_path + "cost_comparison_bar_chart.png")
plt.close()

# -----------------------------
# E. Time with Error Bars (if needed later)
# -----------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="time_sec", ci=None, estimator="mean", palette="dark")
plt.title("Time per Heuristic with Error Bars")
plt.ylabel("Time (seconds)")
plt.xlabel("Heuristic")
for container in plt.gca().containers:
    plt.bar_label(container, fmt="%.4f", padding=3)
plt.tight_layout()
plt.savefig(save_path + "time_with_error_bars.png")
plt.close()

# -----------------------------
# F. Average Expected vs Actual Cost per Heuristic
# -----------------------------
df_cost_grouped = df.dropna(subset=["expected_cost", "actual_cost"])
grouped_avg = df_cost_grouped.groupby("heuristic")[["expected_cost", "actual_cost"]].mean().reset_index()
grouped_melted = pd.melt(
    grouped_avg,
    id_vars="heuristic",
    value_vars=["expected_cost", "actual_cost"],
    var_name="cost_type",
    value_name="avg_cost"
)

plt.figure(figsize=(8, 6))
sns.barplot(
    data=grouped_melted,
    x="heuristic",
    y="avg_cost",
    hue="cost_type",
    palette="Set2"
)
plt.title("Average Expected vs Actual Cost per Heuristic")
plt.ylabel("Average Cost")
plt.xlabel("Heuristic")
plt.legend(title="Cost Type")
for container in plt.gca().containers:
    plt.bar_label(container, fmt="%.3f", padding=3)
y_max = grouped_melted["avg_cost"].max()
plt.ylim(0, y_max * 1.5)
plt.tight_layout()
plt.savefig(save_path + "avg_cost_per_heuristic.png")
plt.close()

print("✅ Graphs generated and saved with value labels.")