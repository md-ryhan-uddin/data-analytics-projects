import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5440"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "motorcycle_sales_db")

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
    
    # Load sales data
    csv_path = os.path.join("data", "sales.csv")
    print(f"→ Loading {csv_path} -> sales table")
    
    df = pd.read_csv(csv_path)
    
    # Normalize column names to lowercase with underscores
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Convert date columns
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Load to PostgreSQL
    df.to_sql('sales', engine, if_exists='replace', index=False)
    print(f"   {len(df):,} rows written to sales table")
    
    # Display sample data and statistics
    print("\nSample data:")
    print(df.head())
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nClient types: {df['client_type'].unique() if 'client_type' in df.columns else 'N/A'}")
    print(f"Product lines: {df['product_line'].unique() if 'product_line' in df.columns else 'N/A'}")
    print(f"Warehouses: {df['warehouse'].unique() if 'warehouse' in df.columns else 'N/A'}")
    print(f"Payment methods: {df['payment'].unique() if 'payment' in df.columns else 'N/A'}")
    
    # Summary statistics
    if 'total' in df.columns:
        print(f"\nTotal sales: ${df['total'].sum():,.2f}")
    if 'client_type' in df.columns:
        print(f"Wholesale orders: {len(df[df['client_type'] == 'Wholesale'])}")
        print(f"Retail orders: {len(df[df['client_type'] == 'Retail'])}")
    
    print("\nDone.")

if __name__ == "__main__":
    main()
