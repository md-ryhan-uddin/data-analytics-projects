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

# Load branch
df_branch = pd.read_csv('data/branch.csv')
df_branch.columns = df_branch.columns.str.lower().str.replace(' ', '_')
df_branch.to_sql('branch', engine, if_exists='replace', index=False)
print(f"✓ branch: {len(df_branch)} rows")
print(f"  Columns: {', '.join(df_branch.columns)}")

# Load request
df_request = pd.read_csv('data/request.csv')
df_request.columns = df_request.columns.str.lower().str.replace(' ', '_')
df_request.to_sql('request', engine, if_exists='replace', index=False)
print(f"✓ request: {len(df_request)} rows")
print(f"  Columns: {', '.join(df_request.columns)}")

# Load service
df_service = pd.read_csv('data/service.csv')
df_service.columns = df_service.columns.str.lower().str.replace(' ', '_')
df_service.to_sql('service', engine, if_exists='replace', index=False)
print(f"✓ service: {len(df_service)} rows")
print(f"  Columns: {', '.join(df_service.columns)}")

print(f"\nTotal records loaded: {len(df_branch) + len(df_request) + len(df_service)}")
print("\nSample data from branch:")
print(df_branch.head(3))
