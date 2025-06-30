# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the combined results CSV
# # df = pd.read_csv("results/combined_metrics.csv")
# df = pd.read_csv("results/metrics_ai_case_16room_002_2.csv")

# # Set plot style
# sns.set(style="whitegrid")
# metrics = ["path_length", "nodes_visited", "time_seconds", "optimality_ratio"]

# # Iterate over each metric and plot
# for metric in metrics:
#     plt.figure(figsize=(14, 6))
#     ax = sns.barplot(
#         data=df,
#         x="heuristic",
#         y=metric,
#         hue="map",
#         ci=None,
#         palette="viridis"
#     )
    
#     ax.set_title(f"{metric.replace('_', ' ').title()} by Heuristic", fontsize=16)
#     ax.set_ylabel(metric.replace('_', ' ').title())
#     ax.set_xlabel("Heuristic")
#     plt.legend(title="Map", bbox_to_anchor=(1.05, 1), loc='upper left')
#     plt.tight_layout()
#     plt.show()


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv("results/combined_metrics.csv")

# Set the style
sns.set(style="whitegrid")
metrics = ["path_length", "nodes_visited", "time_seconds", "optimality_ratio"]

# Create a bar chart for each metric
for metric in metrics:
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=df,
        x="heuristic",
        y=metric,
        hue="map",
        ci=None,
        edgecolor='black'
    )
    
    # Aesthetics
    ax.set_title(f"{metric.replace('_', ' ').title()} by Heuristic and Map", fontsize=16)
    ax.set_ylabel(metric.replace('_', ' ').title())
    ax.set_xlabel("Heuristic")
    plt.xticks(rotation=45)
    plt.legend(title="Map", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()