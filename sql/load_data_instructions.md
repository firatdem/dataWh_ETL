# Load Data Instructions

This guide will help you load the cleaned CSV files into your PostgreSQL database for the `dataWH_ETL` project.

---

## Prerequisites

- PostgreSQL installed (tested with v14+)
- pgAdmin (optional but recommended for easier import)
- All `.csv` files placed in the `/data` folder of this repo

---

## Step 1: Create the Database & Tables

You can create the tables manually using the SQL scripts provided:

```bash
psql -U your_username -d your_database -f sql/create_tables.sql
```

Or copy-paste each `.sql` file inside the `/sql/` folder into the pgAdmin Query Tool and run them in this order:

1. `dim_patients.sql`
2. `dim_doctors.sql`
3. `dim_hospitals.sql`
4. `dim_medications.sql`
5. `dim_insurance.sql`
6. `fact_visits.sql`

---

## Step 2: Import the CSV Files

> **Important:** When using the pgAdmin import tool, make sure to check **"Header"** and specify the correct column order — otherwise you may get syntax/type errors.

### Example for `dim_doctors.csv` using pgAdmin:

1. Right-click the `dim_doctors` table → `Import/Export`
2. Choose the file `dim_doctors.csv`
3. Set **Format** to `CSV`
4. Check the **Header** box
5. Set **Delimiter** to `,`
6. Match the column order (e.g., `doctor_id,doctor`) or use:

```sql
\copy public.dim_doctors(doctor, doctor_id)
FROM 'path/to/dim_doctors.csv'
DELIMITER ',' CSV HEADER;
```

> If you do not check the **Header** box, you may get errors like: `ERROR: invalid input syntax for type integer: "doctor"`

Repeat this process for all other tables, making sure the column order in the import matches the schema.

---

## Troubleshooting

- **Invalid input syntax for type integer**: Usually means the header row was not skipped. Always enable `CSV HEADER`.
- **Foreign key errors when inserting into **``: Ensure dimension tables are loaded first and contain matching keys.
- If using the `\copy` command from `psql`, remember it's relative to the *client*, not the *server*.

---

## Suggested Load Order

1. `dim_patients.csv`
2. `dim_doctors.csv`
3. `dim_hospitals.csv`
4. `dim_medications.csv`
5. `dim_insurance.csv`
6. `fact_visits.csv` (must come last — relies on foreign keys)

---

## Test Your Setup

Run the following to verify the data is loaded correctly:

```sql
SELECT COUNT(*) FROM fact_visits;
SELECT COUNT(*) FROM dim_patients;
```

You should see non-zero row counts if everything worked.

