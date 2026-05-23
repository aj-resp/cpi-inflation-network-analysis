import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import os

# -----------------------------
# LOAD VECTORS AND CLEAN
# -----------------------------
df = pd.read_excel("CPI_Vectors.xlsx")

# Drop rows where Category is missing
df = df.dropna(subset=["Category"])

# Get unique lists
cities = sorted(df["City"].unique())
categories = sorted(df["Category"].unique())
years = [2023, 2024]

# -----------------------------
# FUNCTION: SAVE HEATMAP
# -----------------------------
def save_heatmap(matrix, labels, title, filename):
    plt.figure(figsize=(10, 8))
    plt.imshow(matrix, interpolation='nearest')
    plt.title(title)
    plt.colorbar(label="Cosine similarity")
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=90)
    plt.yticks(ticks=range(len(labels)), labels=labels)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# -----------------------------
# CREATE OUTPUT FOLDER
# -----------------------------
os.makedirs("heatmaps", exist_ok=True)

# -----------------------------
# MAIN LOOP: CATEGORY × YEAR
# -----------------------------
for cat in categories:
    for year in years:
        # Filter for this category & year
        temp = df[(df["Category"] == cat) & (df["Year"] == year)]

        vectors = []
        city_list = []

        for city in cities:
            row = temp[temp["City"] == city]
            if len(row) == 1:
                # columns: City, Category, Year, March...December
                vec = row.iloc[:, 3:].values.flatten()
                vectors.append(vec)
                city_list.append(city)

        vectors = np.array(vectors)

        # Need at least 2 cities to compute similarity
        if vectors.shape[0] < 2:
            print(f"Skipping {cat}, {year} (not enough cities)")
            continue

        # Compute cosine similarity matrix
        sim_matrix = cosine_similarity(vectors)

        # Build filename & title
        safe_cat = str(cat)
        filename = f"heatmaps/{safe_cat}_{year}_similarity.png"
        title = f"Cosine Similarity Heatmap — {safe_cat} — {year}"

        # Save heatmap
        save_heatmap(sim_matrix, city_list, title, filename)
        print(f"Saved: {filename}")

print("STEP 3 COMPLETED — All possible heatmaps generated!")
