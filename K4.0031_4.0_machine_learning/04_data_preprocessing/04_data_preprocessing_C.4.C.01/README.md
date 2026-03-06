# Exercise 4.C.01 — Data Cleansing
**Course:** K4.0031 Machine Learning  
**Topic:** Data Preprocessing — Cleaning a Customer Ratings Dataset  
**Script:** `4_C_01_DataCleansing.py`

---

## Table of Contents

1. [What is Data Cleansing?](#1-what-is-data-cleansing)
2. [The Dataset](#2-the-dataset)
3. [Step (a) — Remove Rows with Missing Values](#3-step-a--remove-rows-with-missing-values)
4. [Step (b) — Replace NaN Comments](#4-step-b--replace-nan-comments)
5. [Step (c) — Replace Empty String Comments](#5-step-c--replace-empty-string-comments)
6. [Step (d) — Remove Comments with Only Special Characters](#6-step-d--remove-comments-with-only-special-characters)
7. [Step (d cont.) — Add a Label Column with pd.cut()](#7-step-d-cont--add-a-label-column-with-pdcut)
8. [Step (e) — Wrapping Everything in a Function](#8-step-e--wrapping-everything-in-a-function)
9. [Key Concepts Summary](#9-key-concepts-summary)
10. [Full Script](#10-full-script)

---

## 1. What is Data Cleansing?

Real-world datasets are almost never clean. They typically contain:

- **Missing values** — cells with no data (`NaN`, `None`, empty strings)
- **Junk entries** — values that are technically present but meaningless (e.g. `"!!!"`)
- **Inconsistent formats** — the same thing represented in different ways
- **Outliers** — values that are far outside the expected range

Before training any Machine Learning model, the data must be cleaned. A model trained on dirty data will produce unreliable predictions — this is sometimes called **"garbage in, garbage out"**.

### Why does this matter for ML?

Most ML algorithms operate on **numerical matrices**. Any `NaN` value in the input will cause the algorithm to crash or silently produce wrong results. Data cleansing ensures that:

1. Every row is complete (no missing values in key columns)
2. Every value is meaningful (no junk text)
3. The data is in the format the algorithm expects

---

## 2. The Dataset

We simulate a small customer ratings dataset with 5 rows and 4 columns:

| Customer ID | Age    | Rating | Comment           |
|-------------|--------|--------|-------------------|
| 1           | 25     | 5      | Super product!    |
| 2           | NaN    | 3      | *(empty string)*  |
| 3           | 35     | NaN    | NaN               |
| 4           | 40     | 1      | !!!               |
| 5           | NaN    | 4      | Could be better   |

This dataset contains three types of problems:
- **Missing Age** → rows 2 and 5
- **Missing Rating** → row 3
- **Junk comment** → row 4 (`"!!!"`)
- **Empty comment** → row 2 (`""`)
- **NaN comment** → row 3

### Code

```python
import numpy as np
import pandas as pd
import re

raw_data = {
    "Customer ID": [1,       2,       3,       4,    5             ],
    "Age":         [25,      np.nan,  35,      40,   np.nan        ],
    "Rating":      [5,       3,       np.nan,  1,    4             ],
    "Comment":     ["Super product!", "", np.nan, "!!!", "Could be better"],
}

customer_ratings = pd.DataFrame(raw_data)
```

> **Note:** `np.nan` is NumPy's representation of a missing value. pandas recognises it as `NaN` (Not a Number) and treats it as "no data present".

---

## 3. Step (a) — Remove Rows with Missing Values

### Theory

A **missing value** (also called `NaN` — Not a Number) is a placeholder for absent data. In pandas, missing values appear as `NaN` in the DataFrame.

Rows with missing `Age` or `Rating` cannot be used for analysis or model training, because:
- We cannot compute statistics (mean, median) on missing values without making assumptions
- ML models require complete input vectors — a row with `NaN` is an incomplete data point

The formal rule:

$$\text{Keep row } i \iff \text{Age}_i \neq \text{NaN} \;\text{ AND }\; \text{Rating}_i \neq \text{NaN}$$

Or equivalently — **drop** row $i$ if *any* of the checked columns is `NaN`.

### pandas Tool: `dropna()`

`dropna()` removes rows containing missing values. The key parameter here is `subset`, which limits the check to specific columns.

| Parameter | Type | Description |
|-----------|------|-------------|
| `subset` | list of column names | Only check these columns for NaN |
| `inplace` | bool | If `True`, modify the DataFrame directly |

### Code

```python
# Remove any row where Age or Rating is missing
df.dropna(subset=["Age", "Rating"], inplace=True)
```

### Before vs After

| Customer ID | Age    | Rating | Comment           |
|-------------|--------|--------|-------------------|
| ~~2~~       | ~~NaN~~| ~~3~~  | ~~(empty)~~       |
| ~~3~~       | ~~35~~ | ~~NaN~~| ~~NaN~~           |
| ~~5~~       | ~~NaN~~| ~~4~~  | ~~Could be better~~|

Rows 2, 3, and 5 are removed. Only rows 1 and 4 remain.

> **pandas 2.x note:** `inplace=True` works reliably with `dropna()`. For column-level operations like `fillna()`, explicit reassignment is safer (see Step b).

---

## 4. Step (b) — Replace NaN Comments

### Theory

After step (a), row 3 (which had a `NaN` comment) has already been removed. However, in a larger dataset there could be rows where `Age` and `Rating` are present but `Comment` is `NaN`. We still want to handle those gracefully rather than dropping the whole row — we replace the missing comment with a placeholder string.

This is called **imputation** — filling in missing values with a reasonable substitute.

$$\text{Comment}_i = \begin{cases} \text{"No comment"} & \text{if Comment}_i = \text{NaN} \\ \text{Comment}_i & \text{otherwise} \end{cases}$$

### pandas Tool: `fillna()`

`fillna()` replaces `NaN` values with a specified value. It only targets actual `NaN` — it does **not** affect empty strings `""`.

### Code

```python
# Replace NaN comments with the string "No comment"
df["Comment"] = df["Comment"].fillna("No comment")
```

> **Why reassign instead of using `inplace=True`?**  
> In pandas 2.x, `fillna(inplace=True)` on a column sometimes does not modify the original DataFrame due to how pandas handles internal copy/view semantics. Explicit reassignment (`df["col"] = df["col"].fillna(...)`) is always reliable.

---

## 5. Step (c) — Replace Empty String Comments

### Theory

`fillna()` only catches `NaN`. An **empty string** `""` is a different thing — it is a valid Python string object, just one with zero characters. pandas does not treat it as missing.

We need a second pass to catch these. The check is:

$$\text{Comment}_i = \begin{cases} \text{"No comment"} & \text{if } \texttt{Comment}_i\text{.strip()} = \text{""} \\ \text{Comment}_i & \text{otherwise} \end{cases}$$

Using `.strip()` is important — it removes leading and trailing whitespace first. This means a comment like `"   "` (just spaces) is also caught.

### pandas Tool: `apply()` with a lambda

`apply()` runs a function on every element of a Series. A **lambda** is a small anonymous (nameless) function written in one line.

```
lambda x: "No comment" if x.strip() == "" else x
```

This reads as: *"For each value x: if x (with whitespace stripped) is empty, return 'No comment'. Otherwise return x unchanged."*

### Code

```python
# Replace empty string comments (and whitespace-only) with "No comment"
df["Comment"] = df["Comment"].apply(
    lambda x: "No comment" if x.strip() == "" else x
)
```

### Why two separate steps (b and c)?

| Situation | `fillna()` catches it? | `apply()` + `.strip()` catches it? |
|-----------|------------------------|-------------------------------------|
| `NaN`     | ✅ Yes                  | ❌ No (`.strip()` crashes on NaN)   |
| `""`      | ❌ No                   | ✅ Yes                               |
| `"   "`   | ❌ No                   | ✅ Yes                               |

Both steps are needed to cover all cases. Step (b) must come first, otherwise the lambda in step (c) would crash when it encounters a `NaN` (you cannot call `.strip()` on `NaN`).

---

## 6. Step (d) — Remove Comments with Only Special Characters

### Theory

Some comments contain only special characters like `"!!!"`, `"???"`, or `"###"`. These are not meaningful feedback — they should be removed entirely (not replaced, because we don't know what the customer intended).

We use **Regular Expressions (regex)** to detect these. A regex is a pattern that describes a set of strings.

### The Regex Pattern: `^[!?.#*]+$`

| Part | Meaning |
|------|---------|
| `^` | Match from the **start** of the string |
| `[!?.#*]` | Match any **single character** from this set: `!`, `?`, `.`, `#`, `*` |
| `+` | Match **one or more** of the preceding character class |
| `$` | Match to the **end** of the string |

Combined: *"The entire string, from start to end, consists of nothing but these special characters."*

Examples:
- `"!!!"` → ✅ matches → row gets **removed**
- `"Super product!"` → ❌ no match → row is **kept**
- `"No comment"` → ❌ no match → row is **kept**

### Boolean Indexing in pandas

To filter rows, we use **boolean indexing** — creating a True/False mask and using it to select rows.

```
only_special_chars = [False, True]   ← row 0 kept, row 1 removed
df = df[~only_special_chars]         ← ~ flips: keep where False
```

The `~` operator inverts the boolean — so `True` (is junk) becomes `False` (do not keep).

### Code

```python
# Build a boolean mask: True where comment is only special characters
only_special_chars = df["Comment"].apply(
    lambda x: bool(re.match(r"^[!?.#*]+$", x))
)

# Keep only rows where the mask is False (i.e. NOT only special chars)
df = df[~only_special_chars]
```

> **Why `r"..."` on the regex string?**  
> The `r` prefix makes it a **raw string** — Python will not interpret backslashes as escape sequences. This is the standard convention for regex patterns.

> **Why `bool(re.match(...))`?**  
> `re.match()` returns a Match object if it finds a match, or `None` if not. Wrapping in `bool()` converts that to `True` / `False`.

---

## 7. Step (d cont.) — Add a Label Column with `pd.cut()`

### Theory

The `Rating` column contains numeric values from 1 to 5. We want to **bin** (group) these into three categories:

$$\text{Label}_i = \begin{cases} \text{"Negative"} & \text{if } 1 \leq \text{Rating}_i \leq 2 \\ \text{"Neutral"}  & \text{if } \text{Rating}_i = 3 \\ \text{"Positive"} & \text{if } 4 \leq \text{Rating}_i \leq 5 \end{cases}$$

This process is called **discretisation** — converting a continuous numerical variable into discrete categories.

### Visualising the Bins

```
Rating scale:   0 ──── 1 ──── 2 ──── 3 ──── 4 ──── 5
                   |         |         |         |
Bins:          (0, 2]     (2, 3]     (3, 5]
Labels:        Negative   Neutral   Positive
```

The notation `(0, 2]` means: *greater than 0, up to and including 2*.  
`include_lowest=True` extends the first bin to also include `0` itself — so it becomes `[0, 2]`.

### pandas Tool: `pd.cut()`

| Parameter | Description |
|-----------|-------------|
| `x` | The Series to bin |
| `bins` | List of boundary points (fence posts) |
| `labels` | Names for each interval |
| `include_lowest` | If `True`, include the left edge of the first bin |

### Code

```python
# Add a Label column by binning the Rating into three categories
df["Label"] = pd.cut(
    df["Rating"],
    bins=[0, 2, 3, 5],
    labels=["Negative", "Neutral", "Positive"],
    include_lowest=True,
)
```

### Worked Example

| Rating | Bin applied | Label |
|--------|-------------|-------|
| 5.0    | (3, 5]      | Positive |
| 1.0    | [0, 2]      | Negative |
| 3.0    | (2, 3]      | Neutral  |
| 4.0    | (3, 5]      | Positive |

---

## 8. Step (e) — Wrapping Everything in a Function

### Theory

A **function** in Python is a reusable block of code. Wrapping the cleansing logic in a function means:

- We can call `clean_customer_data(df)` on any DataFrame with the same structure
- The steps are logically grouped and easier to test
- We avoid repeating the same code in different places (**DRY principle** — Don't Repeat Yourself)

### Function Anatomy

```python
def function_name(parameter):
    # body — the steps to execute
    return result
```

- `def` — declares a new function
- `parameter` — the input the function receives (here: a DataFrame)
- `return` — sends back the result to whoever called the function

### Code

```python
def clean_customer_data(df):
    """
    Cleans the customer ratings DataFrame.
    Returns the cleaned DataFrame.
    """
    df.dropna(subset=["Age", "Rating"], inplace=True)
    df["Comment"] = df["Comment"].fillna("No comment")
    df["Comment"] = df["Comment"].apply(
        lambda x: "No comment" if x.strip() == "" else x
    )
    only_special_chars = df["Comment"].apply(
        lambda x: bool(re.match(r"^[!?.#*]+$", x))
    )
    df = df[~only_special_chars]
    df["Label"] = pd.cut(
        df["Rating"],
        bins=[0, 2, 3, 5],
        labels=["Negative", "Neutral", "Positive"],
        include_lowest=True,
    )
    return df

# Call the function and store the result
cleaned_data = clean_customer_data(customer_ratings)
print(cleaned_data)
```

---

## 9. Key Concepts Summary

| Concept | What it means | Used in |
|---------|---------------|---------|
| `NaN` | Missing value (Not a Number) | All steps |
| `dropna()` | Remove rows with missing values | Step (a) |
| `fillna()` | Replace NaN with a value | Step (b) |
| `apply()` | Run a function on every row/column value | Steps (c), (d) |
| `lambda` | Anonymous one-line function | Steps (c), (d) |
| `.strip()` | Remove leading/trailing whitespace | Step (c) |
| `re.match()` | Check if string matches a regex pattern | Step (d) |
| `^[!?.#*]+$` | Regex: string is only special chars | Step (d) |
| `~` | Boolean NOT — flip True/False | Step (d) |
| `pd.cut()` | Bin a numeric column into categories | Step (d cont.) |
| `include_lowest` | Include left edge of first bin | Step (d cont.) |
| Data leakage | Using test data statistics during training | General preprocessing principle |

---

## 10. Full Script

```python
# =============================================================================
# Exercise 4.C.01 — Data Cleansing
# Course: K4.0031 Machine Learning
# =============================================================================

import numpy as np
import pandas as pd
import re

# -----------------------------------------------------------------------------
# Step 0 — Create the raw dataset
# -----------------------------------------------------------------------------

raw_data = {
    "Customer ID": [1,       2,       3,       4,    5             ],
    "Age":         [25,      np.nan,  35,      40,   np.nan        ],
    "Rating":      [5,       3,       np.nan,  1,    4             ],
    "Comment":     ["Super product!", "", np.nan, "!!!", "Could be better"],
}

customer_ratings = pd.DataFrame(raw_data)


# -----------------------------------------------------------------------------
# Step (e) — Wrap all cleaning steps in a reusable function
# -----------------------------------------------------------------------------

def clean_customer_data(df):
    """
    Cleans the customer ratings DataFrame by:
      (a) Removing rows with missing Age or Rating
      (b) Replacing missing Comments with 'No comment'
      (c) Replacing empty string Comments with 'No comment'
      (d) Removing rows where Comment is only special characters
      (e) Adding a 'Label' column based on the Rating value
    Returns the cleaned DataFrame.
    """

    # Step (a) — Remove rows where Age or Rating is missing
    df.dropna(subset=["Age", "Rating"], inplace=True)

    # Step (b) — Replace NaN comments with "No comment"
    df["Comment"] = df["Comment"].fillna("No comment")

    # Step (c) — Replace empty string comments with "No comment"
    df["Comment"] = df["Comment"].apply(
        lambda x: "No comment" if x.strip() == "" else x
    )

    # Step (d) — Remove rows where Comment is only special characters
    only_special_chars = df["Comment"].apply(
        lambda x: bool(re.match(r"^[!?.#*]+$", x))
    )
    df = df[~only_special_chars]

    # Step (d cont.) — Add a Label column based on Rating
    df["Label"] = pd.cut(
        df["Rating"],
        bins=[0, 2, 3, 5],
        labels=["Negative", "Neutral", "Positive"],
        include_lowest=True,
    )

    return df


# -----------------------------------------------------------------------------
# Run the function and display the result
# -----------------------------------------------------------------------------

cleaned_data = clean_customer_data(customer_ratings)

print("Cleaned customer ratings dataset:")
print(cleaned_data)
```

---

*Documentation generated for K4.0031 — Exercise 4.C.01*