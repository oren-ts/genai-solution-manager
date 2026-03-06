# =============================================================================
# Exercise 4.C.01 — Data Cleansing
# Course: K4.0031 Machine Learning
# =============================================================================
# Goal: Clean a customer ratings dataset by removing incomplete rows,
#       fixing missing comments, filtering junk text, and adding labels.
# =============================================================================

import numpy as np
import pandas as pd
import re


# -----------------------------------------------------------------------------
# Step 0 — Create the raw dataset
# -----------------------------------------------------------------------------

# Simulate a dataset with missing values and messy comments
raw_data = {
    "Customer ID": [1, 2, 3, 4, 5],
    "Age": [25, np.nan, 35, 40, np.nan],
    "Rating": [5, 3, np.nan, 1, 4],
    "Comment": ["Super product!", "", np.nan, "!!!", "Could be better"],
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

    # -------------------------------------------------------------------------
    # Step (a) — Remove rows where Age or Rating is missing
    # -------------------------------------------------------------------------
    # dropna() with subset only checks the listed columns.
    # inplace=True modifies df directly instead of returning a new one.
    df.dropna(subset=["Age", "Rating"], inplace=True)

    # -------------------------------------------------------------------------
    # Step (b) — Replace NaN comments with "No comment"
    # -------------------------------------------------------------------------
    # fillna() only catches actual NaN values — not empty strings.
    # We reassign the column because pandas 2.x doesn't reliably
    # update in-place via fillna(inplace=True).
    df["Comment"] = df["Comment"].fillna("No comment")

    # -------------------------------------------------------------------------
    # Step (c) — Replace empty string comments with "No comment"
    # -------------------------------------------------------------------------
    # apply() runs the lambda function on every value in the column.
    # x.strip() removes whitespace — so "  " (just spaces) also counts as empty.
    df["Comment"] = df["Comment"].apply(
        lambda x: "No comment" if x.strip() == "" else x
    )

    # -------------------------------------------------------------------------
    # Step (d) — Remove rows where Comment is only special characters
    # -------------------------------------------------------------------------
    # re.match() checks if the comment matches the pattern:
    #   ^        = start of string
    #   [!?.#*]+ = one or more special characters
    #   $        = end of string
    # bool() converts the match result to True/False.
    # ~ flips the boolean — so we KEEP rows that do NOT match.
    only_special_chars = df["Comment"].apply(lambda x: bool(re.match(r"^[!?.#*]+$", x)))
    df = df[~only_special_chars]

    # -------------------------------------------------------------------------
    # Step (d cont.) — Add a 'Label' column based on Rating
    # -------------------------------------------------------------------------
    # pd.cut() divides a continuous range into named bins (like buckets).
    # bins=[0, 2, 3, 5] creates three intervals:
    #   (0–2] → "Negative"
    #   (2–3] → "Neutral"
    #   (3–5] → "Positive"
    # include_lowest=True ensures rating 1 is included in the first bin.
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
