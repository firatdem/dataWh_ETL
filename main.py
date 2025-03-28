"""

Project to showcase SQL and Big data handling

High level view:

1. Understand the data - REUSABLE
2. Handle missing values - REUSABLE
3. Fix column names - REUSABLE
4. Fix data types - REUSABLE WITH CHANGES
5. Standardize Categorical data - REUSABLE WITH CHANGES
6. Remove duplicates - REUSABLE WITH (MINOR) CHANGES
7. Outlier detection
8. Feature engineering
9. Final checks

"""

import numpy as np
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
3. Fix column names
"""
# Clean column names: lower case, replace spaces with underscores
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# Confirm changes
print("\nCleaned Column Names:")
print(df.columns.tolist())

"""
4. Fix Data types
"""

# Convert date columns to datetime
df['date_of_admission'] = pd.to_datetime(df['date_of_admission'], errors='coerce')
df['discharge_date'] = pd.to_datetime(df['discharge_date'], errors='coerce')

# Confirm the data types changed
print("\nUpdated Data Types:")
print(df.dtypes[['date_of_admission', 'discharge_date']])

# Create a new column: length of stay (in days)
df['length_of_stay'] = (df['discharge_date'] - df['date_of_admission']).dt.days

# Preview the new column
print("\nSample Length of Stay Values:")
print(df[['date_of_admission', 'discharge_date', 'length_of_stay']].head())

"""
5. Standardize Categorical Data
"""

# Standardize gender values
df['gender'] = df['gender'].str.strip().str.lower().map({
    'male': 'Male',
    'female': 'Female'
})

# Capitalize test results properly
df['test_results'] = df['test_results'].str.strip().str.capitalize()

# Normalize admission types
df['admission_type'] = df['admission_type'].str.strip().str.title()

# Strip and title-case medication names
df['medication'] = df['medication'].str.strip().str.title()

# Optional: fix name casing
df['name'] = df['name'].str.title()

# Optional: display unique values for inspection
print("\nUnique Genders:", df['gender'].unique())
print("Unique Test Results:", df['test_results'].unique())
print("Unique Admission Types:", df['admission_type'].unique())

"""
6. Removing Duplicates
"""

# Count duplicates before
before = df.duplicated().sum()
print(f"\nDuplicate Rows Before: {before}")

# Drop duplicate rows
df = df.drop_duplicates()

# Count after
after = df.duplicated().sum()
print(f"Duplicate Rows After: {after}")

# New shape
print(f"New DataFrame Shape: {df.shape}")

# Optional: remove based on a subset of columns
df = df.drop_duplicates(subset=['name', 'date_of_admission', 'doctor'])

"""
7. Detect & Investigate Outliers
"""

# Summary of key numeric columns
print("\nSummary Stats - Age, Billing Amount, Length of Stay:")
print(df[['age', 'billing_amount', 'length_of_stay']].describe())

# View possible outliers
print("\nPotential Age Outliers:")
print(df[df['age'] > 100][['name', 'age']].head())

print("\nLength of Stay Outliers:")
print(df[df['length_of_stay'] < 0][['name', 'length_of_stay']])
print(df[df['length_of_stay'] > 60][['name', 'length_of_stay']].head())

print("\nHigh Billing Amounts (Top 5):")
print(df.sort_values('billing_amount', ascending=False)[['name', 'billing_amount']].head())

# -------------------------------
# Flag Outliers (Non-destructive)
# -------------------------------

df['age_outlier'] = df['age'] > 100

# Top 0.1% of billing amounts flagged as outliers
billing_threshold = df['billing_amount'].quantile(0.999)
df['billing_outlier'] = df['billing_amount'] > billing_threshold

# Flag negative or overly long hospital stays
df['los_outlier'] = (df['length_of_stay'] < 0) | (df['length_of_stay'] > 60)

# -------------------------------
# Optional: Remove Outliers
# Uncomment below lines to drop them
# -------------------------------

# df = df[df['age'] <= 100]
# df = df[df['billing_amount'] <= billing_threshold]
# df = df[(df['length_of_stay'] >= 0) & (df['length_of_stay'] <= 60)]

# Show sample flagged outliers
print("\nFlagged Age Outliers:")
print(df[df['age_outlier']][['name', 'age']].head())

print("\nFlagged Billing Outliers:")
print(df[df['billing_outlier']][['name', 'billing_amount']].head())

print("\nFlagged Length of Stay Outliers:")
print(df[df['los_outlier']][['name', 'length_of_stay']].head())

"""
8. Feature Engineering
"""

# Age buckets for demographic analysis
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 65, 100], labels=['0-18', '19-35', '36-50', '51-65', '66+'])

# Calculate stay per night
df['cost_per_day'] = df.apply(
    lambda row: row['billing_amount'] / row['length_of_stay']
    if row['length_of_stay'] and row['length_of_stay'] > 0 else None,
    axis=1
)

df['is_emergency'] = df['admission_type'].str.lower() == 'emergency'

df['admit_month'] = df['date_of_admission'].dt.month
df['admit_quarter'] = df['date_of_admission'].dt.quarter

# Flag for chronic illness (simple example)
chronic_conditions = ['Diabetes', 'Hypertension', 'COPD']
df['has_chronic'] = df['medical_condition'].isin(chronic_conditions)

# Map medications to categories
med_mapping = {
    'Lipitor': 'Cardiovascular',
    'Aspirin': 'Pain Relief',
    'Ibuprofen': 'Pain Relief',
    'Paracetamol': 'Pain Relief',
    'Penicillin': 'Antibiotic'
}
df['medication_type'] = df['medication'].map(med_mapping)

# Count how many patients per hospital
hospital_counts = df['hospital'].value_counts().to_dict()
df['hospital_patient_count'] = df['hospital'].map(hospital_counts)

df['visit_count'] = df.groupby('name')['name'].transform('count')

"""
9. Final Checks
"""

print("\nFinal Data Types:")
print(df.dtypes)

print("\nNull Counts by Column:")
print(df.isnull().sum())

# Drop columns used for derived aggregations (not part of stored output)
df.drop(columns=['hospital_patient_count', 'visit_count'], inplace=True)

# Drop columns related to outlier data
df.drop(columns=['age_outlier', 'billing_outlier', 'los_outlier'], inplace=True)

print("\nFinal Shape:", df.shape)
print("Unique Patient Names:", df['name'].nunique())

# Round billing_amount and cost_per_day UP to 2 decimal places
df['billing_amount'] = np.ceil(df['billing_amount'] * 100) / 100
df['cost_per_day'] = df['cost_per_day'].apply(
    lambda x: np.ceil(x * 100) / 100 if pd.notnull(x) else x
)

# Save as CSV with float values shown as xx.00
df.to_csv("cleaned_healthcare_data.csv", index=False, float_format="%.2f")
print("\n✅ Cleaned dataset saved as 'cleaned_healthcare_data.csv'")




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

