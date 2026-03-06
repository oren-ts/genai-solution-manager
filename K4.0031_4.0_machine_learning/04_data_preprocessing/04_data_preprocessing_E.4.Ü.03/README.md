# 4.Ü.03 — Column Transformer

**Course:** velpTEC K4.0031 — Machine Learning
**Topic:** Data Preprocessing — Handling Categorical Data with `ColumnTransformer`
**Script:** `4_Ü_03_ColumnTransformer.py`

---

## Table of Contents

1. [Overview](#overview)
2. [Theory: Why Can't ML Models Read Text?](#theory-why-cant-ml-models-read-text)
3. [Theory: One-Hot Encoding](#theory-one-hot-encoding)
4. [Theory: The Dummy Variable Trap & Collinearity](#theory-the-dummy-variable-trap--collinearity)
5. [Theory: The ColumnTransformer](#theory-the-columntransformer)
6. [Theory: sklearn's Estimator API — fit vs transform](#theory-sklearns-estimator-api--fit-vs-transform)
7. [Implementation — Step by Step](#implementation--step-by-step)
8. [Full Script](#full-script)
9. [Output Walkthrough](#output-walkthrough)
10. [Comparison: ColumnTransformer vs pd.get_dummies](#comparison-columntransformer-vs-pdget_dummies)
11. [Key Takeaways](#key-takeaways)

---

## Overview

This exercise builds a preprocessing pipeline using sklearn's `ColumnTransformer`.
The goal is to convert a **categorical column** (`color`) into numeric binary columns
using `OneHotEncoder`, while leaving the **numeric columns** (`size`, `price`) untouched.

This is a core real-world task: most datasets contain a mix of categorical and numeric
features, and ML models require all input to be numeric.

---

## Theory: Why Can't ML Models Read Text?

Machine learning algorithms are built on linear algebra — they perform operations like
matrix multiplication, distance calculations, and gradient descent. All of these require
**numbers**, not strings.

Given a column like this:

| color |
|-------|
| Red   |
| Green |
| Blue  |
| Red   |

A naive approach would be to assign integers:

$$\text{Blue} = 0, \quad \text{Green} = 1, \quad \text{Red} = 2$$

But this introduces a false **ordering assumption**. The model would interpret:

$$\text{Red} > \text{Green} > \text{Blue}$$

...which is meaningless for colors. This is the fundamental problem that **one-hot encoding** solves.

---

## Theory: One-Hot Encoding

One-hot encoding creates a **new binary column for each unique category**.
Each row gets a `1` in exactly one of those columns, and `0` everywhere else.

For the `color` column with values `{Blue, Green, Red}`, one-hot encoding produces:

| color | color_Blue | color_Green | color_Red |
|-------|-----------|------------|----------|
| Red   | 0         | 0          | 1        |
| Green | 0         | 1          | 0        |
| Blue  | 1         | 0          | 0        |
| Red   | 0         | 0          | 1        |

### Mathematical representation

For a categorical feature $x$ with $k$ unique categories $\{c_1, c_2, \ldots, c_k\}$,
one-hot encoding maps each value to a binary vector of length $k$:

$$x = c_j \quad \Rightarrow \quad \mathbf{v} = [0, \ldots, 0, \underbrace{1}_{j\text{-th position}}, 0, \ldots, 0]$$

The key property: each encoded vector satisfies:

$$\sum_{i=1}^{k} v_i = 1 \qquad \text{(exactly one position is active)}$$

No ordering is implied. The model treats each color as an independent, unrelated feature.

---

## Theory: The Dummy Variable Trap & Collinearity

### What is collinearity?

**Collinearity** means that one feature can be perfectly predicted from the others.
After full one-hot encoding of 3 colors, the three columns are **not independent**:

$$\text{color\_Blue} = 1 - \text{color\_Green} - \text{color\_Red}$$

Knowing any two columns, you can always calculate the third. This creates a
**redundant feature** that causes problems for models that invert matrices
(e.g. linear regression, logistic regression), leading to **numerically unstable estimates**.

### The fix: drop one column

By dropping one dummy column (the **reference category**), we preserve all the
information while eliminating the redundancy.

With `drop='first'` (drops `color_Blue` — alphabetically first):

| color | color_Green | color_Red | implied         |
|-------|------------|----------|-----------------|
| Red   | 0          | 1        | not Blue ✓      |
| Green | 1          | 0        | not Blue ✓      |
| Blue  | 0          | 0        | must be Blue ✓  |
| Red   | 0          | 1        | not Blue ✓      |

**Mathematically**, if we have $k$ categories, we need only $k - 1$ dummy columns
to represent all information:

$$k \text{ categories} \quad \Rightarrow \quad k - 1 \text{ binary columns}$$

The dropped category is **implicitly encoded** by all remaining columns being `0`.

> **Rule of thumb:** Always use `drop='first'` (or `drop_first=True`) when your
> model is sensitive to collinearity (linear models, logistic regression, neural networks).
> Tree-based models (Decision Trees, Random Forests) are generally unaffected.

---

## Theory: The ColumnTransformer

### The problem it solves

Real datasets have mixed column types. You might want to:
- One-hot encode `color`
- Standardize `price`
- Leave `size` unchanged

Applying these transformations manually — column by column — is tedious and error-prone.
`ColumnTransformer` lets you declare all transformations in one place and applies them
in a single call.

### Structure

```python
ColumnTransformer([
    (name, transformer, columns),
    (name, transformer, columns),
    ...
])
```

Each **tuple** has exactly three elements:

| Position | Type | Description |
|----------|------|-------------|
| `name` | `str` | A label you choose — used for debugging and pipeline inspection |
| `transformer` | sklearn transformer or `'passthrough'` | What transformation to apply |
| `columns` | list of column names or indices | Which columns to apply it to |

The special string `'passthrough'` means: *do nothing, let these columns through unchanged*.

### How it processes columns

```
Input DataFrame:
┌───────┬──────┬───────┐
│ color │ size │ price │
├───────┼──────┼───────┤
│  Red  │  1   │ 10.2  │
│ Green │  2   │  9.6  │
│ Blue  │  3   │ 12.5  │
│  Red  │  2   │ 11.1  │
└───────┴──────┴───────┘
         │               │
         ▼               ▼
  OneHotEncoder      passthrough
  (drop='first')
  ┌─────┬─────┐     ┌──────┬───────┐
  │G    │R    │     │ size │ price │
  ├─────┼─────┤     ├──────┼───────┤
  │ 0   │ 1   │     │  1   │ 10.2  │
  │ 1   │ 0   │     │  2   │  9.6  │
  │ 0   │ 0   │     │  3   │ 12.5  │
  │ 0   │ 1   │     │  2   │ 11.1  │
  └─────┴─────┘     └──────┴───────┘
         │               │
         └───────┬───────┘
                 ▼
  Output NumPy array (columns concatenated):
  [color_Green, color_Red, size, price]
```

> **Important:** The encoded columns always come **first** in the output,
> regardless of the original column order. `passthrough` columns follow after.

---

## Theory: sklearn's Estimator API — fit vs transform

`ColumnTransformer` follows sklearn's standard **Estimator API**:

| Method | What it does |
|--------|-------------|
| `.fit(X)` | Learns parameters from the data (e.g. which categories exist) |
| `.transform(X)` | Applies the learned transformation to data |
| `.fit_transform(X)` | Does both in one step — equivalent to `.fit(X).transform(X)` |

### Why does fit exist?

When working with train/test splits, you must **fit only on training data**,
then **transform both** training and test data using the same fitted parameters.
This prevents **data leakage** — the model should never learn anything from test data.

```python
# Correct workflow with train/test split:
column_transformer.fit(X_train)           # learn categories from training data only
X_train_transformed = column_transformer.transform(X_train)
X_test_transformed  = column_transformer.transform(X_test)   # apply same encoding

# In this exercise we use fit_transform() because there is no split:
transformed_data = column_transformer.fit_transform(clothing_df)
```

---

## Implementation — Step by Step

### a) Imports

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder   # converts categories → binary columns
from sklearn.compose import ColumnTransformer     # applies different transforms per column
```

- `OneHotEncoder` lives in `sklearn.preprocessing` — the module for data transformation utilities
- `ColumnTransformer` lives in `sklearn.compose` — the module for combining transformers

---

### b) Define the DataFrame

```python
sample_data = {
    "color": ["Red", "Green", "Blue", "Red"],
    "size":  [1,     2,       3,      2    ],
    "price": [10.2,  9.6,     12.5,   11.1 ],
}

clothing_df = pd.DataFrame(sample_data)
```

**Output:**

```
   color  size  price
0    Red     1   10.2
1  Green     2    9.6
2   Blue     3   12.5
3    Red     2   11.1
```

The DataFrame has three columns:
- `color` — **nominal categorical** (no natural order, must be encoded)
- `size` — **numeric** (passed through unchanged)
- `price` — **numeric** (passed through unchanged)

---

### c) Create the ColumnTransformer

```python
column_transformer = ColumnTransformer([
    ("encode_color", OneHotEncoder(drop="first"), ["color"]),
    ("passthrough",  "passthrough",               ["size", "price"]),
])
```

**Breaking down each tuple:**

**Tuple 1** — `("encode_color", OneHotEncoder(drop="first"), ["color"])`

| Part | Value | Meaning |
|------|-------|---------|
| name | `"encode_color"` | Label for this transformation step |
| transformer | `OneHotEncoder(drop="first")` | Apply one-hot encoding, drop first category |
| columns | `["color"]` | Apply only to the `color` column |

`drop="first"` drops the alphabetically first category. For `{Blue, Green, Red}`, that is **Blue**.

**Tuple 2** — `("passthrough", "passthrough", ["size", "price"])`

| Part | Value | Meaning |
|------|-------|---------|
| name | `"passthrough"` | Label for this step |
| transformer | `"passthrough"` | Special keyword: do nothing, pass columns through unchanged |
| columns | `["size", "price"]` | Apply to both numeric columns |

> **Why use column names instead of index numbers?**
> `["color"]` is safer than `[0]`. If the DataFrame's column order ever changes,
> index-based references silently break. Name-based references always target the right column.

---

### d) Apply the Transformer

```python
transformed_data = column_transformer.fit_transform(clothing_df)
print(transformed_data)
```

`fit_transform()` does two things in one call:
1. **Fit:** scans `clothing_df`, discovers the unique categories in `color` → `{Blue, Green, Red}`
2. **Transform:** encodes `color` into 2 binary columns and concatenates with `size` and `price`

---

## Full Script

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4.Ü.03 - Column Transformer
============================
Use sklearn's ColumnTransformer to apply OneHotEncoding to a categorical
column while leaving numeric columns unchanged.
"""

# ── a) Import required modules ────────────────────────────────────────────────

import pandas as pd
from sklearn.preprocessing import OneHotEncoder   # converts categories → binary columns
from sklearn.compose import ColumnTransformer     # applies different transforms per column


# ── b) Define the DataFrame ───────────────────────────────────────────────────

sample_data = {
    "color": ["Red", "Green", "Blue", "Red"],
    "size":  [1,     2,       3,      2    ],
    "price": [10.2,  9.6,     12.5,   11.1 ],
}

clothing_df = pd.DataFrame(sample_data)

print("Original DataFrame:")
print(clothing_df)
print()


# ── c) Create the ColumnTransformer ──────────────────────────────────────────

column_transformer = ColumnTransformer([
    ("encode_color", OneHotEncoder(drop="first"), ["color"]),
    ("passthrough",  "passthrough",               ["size", "price"]),
])


# ── d) Apply the Transformer and print the result ─────────────────────────────

transformed_data = column_transformer.fit_transform(clothing_df)

print("Transformed array (color encoded, size & price unchanged):")
print(transformed_data)
print()

# Column layout of the output:
#   Col 0 → color_Green  (1 = Green, 0 = not Green)
#   Col 1 → color_Red    (1 = Red,   0 = not Red)
#   Col 2 → size         (passed through as-is)
#   Col 3 → price        (passed through as-is)
print("Output column order: [color_Green, color_Red, size, price]")
```

---

## Output Walkthrough

```
Transformed array (color encoded, size & price unchanged):
[[0.0  1.0  1.0  10.2]
 [1.0  0.0  2.0   9.6]
 [0.0  0.0  3.0  12.5]
 [0.0  1.0  2.0  11.1]]
```

Reading each row against the original data:

| Row | Original color | color_Green | color_Red | size | price | Explanation |
|-----|---------------|------------|----------|------|-------|-------------|
| 0 | Red   | 0 | 1 | 1 | 10.2 | Red → color_Red = 1 |
| 1 | Green | 1 | 0 | 2 |  9.6 | Green → color_Green = 1 |
| 2 | Blue  | 0 | 0 | 3 | 12.5 | Blue → both 0 (dropped reference category) |
| 3 | Red   | 0 | 1 | 2 | 11.1 | Red → color_Red = 1 |

**Row 2 (Blue)** is the key insight: both dummy columns are `0`, which **unambiguously implies Blue**.
No information is lost by dropping the Blue column.

### Why is the output a NumPy array, not a DataFrame?

`ColumnTransformer.fit_transform()` always returns a NumPy array. Column names are not preserved.
To convert back to a named DataFrame you would need to reconstruct the column names manually:

```python
import numpy as np

output_columns = (
    column_transformer
    .named_transformers_["encode_color"]
    .get_feature_names_out(["color"])
    .tolist()
    + ["size", "price"]
)

result_df = pd.DataFrame(transformed_data, columns=output_columns)
print(result_df)
```

---

## Comparison: ColumnTransformer vs pd.get_dummies

| Feature | `pd.get_dummies()` | `ColumnTransformer` |
|---------|-------------------|---------------------|
| Origin | pandas | sklearn |
| Output type | DataFrame (keeps column names) | NumPy array |
| Drop first column | `drop_first=True` | `drop='first'` |
| Works in sklearn Pipelines | ✗ No | ✓ Yes |
| Handles multiple transformations | ✗ No | ✓ Yes |
| Handles unseen categories (test data) | ✗ No | ✓ Yes (with `handle_unknown`) |
| Best for | Quick exploration | Production preprocessing pipelines |

> **Rule of thumb:** Use `pd.get_dummies()` for quick exploration and single scripts.
> Use `ColumnTransformer` when building reusable preprocessing pipelines with sklearn.

---

## Key Takeaways

| Concept | Summary |
|---------|---------|
| **One-hot encoding** | Converts $k$ categories into $k$ binary columns — no false ordering |
| **Dummy variable trap** | Full one-hot encoding creates collinearity: one column is always predictable from the others |
| **drop='first'** | Removes the reference category → reduces $k$ columns to $k-1$, eliminates redundancy |
| **ColumnTransformer** | Applies different sklearn transformations to different columns in one step |
| **passthrough** | Special keyword that leaves selected columns completely unchanged |
| **fit_transform()** | Learns from data (`fit`) then applies the transformation (`transform`) in one call |
| **Data leakage rule** | In train/test scenarios: always `fit` on training data only, then `transform` both sets |