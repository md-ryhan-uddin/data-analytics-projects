# Grocery Store Sales - Data Analyst Practical Exam

A comprehensive data cleaning and analysis project for FoodYum, a US-based grocery store chain. This project demonstrates essential data analyst skills including missing value imputation, data standardization, and SQL analytics for product pricing strategy across multiple categories.

## 📊 Project Overview

FoodYum sells produce, meat, dairy, baked goods, snacks, and household food staples across the United States. As food costs rise, the company needs to ensure they stock products across all categories covering a range of prices to serve customers with diverse budgets.

**Key Objectives:**
- Clean and validate product data with proper missing value handling
- Identify data quality issues (missing year_added values from 2022 bug)
- Analyze price ranges across product categories
- Focus analysis on high-demand meat and dairy products

## 🗃️ Dataset Description

The `products` table contains **1,700 grocery product records** with 8 attributes:

| Column Name | Data Type | Description | Missing Value Strategy |
|-------------|-----------|-------------|----------------------|
| `product_id` | INTEGER | Unique product identifier (PRIMARY KEY) | Not possible due to DB structure |
| `product_type` | TEXT | Product category: Produce, Meat, Dairy, Bakery, Snacks | Replace with "Unknown" |
| `brand` | TEXT | Product brand (7 possible values) | Replace with "Unknown" |
| `weight` | TEXT | Product weight in grams (with units as text) | Replace with median weight |
| `price` | NUMERIC | Sale price in USD | Replace with median price |
| `average_units_sold` | INTEGER | Average monthly units sold | Replace with 0 |
| `year_added` | TEXT | Year product added to stock | Replace with 2022 |
| `stock_location` | TEXT | Warehouse location: A, B, C, or D | Replace with "Unknown" |

**Data Quality Issues:**
- **170 products** (10%) have missing `year_added` values due to 2022 system bug
- Weight values stored as text with mixed formats ("602.61 grams", "478.26", etc.)
- Various NULL and invalid values requiring cleaning

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
cd "Project Data Analyst Associate Practical Exam Grocery Store Sales"
```

2. **Configure environment variables**:
The `.env` file contains database credentials:
```env
DB_HOST=localhost
DB_PORT=5437
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=grocery_sales_db
```

3. **Start PostgreSQL Docker container**:
```bash
docker-compose up -d
```

4. **Load grocery data**:
```bash
python load_data.py
```

5. **Open and run the Jupyter notebook**:
```bash
jupyter notebook notebook.ipynb
```

## 📁 Project Structure

```
Project Data Analyst Associate Practical Exam Grocery Store Sales/
├── data/                              # Dataset directory (gitignored)
│   └── products.csv                   # 1,700 product records
├── notebook.ipynb                     # Analysis and data cleaning tasks
├── load_data.py                       # Data loading script
├── docker-compose.yml                 # Database container config
├── .env                              # Environment variables (not tracked)
└── README.md                         # This file
```

## 🔍 Analysis Tasks

### Task 1: Identify Missing Year Values

**Challenge**: Quantify the impact of the 2022 system bug on data completeness.

**SQL Query**:
```sql
SELECT COUNT(*) AS missing_year
FROM products
WHERE year_added IS NULL;
```

**Result**: **170 products** affected by the bug

### Task 2: Comprehensive Data Cleaning

**Challenge**: Clean entire dataset according to business rules for missing values.

**SQL Implementation**:
```sql
SELECT
    product_id,
    
    -- Standardize product_type to proper case
    CASE
        WHEN TRIM(LOWER(product_type)) IN ('produce') THEN 'Produce'
        WHEN TRIM(LOWER(product_type)) IN ('meat') THEN 'Meat'
        WHEN TRIM(LOWER(product_type)) IN ('dairy') THEN 'Dairy'
        WHEN TRIM(LOWER(product_type)) IN ('bakery') THEN 'Bakery'
        WHEN TRIM(LOWER(product_type)) IN ('snacks') THEN 'Snacks'
        ELSE 'Unknown'
    END AS product_type,
    
    -- Handle missing brands
    CASE
        WHEN TRIM(LOWER(brand)) IN ('', '-', 'missing') OR brand IS NULL 
            THEN 'Unknown'
        ELSE TRIM(brand)
    END AS brand,
    
    -- Extract numeric weight and impute with median
    ROUND((
        COALESCE(
            NULLIF(REGEXP_REPLACE(weight, '[^0-9\.]', '', 'g'), '')::NUMERIC,
            (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (
                ORDER BY NULLIF(REGEXP_REPLACE(weight, '[^0-9\.]', '', 'g'), '')::NUMERIC
            ) FROM products
             WHERE NULLIF(REGEXP_REPLACE(weight, '[^0-9\.]', '', 'g'), '') IS NOT NULL)
        )
    )::NUMERIC, 2) AS weight,
    
    -- Impute missing prices with median
    ROUND((
        COALESCE(
            price,
            (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)
             FROM products WHERE price IS NOT NULL)
        )
    )::NUMERIC, 2) AS price,
    
    -- Replace NULL units sold with 0
    COALESCE(average_units_sold, 0) AS average_units_sold,
    
    -- Fix missing year_added with 2022
    COALESCE(year_added, '2022') AS year_added,
    
    -- Standardize warehouse locations
    CASE
        WHEN TRIM(LOWER(stock_location)) IN ('a','b','c','d') 
            THEN UPPER(TRIM(stock_location))
        ELSE 'Unknown'
    END AS stock_location
    
