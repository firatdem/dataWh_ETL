"""

Fact table surrounded by dim tables:

                         +------------------+
                         |   dim_patients   |
                         +------------------+
                                 ▲
                                 |
                                 ▼
+--------------+       +------------------+       +-------------------+
| dim_hospitals|<----->|   fact_visits    |<----->| dim_medications   |
+--------------+       +------------------+       +-------------------+
                                 ▲
                                 |
                       +--------------------+
                       |    dim_doctors     |
                       +--------------------+
                                 ▲
                                 |
                          +--------------+
                          | dim_insurance|
                          +--------------+



Fact vs Dimesion table:

## Fact Table	                ## Dimension Table

Stores events/transactions	    Stores descriptive context
Answers "how much?"	            Answers "who / what / where?"
Has metrics/numbers to analyze	Has attributes to describe
Usually contains foreign keys	Usually contains primary keys
Gets big fast (millions of rows)	Typically smaller in size


name - dim
age	- dim
gender - dim
blood_type - dim
medical_condition - dim
date_of_admission - fact
doctor - fact
hospital - fact
insurance_provider - dim
billing_amount - fact
room_number - fact
admission_type - fact
discharge_date - fact
medication - dim
test_results - fact
length_of_stay - fact
age_group - dim
total_stay_cost - fact
is_emergency - dim
admit_month	- fact
admit_quarter - fact
has_chronic - dim
medication_type - dim
hospital_patient_count - derived aggregation, not to be stored
visit_count - derived aggregation, not to be stored

## Core table

Column	Description
visit_id	Primary Key
patient_id	FK to dim_patients
doctor_id	FK to dim_doctors
hospital_id	FK to dim_hospitals
insurance_id	FK to dim_insurance
medication_id	FK to dim_medications
date_of_admission	Visit start date
discharge_date	Visit end date
admission_type	Label (or use admission_type_id FK)
test_results	Label (or link to a small dim_test_results)
billing_amount	Total cost of the visit
length_of_stay	Derived from date fields
total_stay_cost	Derived billing per day
admit_month	Derived from date of admission
admit_quarter	Derived from date of admission

## dim_patients

Column	Description
patient_id	Primary Key
name	Patient's full name
age	Age at time of data snapshot
gender	Categorical (e.g., Male, Female)
blood_type	Blood type (A+, O-, etc.)
medical_condition	Chronic or diagnosed condition (e.g., Diabetes)
age_group	Binned age ranges for analysis
has_chronic	Boolean or flag for chronic illness

## dim_hospitals

Column	Description
hospital_id	Primary Key
hospital_name	Hospital name
location	City or region
type	e.g., General, Children’s, Specialty

## dim_doctors

Column	Description
doctor_id	Primary Key
name	Full name of doctor
specialty	e.g., Cardiology, General Practice
hospital_id	Optional FK if each doctor belongs to one

## dim_medications

Column	Description
medication_id	Primary Key
medication_name	Standardized medication name
medication_type	Category (e.g., Antibiotic, Pain Relief)

## dim_insurance

Column	Description
insurance_id	Primary Key
insurance_provider	Name of the insurance company
plan_type	(Optional) HMO, PPO, etc.

"""

import pandas as pd

# Load your cleaned dataset
df = pd.read_csv("cleaned_healthcare_data.csv")


# --------- Helper to create surrogate keys ---------
def generate_surrogate_key(df_slice, key_name):
    df_unique = df_slice.drop_duplicates().reset_index(drop=True)
    df_unique[key_name] = df_unique.index + 1
    return df_unique

# 1. dim_patients
dim_patients = generate_surrogate_key(
    df[['name', 'age', 'gender', 'blood_type', 'medical_condition', 'age_group', 'has_chronic']],
    'patient_id'
)

# 2. dim_doctors
dim_doctors = generate_surrogate_key(df[['doctor']], 'doctor_id')

# 3. dim_hospitals
dim_hospitals = generate_surrogate_key(df[['hospital']], 'hospital_id')

# 4. dim_medications
dim_medications = generate_surrogate_key(df[['medication', 'medication_type']], 'medication_id')

# 5. dim_insurance
dim_insurance = generate_surrogate_key(df[['insurance_provider']], 'insurance_id')

# --------- Create fact_visits table by merging surrogate keys ---------
fact_visits = df \
    .merge(dim_patients, on=['name', 'age', 'gender', 'blood_type', 'medical_condition', 'age_group', 'has_chronic']) \
    .merge(dim_doctors, on='doctor') \
    .merge(dim_hospitals, on='hospital') \
    .merge(dim_medications, on=['medication', 'medication_type']) \
    .merge(dim_insurance, on='insurance_provider')

fact_visits = fact_visits[[
    'patient_id', 'doctor_id', 'hospital_id', 'medication_id', 'insurance_id',
    'date_of_admission', 'discharge_date', 'admission_type', 'test_results',
    'billing_amount', 'length_of_stay', 'cost_per_day',
    'admit_month', 'admit_quarter'
]].reset_index(drop=True)

fact_visits['visit_id'] = fact_visits.index + 1

# --------- Save each table to CSV ---------
dim_patients.to_csv("dim_patients.csv", index=False)
dim_doctors.to_csv("dim_doctors.csv", index=False)
dim_hospitals.to_csv("dim_hospitals.csv", index=False)
dim_medications.to_csv("dim_medications.csv", index=False)
dim_insurance.to_csv("dim_insurance.csv", index=False)
fact_visits.to_csv("fact_visits.csv", index=False)

print("All dimension and fact tables exported successfully.")

"""
SQL TABLE CREATION STATEMENTS:

dim_patients.sql:

CREATE TABLE dim_patients (
    patient_id SERIAL PRIMARY KEY,
    name TEXT,
    age INT,
    gender TEXT,
    blood_type TEXT,
    medical_condition TEXT,
    age_group TEXT,
    has_chronic BOOLEAN
);

dim_doctors.sql:

CREATE TABLE dim_doctors (
    doctor_id SERIAL PRIMARY KEY,
    doctor TEXT
);

dim_hospitals.sql:

CREATE TABLE dim_hospitals (
    hospital_id SERIAL PRIMARY KEY,
    hospital TEXT
);

dim_medications.sql:

CREATE TABLE dim_medications (
    medication_id SERIAL PRIMARY KEY,
    medication TEXT,
    medication_type TEXT
);

dim_insurance.sql:

CREATE TABLE dim_insurance (
    insurance_id SERIAL PRIMARY KEY,
    insurance_provider TEXT
);

fact_visits.sql:

CREATE TABLE fact_visits (
    visit_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES dim_patients(patient_id),
    doctor_id INT REFERENCES dim_doctors(doctor_id),
    hospital_id INT REFERENCES dim_hospitals(hospital_id),
    medication_id INT REFERENCES dim_medications(medication_id),
    insurance_id INT REFERENCES dim_insurance(insurance_id),
    date_of_admission DATE,
    discharge_date DATE,
    admission_type TEXT,
    test_results TEXT,
    billing_amount NUMERIC,
    length_of_stay INT,
    cost_per_day NUMERIC,
    admit_month INT,
    admit_quarter INT
);


"""