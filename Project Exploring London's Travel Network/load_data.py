import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5439"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "tfl")

def make_url(dbname: str) -> URL:
    """Build a SQLAlchemy URL that properly escapes special chars in password."""
    return URL.create(
        "postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=dbname,
    )

def ensure_database():
    """Create database if it doesn't exist."""
    admin_engine = create_engine(make_url("postgres"), isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :d"),
            {"d": DB_NAME},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}";'))
            print(f'Created database "{DB_NAME}".')

def main():
    ensure_database()
    engine = create_engine(make_url(DB_NAME))
    
    # Load TFL journeys data
    csv_path = os.path.join("data", "TFL.JOURNEYS.csv")
    print(f"→ Loading {csv_path} -> journeys table")
    
    df = pd.read_csv(csv_path)
    
    # Normalize column names to lowercase with underscores
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Convert date columns
    if 'report_date' in df.columns:
        df['report_date'] = pd.to_datetime(df['report_date'], errors='coerce')
    
    # Load to PostgreSQL
    df.to_sql('journeys', engine, if_exists='replace', index=False)
    print(f"   {len(df):,} rows written to journeys table")
    
    # Display sample data
    print("\nSample data:")
    print(df.head())
    print(f"\nColumns: {list(df.columns)}")
    print(f"Journey types: {df['journey_type'].unique() if 'journey_type' in df.columns else 'N/A'}")
    
    print("\nDone.")

if __name__ == "__main__":
    main()
