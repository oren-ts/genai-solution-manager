# Import the pandas library for data analysis
import pandas as pd


# Define a function that analyzes a CSV file
def analyze_csv_data(filepath):

    # Read the CSV file into a DataFrame
    df = pd.read_csv(filepath)
    print(df)

    # Get the number of rows and columns
    rows, columns = df.shape
    print(f"Number of rows: {rows}\nNumber of columns: {columns}")

    # Get the first five rows of the dataset
    top_rows = df.head()
    print(top_rows)

    # Calculate the average of all numeric columns
    mean_num = df.mean(numeric_only=True)
    print(mean_num)


# Call the function with the path to the CSV file
analyze_csv_data(
    "/Users/orentauber-sharon/Documents/GitHub/genai-python-exercises/K4.0031_4.0_machine_learning/01_learn_from_data/01_learn_from_data_E1.Ü.02/sample_data.csv"
)
