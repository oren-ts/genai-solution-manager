# 4.Ü.01 — Data Cleansing: Replacing Missing Values with the Median

**Course:** velpTEC K4.0031 — Machine Learning  
**Topic:** Data Preprocessing — Handling Missing Values  
**Script:** `DataCleansing.py`

---

## Table of Contents

1. [Why Data Cleansing Matters](#1-why-data-cleansing-matters)
2. [What Are Missing Values?](#2-what-are-missing-values)
3. [Strategies for Handling Missing Values](#3-strategies-for-handling-missing-values)
4. [The Median — Theory and Math](#4-the-median--theory-and-math)
5. [Implementation Walkthrough](#5-implementation-walkthrough)
6. [Full Script](#6-full-script)
7. [Expected Output](#7-expected-output)
8. [Key Pandas Methods Used](#8-key-pandas-methods-used)
9. [Common Pitfalls](#9-common-pitfalls)

---

## 1. Why Data Cleansing Matters

Real-world datasets are rarely clean. Sensors fail, users skip form fields, data pipelines drop rows — the result is a dataset full of gaps. Most machine learning algorithms cannot handle missing values at all. Feeding a model a `NaN` typically causes a crash or produces silent, incorrect results.

Data cleansing is therefore one of the first and most important steps in any ML pipeline:

```
Raw Data → Clean Data → Feature Engineering → Model Training → Evaluation
    ↑
  We are here
```

The goal is to produce a complete, consistent dataset that a model can actually learn from — without distorting the underlying distribution of the data.

---

## 2. What Are Missing Values?

In Python and pandas, missing values are represented as `NaN` — **Not a Number**. This is a special floating-point value defined by the IEEE 754 standard. It propagates through arithmetic: any operation involving `NaN` returns `NaN`.

```python
import numpy as np

x = np.nan
print(x + 5)     # nan
print(x > 3)     # False
print(x == x)    # False  ← NaN is not equal to itself!
print(np.isnan(x))  # True  ← correct way to check
```

In a pandas DataFrame, `NaN` appears wherever data is absent:

```
     A     B   C
0  1.0   5.0  10
1  2.0   NaN  20   ← B is missing here
2  NaN   NaN  30   ← A and B are both missing here
3  4.0   8.0  40
4  5.0  10.0  50
```

---

## 3. Strategies for Handling Missing Values

There are several standard approaches, each with trade-offs:

| Strategy | Description | When to use |
|---|---|---|
| **Drop rows** | Remove any row containing a `NaN` | When missing data is rare and rows are plentiful |
| **Drop columns** | Remove columns with too many `NaN`s | When a feature is mostly missing |
| **Fill with mean** | Replace `NaN` with the column average | Normally distributed data, no outliers |
| **Fill with median** | Replace `NaN` with the column middle value | Skewed data or data with outliers |
| **Fill with mode** | Replace `NaN` with the most common value | Categorical data |
| **Forward/backward fill** | Carry the previous/next value forward | Time series data |
| **Model-based imputation** | Predict the missing value using other features | High-stakes datasets requiring precision |

### Why the Median is Often Preferred Over the Mean

The **mean** is sensitive to outliers. If column B contains `[5, NaN, NaN, 8, 1000]`, the mean is distorted by the outlier `1000`, giving `337.67` — which is not representative of the typical value.

The **median** is robust: it always gives the middle value of the sorted data, ignoring extremes.

$$\text{mean}([5, 8, 1000]) = \frac{5 + 8 + 1000}{3} = 337.67$$

$$\text{median}([5, 8, 1000]) = 8$$

In this exercise we use the **median** strategy.

---

## 4. The Median — Theory and Math

The median is the value that sits in the **middle** of a sorted dataset. It divides the data into two equal halves.

### Formula

Given a sorted dataset of $n$ values $x_1 \leq x_2 \leq \dots \leq x_n$:

$$
\text{median} =
\begin{cases}
x_{\frac{n+1}{2}} & \text{if } n \text{ is odd} \\[6pt]
\dfrac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2} & \text{if } n \text{ is even}
\end{cases}
$$

### Worked Example — Column A

Column A has values: `[1, 2, NaN, 4, 5]`

Available (non-NaN) values: `[1, 2, 4, 5]` → $n = 4$ (even)

$$\text{median} = \frac{x_2 + x_3}{2} = \frac{2 + 4}{2} = 3.0$$

The `NaN` in row 2 is replaced with **3.0**.

### Worked Example — Column B

Column B has values: `[5, NaN, NaN, 8, 10]`

Available values: `[5, 8, 10]` → $n = 3$ (odd)

$$\text{median} = x_{\frac{3+1}{2}} = x_2 = 8.0$$

Both `NaN`s in rows 1 and 2 are replaced with **8.0**.

### Column C

Column C has no missing values — it is left untouched.

---

## 5. Implementation Walkthrough

### Step 1 — Create the Example DataFrame

```python
import pandas as pd
import numpy as np

# Example DataFrame with intentional missing values
data = {
    "A": [1, 2, np.nan, 4, 5],
    "B": [5, np.nan, np.nan, 8, 10],
    "C": [10, 20, 30, 40, 50],
}
house_data = pd.DataFrame(data)
```

`np.nan` is used to explicitly insert missing values. Pandas stores these as `float64` — which is why column A shows `1.0`, `2.0` etc. rather than integers.

---

### Step 2 — Identify Columns with Missing Values

```python
columns_with_missing_values = cleaned_df.columns[cleaned_df.isnull().any()].tolist()
```

This line chains three operations:

**`cleaned_df.isnull()`** — returns a boolean DataFrame, `True` wherever a value is missing:

```
       A      B      C
0  False  False  False
1  False   True  False
2   True   True  False
3  False  False  False
4  False  False  False
```

**`.any()`** — collapses each column to a single `True`/`False`: "does this column contain *any* `True`?"

```
A     True
B     True
C    False
dtype: bool
```

**`cleaned_df.columns[...]`** — uses the boolean mask to filter to only the column names that are `True`:

```
Index(['A', 'B'], dtype='object')
```

**`.tolist()`** — converts to a plain Python list: `['A', 'B']`

---

### Step 3 — Loop and Fill

```python
for column_name in columns_with_missing_values:
    column_median = cleaned_df[column_name].median()
    cleaned_df[column_name] = cleaned_df[column_name].fillna(column_median)
```

For each column that has missing values:

1. **`.median()`** — calculates the median, automatically ignoring `NaN` values
2. **`.fillna(column_median)`** — returns a new Series with every `NaN` replaced by `column_median`
3. **`cleaned_df[column_name] = ...`** — assigns the result back, updating the DataFrame

> ⚠️ **Important:** We use explicit reassignment (`df[col] = df[col].fillna(...)`) rather than `fillna(inplace=True)`. In modern pandas (2.x), `inplace=True` on a column slice does not reliably modify the original DataFrame. Explicit reassignment is the safe, recommended pattern.

---

### Step 4 — Working on a Copy

```python
cleaned_df = input_df.copy()
```

This creates a full independent copy of the input DataFrame. Without `.copy()`, `cleaned_df` would be a **view** of the original — modifying it would also modify `house_data` outside the function. This is called a **side effect**, and it can cause hard-to-find bugs.

With `.copy()`, the original data is preserved and the function is **pure** — its only effect is the value it returns.

---

## 6. Full Script

```python
import pandas as pd
import numpy as np

# Example DataFrame with missing values
data = {
    "A": [1, 2, np.nan, 4, 5],
    "B": [5, np.nan, np.nan, 8, 10],
    "C": [10, 20, 30, 40, 50],
}
house_data = pd.DataFrame(data)


def replace_missing_with_median(input_df):
    # Work on a copy so we don't modify the original DataFrame
    cleaned_df = input_df.copy()

    # Get a list of column names that contain at least one missing value
    columns_with_missing_values = cleaned_df.columns[cleaned_df.isnull().any()].tolist()

    # Fill missing values column by column using each column's median
    for column_name in columns_with_missing_values:
        column_median = cleaned_df[column_name].median()
        cleaned_df[column_name] = cleaned_df[column_name].fillna(column_median)

    return cleaned_df


# Apply the function and print the result
cleaned_house_data = replace_missing_with_median(house_data)
print(cleaned_house_data)
```

---

## 7. Expected Output

```
     A     B   C
0  1.0   5.0  10
1  2.0   8.0  20
2  3.0   8.0  30
3  4.0   8.0  40
4  5.0  10.0  50
```

- Row 2, Column A: `NaN` → `3.0` (median of `[1, 2, 4, 5]`)
- Rows 1 & 2, Column B: `NaN` → `8.0` (median of `[5, 8, 10]`)
- Column C: unchanged (no missing values)

---

## 8. Key Pandas Methods Used

| Method | Purpose |
|---|---|
| `pd.DataFrame(data)` | Creates a DataFrame from a dictionary |
| `df.isnull()` | Returns a boolean DataFrame — `True` where values are `NaN` |
| `.any()` | Returns `True` for each column that contains at least one `True` |
| `df.columns[mask]` | Filters column names using a boolean mask |
| `.tolist()` | Converts a pandas Index to a plain Python list |
| `df[col].median()` | Calculates the median of a column, ignoring `NaN` |
| `df[col].fillna(value)` | Returns a new Series with `NaN` replaced by `value` |
| `df.copy()` | Creates a full independent copy of the DataFrame |

---

## 9. Common Pitfalls

### Pitfall 1 — Using `inplace=True` in modern pandas

```python
# ❌ Unreliable in pandas 2.x
df[column_name].fillna(median, inplace=True)

# ✅ Always use explicit reassignment
df[column_name] = df[column_name].fillna(median)
```

### Pitfall 2 — Forgetting `.copy()`

```python
# ❌ This modifies the original DataFrame as a side effect
def replace_missing_with_median(input_df):
    input_df["A"] = input_df["A"].fillna(3.0)  # Modifies house_data too!
    return input_df

# ✅ Always copy first
def replace_missing_with_median(input_df):
    cleaned_df = input_df.copy()  # Safe — original is untouched
    ...
```

### Pitfall 3 — Fitting on the full dataset before splitting

In a real ML pipeline, you must calculate the median **only on training data**, then apply it to test data. Calculating the median on the full dataset (including test rows) introduces **data leakage** — the model indirectly "sees" test data during preprocessing.

```python
# ❌ Data leakage — median computed on full dataset
median = full_dataset["A"].median()

# ✅ Correct — median computed only on training split
median = X_train["A"].median()
X_train["A"] = X_train["A"].fillna(median)
X_test["A"] = X_test["A"].fillna(median)  # Apply same median to test set
```

---

*Document prepared as part of velpTEC K4.0031 — Machine Learning course.*