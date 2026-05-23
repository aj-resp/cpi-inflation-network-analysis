import pandas as pd
import numpy as np
import os

df = pd.read_csv("influence_scores/All_Scores.csv")

os.makedirs("top5", exist_ok=True)

# --- Weighting Scheme Fix ---
def get_corr_weights_safe(df):
    corr = df[["Degree", "Closeness", "Betweenness", "Eigenvector"]].corr().abs()

    # Compute uniqueness weights
    try:
        w = {}
        for col in corr.columns:
            denom = (1 + sum(corr[col]) - 1)
            if denom == 0:
                raise ZeroDivisionError
            w[col] = 1 / denom

        total = sum(w.values())
        for k in w:
            w[k] /= total

        if any(np.isnan(list(w.values()))):
            raise ValueError

        return w

    except:
        # FALLBACK: Variance-based weighting
        print("⚠ Correlation failed — using variance-based weights instead.")
        vars_ = df[["Degree", "Closeness", "Betweenness", "Eigenvector"]].var()
        total = vars_.sum()
        w = {col: vars_[col] / total for col in vars_.index}
        return w


# ====== Recompute Score_Corr using safe weights ======
corr_weights = get_corr_weights_safe(df)

df["Score_Corr"] = (
    corr_weights["Degree"] * df["Degree"] +
    corr_weights["Closeness"] * df["Closeness"] +
    corr_weights["Betweenness"] * df["Betweenness"] +
    corr_weights["Eigenvector"] * df["Eigenvector"]
)

# ------- Top 5 Extraction -------
def get_top5(df, score_col, outname):
    result = (
        df.groupby("City")[score_col]
          .mean()
          .sort_values(ascending=False)
          .head(5)
    )
    result_df = result.reset_index()
    result_df.columns = ["City", score_col]
    result_df.to_csv(f"top5/{outname}.csv", index=False)
    return result_df

top_equal = get_top5(df, "Score_Equal", "Top5_Equal_Weights")
top_corr  = get_top5(df, "Score_Corr", "Top5_Corr_Weights_FIXED")
top_categ = get_top5(df, "Score_Category", "Top5_Category_Weights")

print("\nTop 5 — Equal weighting:\n", top_equal)
print("\nTop 5 — Correlation/Variance weighting:\n", top_corr)
print("\nTop 5 — Category weighting:\n", top_categ)

print("\nSTEP 7 FIXED — New top 5 tables saved in /top5/")
