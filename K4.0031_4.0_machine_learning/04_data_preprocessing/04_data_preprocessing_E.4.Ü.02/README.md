# Categorical Data & One-Hot Encoding

**Course:** velpTEC K4.0031 — Machine Learning  
**Topic:** Data Preprocessing — Categorical Data  
**Exercise:** 4.Ü.02 — One-Hot Encoding  
**Script:** `CategoricalData.py`

---

## Table of Contents

1. [What is Categorical Data?](#1-what-is-categorical-data)
2. [The Problem with Categories in ML](#2-the-problem-with-categories-in-ml)
3. [Encoding Strategies](#3-encoding-strategies)
4. [One-Hot Encoding — Theory](#4-one-hot-encoding--theory)
5. [The Math Behind One-Hot Encoding](#5-the-math-behind-one-hot-encoding)
6. [The Dummy Variable Trap](#6-the-dummy-variable-trap)
7. [Implementation with Pandas](#7-implementation-with-pandas)
8. [Full Annotated Script](#8-full-annotated-script)
9. [Output Walkthrough](#9-output-walkthrough)
10. [When to Use One-Hot Encoding](#10-when-to-use-one-hot-encoding)

---

## 1. What is Categorical Data?

**Categorical data** represents values that belong to a fixed set of named groups — called *categories* or *classes*. These values describe *which group* something belongs to, not a measurable quantity.

### Examples

| Feature | Type | Values |
|---|---|---|
| Color | Categorical (nominal) | Red, Green, Blue |
| Gender | Categorical (binary) | Male, Female |
| Size | Categorical (ordinal) | Small, Medium, Large |
| Temperature | Numerical (continuous) | 12.4, 33.1, -5.0 |
| Bedrooms | Numerical (discrete) | 1, 2, 3, 4 |

There are two sub-types of categorical data:

- **Nominal** — categories have no natural order (e.g. colors, country names)
- **Ordinal** — categories have a meaningful order (e.g. Small < Medium < Large)

One-hot encoding is most appropriate for **nominal** data.

---

## 2. The Problem with Categories in ML

Machine learning algorithms are mathematical — they operate on numbers. When a column contains strings like `"Red"`, `"Green"`, or `"Blue"`, the algorithm has no way to process them.

A naive fix might be to assign integers:

```
Red   → 0
Green → 1
Blue  → 2
```

This is called **label encoding**, and it works for *ordinal* data. But for nominal categories, it introduces a false mathematical relationship. The model would infer:

$$\text{Blue} = \text{Red} + \text{Green}$$
$$\text{Blue} > \text{Green} > \text{Red}$$

Neither of these is true. Colors have no ranking or arithmetic relationship. This false ordering can distort model predictions — particularly in linear models, SVMs, and neural networks.

**One-hot encoding solves this problem.**

---

## 3. Encoding Strategies

| Strategy | Best For | Risk |
|---|---|---|
| **Label Encoding** | Ordinal categories (Small/Med/Large) | Implies false numeric order for nominal data |
| **One-Hot Encoding** | Nominal categories (colors, countries) | Can create many columns for high-cardinality data |
| **Ordinal Encoding** | Ordinal categories with known rank | Must define the rank order explicitly |
| **Target Encoding** | High-cardinality nominal data | Risk of data leakage if not handled carefully |

---

## 4. One-Hot Encoding — Theory

One-hot encoding transforms a single categorical column with $k$ unique values into $k$ new binary columns — one per unique category. Each row gets a `1` in the column that matches its original category, and `0` in all other columns.

### Intuition

Think of it as a set of yes/no questions:

> Given a row with color = `"Red"`:
> - *Is this Red?* → **1**
> - *Is this Green?* → **0**
> - *Is this Blue?* → **0**

The result is a **binary vector** that encodes membership without implying any ordering.

### Before Encoding

| Index | Color |
|---|---|
| 0 | Red |
| 1 | Green |
| 2 | Blue |
| 3 | Red |

### After One-Hot Encoding

| Index | Color_Blue | Color_Green | Color_Red |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 0 | 0 | 1 |

Each row now contains exactly one `1` — the column representing the original category.

---

## 5. The Math Behind One-Hot Encoding

### Binary Vector Representation

For a categorical feature $x$ with $k$ unique categories $\{c_1, c_2, \ldots, c_k\}$, one-hot encoding maps each value to a vector in $\mathbb{R}^k$:

$$\text{one\_hot}(c_i) = \mathbf{e}_i \in \{0, 1\}^k$$

where $\mathbf{e}_i$ is the $i$-th standard basis vector:

$$\mathbf{e}_i = (0, \ldots, 0, \underbrace{1}_{i\text{-th position}}, 0, \ldots, 0)$$

### Example

With 3 unique colors: Red, Green, Blue — the encoding assigns:

$$\text{Red} \rightarrow \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}, \quad \text{Green} \rightarrow \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}, \quad \text{Blue} \rightarrow \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}$$

> **Note:** The column order (alphabetical by default in `pd.get_dummies`) determines which category maps to which position.

### Key Properties

$$\sum_{j=1}^{k} \mathbf{e}_j^{(i)} = 1 \quad \text{(exactly one 1 per row)}$$

$$\mathbf{e}_i \cdot \mathbf{e}_j = \delta_{ij} = \begin{cases} 1 & \text{if } i = j \\ 0 & \text{if } i \neq j \end{cases}$$

The vectors are **orthonormal** — each category is equidistant from every other in the encoded space. This is exactly the property needed to prevent any false ordering.

---

## 6. The Dummy Variable Trap

When using one-hot encoding in **linear models** (linear regression, logistic regression), including all $k$ columns creates a problem called **multicollinearity** — the dummy variable trap.

### Why It Happens

If you know the values of $k-1$ columns, the last column is always predictable:

$$\text{Color\_Red} = 1 - \text{Color\_Blue} - \text{Color\_Green}$$

This perfect linear dependency causes issues for models that invert the feature matrix (like linear regression), as the matrix becomes **singular** (non-invertible).

### Solution: Drop One Column

Use $k-1$ columns instead of $k$. The dropped category is implicitly represented when all remaining columns are `0`.

```python
# Drop one column to avoid the dummy variable trap
pd.get_dummies(dataframe, columns=["Color"], dtype=int, drop_first=True)
```

| Index | Color_Green | Color_Red |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 1 | 0 |
| 2 | 0 | 0 |  ← Blue is encoded as (0, 0)
| 3 | 0 | 1 |

> **Rule of thumb:** Use `drop_first=True` for linear models. For tree-based models (Decision Tree, Random Forest) and neural networks, it is generally not necessary.

---

## 7. Implementation with Pandas

### `pd.get_dummies()` — Key Parameters

```python
pd.get_dummies(
    data,              # DataFrame or Series to encode
    columns=["Color"], # List of columns to encode (must be a list)
    dtype=int,         # Output type: int gives 0/1, bool gives True/False
    drop_first=False   # If True, drops first category to avoid multicollinearity
)
```

### Common Pitfall: `columns=` must be a list

```python
# ❌ Wrong — passing a string raises TypeError
pd.get_dummies(df, columns="Color")

# ✅ Correct — pass a list, even for a single column
pd.get_dummies(df, columns=["Color"])
```

### Common Pitfall: `dtype` default is `bool`

```python
# ❌ Default output — produces True/False, not ML-friendly
pd.get_dummies(df, columns=["Color"])
# Output: Color_Blue  Color_Green  Color_Red
#              False        False       True

# ✅ Explicit dtype — produces clean 0/1 integers
pd.get_dummies(df, columns=["Color"], dtype=int)
# Output: Color_Blue  Color_Green  Color_Red
#                  0            0          1
```

---

## 8. Full Annotated Script

```python
import pandas as pd

# Create a simple DataFrame with one column of categorical color data
color_data = pd.DataFrame({
    "Color": ["Red", "Green", "Blue", "Red"]
})

print("Original DataFrame:")
print(color_data)
print()


def one_hot_encode(dataframe):
    # Convert the categorical 'Color' column into separate 0/1 columns
    # Each unique color becomes its own column (e.g. Color_Red, Color_Blue)
    return pd.get_dummies(dataframe, columns=["Color"], dtype=int)


# Apply one-hot encoding to the color data
encoded_color_data = one_hot_encode(color_data)

print("One-Hot Encoded DataFrame:")
print(encoded_color_data)
```

### Line-by-Line Breakdown

| Line | What it does |
|---|---|
| `import pandas as pd` | Imports the Pandas library for DataFrame operations |
| `pd.DataFrame({...})` | Creates a DataFrame from a dictionary — keys become column names |
| `def one_hot_encode(dataframe)` | Defines a reusable function that takes any DataFrame as input |
| `pd.get_dummies(dataframe, columns=["Color"], dtype=int)` | Expands the `Color` column into binary integer columns |
| `encoded_color_data = one_hot_encode(color_data)` | Calls the function and stores the result |

---

## 9. Output Walkthrough

### Original DataFrame

```
   Color
0    Red
1  Green
2   Blue
3    Red
```

### After `one_hot_encode(color_data)`

```
   Color_Blue  Color_Green  Color_Red
0           0            0          1
1           0            1          0
2           1            0          0
3           0            0          1
```

### Reading the Output Row by Row

| Row | Original Color | Color_Blue | Color_Green | Color_Red | Interpretation |
|---|---|---|---|---|---|
| 0 | Red | 0 | 0 | 1 | Is Red? Yes |
| 1 | Green | 0 | 1 | 0 | Is Green? Yes |
| 2 | Blue | 1 | 0 | 0 | Is Blue? Yes |
| 3 | Red | 0 | 0 | 1 | Is Red? Yes |

Each row contains exactly one `1`. The columns are named with the prefix `Color_` because we passed the full DataFrame — this makes it clear which original column each binary column came from.

---

## 10. When to Use One-Hot Encoding

| Situation | Use One-Hot? | Notes |
|---|---|---|
| Nominal categories (colors, cities) | ✅ Yes | Core use case |
| Binary categories (Yes/No, Male/Female) | ✅ Yes (or label encode) | One-hot is safe; label encode also works |
| Ordinal categories (Small/Med/Large) | ⚠️ Use ordinal encoding instead | One-hot loses the ordering information |
| High-cardinality features (1000+ unique values) | ⚠️ Caution | Creates too many columns; consider target encoding |
| Tree-based models (Decision Tree, Random Forest) | ✅ Optional | Trees handle label encoding fine; one-hot not required |
| Linear models (Logistic Regression, SVM) | ✅ Required | Use `drop_first=True` to avoid dummy variable trap |
| Neural networks | ✅ Yes | One-hot is standard for categorical inputs |