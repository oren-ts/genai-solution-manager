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
