import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import time

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'manufacturing_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_PORT = os.getenv('DB_PORT', '5434')

def create_connection():
    """Create database connection with retry logic"""
    # URL encode the password to handle special characters
    encoded_password = quote_plus(DB_PASSWORD)
    connection_string = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Retry connection up to 5 times with 2 second delays
    for attempt in range(5):
        try:
            engine = create_engine(connection_string)
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Successfully connected to PostgreSQL database!")
            return engine
        except Exception as e:
            if attempt < 4:
                print(f"⏳ Waiting for database to be ready... (attempt {attempt + 1}/5)")
                time.sleep(2)
            else:
                print(f"❌ Failed to connect to database after 5 attempts: {e}")
                raise

def load_csv_to_db():
    """Load manufacturing CSV files to PostgreSQL database"""
    engine = create_connection()
    
    # Load manufacturing_parts.csv (main table)
    print(f"Loading data/manufacturing_parts.csv to table 'manufacturing_parts'...")
    df_manufacturing = pd.read_csv('data/manufacturing_parts.csv')
    df_manufacturing.to_sql('manufacturing_parts', engine, if_exists='replace', index=False)
    print(f"✅ Successfully loaded {len(df_manufacturing)} rows to 'manufacturing_parts' table")
    
    # Load parts.csv (reference table)
    print(f"\nLoading data/parts.csv to table 'parts'...")
    df_parts = pd.read_csv('data/parts.csv')
    df_parts.to_sql('parts', engine, if_exists='replace', index=False)
    print(f"✅ Successfully loaded {len(df_parts)} rows to 'parts' table")
    
    print(f"\n📊 Manufacturing Parts Columns: {', '.join(df_manufacturing.columns.tolist())}")
    print(f"📊 Parts Columns: {', '.join(df_parts.columns.tolist())}")
    print(f"\n🎉 All data loading complete!")

if __name__ == "__main__":
    load_csv_to_db()
