import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5441"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "superstore_db")

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
    
    # Load all CSV files
    csv_files = {
        'orders': 'orders.csv',
        'products': 'products.csv',
        'people': 'people.csv',
        'returned_orders': 'returned_orders.csv'
    }
    
    for table_name, csv_file in csv_files.items():
        csv_path = os.path.join("data", csv_file)
        print(f"→ Loading {csv_path} -> {table_name} table")
        
        df = pd.read_csv(csv_path)
        
        # Normalize column names to lowercase with underscores
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        # Load to PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"   {len(df):,} rows written to {table_name} table")
        print(f"   Columns: {list(df.columns)}")
    
    # Display summary
    print("\n=== Database Summary ===")
    print(f"Total tables loaded: {len(csv_files)}")
    
    # Show sample data from orders
    print("\nSample from orders table:")
    df_orders = pd.read_sql("SELECT * FROM orders LIMIT 3", engine)
    print(df_orders)
    
    print("\nDone.")

if __name__ == "__main__":
    main()
