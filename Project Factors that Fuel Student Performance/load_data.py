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

def load_student_performance_data():
    """Load student performance data into PostgreSQL."""
    
    # Connect to database
    conn = connect_with_retry()
    cur = conn.cursor()
    
    try:
        # Read CSV
        df = pd.read_csv('data/StudentPerformanceFactors.csv')
        
        # Clean column names (lowercase and snake_case)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        print(f"\n📊 Loaded {len(df)} rows from StudentPerformanceFactors.csv")
        print(f"📋 Columns: {', '.join(df.columns)}")
        
        # Drop table if exists and create new one
        cur.execute("DROP TABLE IF EXISTS student_performance CASCADE;")
        
        # Create table with appropriate data types
        create_table_query = """
        CREATE TABLE student_performance (
            hours_studied INTEGER,
            attendance FLOAT,
            parental_involvement VARCHAR(10),
            access_to_resources VARCHAR(10),
            extracurricular_activities VARCHAR(5),
            sleep_hours FLOAT,
            previous_scores INTEGER,
            motivation_level VARCHAR(10),
            internet_access VARCHAR(5),
            tutoring_sessions INTEGER,
            family_income VARCHAR(10),
            teacher_quality VARCHAR(10),
            school_type VARCHAR(10),
            peer_influence VARCHAR(10),
            physical_activity INTEGER,
            learning_disabilities VARCHAR(5),
            parental_education_level VARCHAR(20),
            distance_from_home VARCHAR(10),
            gender VARCHAR(10),
            exam_score FLOAT
        );
        """
        
        cur.execute(create_table_query)
        print("✅ Created student_performance table")
        
        # Insert data
        for _, row in df.iterrows():
            insert_query = """
            INSERT INTO student_performance (
                hours_studied, attendance, parental_involvement, access_to_resources,
                extracurricular_activities, sleep_hours, previous_scores, motivation_level,
                internet_access, tutoring_sessions, family_income, teacher_quality,
                school_type, peer_influence, physical_activity, learning_disabilities,
                parental_education_level, distance_from_home, gender, exam_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, tuple(row))
        
        conn.commit()
        
        # Verify data
        cur.execute("SELECT COUNT(*) FROM student_performance;")
        count = cur.fetchone()[0]
        print(f"✅ Loaded {count} rows into student_performance table")
        
        # Show sample data
        cur.execute("SELECT * FROM student_performance LIMIT 3;")
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
    load_student_performance_data()