FROM products;
```

**Key Techniques**:
- `REGEXP_REPLACE()` for text parsing (remove non-numeric from weight)
- `PERCENTILE_CONT()` for median calculation
- `COALESCE()` for NULL handling
- `CASE` statements for conditional logic
- Nested subqueries for aggregate calculations

### Task 3: Price Range Analysis by Category

**Challenge**: Understand price diversity within each product category.

**SQL Query**:
```sql
SELECT 
    COALESCE(product_type, 'Unknown') AS product_type,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products
GROUP BY COALESCE(product_type, 'Unknown');
```

**Business Value**: Identifies whether each category offers products across price points

### Task 4: High-Demand Meat & Dairy Analysis

**Challenge**: Focus on popular meat and dairy products for inventory optimization.

**SQL Query**:
```sql
SELECT 
    product_id, 
    price, 
    average_units_sold
FROM products
WHERE 
    product_type IN ('Meat', 'Dairy')
    AND average_units_sold > 10;
```

**Business Value**: Targets high-velocity products for pricing and stock strategies

## 📈 SQL & Data Analysis Skills Demonstrated

- ✅ **Missing Value Analysis**: Quantifying data quality issues
- ✅ **Complex Data Cleaning**: Multi-step CASE statements for standardization
- ✅ **Text Processing**: REGEXP_REPLACE for pattern extraction
- ✅ **Statistical Functions**: PERCENTILE_CONT for median imputation
- ✅ **Aggregate Analysis**: MIN/MAX/GROUP BY for category insights
- ✅ **Filtering**: Multi-condition WHERE clauses for targeted analysis
- ✅ **NULL Handling**: COALESCE for robust default values
- ✅ **Data Type Conversion**: CAST and :: operators

## 🎯 Key Findings

### Data Quality:
- **10% of products** missing year_added (2022 bug impact)
- Weight data requires text parsing before numeric analysis
- Multiple missing value patterns requiring different strategies

### Business Insights:
- Price ranges vary significantly across categories
- Meat and dairy categories have distinct high-demand products
- Warehouse distribution (A, B, C, D) affects stock location patterns

## 📚 Business Value

- **For Pricing Strategy**: Understand price positioning across categories
- **For Inventory Management**: Identify high-demand products by category
- **For Data Quality**: Document and fix systematic data issues
- **For Customer Service**: Ensure product range meets diverse budget needs
- **For Operations**: Optimize warehouse allocation based on product analysis

## 💡 Data Cleaning Best Practices

1. **Document Data Issues**: Track bugs like the 2022 year_added problem
2. **Use Statistical Imputation**: Median for continuous variables (weight, price)
3. **Business-Driven Defaults**: 2022 for missing years, 0 for missing sales
4. **Standardization**: Consistent casing and formats (Produce vs produce)
5. **Text Processing**: Handle mixed formats in text-stored numeric data

---

*Part of my data analyst portfolio showcasing PostgreSQL, data cleaning, statistical imputation, and SQL analytics.*
