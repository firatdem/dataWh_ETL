-- SQL TABLE CREATION STATEMENTS:

-- dim_patients.sql:

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

-- dim_doctors.sql:

CREATE TABLE dim_doctors (
    doctor_id SERIAL PRIMARY KEY,
    doctor TEXT
);

-- dim_hospitals.sql:

CREATE TABLE dim_hospitals (
    hospital_id SERIAL PRIMARY KEY,
    hospital TEXT
);

-- dim_medications.sql:

CREATE TABLE dim_medications (
    medication_id SERIAL PRIMARY KEY,
    medication TEXT,
    medication_type TEXT
);

-- dim_insurance.sql:

CREATE TABLE dim_insurance (
    insurance_id SERIAL PRIMARY KEY,
    insurance_provider TEXT
);

-- fact_visits.sql:

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
