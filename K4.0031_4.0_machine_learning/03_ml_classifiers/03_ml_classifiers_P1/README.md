# Partial Exam 1 — Data Preprocessing Pipeline

## Overview

This project loads a real estate dataset, cleans and transforms it, applies feature scaling, and saves the processed data — all as preparation for machine learning modeling. The goal is not just to make the data look clean, but to make it **ready for algorithms** that are sensitive to scale and missing values.

---

## File Structure

```
03_ml_classifiers_P1/
├── partialExam1.py     # Main script
├── data.csv            # Raw input data
└── clean_data.csv      # Output: cleaned and scaled data
```

---

## Part 1 — Data Import and Cleaning

### What the code does
Loads the raw dataset, detects missing values, fills them with the column median, and removes duplicate rows.

### Why
Missing values break most ML algorithms. We use the **median** (not the mean) because it is more robust to outliers — a single extreme price won't distort it. Duplicates are removed to prevent the model from learning the same example twice.

### Code
```python
data = pd.read_csv(os.path.join(script_folder, "data.csv"))
df = pd.DataFrame(data)

df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].median())
df = df.drop_duplicates()
```

### Output
```
Part 1 — Missing values per column:
house_id    0
area        0
bedrooms    1
price       0

Part 1 — Data after cleaning:
   house_id  area  bedrooms   price
0         1  1000       2.0  300000
...
9        10  1400       3.0  420000
```

---

## Part 2 — Data Analysis and Transformation

### What the code does
Calculates the average price, identifies the most expensive property, adds a `price_per_sqft` column, and flags properties above average price with a binary `high_price` column.

### Why
These transformations extract useful signals from raw numbers. `price_per_sqft` normalizes price by size — a fairer comparison between properties. `high_price` converts a continuous value into a binary label, which is useful for classification tasks.

### Code
```python
average_price = np.mean(df["price"])

max_index = df["price"].idxmax()

df["price_per_sqft"] = (df["price"] / df["area"]).round(2)

df["high_price"] = np.where(df["price"] > average_price, 1, 0)
```

### Output
```
Part 2 — Average property price: €466,000
Part 2 — Most expensive house ID: 9
Part 2 — Most expensive house price: €620,000
```

---

## Part 3 — Standardization and Scaling

### What the code does
Applies Z-Score standardization to `area` and `price_per_sqft`, and Min-Max scaling to `bedrooms`.

### Why
ML algorithms that use distance or gradient descent (e.g. KNN, SVM, ADALINE) are sensitive to feature scale. A house with 3 bedrooms and an area of 2000 sqft would have the algorithm dominated by the area value — simply because it is a larger number. Scaling puts all features on a level playing field.

**Z-Score formula:**
```
z = (value - mean) / standard_deviation
```
Centers values around 0 with a standard deviation of 1.

**Min-Max formula:**
```
scaled = (value - min) / (max - min)
```
Squeezes values into the range [0, 1].

### Code
```python
# Z-Score standardization
df["area"] = (df["area"] - np.mean(df["area"])) / np.std(df["area"])
df["price_per_sqft"] = (df["price_per_sqft"] - np.mean(df["price_per_sqft"])) / np.std(df["price_per_sqft"])

# Min-Max scaling
bedrooms_min = np.min(df["bedrooms"])
bedrooms_max = np.max(df["bedrooms"])
df["bedrooms"] = (df["bedrooms"] - bedrooms_min) / (bedrooms_max - bedrooms_min)
```

### Output
```
Part 3 — Data after standardization and scaling:
   house_id      area  bedrooms   price  price_per_sqft  high_price
0         1 -1.527525       0.0  300000        0.393970           0
...
9        10 -0.436436       0.5  420000        0.393970           0
```

---

## Part 4 — Summary and Output

### What the code does
Prints a human-readable summary of the processed dataset and saves it to `clean_data.csv`.

### Why
Saving the cleaned data means the preprocessing step only needs to run once — future scripts can load `clean_data.csv` directly and start modeling immediately.

### Code
```python
print(f"  Total properties:         {len(df)}")
print(f"  Average price:            €{average_price:,.0f}")
print(f"  Most expensive property:  €{df['price'].max():,.0f}")
print(f"  Cheapest property:        €{df['price'].min():,.0f}")
print(f"  High price properties:    {df['high_price'].sum()} out of {len(df)}")

df.to_csv(os.path.join(script_folder, "clean_data.csv"), index=False)
```

### Output
```
Part 4 — Data Summary:
  Total properties:         10
  Average price:            €466,000
  Most expensive property:  €620,000
  Cheapest property:        €300,000
  High price properties:    5 out of 10
  Bedrooms range:           0.0 to 1.0 (scaled)
  Area range:               -1.53 to 1.47 (standardized)

Clean data saved to clean_data.csv ✓
```

---

## Dependencies

```
numpy
pandas
```