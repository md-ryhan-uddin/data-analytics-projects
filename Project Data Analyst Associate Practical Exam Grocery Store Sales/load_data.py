import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def connect_with_retry(max_retries=5, delay=2):
    """Attempt to connect to PostgreSQL with retries."""
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            print(f"✅ Successfully connected to database on attempt {attempt + 1}")
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"⏳ Connection attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"❌ Failed to connect after {max_retries} attempts")
                raise e

def load_grocery_sales_data():
    """Load grocery store sales data into PostgreSQL."""
    
    # Connect to database
    conn = connect_with_retry()
    cur = conn.cursor()
    
    try:
        # Read CSV
        df = pd.read_csv('data/products.csv')
        
        print(f"\n📊 Loaded {len(df)} rows from products.csv")
        print(f"📋 Columns: {', '.join(df.columns)}")
        
        # Drop table if exists
        cur.execute("DROP TABLE IF EXISTS products CASCADE;")
        
        # Create table - keep year_added as TEXT since it has NULL values to handle
        create_table_query = """
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_type TEXT,
            brand TEXT,
            weight TEXT,
            price NUMERIC,
            average_units_sold INTEGER,
            year_added TEXT,
            stock_location TEXT
        );
        """
        
        cur.execute(create_table_query)
        print("✅ Created products table")
        
        # Insert data
        for _, row in df.iterrows():
            insert_query = """
            INSERT INTO products (
                product_id, product_type, brand, weight, price,
                average_units_sold, year_added, stock_location
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Handle empty strings as NULL
            year_val = row['year_added'] if pd.notna(row['year_added']) and row['year_added'] != '' else None
            
            cur.execute(insert_query, (
                int(row['product_id']),
                row['product_type'] if pd.notna(row['product_type']) else None,
                row['brand'] if pd.notna(row['brand']) else None,
                row['weight'] if pd.notna(row['weight']) else None,
                float(row['price']) if pd.notna(row['price']) else None,
                int(row['average_units_sold']) if pd.notna(row['average_units_sold']) else None,
                year_val,
                row['stock_location'] if pd.notna(row['stock_location']) else None
            ))
        
        conn.commit()
        
        # Verify data
        cur.execute("SELECT COUNT(*) FROM products;")
        count = cur.fetchone()[0]
        print(f"✅ Loaded {count} rows into products table")
        
        # Show NULL counts
        cur.execute("SELECT COUNT(*) FROM products WHERE year_added IS NULL;")
        null_years = cur.fetchone()[0]
        print(f"ℹ️  Products with NULL year_added: {null_years}")
        
        # Show sample data
        cur.execute("SELECT * FROM products LIMIT 3;")
        print("\n📋 Sample data:")
        for row in cur.fetchall():
            print(row)
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    load_grocery_sales_data()
