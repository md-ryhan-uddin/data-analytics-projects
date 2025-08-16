# load_csvs_to_postgres.py
import os
import glob
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# --- Config ---
CSV_DIR = os.path.join("data")  # folder containing your CSVs
IF_EXISTS = "replace"            # or "replace"
# ---------------

# Load environment variables from .env (not tracked in GitHub)
load_dotenv()

# Read values from .env
PG_HOST = os.getenv("DB_HOST", "localhost")
PG_PORT = int(os.getenv("DB_PORT", "5432"))
PG_USER = os.getenv("DB_USER", "postgres")
PG_PASSWORD = os.getenv("DB_PASS")
PG_DB = os.getenv("DB_NAME", "Oldest_Businesses_DB")


def make_url(dbname: str) -> URL:
    """Build a SQLAlchemy URL that properly escapes special chars in password."""
    return URL.create(
        "postgresql+psycopg2",
        username=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        database=dbname,
    )

def ensure_database():
    # connect to admin DB 'postgres' and create PG_DB if not exists
    admin_engine = create_engine(make_url("postgres"), isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :d"),
            {"d": PG_DB},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{PG_DB}";'))
            print(f'Created database "{PG_DB}".')

def norm_table_name(path: str) -> str:
    base = os.path.splitext(os.path.basename(path))[0]
    return base.strip().lower().replace(" ", "_")

def norm_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def main():
    ensure_database()
    engine = create_engine(make_url(PG_DB))

    csv_paths = sorted(glob.glob(os.path.join(CSV_DIR, "*.csv")))
    if not csv_paths:
        print(f"No CSVs found under: {CSV_DIR}")
        return

    for csv_path in csv_paths:
        table = norm_table_name(csv_path)
        print(f"→ Loading {csv_path} -> {table}")
        df = pd.read_csv(csv_path)
        df = norm_cols(df)
        # optional: gently convert year columns
        for col in df.columns:
            if col.endswith("year") or col.endswith("year_founded"):
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        df.to_sql(table, engine, if_exists=IF_EXISTS, index=False)
        print(f"   {len(df):,} rows written to {table}")

    print("\nDone.")

if __name__ == "__main__":
    main()
