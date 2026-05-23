import pandas as pd
import os

EDGE_FOLDER = "edge_lists"
TAU = "0.7"

# Get all edge list files for this threshold
edge_files = [f for f in os.listdir(EDGE_FOLDER) if f.endswith(f"tau{TAU}.csv")]

# Convert edge list dataframe → set of undirected edges
def edge_set_from_csv(path):
    df = pd.read_csv(path)
    edges = set()
    for _, row in df.iterrows():
        u = row["source"]
        v = row["target"]
        edge = tuple(sorted([u, v]))   # undirected edge
        edges.add(edge)
    return edges

results = []

categories = [
    "Clothing_Misc",
    "Food_Staples_Grains",
    "Fruits_Vegetables",
    "Meat_Poultry_Dairy",
    "Non_Food_Essentials",
    "Oils_Sweeteners_Condiments",
    "Utilities_Transport"
]

for cat in categories:
    file_2023 = f"{cat}_2023_tau{TAU}.csv"
    file_2024 = f"{cat}_2024_tau{TAU}.csv"

    path23 = os.path.join(EDGE_FOLDER, file_2023)
    path24 = os.path.join(EDGE_FOLDER, file_2024)

    if not (os.path.exists(path23) and os.path.exists(path24)):
        print(f"❌ Missing: {cat}")
        continue

    E23 = edge_set_from_csv(path23)
    E24 = edge_set_from_csv(path24)

    # Determine temporal relation
    if E23 == E24:
        relation = "Equal (E2023 = E2024)"
    elif E23.issubset(E24):
        relation = "E2023 ⊆ E2024 (2023 T 2024)"
    elif E24.issubset(E23):
        relation = "E2024 ⊆ E2023 (2024 T 2023)"
    else:
        relation = "No relation (incomparable)"

    print(f"{cat}: {relation}")
    results.append({"Category": cat, "Relation": relation})

# Save the summary
summary_path = "temporal_relation_summary.csv"
pd.DataFrame(results).to_csv(summary_path, index=False)
print(f"\nSTEP 8 COMPLETED — summary saved to {summary_path}")
