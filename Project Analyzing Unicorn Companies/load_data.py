import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'unicorns_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_PORT = os.getenv('DB_PORT', '5432')

def create_connection():
    """Create database connection"""
    # URL encode the password to handle special characters
    encoded_password = quote_plus(DB_PASSWORD)
    connection_string = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)
    return engine

def load_csv_to_db():
    """Load all CSV files to PostgreSQL database"""
    engine = create_connection()
    
    # Define CSV files and corresponding table names
    csv_files = {
        'companies': 'data/companies.csv',
        'dates': 'data/dates.csv',
        'funding': 'data/funding.csv',
        'industries': 'data/industries.csv'
    }
    
    for table_name, csv_path in csv_files.items():
        print(f"Loading {csv_path} to table '{table_name}'...")
        
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Load to PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"✅ Successfully loaded {len(df)} rows to '{table_name}' table")
    
    print("\n🎉 All CSV files loaded successfully!")

if __name__ == "__main__":
    load_csv_to_db()
