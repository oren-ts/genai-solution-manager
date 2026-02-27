import numpy as np
import pandas as pd
import os

# ── Part 1: Data Import and Cleaning ──────────────────────────────────────────

# Build the path to data.csv relative to where this script lives
script_folder = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(os.path.join(script_folder, "data.csv"))
df = pd.DataFrame(data)

# Check for missing values per column
print("Part 1 — Missing values per column:")
print(df.isnull().sum())

# Fill missing bedroom values with the column median
df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].median())

# Remove duplicate rows
df = df.drop_duplicates()

print("\nPart 1 — Data after cleaning:")
print(df)

# ── Part 2: Data Analysis and Transformation ──────────────────────────────────

# Calculate the average price of all properties
average_price = np.mean(df["price"])
print(f"\nPart 2 — Average property price: €{average_price:,.0f}")

# Find the most expensive house
max_index = df["price"].idxmax()
print(f"Part 2 — Most expensive house ID: {df.loc[max_index, 'house_id']}")
print(f"Part 2 — Most expensive house price: €{df.loc[max_index, 'price']:,.0f}")

# Calculate price per square foot for each property
df["price_per_sqft"] = (df["price"] / df["area"]).round(2)

# Flag properties above average price as 1, below as 0
df["high_price"] = np.where(df["price"] > average_price, 1, 0)

print("\nPart 2 — Data after transformation:")
print(df)

# ── Part 3: Data Standardization and Normalization ────────────────────────────

# Z-Score standardization for area
area_mean = np.mean(df["area"])
area_std = np.std(df["area"])
df["area"] = (df["area"] - area_mean) / area_std

# Z-Score standardization for price_per_sqft
price_per_sqft_mean = np.mean(df["price_per_sqft"])
price_per_sqft_std = np.std(df["price_per_sqft"])
df["price_per_sqft"] = (df["price_per_sqft"] - price_per_sqft_mean) / price_per_sqft_std

# Min-Max scaling for bedrooms (scaled to range 0-1)
bedrooms_min = np.min(df["bedrooms"])
bedrooms_max = np.max(df["bedrooms"])
df["bedrooms"] = (df["bedrooms"] - bedrooms_min) / (bedrooms_max - bedrooms_min)

print("\nPart 3 — Data after standardization and scaling:")
print(df)

# ── Part 4: Summary and Output ────────────────────────────────────────────────

# Print a human-readable summary of the cleaned and transformed data
print("\nPart 4 — Data Summary:")
print(f"  Total properties:         {len(df)}")
print(f"  Average price:            €{average_price:,.0f}")
print(f"  Most expensive property:  €{df['price'].max():,.0f}")
print(f"  Cheapest property:        €{df['price'].min():,.0f}")
print(f"  High price properties:    {df['high_price'].sum()} out of {len(df)}")
print(
    f"  Bedrooms range:           {df['bedrooms'].min()} to {df['bedrooms'].max()} (scaled)"
)
print(
    f"  Area range:               {df['area'].min():.2f} to {df['area'].max():.2f} (standardized)"
)

# Save the cleaned dataset to a new CSV file
df.to_csv(os.path.join(script_folder, "clean_data.csv"), index=False)
print("\nClean data saved to clean_data.csv")
