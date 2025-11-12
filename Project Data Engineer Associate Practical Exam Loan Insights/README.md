# Loan Insights - Data Engineering Practical Exam

A comprehensive data engineering project focused on cleaning, transforming, and analyzing loan data for EasyLoan, a lending company operating across Canada, United Kingdom, and United States. This project demonstrates essential data engineering skills including data validation, imputation, and multi-table joins.

![Lending Schema](lending_schema.png)
*Database schema for the lending system*

## 📊 Project Overview

EasyLoan offers a wide range of loan services including personal loans, car loans, and mortgages across three countries. The analytics team needs clean, reliable data to report performance across different geographic areas and identify business strengths and weaknesses.

**Key Objectives:**
- Clean and validate client data with proper type casting and standardization
- Impute missing repayment channel values based on business rules
- Analyze US market adoption of new online contract system (2022+)
- Compare average interest rates across countries for competitive positioning

## 🗃️ Database Schema

The lending database contains **4 interconnected tables**:

### `client` (300 records)
Client demographic and status information:
- `client_id`: Unique integer identifier (PRIMARY KEY)
- `date_of_birth`: Birth date (TEXT, requires casting to DATE)
- `employment_status`: Employment status (TEXT, needs standardization)
- `country`: Country of residence (TEXT, requires uppercase standardization)

### `contract` (500 records)
Contract signing information:
- `contract_id`: Unique contract identifier (PRIMARY KEY)
- `contract_date`: Date contract was signed (TEXT format)

### `loan` (1,000 records)
Loan details and terms:
- `loan_id`: Unique loan identifier (PRIMARY KEY)
- `client_id`: Foreign key to client table
- `contract_id`: Foreign key to contract table
- `principal_amount`: Loan principal amount (NUMERIC)
- `interest_rate`: Annual interest rate (NUMERIC)
- `loan_type`: Type of loan (car, personal, mortgage)

### `repayment` (1,500 records)
Repayment transaction history:
- `repayment_id`: Unique repayment identifier (PRIMARY KEY)
- `loan_id`: Foreign key to loan table
- `repayment_date`: Date of repayment (TEXT)
- `repayment_amount`: Amount repaid (NUMERIC)
- `repayment_channel`: Payment method (TEXT, has missing values marked as '-')

## 🛠️ Technical Stack

- **Database**: PostgreSQL 15 (Docker container)
- **Languages**: SQL, Python
- **Libraries**: pandas, psycopg2, python-dotenv
- **Environment**: Jupyter Notebook
- **Containerization**: Docker Compose

## 🚀 Getting Started

### Prerequisites
1. Docker and Docker Desktop installed and running
2. Python 3.7+ with pip

### Installation

1. **Navigate to project directory**:
```bash
cd "Project Data Engineer Associate Practical Exam Loan Insights"
```

2. **Configure environment variables**:
The `.env` file contains database credentials:
```env
DB_HOST=localhost
DB_PORT=5436
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=lending
```

3. **Start PostgreSQL Docker container**:
```bash
docker-compose up -d
```

4. **Load lending data**:
```bash
python load_data.py
```

5. **Open and run the Jupyter notebook**:
```bash
jupyter notebook notebook.ipynb
```

## 📁 Project Structure

```
Project Data Engineer Associate Practical Exam Loan Insights/
├── data/                              # CSV datasets (gitignored)
│   ├── client.csv                     # 300 client records
│   ├── contract.csv                   # 500 contracts
│   ├── loan.csv                       # 1,000 loans
│   └── repayment.csv                  # 1,500 repayment transactions
├── notebook.ipynb                     # Analysis and data engineering tasks
├── load_data.py                       # Data loading script
├── docker-compose.yml                 # Database container config
├── lending_schema.png                 # Database ERD
├── .env                              # Environment variables (not tracked)
└── README.md                         # This file
```

## 🔍 Data Engineering Tasks

### Task 1: Client Data Cleaning

**Challenge**: Clean the client table for analytics dashboard usage with proper data types and standardization.

**Requirements**:
- `client_id`: Keep as INTEGER
- `date_of_birth`: Cast TEXT to DATE (invalid values → NULL)
- `employment_status`: Standardize to lowercase 'employed' or 'unemployed' (else NULL)
- `country`: Standardize to uppercase 'USA', 'UK', 'CA' (else NULL)

**SQL Implementation**:
```sql
SELECT
    client_id,
    CAST(date_of_birth AS DATE) AS date_of_birth,
    CASE
        WHEN employment_status ILIKE 'un%' THEN 'unemployed'
        WHEN employment_status ILIKE 'e%' 
          OR employment_status ILIKE 'f%' 
          OR employment_status ILIKE 'p%' THEN 'employed'
        ELSE NULL
    END AS employment_status,
    country
FROM client;
```

