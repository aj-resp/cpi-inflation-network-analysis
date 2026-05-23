# 📊 CPI Inflation Network Analysis — Pakistan (2023–2024)

A **Discrete Mathematics** final project that applies **graph theory**, **cosine similarity**, and **network centrality** to analyze Pakistan's Consumer Price Index (CPI) inflation data across multiple cities and product categories.

---

## 🔍 What This Project Does

This project treats inflation data as a **network/graph problem**:
- Each product item is a **node**
- If two items have similar price movement patterns, they are connected by an **edge**
- Graph centrality then reveals **which items drive inflation the most**

The full pipeline runs in 8 steps, from raw data cleaning all the way to temporal inflation pattern analysis.

---

## 🗂️ Project Structure

```
cpi-inflation-network-analysis/
│
├── Python Code/
│   ├── pp.py                          # Step 1 - Data preprocessing & category mapping
│   ├── step2_build_vectors.py         # Step 2 - Build CPI price vectors per city
│   ├── step3_cosine_similarity.py     # Step 3 - Compute cosine similarity + heatmaps
│   ├── step4_build_networks.py        # Step 4 - Build correlation networks (τ = 0.6/0.7/0.8)
│   ├── step5_centrality.py            # Step 5 - Calculate degree/betweenness centrality
│   ├── step6_weighted_centrality.py   # Step 6 - Weighted centrality scores
│   ├── step7_top5.py                  # Step 7 - Identify top 5 most influential items
│   ├── step8_temporal_relation.py     # Step 8 - Temporal inflation pattern analysis
│   │
│   ├── CPI_Vectors.xlsx               # Input - CPI price vectors
│   ├── Cleaned_CPI_Data.xlsx          # Input - Cleaned raw CPI data
│   ├── temporal_relation_summary.csv  # Output - Temporal analysis results
│   │
│   ├── heatmaps/                      # Output - Cosine similarity heatmap images
│   ├── edge_lists/                    # Output - Network edge lists (CSV)
│   ├── centrality/                    # Output - Centrality scores (CSV)
│   ├── top5/                          # Output - Top 5 influential items (CSV)
│   └── influence_scores/              # Output - Full influence score rankings
│
├── Report/
│   └── report.docx                    # Full project report with methodology & findings
│
└── README.md
```

> ⚠️ **Note:** The `graphs/` folder (network visualizations) is not included in this repo due to its large size (37MB). It is **automatically generated** when you run `step4_build_networks.py`.

---

## 📦 Categories Analyzed

| Category | Examples |
|----------|----------|
| 🌾 Food Staples & Grains | Wheat flour, Rice, Bread, Sugar, Milk |
| 🥩 Meat, Poultry & Dairy | Beef, Mutton, Chicken, Eggs |
| 🥦 Fruits & Vegetables | Potatoes, Tomatoes, Onions, Bananas |
| 🫙 Oils, Sweeteners & Condiments | Cooking oil, Ghee, Tea, Chilies powder |
| 🧴 Non-Food Essentials | Soap, Washing powder, Shoes, Cigarettes |
| ⚡ Utilities & Transport | Petrol, Electricity, Telephone, Firewood |
| 👕 Clothing & Misc | Shirting, Tailoring charges, Energy savers |

---

## 🛠️ Requirements

- Python 3.8 or higher
- The following libraries:

```
pandas
numpy
networkx
matplotlib
scikit-learn
openpyxl
```

Install all:
```
pip install pandas numpy networkx matplotlib scikit-learn openpyxl
```

---

## 🚀 How to Run

1. Open the `Python Code/` folder
2. Run each script one by one in this order:

```
python pp.py
python step2_build_vectors.py
python step3_cosine_similarity.py
python step4_build_networks.py
python step5_centrality.py
python step6_weighted_centrality.py
python step7_top5.py
python step8_temporal_relation.py
```

---

## 📈 Key Concepts Used

- **Cosine Similarity** — measures how similar two items' price movement vectors are
- **Threshold (τ)** — controls how strong a connection must be to form an edge (tested at 0.6, 0.7, 0.8)
- **Degree Centrality** — how many connections an item has
- **Betweenness Centrality** — how often an item acts as a bridge in the network
- **Temporal Analysis** — tracks how inflation relationships changed from 2023 to 2024

---

## 📄 Report

The full methodology, results, and analysis are documented in [`Report/report.docx`](Report/report.docx).

---

## 👨‍💻 Authors

| Student ID |
|------------|
| 24i-0569 |
| 24i-0549 |
| 24p-0773 |

**Course:** Discrete Mathematics — Final Project
