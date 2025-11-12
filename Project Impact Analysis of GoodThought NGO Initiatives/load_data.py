import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Create database engine
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Load CSV files
print("Loading data...")

# Load assignments
df_assignments = pd.read_csv('data/assignments.csv')
df_assignments.columns = df_assignments.columns.str.lower().str.replace(' ', '_')
df_assignments.to_sql('assignments', engine, if_exists='replace', index=False)
print(f"✓ assignments: {len(df_assignments)} rows")
print(f"  Columns: {', '.join(df_assignments.columns)}")

# Load donars
df_donars = pd.read_csv('data/donars.csv')
df_donars.columns = df_donars.columns.str.lower().str.replace(' ', '_')
df_donars.to_sql('donars', engine, if_exists='replace', index=False)
print(f"✓ donars: {len(df_donars)} rows")
print(f"  Columns: {', '.join(df_donars.columns)}")

# Load donations
df_donations = pd.read_csv('data/donations.csv')
df_donations.columns = df_donations.columns.str.lower().str.replace(' ', '_')
df_donations.to_sql('donations', engine, if_exists='replace', index=False)
print(f"✓ donations: {len(df_donations)} rows")
print(f"  Columns: {', '.join(df_donations.columns)}")

print(f"\nTotal records loaded: {len(df_assignments) + len(df_donars) + len(df_donations)}")
print("\nSample data from assignments:")
print(df_assignments.head(3))