**Key Techniques**:
- Type casting with `CAST()`
- Pattern matching with `ILIKE` for case-insensitive comparison
- CASE statements for conditional standardization
- NULL handling for invalid values

### Task 2: Impute Missing Repayment Channels

**Challenge**: Fill missing repayment_channel values (marked as '-') based on business rules.

**Business Rules**:
- Repayments > $4,000 → 'bank account'
- Repayments < $1,000 → 'mail'
- Otherwise → keep existing value

**SQL Implementation**:
```sql
SELECT
    repayment_id,
    loan_id,
    repayment_date,
    repayment_amount,
    CASE
        WHEN repayment_channel = '-' AND repayment_amount > 4000 
            THEN 'bank account'
        WHEN repayment_channel = '-' AND repayment_amount < 1000 
            THEN 'mail'
        ELSE repayment_channel
    END AS repayment_channel
FROM repayment;
```

**Key Techniques**:
- Conditional imputation with CASE statements
- Multi-condition logic with AND operators
- Data quality improvement through business rule application

### Task 3: US Online System Adoption Analysis

**Challenge**: Identify US clients who used the new online contract system (launched January 1, 2022).

**Requirements**:
- Filter for USA clients only
- Contracts dated 2022-01-01 or later
- Return: client_id, contract_date, principal_amount, loan_type

**SQL Implementation**:
```sql
SELECT
    c.client_id,
    ctr.contract_date,
    l.principal_amount,
    l.loan_type
FROM loan AS l
JOIN client AS c ON c.client_id = l.client_id
JOIN contract AS ctr ON ctr.contract_id = l.contract_id
WHERE c.country = 'USA'
  AND CAST(ctr.contract_date AS DATE) >= DATE '2022-01-01';
```

**Result**: **94 loans** from US clients using the online system

**Key Techniques**:
- Multi-table INNER JOINs across 3 tables
- Date comparison with proper type casting
- Geographic filtering for specific market analysis

### Task 4: Competitive Interest Rate Analysis

**Challenge**: Compare average interest rates by loan type across countries to assess competitive positioning.

**Requirements**:
- Group by loan_type and country
- Calculate average interest rate
- Enable country comparison for same loan types

**SQL Implementation**:
```sql
SELECT
    l.loan_type,
    c.country AS country,
    AVG(l.interest_rate) AS avg_rate
FROM loan AS l
JOIN client AS c ON c.client_id = l.client_id
GROUP BY l.loan_type, c.country
ORDER BY l.loan_type, c.country;
```

**Key Techniques**:
- Aggregate functions with `AVG()`
- Multi-column GROUP BY for segmentation
- JOIN operations for cross-table analysis
- Ordered results for easy comparison

## 📈 SQL & Data Engineering Skills Demonstrated

- ✅ **Data Cleaning**: Type casting, standardization, validation
- ✅ **Data Imputation**: Business rule-based missing value filling
- ✅ **Multi-Table Joins**: Complex relationships across 3-4 tables
- ✅ **Aggregate Functions**: AVG(), GROUP BY for statistical analysis
- ✅ **CASE Statements**: Conditional logic for data transformation
- ✅ **Pattern Matching**: ILIKE for flexible string matching
- ✅ **Date Handling**: Type casting and date comparisons
- ✅ **Foreign Key Relationships**: Understanding relational database design
- ✅ **NULL Handling**: Proper treatment of invalid/missing data

## 🎯 Key Insights

### Data Quality Findings:
- **Client Data**: Contains inconsistent employment status formats requiring standardization
- **Repayment Channels**: Missing values follow predictable patterns based on amount
- **Date Fields**: Stored as TEXT, requiring casting for date operations

### Business Insights:
- **US Online Adoption**: 94 loans originated through new online system (post-2022)
- **Multi-Country Operations**: Successfully serving clients in USA, UK, and Canada
- **Loan Portfolio**: Mix of car, personal, and mortgage products
- **Repayment Patterns**: Clear channel preferences based on transaction size

## 📚 Business Value

- **For Analytics Team**: Clean, reliable data ready for dashboard visualization
- **For Strategy Team**: Interest rate comparison data for competitive positioning
- **For Operations**: Understanding of online system adoption rates
- **For Data Engineers**: Reproducible ETL patterns for data quality improvement
- **For Business Leaders**: Market-specific insights for decision making

## 💡 Data Engineering Best Practices

1. **Type Safety**: Explicit type casting prevents runtime errors
2. **Data Validation**: CASE statements ensure only valid values pass through
3. **Business Logic in SQL**: Imputation rules codified directly in queries
4. **Reproducibility**: All transformations documented and version-controlled
5. **Foreign Key Integrity**: Proper JOIN operations respect relational structure

---

*Part of my data engineering portfolio showcasing PostgreSQL, data cleaning, transformation, and multi-table analysis.*
