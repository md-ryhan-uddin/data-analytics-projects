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

def load_lending_data():
    """Load loan insights data into PostgreSQL."""
    
    # Connect to database
    conn = connect_with_retry()
    cur = conn.cursor()
    
    try:
        # Read CSV files
        df_client = pd.read_csv('data/client.csv')
        df_contract = pd.read_csv('data/contract.csv')
        df_loan = pd.read_csv('data/loan.csv')
        df_repayment = pd.read_csv('data/repayment.csv')
        
        print(f"\n📊 Data loaded:")
        print(f"   - client.csv: {len(df_client)} rows")
        print(f"   - contract.csv: {len(df_contract)} rows")
        print(f"   - loan.csv: {len(df_loan)} rows")
        print(f"   - repayment.csv: {len(df_repayment)} rows")
        
        # Drop tables if they exist (in correct order due to foreign keys)
        cur.execute("DROP TABLE IF EXISTS repayment CASCADE;")
        cur.execute("DROP TABLE IF EXISTS loan CASCADE;")
        cur.execute("DROP TABLE IF EXISTS contract CASCADE;")
        cur.execute("DROP TABLE IF EXISTS client CASCADE;")
        
        # Create client table
        cur.execute("""
        CREATE TABLE client (
            client_id INTEGER PRIMARY KEY,
            date_of_birth TEXT,
            employment_status TEXT,
            country TEXT
        );
        """)
        print("✅ Created client table")
        
        # Create contract table
        cur.execute("""
        CREATE TABLE contract (
            contract_id INTEGER PRIMARY KEY,
            contract_date TEXT
        );
        """)
        print("✅ Created contract table")
        
        # Create loan table
        cur.execute("""
        CREATE TABLE loan (
            loan_id INTEGER PRIMARY KEY,
            client_id INTEGER REFERENCES client(client_id),
            contract_id INTEGER REFERENCES contract(contract_id),
            principal_amount NUMERIC,
            interest_rate NUMERIC,
            loan_type TEXT
        );
        """)
        print("✅ Created loan table")
        
        # Create repayment table
        cur.execute("""
        CREATE TABLE repayment (
            repayment_id INTEGER PRIMARY KEY,
            loan_id INTEGER REFERENCES loan(loan_id),
            repayment_date TEXT,
            repayment_amount NUMERIC,
            repayment_channel TEXT
        );
        """)
        print("✅ Created repayment table")
        
        # Insert client data
        for _, row in df_client.iterrows():
            cur.execute("""
                INSERT INTO client (client_id, date_of_birth, employment_status, country)
                VALUES (%s, %s, %s, %s)
            """, (int(row['client_id']), row['date_of_birth'], row['employment_status'], row['country']))
        
        # Insert contract data
        for _, row in df_contract.iterrows():
            cur.execute("""
                INSERT INTO contract (contract_id, contract_date)
                VALUES (%s, %s)
            """, (int(row['contract_id']), row['contract_date']))
        
        # Insert loan data
        for _, row in df_loan.iterrows():
            cur.execute("""
                INSERT INTO loan (loan_id, client_id, contract_id, principal_amount, interest_rate, loan_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (int(row['loan_id']), int(row['client_id']), int(row['contract_id']), 
                  float(row['principal_amount']), float(row['interest_rate']), row['loan_type']))
        
        # Insert repayment data
        for _, row in df_repayment.iterrows():
            cur.execute("""
                INSERT INTO repayment (repayment_id, loan_id, repayment_date, repayment_amount, repayment_channel)
                VALUES (%s, %s, %s, %s, %s)
            """, (int(row['repayment_id']), int(row['loan_id']), row['repayment_date'], 
                  float(row['repayment_amount']), row['repayment_channel']))
        
        conn.commit()
        
        # Verify data
        cur.execute("SELECT COUNT(*) FROM client;")
        print(f"\n✅ Loaded {cur.fetchone()[0]} rows into client table")
        
        cur.execute("SELECT COUNT(*) FROM contract;")
        print(f"✅ Loaded {cur.fetchone()[0]} rows into contract table")
        
        cur.execute("SELECT COUNT(*) FROM loan;")
        print(f"✅ Loaded {cur.fetchone()[0]} rows into loan table")
        
        cur.execute("SELECT COUNT(*) FROM repayment;")
        print(f"✅ Loaded {cur.fetchone()[0]} rows into repayment table")
        
        # Show sample data
        print("\n📋 Sample from client table:")
        cur.execute("SELECT * FROM client LIMIT 3;")
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
    load_lending_data()
