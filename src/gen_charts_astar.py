import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV data
graph_name = "arena"
csv_path = "./results/csv/arena_evaluation.csv"
save_path = f"./results/img/{graph_name}/"
df = pd.read_csv(csv_path)

# Set plot style
sns.set(style="whitegrid")

# Convert column names to lower case for consistency
df.columns = [col.lower() for col in df.columns]

# -------------------------------
# A. Average Time per Heuristic
# -------------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="time_sec", ci="sd", estimator="mean", palette="muted")
plt.title("Average Time per Heuristic")
plt.ylabel("Time (seconds)")
plt.xlabel("Heuristic")
plt.tight_layout()
plt.savefig(save_path+"avg_time_per_heuristic.png")
plt.close()

# ----------------------------------
# B. Average Nodes Visited per Heuristic
# ----------------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="visited_nodes", ci="sd", estimator="mean", palette="pastel")
plt.title("Average Visited Nodes per Heuristic")
plt.ylabel("Visited Nodes")
plt.xlabel("Heuristic")
plt.tight_layout()
plt.savefig(save_path+"avg_visited_nodes.png")
plt.close()

# -----------------------------
# C. Average Path Length
# -----------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="path_length", ci="sd", estimator="mean", palette="deep")
plt.title("Average Path Length per Heuristic")
plt.ylabel("Path Length")
plt.xlabel("Heuristic")
plt.tight_layout()
plt.savefig(save_path+"avg_path_length.png")
plt.close()

# -----------------------------
# D. Total Cost vs. Expected Cost (Bar Chart Version)
# -----------------------------
# Drop rows where cost is missing
df_cost = df.dropna(subset=["expected_cost", "actual_cost"])

# Melt data for bar chart comparison
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

# Skip every 3rd label
xticks = plt.gca().get_xticks()
xticklabels = plt.gca().get_xticklabels()
plt.xticks(ticks=xticks[::3], labels=[label.get_text() for label in xticklabels[::3]], rotation=45)

plt.title("Expected vs Actual Cost by Case (Bar Chart)")
plt.ylabel("Cost")
plt.xlabel("Case ID")
plt.legend(title="Cost Type")
plt.tight_layout()
plt.savefig(save_path+"cost_comparison_bar_chart.png")
plt.close()


# -----------------------------
# E. Error Bars (example on time_sec with SD)
# -----------------------------
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x="heuristic", y="time_sec", ci="sd", estimator="mean", palette="dark")
plt.title("Time per Heuristic with Error Bars")
plt.ylabel("Time (seconds)")
plt.xlabel("Heuristic")
plt.tight_layout()
plt.savefig(save_path+"time_with_error_bars.png")
plt.close()

# -----------------------------
# F. Average Expected vs Actual Cost per Heuristic
# -----------------------------
# Drop rows with missing costs
df_cost_grouped = df.dropna(subset=["expected_cost", "actual_cost"])

# Group by heuristic and compute averages
grouped_avg = df_cost_grouped.groupby("heuristic")[["expected_cost", "actual_cost"]].mean().reset_index()

# Melt for bar plot format
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
plt.tight_layout()
y_max = grouped_melted["avg_cost"].max()
plt.ylim(0, y_max * 1.5)
plt.savefig(save_path+"avg_cost_per_heuristic.png")
plt.close()

print("✅ Graphs generated and saved as PNGs.")


