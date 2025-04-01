# Healthcare Data ETL & Warehousing Pipeline

**Project Repo:** `dataWH_ETL`

This project demonstrates a complete data cleaning and feature engineering pipeline for a simulated healthcare dataset. It is designed to showcase practical data engineering skills with an emphasis on ETL (Extract, Transform, Load), data profiling, and warehouse-readiness.

---

## Goals

- Clean and standardize a realistic healthcare dataset
- Perform feature engineering to enable deep analysis
- Prepare the dataset for warehousing, SQL analytics, and big data tools like Apache Spark
- Showcase skills relevant to data engineering and analytics roles

---

## Technologies Used

- **Python / Pandas** – data manipulation and transformation
- **PyCharm** – local dev & exploration
- *(Future-ready for: Apache Spark, PostgreSQL, dbt, Airflow, etc.)*

---

## Steps Performed

### 1. Understand the Data
- Previewed structure, types, and distributions

### 2. Handle Missing Values
- Checked for true nulls and "soft nulls" (e.g., `'Unknown'`, `'N/A'`)

### 3. Fix Column Names
- Standardized to `snake_case` for consistency and code-friendliness

### 4. Fix Data Types
- Parsed admission and discharge dates
- Calculated `length_of_stay`

### 5. Standardize Categorical Values
- Cleaned gender, medication names, admission types, etc.

### 6. Remove Duplicates
- Dropped exact duplicates
- Optionally deduplicated by key fields

### 7. Outlier Detection
- Flagged high/low age, cost, and length of stay values
- Optional: removed outliers based on thresholds

### 8. Feature Engineering
- Age groups
- Total stay cost (billing per day)
- Admission urgency
- Medication class
- Hospital load
- Chronic condition flags
- Patient visit count

### 9. Final Checks
- Null audit
- Data type audit
- Export to clean CSV

---

## Output

Final cleaned file:

cleaned_healthcare_data.csv


Ready for:
- SQL-based analytics
- Spark ingestion
- Warehousing
- ML pipelines

---

## Next Steps (Planned)

- ~~Load into PostgreSQL or Redshift~~
- Build SQL queries or dashboards
- Create Apache Spark-based transformation pipeline
- Automate with Apache Airflow or dbt

---

## Author

Built by Firat Demirbulakli — aspiring Data Engineer with a focus on building real-world pipelines and automating data transformation workflows.

---

## Like this project?
Star it, fork it, or reach out if you'd like to collaborate!


