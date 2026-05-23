import pandas as pd
import numpy as np
import os

CENT_FOLDER = "centrality"
OUTPUT_FOLDER = "influence_scores"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load all centrality files
files = [f for f in os.listdir(CENT_FOLDER) if f.endswith(".csv")]

all_data = []

for file in files:
    df = pd.read_csv(os.path.join(CENT_FOLDER, file))
    df["SourceFile"] = file
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)

# ------------------------------
# SCHEME 1: Equal Weighting
# ------------------------------
data["Score_Equal"] = (
    0.25 * data["Degree"] +
    0.25 * data["Closeness"] +
    0.25 * data["Betweenness"] +
    0.25 * data["Eigenvector"]
)

# ------------------------------
# SCHEME 2: CORRELATION-BASED
# ------------------------------
def correlation_weights(df):
    corr = df[["Degree", "Closeness", "Betweenness", "Eigenvector"]].corr().abs()
    
    # uniqueness score: 1 / (1 + sum of correlations)
    w = {}
    for col in corr.columns:
        w[col] = 1 / (1 + sum(corr[col]) - 1)  # subtract self-correlation
    total = sum(w.values())
    for k in w:
        w[k] /= total
    return w

weights_corr = correlation_weights(data)

data["Score_Corr"] = (
    weights_corr["Degree"] * data["Degree"] +
    weights_corr["Closeness"] * data["Closeness"] +
    weights_corr["Betweenness"] * data["Betweenness"] +
    weights_corr["Eigenvector"] * data["Eigenvector"]
)

# ------------------------------
# SCHEME 3: CATEGORY IMPORTANCE
# ------------------------------

category_weights = {
    "Food_Staples_Grains": 0.25,
    "Utilities_Transport": 0.20,
    "Oils_Sweeteners_Condiments": 0.10,
    "Fruits_Vegetables": 0.10,
    "Meat_Poultry_Dairy": 0.10,
    "Non_Food_Essentials": 0.10,
    "Clothing_Misc": 0.15
}

data["Score_Category"] = (
    category_weights.get(data["Category"].iloc[0], 0.10) *
    (0.25 * data["Degree"] +
     0.25 * data["Closeness"] +
     0.25 * data["Betweenness"] +
     0.25 * data["Eigenvector"])
)

# ------------------------------
# SAVE MASTER FILE
# ------------------------------
data.to_csv(f"{OUTPUT_FOLDER}/All_Scores.csv", index=False)

print("Weighted centrality scores saved in: influence_scores/")
