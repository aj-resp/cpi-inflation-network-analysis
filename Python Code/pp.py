import pandas as pd

# Load data
df = pd.read_excel("Data Combined.xlsx")

# -------- CATEGORY MAPPING -------- #

category_map = {
    "Food_Staples_Grains": [
        "Wheat Flour Bag - 20kg", "Rice Basmati Broken (Average Quality)", "Rice IRRI-6/9 (Sindh/Punjab)",
        "Bread plain (Small Size)", "Pulse Moong (Washed)", "Pulse Mash (Washed)",
        "Pulse Masoor (Washed)", "Cooked Daal at Average Hotel (per plate)", "Sugar Refined",
        "Tea Prepared Ordinary (per cup)", "Tea Lipton Yellow Label 190 gm Pack", "Milk Fresh",
        "Milk (Packed)", "Vegetable Ghee DALDA/HABIB or Oth", "Vegetable Ghee DALDA/HABIB 2.5 kg",
        "Cooking Oil DALDA or Other Similar B", "Salt Powdered (NATIONAL/SHAN) 80",
        "Cooked Beef at Average Hotel (per plate)", "Curd (Dahi) Loose"
    ],

    "Meat_Poultry_Dairy": [
        "Beef with Bone (Average Quality)", "Mutton (Average Quality)",
        "Chicken Farm Broiler (Live)", "Chicken Broiler Dressed (Average Qualit)",
        "Eggs Hen (Farm) - 1 Dozen"
    ],

    "Oils_Sweeteners_Condiments": [
        "Cooking Oil DALDA or Other Similar B", "Vegetable Ghee DALDA/HABIB 2.5 kg",
        "Vegetable Ghee DALDA/HABIB or Oth", "Chilies Powder NATIONAL 200 gm Pa",
        "Salt Powdered (NATIONAL/SHAN) 80", "Tea Lipton Yellow Label 190 gm Pack"
    ],

    "Fruits_Vegetables": [
        "Potatoes", "Tomatoes", "Onions", "Bananas (Kela) Local - 1 Dozen",
        "Garlic (Lehsun)", "Ginger (Adrak)"
    ],

    "Non_Food_Essentials": [
        "Toilet Soap LIFEBUOY 115 gm", "Sufi Washing Soap 250 gm Cake",
        "Washing Powder", "Shaving Blade", "Cigarettes Capstan 20'S Packet",
        "Match Box", "Energy Saver Philips 14 Watt", "Shoes Gents", "Shoes Ladies",
        "Shirting (Average Quality)", "Tailoring Charges"
    ],

    "Utilities_Transport": [
        "Petrol Super", "Electricity Charges upto 50 Units (per unit)",
        "Telephone Call Charges (per mins)", "Firewood Whole (40kg)"
    ],

    "Clothing_Misc": [
        "Shirting (Average Quality)", "Shoes Gents", "Shoes Ladies",
        "Energy Saver Philips 14 Watt", "Tailoring Charges"
    ]
}

# Reverse mapping: product → category
reverse_map = {}
for cat, items in category_map.items():
    for item in items:
        reverse_map[item] = cat

# Assign category to each product
df["Category"] = df["Product"].map(reverse_map)

# -------- FILTER YEARS -------- #
df = df[df["Year"].isin([2023, 2024])]

# -------- KEEP ONLY MARCH–DECEMBER -------- #
valid_months = ["March", "April", "May", "June", "July", "August",
                "September", "October", "November", "December"]

df = df[df["Month"].isin(valid_months)]

# -------- SORT DATA -------- #
df = df.sort_values(["City", "Category", "Product", "Year", "Month"])

# -------- FORWARD FILL -------- #
df["Price"] = df.groupby(["City", "Product", "Year"])["Price"].fillna(method="ffill")

# -------- SAVE CLEANED DATA -------- #
df.to_excel("Cleaned_CPI_Data.xlsx", index=False)

print("STEP 1 COMPLETED — Cleaned_CPI_Data.xlsx generated successfully!")
