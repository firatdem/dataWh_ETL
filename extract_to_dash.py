import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# .env get
db_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB")
}

# Create SQLAlchemy engine
engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")


# Example to test
def get_doctor_visit_summary():
    query = """
    SELECT d.doctor, COUNT(*) AS total_visits
    FROM fact_visits fv
    JOIN dim_doctors d ON fv.doctor_id = d.doctor_id
    GROUP BY d.doctor
    ORDER BY total_visits DESC;
    """
    return pd.read_sql(query, engine)


# Place holder export function
def export_to_csv(df, filename):
    print("Working dir:", os.getcwd())
    df.to_csv(f"exports/{filename}", index=False)


if __name__ == "__main__":
    df_summary = get_doctor_visit_summary()
    print(df_summary.head())
    export_to_csv(df_summary, "doctor_visit_summary.csv")
