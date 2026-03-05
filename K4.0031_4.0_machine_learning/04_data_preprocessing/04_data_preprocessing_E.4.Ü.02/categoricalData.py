import pandas as pd

# Create a simple DataFrame with one column of categorical color data
color_data = pd.DataFrame({"Color": ["Red", "Green", "Blue", "Red"]})

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
