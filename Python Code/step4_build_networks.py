import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt
import os

# Load vector dataset
df = pd.read_excel("CPI_Vectors.xlsx")
df = df.dropna(subset=["Category"])

cities = sorted(df["City"].unique())
categories = sorted(df["Category"].unique())
years = [2023, 2024]

# Create output folders
os.makedirs("graphs", exist_ok=True)
os.makedirs("edge_lists", exist_ok=True)

# Function: build graph from similarity matrix
def build_graph(sim_matrix, labels, threshold):
    G = nx.Graph()
    G.add_nodes_from(labels)

    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i, j] >= threshold:
                G.add_edge(labels[i], labels[j], weight=sim_matrix[i, j])
    return G

# Function: save graph image
def save_graph(G, title, filename):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=8, edge_color="gray")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# MAIN LOOP
thresholds = [0.6, 0.7, 0.8]

for cat in categories:
    for year in years:
        print(f"\nProcessing {cat}, {year}")

        # Get vectors
        temp = df[(df["Category"] == cat) & (df["Year"] == year)]
        vectors = []
        city_list = []

        for city in cities:
            row = temp[temp["City"] == city]
            if len(row) == 1:
                vec = row.iloc[:, 3:].values.flatten()
                vectors.append(vec)
                city_list.append(city)

        vectors = np.array(vectors)
        if vectors.shape[0] < 2:
            print("Not enough cities!")
            continue

        # Build similarity matrix
        sim_matrix = cosine_similarity(vectors)

        # PROCESS FOR EACH THRESHOLD
        for tau in thresholds:
            G = build_graph(sim_matrix, city_list, tau)

            title = f"{cat} — {year} — Threshold {tau}"
            filename_img = f"graphs/{cat}_{year}_tau{tau}.png"
            filename_edges = f"edge_lists/{cat}_{year}_tau{tau}.csv"

            # Save graph image
            save_graph(G, title, filename_img)

            # Save edge list
            edge_data = nx.to_pandas_edgelist(G)
            edge_data.to_csv(filename_edges, index=False)

            print(f"Graph saved: {filename_img}")
            print(f"Edges saved: {filename_edges}")

print("STEP 4 COMPLETED — All networks generated!")
