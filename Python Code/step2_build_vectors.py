import pandas as pd
import numpy as np

# Load cleaned data
df = pd.read_excel("Cleaned_CPI_Data.xlsx")

# Make sure months are ordered correctly
month_order = ["March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]

df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

# Create a pivot table: City × Category × Year → Monthly vector
vectors = {}

cities = df["City"].unique()
categories = df["Category"].unique()
years = [2023, 2024]

for city in cities:
    for cat in categories:
        for year in years:
            temp = df[(df["City"] == city) &
                      (df["Category"] == cat) &
                      (df["Year"] == year)].sort_values("Month")

            monthly_prices = temp["Price"].values

            if len(monthly_prices) == 10:
                vectors[(city, cat, year)] = monthly_prices
            else:
                # Handle missing month values safely
                # Fill with the mean price if something is missing
                fixed = list(monthly_prices)
                while len(fixed) < 10:
                    fixed.append(np.mean(fixed))
                vectors[(city, cat, year)] = np.array(fixed)

# Convert vectors into a DataFrame for export
rows = []
for key, values in vectors.items():
    city, cat, year = key
    row = {"City": city, "Category": cat, "Year": year}
    for i, month in enumerate(month_order):
        row[month] = values[i]
    rows.append(row)

vector_df = pd.DataFrame(rows)
vector_df.to_excel("CPI_Vectors.xlsx", index=False)

print("STEP 2 COMPLETED — CPI_Vectors.xlsx generated!")
