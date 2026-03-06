"""
4.Ü.03 - Column Transformer
============================
Use sklearn's ColumnTransformer to apply OneHotEncoding to a categorical
column while leaving numeric columns unchanged.

Concepts covered:
  - ColumnTransformer: apply different transformations to different columns
  - OneHotEncoder:     convert categorical text values into binary columns
  - drop='first':      remove one dummy column to avoid the dummy variable trap
  - passthrough:       leave selected columns exactly as they are
"""

# ── a) Import required modules ────────────────────────────────────────────────

import pandas as pd
from sklearn.preprocessing import OneHotEncoder  # converts categories → binary columns
from sklearn.compose import ColumnTransformer  # applies different transforms per column


# ── b) Define the DataFrame ───────────────────────────────────────────────────

# Sample data with one categorical column (color) and two numeric columns
sample_data = {
    "color": ["Red", "Green", "Blue", "Red"],
    "size": [1, 2, 3, 2],
    "price": [10.2, 9.6, 12.5, 11.1],
}

clothing_df = pd.DataFrame(sample_data)

print("Original DataFrame:")
print(clothing_df)
print()


# ── c) Create the ColumnTransformer ──────────────────────────────────────────

# The ColumnTransformer takes a list of (name, transformer, columns) tuples.
#
# Tuple 1 — "encode_color":
#   Apply OneHotEncoder to the 'color' column.
#   drop='first' removes the first dummy column (Blue) to avoid collinearity.
#   With 3 colors (Blue, Green, Red), we only need 2 columns to represent all 3.
#
# Tuple 2 — "passthrough":
#   Leave 'size' and 'price' completely unchanged.

column_transformer = ColumnTransformer(
    [
        ("encode_color", OneHotEncoder(drop="first"), ["color"]),
        ("passthrough", "passthrough", ["size", "price"]),
    ]
)


# ── d) Apply the Transformer and print the result ─────────────────────────────

# fit_transform() learns the categories from the data, then transforms it.
# The result is a NumPy array — column names are not preserved.
transformed_data = column_transformer.fit_transform(clothing_df)

print("Transformed array (color encoded, size & price unchanged):")
print(transformed_data)
print()

# Column layout of the output:
#   Col 0 → color_Green  (1 = Green, 0 = not Green)
#   Col 1 → color_Red    (1 = Red,   0 = not Red)
#   Col 2 → size         (passed through as-is)
#   Col 3 → price        (passed through as-is)
#
# Note: Blue is the dropped category.
#       If both color_Green and color_Red are 0, the color must be Blue.
print("Output column order: [color_Green, color_Red, size, price]")
