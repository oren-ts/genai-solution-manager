# Exercise 10.Ü.01 — Correlation Matrix

**Course:** velpTEC K4.0031 — Machine Learning  
**Chapter:** 10 — Exploratory Data Analysis & Regression  
**Topic:** Generating a fictitious housing dataset and visualizing its correlation matrix  

---

## Table of Contents

1. [What is a Correlation Matrix?](#1-what-is-a-correlation-matrix)
2. [The Math — Pearson Correlation Coefficient](#2-the-math--pearson-correlation-coefficient)
3. [Why Correlation Matters in Machine Learning](#3-why-correlation-matters-in-machine-learning)
4. [The Dataset — Variables and Their Meaning](#4-the-dataset--variables-and-their-meaning)
5. [Code Walkthrough](#5-code-walkthrough)
   - [Section 1 — Imports](#section-1--imports)
   - [Section 2 — Generating the Dataset](#section-2--generating-the-dataset)
   - [Section 3 — Computing the Correlation Matrix](#section-3--computing-the-correlation-matrix)
   - [Section 4 — Visualizing the Heatmap](#section-4--visualizing-the-heatmap)
6. [Reading the Heatmap](#6-reading-the-heatmap)
7. [Key Takeaways](#7-key-takeaways)

---

## 1. What is a Correlation Matrix?

Before training any machine learning model it is good practice to first
**explore and understand the data**. This process is called
**Exploratory Data Analysis (EDA)**.

One of the most powerful EDA tools is the **correlation matrix**. It is a
square table that contains the **correlation coefficient** between every pair
of variables in a dataset.

### Structure of a correlation matrix

For a dataset with variables A, B, and C the matrix looks like this:

|         | **A** | **B** | **C** |
|---------|-------|-------|-------|
| **A**   | 1.00  | 0.72  | -0.45 |
| **B**   | 0.72  | 1.00  | 0.10  |
| **C**   | -0.45 | 0.10  | 1.00  |

Three important properties to notice:

- The **diagonal is always 1.00** — every variable is perfectly correlated
  with itself.
- The matrix is **symmetric** — the value at row A, column B is always
  identical to the value at row B, column A.
- Values range from **-1 to +1**.

---

## 2. The Math — Pearson Correlation Coefficient

The correlation coefficient is formally known as the
**Pearson correlation coefficient**, denoted by $r$.

### Formula

$$r_{xy} = \frac{\sum_{i=1}^{n}(x^{(i)} - \mu_x)(y^{(i)} - \mu_y)}{\sqrt{\sum_{i=1}^{n}(x^{(i)} - \mu_x)^2} \cdot \sqrt{\sum_{i=1}^{n}(y^{(i)} - \mu_y)^2}}$$

### What each symbol means

| Symbol | Meaning |
|--------|---------|
| $x^{(i)}$ | The $i$-th observation of variable $x$ |
| $y^{(i)}$ | The $i$-th observation of variable $y$ |
| $\mu_x$ | The mean (average) of variable $x$ |
| $\mu_y$ | The mean (average) of variable $y$ |
| $n$ | Total number of observations |

### Intuition behind the formula

The numerator multiplies how far each $x$ value sits from its mean by how
far the corresponding $y$ value sits from its mean:

- If **both deviate in the same direction** (both above or both below their
  means) the product is **positive** → positive correlation accumulates.
- If they **deviate in opposite directions** the product is **negative** →
  negative correlation accumulates.
- The denominator **scales** the result so it always lands between -1 and +1.

### Equivalent form using covariance

The formula can also be written as:

$$r_{xy} = \frac{\sigma_{xy}}{\sigma_x \cdot \sigma_y}$$

Where:

| Symbol | Meaning |
|--------|---------|
| $\sigma_{xy}$ | Covariance of $x$ and $y$ |
| $\sigma_x$ | Standard deviation of $x$ |
| $\sigma_y$ | Standard deviation of $y$ |

So correlation is simply **covariance normalized by the product of the two
standard deviations**. This normalization is what keeps the value bounded
between -1 and +1.

### Interpreting the value of $r$

| Value of $r$ | Meaning |
|--------------|---------|
| $r = +1.0$ | Perfect positive linear relationship |
| $0.5 \leq r < 1.0$ | Strong positive relationship |
| $0 < r < 0.5$ | Weak positive relationship |
| $r = 0$ | No linear relationship |
| $-0.5 < r < 0$ | Weak negative relationship |
| $-1.0 < r \leq -0.5$ | Strong negative relationship |
| $r = -1.0$ | Perfect negative linear relationship |

### Concrete example

Suppose we have four observations of rooms (RM) and house price (MEDV):

| $i$ | RM ($x$) | MEDV ($y$) |
|-----|----------|------------|
| 1   | 4        | 200        |
| 2   | 5        | 250        |
| 3   | 6        | 300        |
| 4   | 7        | 350        |

Here $\mu_x = 5.5$ and $\mu_y = 275$. Every time RM increases, MEDV
increases by the same proportion — so $r = +1.0$. This is a perfect positive
correlation.

---

## 3. Why Correlation Matters in Machine Learning

### Feature selection

Correlation tells us which input variables (features) are likely to influence
the target variable. A high absolute correlation between a feature and the
target is a signal that the feature will be useful in a regression model.

**Example — Boston Housing dataset:**

| Feature | Correlation with MEDV | Interpretation |
|---------|-----------------------|----------------|
| RM      | +0.70                 | More rooms → higher price |
| LSTAT   | -0.74                 | Higher poverty rate → lower price |
| NOX     | -0.43                 | Higher pollution → lower price |

### Detecting redundant features

If two input features are strongly correlated with **each other** (not just
with the target), they carry similar information. Including both in a model
can cause **multicollinearity**, which makes regression coefficients
unreliable.

### Guiding regression coefficient expectations

Before training a model, correlation lets us anticipate the **sign** of
regression weights:

- If $r(x, y) > 0$ we expect the regression weight $w > 0$
- If $r(x, y) < 0$ we expect the regression weight $w < 0$

### Important note — normality is NOT required

A common misconception is that linear regression requires normally
distributed variables. This is **not true**. The normality assumption in
classical statistics applies only to the **residuals** (prediction errors),
not to the features or target variable themselves.

---

## 4. The Dataset — Variables and Their Meaning

This exercise uses a **fictitious** dataset that mimics the structure of the
Boston Housing dataset. It contains 100 randomly generated observations and
10 variables representing housing conditions in a city.

| Variable  | Full Name | Description | Range |
|-----------|-----------|-------------|-------|
| `CRIM`    | Crime rate | Per capita crime rate | 0–1 |
| `ZN`      | Zoning | % of residential land for large lots | 0–100 |
| `INDUS`   | Industry | % of non-retail business land | 0–25 |
| `NOX`     | Pollution | Nitrogen monoxide concentration | 0–1 |
| `RM`      | Rooms | Average number of rooms per dwelling | 0–10 |
| `AGE`     | Age | % of owner-occupied homes built before 1940 | 0–100 |
| `DIS`     | Distance | Weighted distance to employment centres | 0–10 |
| `RAD`     | Roads | Accessibility index for arterial roads | 1–9 |
| `TAX`     | Tax | Property tax per $10,000 | 200–700 |
| `PTRATIO` | School ratio | Pupil-to-teacher ratio | 0–20 |

> **Note:** Because this is a fictitious dataset generated with random
> numbers, the correlations between variables will be weak and close to zero.
> In a real housing dataset the correlations reflect genuine relationships
> between variables.

---

## 5. Code Walkthrough

### Section 1 — Imports

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
```

| Library | Alias | Purpose in this exercise |
|---------|-------|--------------------------|
| `pandas` | `pd` | Creating and managing the DataFrame |
| `numpy` | `np` | Generating random numbers |
| `seaborn` | `sns` | Drawing the heatmap |
| `matplotlib.pyplot` | `plt` | Controlling the figure and display |

---

### Section 2 — Generating the Dataset

#### Setting the random seed

```python
np.random.seed(0)
```

`np.random.seed(0)` initializes NumPy's random number generator at a fixed
starting point. This guarantees that every time the script runs, the same
sequence of "random" numbers is produced — making results **reproducible**.

Without this line, every run would produce a different dataset and a
different correlation matrix.

#### Two types of random number generators

This exercise uses two different NumPy functions:

**`np.random.rand(n)`** — generates $n$ random floats uniformly distributed
between 0 and 1:

$$x \sim \mathcal{U}(0, 1)$$

To scale to a different range, multiply by a scalar:

```python
np.random.rand(100) * 25   # produces values between 0 and 25
```

**`np.random.randint(low, high, size)`** — generates `size` random
**integers** between `low` (inclusive) and `high` (exclusive):

```python
np.random.randint(1, 10, 100)    # integers from 1 to 9
np.random.randint(200, 700, 100) # integers from 200 to 699
```

`RAD` and `TAX` use `randint` because they represent whole-number values
(an accessibility index and a tax amount).

#### Building the dictionary and DataFrame

```python
housing_data = {
    'CRIM':    np.random.rand(100),
    'ZN':      np.random.rand(100) * 100,
    'INDUS':   np.random.rand(100) * 25,
    'NOX':     np.random.rand(100),
    'RM':      np.random.rand(100) * 10,
    'AGE':     np.random.rand(100) * 100,
    'DIS':     np.random.rand(100) * 10,
    'RAD':     np.random.randint(1, 10, 100),
    'TAX':     np.random.randint(200, 700, 100),
    'PTRATIO': np.random.rand(100) * 20
}

housing_df = pd.DataFrame(housing_data)
```

A Python **dictionary** maps each column name (key) to an array of values.
`pd.DataFrame()` converts that dictionary into a structured table where:

- Each **row** is one observation (one fictitious house / district)
- Each **column** is one variable

The result looks like this (first 3 rows as example):

| CRIM | ZN | INDUS | NOX | RM | AGE | DIS | RAD | TAX | PTRATIO |
|------|----|-------|-----|----|-----|-----|-----|-----|---------|
| 0.55 | 71.5 | 6.0 | 0.02 | 9.7 | 83.2 | 7.8 | 5 | 412 | 14.3 |
| 0.43 | 9.2  | 18.3 | 0.87 | 4.1 | 11.0 | 2.1 | 3 | 567 | 8.6  |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

### Section 3 — Computing the Correlation Matrix

```python
correlation_matrix = housing_df.corr(method='pearson')
```

`DataFrame.corr()` computes the Pearson correlation coefficient for every
pair of columns and returns a square DataFrame. Internally it implements the
formula:

$$r_{xy} = \frac{\sigma_{xy}}{\sigma_x \cdot \sigma_y}$$

The `method='pearson'` argument explicitly selects the Pearson formula.
Other options exist (`'spearman'`, `'kendall'`) but Pearson is the standard
choice for continuous numerical data.

The output is a $10 \times 10$ matrix:

- **Diagonal** = 1.0 (every variable perfectly correlates with itself)
- **Off-diagonal** = correlation coefficient between each pair of variables
- **Symmetric** — `corr(CRIM, RM)` equals `corr(RM, CRIM)`

---

### Section 4 — Visualizing the Heatmap

```python
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix — Fictitious Housing Dataset')
plt.tight_layout()
plt.show()
```

#### Line by line

**`plt.figure(figsize=(10, 8))`**  
Creates a blank figure canvas of width 10 inches and height 8 inches. Without
specifying size the plot may be too small to read the annotated values.

**`sns.heatmap(...)`**  
Draws the heatmap. The three key arguments are:

| Argument | Value | Effect |
|----------|-------|--------|
| First positional | `correlation_matrix` | The data to visualize |
| `annot` | `True` | Prints the numeric correlation value inside each cell |
| `cmap` | `'coolwarm'` | Color scheme: red for positive, blue for negative |

**`plt.title(...)`**  
Adds a descriptive title to the figure.

**`plt.tight_layout()`**  
Automatically adjusts spacing between plot elements so axis labels do not
overlap.

**`plt.show()`**  
Renders and displays the completed figure.

---

## 6. Reading the Heatmap

The `coolwarm` color map encodes correlation values as follows:

| Color | Correlation value | Meaning |
|-------|-------------------|---------|
| Deep red | close to +1 | Strong positive relationship |
| Light pink / white | close to 0 | Weak or no relationship |
| Deep blue | close to -1 | Strong negative relationship |

The **diagonal** always appears deep red because each variable correlates
perfectly with itself ($r = 1.0$).

Because this exercise uses a **randomly generated** dataset with no real
relationships between variables, all off-diagonal cells will appear light
(close to 0). In a real dataset such as the original Boston Housing data you
would see:

- `RM` vs `MEDV` → strong red (+0.70) — more rooms, higher price
- `LSTAT` vs `MEDV` → strong blue (-0.74) — higher poverty, lower price
- `NOX` vs `INDUS` → strong red (industrial areas have more pollution)

---

## 7. Key Takeaways

| Concept | Summary |
|---------|---------|
| EDA | Always explore data visually and statistically before training a model |
| Pearson $r$ | Measures the strength and direction of a linear relationship between two variables |
| Range of $r$ | Always between -1 and +1 |
| Diagonal | Always 1.0 — a variable is perfectly correlated with itself |
| Symmetry | `corr(A, B)` = `corr(B, A)` |
| `df.corr()` | Pandas method that computes the full correlation matrix in one line |
| `sns.heatmap()` | Seaborn function that visualizes the matrix using colors |
| `annot=True` | Displays the numeric value inside each heatmap cell |
| `cmap='coolwarm'` | Red = positive correlation, Blue = negative correlation |
| Normality | Linear regression does NOT require normally distributed features — only residuals |
| Feature selection | High absolute correlation with the target variable suggests a useful feature |

---

*Exercise completed — velpTEC K4.0031 | Chapter 10*