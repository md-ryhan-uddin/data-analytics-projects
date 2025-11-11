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
DB_NAME = os.getenv('DB_NAME', 'students_mental_health_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_PORT = os.getenv('DB_PORT', '5432')

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
    """Load students CSV file to PostgreSQL database"""
    engine = create_connection()
    
    print(f"Loading data/students.csv to table 'students'...")
    
    # Read CSV
    df = pd.read_csv('data/students.csv')
    
    # Load to PostgreSQL
    df.to_sql('students', engine, if_exists='replace', index=False)
    
    print(f"✅ Successfully loaded {len(df)} rows to 'students' table")
    print(f"\nColumns: {', '.join(df.columns.tolist())}")
    print(f"\n🎉 Data loading complete!")

if __name__ == "__main__":
    load_csv_to_db()
