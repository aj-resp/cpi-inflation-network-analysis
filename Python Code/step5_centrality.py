import pandas as pd
import networkx as nx
import os

# Folder where edge lists are stored
EDGE_FOLDER = "edge_lists"

# Output folder for centrality results
os.makedirs("centrality", exist_ok=True)

# We only analyse threshold = 0.7 (simpler and enough for project)
TAU = "0.7"

# Get all edge list files for tau=0.7
edge_files = [f for f in os.listdir(EDGE_FOLDER) if f.endswith(f"tau{TAU}.csv")]

for file in edge_files:
    path = os.path.join(EDGE_FOLDER, file)
    print(f"Processing centrality for: {file}")

    # Example filename: Food_Staples_Grains_2023_tau0.7.csv
    parts = file.replace(".csv", "").split("_")
    # Category may contain underscores, so we join all except last 2
    cat = "_".join(parts[:-2])
    year = parts[-2]

    # Load edge list
    edges_df = pd.read_csv(path)

    # Build graph
    G = nx.Graph()
    for _, row in edges_df.iterrows():
        u = row["source"]
        v = row["target"]
        if "weight" in row:
            w = row["weight"]
            G.add_edge(u, v, weight=w)
        else:
            G.add_edge(u, v)

    # Compute centralities
    if len(G.nodes) == 0:
        print("Graph has no nodes, skipping.")
        continue

    degree = nx.degree_centrality(G)
    closeness = nx.closeness_centrality(G)
    betweenness = nx.betweenness_centrality(G, normalized=True)

    # eigenvector can sometimes fail; handle safely
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        eigenvector = {n: 0.0 for n in G.nodes}

    # Build DataFrame
    rows = []
    for node in G.nodes:
        rows.append({
            "City": node,
            "Category": cat,
            "Year": int(year),
            "Degree": degree.get(node, 0),
            "Closeness": closeness.get(node, 0),
            "Betweenness": betweenness.get(node, 0),
            "Eigenvector": eigenvector.get(node, 0)
        })

    cent_df = pd.DataFrame(rows)

    # Save per category-year file
    out_name = f"centrality/{cat}_{year}_centrality_tau{TAU}.csv"
    cent_df.to_csv(out_name, index=False)
    print(f"Saved centrality: {out_name}")

print("STEP 5 COMPLETED — Centrality tables generated!")
