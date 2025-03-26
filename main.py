"""

Project to showcase SQL and Big data handling

High level view:

1. Understand the data
2. Handle missing values
3. Fix column names
4. Fix data types
5. Standardize Categorical data
6. Remove duplicates
7. Outlier detection
8. Feature engineering
9. Final checks

"""


import pandas as pd
"""
1. Understand the data
Handled by loading and previewing the data set, by loading it, then using df.head() to print the first few rows

Can also explore structure & meta data, below is quick commands to understand data using pandas
"""
# Replace with the correct path to your CSV file
csv_path = "healthcare_dataset.csv"

# Load the CSV into a pandas DataFrame
df = pd.read_csv(csv_path)

# Print first few elements
print(f"Snippet of data: \n{df.head()}")

# Get number of rows and columns
print(f"Shape: {df.shape}")

# Show all column names
print("\nColumn Names:")
print(df.columns.tolist())

# Show data types, non-null counts
print("\nDataFrame Info:")
print(df.info())

# Summary stats for all columns (including categorical)
print("\nSummary Statistics:")
print(df.describe(include='all'))

# Count unique values per column
print(df.nunique())

# Count missing values
print(df.isnull().sum())

# Count duplicate rows
print(f"Duplicate Rows: {df.duplicated().sum()}")


"""
2. Handle missing data values
"""

# Look for "blank" values
for col in df.columns:
    print(f"{col} blank entries:", df[col].isin(['', 'None', 'Unknown', 'N/A']).sum())




"""

# Optional: Show basic info about columns and data types
print("\nDataFrame Info:")
print(df.info())

# Optional: Show basic statistics
print("\nSummary Statistics:")
print(df.describe(include='all'))

print("\nShape of Dataset")
print(df.shape)

print("\nPrint null results")
print(df.isnull().sum())             # Count of missing values

"""

