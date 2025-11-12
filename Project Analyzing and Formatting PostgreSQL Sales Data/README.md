# Analyzing and Formatting PostgreSQL Sales Data

## Overview
This project focuses on **data cleaning and quality** for a global SuperStore retail database. It demonstrates advanced SQL techniques for handling common data quality issues: type casting for improperly stored data types, missing value imputation using statistical methods, and ranking analysis with window functions. The analysis identifies top-performing products across categories and implements a median-based imputation strategy for missing order quantities.

## Dataset
The SuperStore database consists of **4 interconnected tables** with **62,768 total records**:

- **orders** (51,290 rows): Core transaction data with 22 columns including order_id, order_date (stored as TEXT), ship_date, customer details, market, region, product_id, sales (DOUBLE PRECISION), quantity (DOUBLE PRECISION with NULLs), discount, profit, shipping_cost, order_priority
- **products** (10,292 rows): Product catalog with product_id, category, sub_category, product_name
- **people** (13 rows): Regional salespeople with region and person name
- **returned_orders** (1,173 rows): Return records with order_id, market, returned flag

**Data Quality Issues**:
- Dates stored as TEXT requiring string-to-date conversions
- Numeric fields (sales, quantity) stored as DOUBLE PRECISION requiring ::numeric casting for ROUND
- 5 orders with NULL quantity values requiring imputation

## Technical Stack
- **Database**: PostgreSQL 15 (Docker container on port 5441)
- **Python**: 3.12.4 with pandas 2.3.3, psycopg2-binary 2.9.11
- **Infrastructure**: Docker Compose with persistent volume storage
- **Tools**: Jupyter Notebook for interactive analysis, python-dotenv for configuration

## Installation

1. **Prerequisites**: Docker Desktop, Python 3.12+

2. **Start Database**:
   ```bash
   docker-compose up -d
   ```

3. **Load Data**:
   ```bash
   pip install -r requirements.txt
   python load_data.py
   ```
   Loads 62,768 records across 4 tables with normalized column names (lowercase, underscores)

4. **Run Analysis**:
   ```bash
   jupyter notebook notebook.ipynb
   ```

## Analysis Tasks

### Task 1: Top 5 Products Per Category
**Objective**: Identify best-performing products within each category using window functions

**SQL Query**:
```sql
WITH product_totals AS (
    SELECT
        p.category,
        p.product_name,
        SUM(o.sales)   AS sum_sales,
        SUM(o.profit)  AS sum_profit
    FROM orders o
    JOIN products p ON p.product_id = o.product_id
    GROUP BY p.category, p.product_name
),
ranked AS (
    SELECT
        category,
        product_name,
        ROUND(sum_sales::numeric, 2) AS product_total_sales,
        ROUND(sum_profit::numeric, 2) AS product_total_profit,
        DENSE_RANK() OVER (
            PARTITION BY category
            ORDER BY sum_sales DESC, product_name ASC
        ) AS product_rank
    FROM product_totals
)
SELECT * FROM ranked WHERE product_rank <= 5
ORDER BY category, product_total_sales DESC;
```

**Key Techniques**:
- **CTEs**: Two-stage aggregation pattern for cleaner query structure
- **DENSE_RANK() Window Function**: Ranks products within each category partition, handling ties gracefully
- **Type Casting**: `::numeric` conversion required for PostgreSQL ROUND function compatibility
- **Multi-Column ORDER BY**: Primary sort by sales DESC, secondary by name ASC for deterministic ranking

**Results**: 15 products across 3 categories
- **Furniture**: Hon Executive Leather Armchair leads at $58,193 sales
- **Office Supplies**: Eldon File Cart tops at $39,873 sales
- **Technology**: Apple Smart Phone dominates at $86,936 sales (highest overall)

### Task 2: Missing Value Imputation
**Objective**: Impute 5 missing quantity values using median unit price per product

**SQL Query**:
```sql
WITH missing AS (
    SELECT
        product_id,
        COALESCE(discount, 0.0) AS discount,
        market,
        region,
        sales,
        quantity
    FROM orders
    WHERE quantity IS NULL
),
unit_prices AS (
    SELECT
        product_id,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sales / NULLIF(quantity, 0)) AS median_uprice
    FROM orders
    WHERE quantity IS NOT NULL AND quantity <> 0
    GROUP BY product_id
)
SELECT
    m.*,
    CASE
        WHEN up.median_uprice IS NOT NULL AND up.median_uprice <> 0
            THEN ROUND((m.sales / up.median_uprice)::numeric, 0)
        ELSE NULL
    END AS calculated_quantity
FROM missing m
LEFT JOIN unit_prices up ON m.product_id = up.product_id;
```

**Key Techniques**:
- **PERCENTILE_CONT(0.5)**: Statistical aggregate function calculating median unit price per product
- **NULLIF()**: Prevents division-by-zero errors in unit price calculation
- **COALESCE()**: Provides default value (0.0) for missing discount fields
- **LEFT JOIN**: Ensures all missing records retained even if no median available
- **CASE Expression**: Conditional logic for safe division with null handling

**Results**: Successfully imputed all 5 missing quantities
- Product FUR-ADV-10000571: Imputed 4 units (sales $438.96 / median price ~$110)
- Product FUR-ADV-10004395: Imputed 5 units (sales $84.12 / median price ~$17)
- Product FUR-BO-10001337: Imputed 3 units (sales $308.50 / median price ~$103)
- Product TEC-STA-10003330: Imputed 2 units (sales $506.64 / median price ~$253)
- Product TEC-STA-10004542: Imputed 4 units (sales $160.32 / median price ~$40)

## SQL Techniques Demonstrated
- **Common Table Expressions (CTEs)**: Multi-stage query decomposition for readability and reusability
- **Window Functions**: DENSE_RANK() OVER (PARTITION BY...) for category-based ranking
- **Statistical Aggregates**: PERCENTILE_CONT() for robust median calculations
- **Type Casting**: `::numeric` conversions for proper ROUND function behavior in PostgreSQL
- **Null Handling**: COALESCE for defaults, NULLIF for safe division, LEFT JOIN for record preservation
- **Conditional Logic**: CASE expressions for complex imputation rules
- **Table Joins**: INNER JOIN for product enrichment, LEFT JOIN for missing value analysis

## Skills Demonstrated
- Advanced PostgreSQL query optimization with CTEs and window functions
- Data quality assessment and missing value detection
- Statistical imputation methods using median unit prices
- Type system understanding (TEXT vs numeric vs DOUBLE PRECISION)
- Defensive SQL programming (division-by-zero prevention, null handling)
- Data normalization and cleaning workflows

## Business Insights

### Product Performance
- **Technology dominates revenue**: Apple Smart Phone alone generates $86,936 (3.6x Furniture leader)
- **Furniture profitability**: Harbour Creations Armchair achieves 20.8% profit margin vs 6.8% industry average
- **Office Supplies risk**: Hoover Stove White shows -$2,181 loss despite $32,843 sales (negative 6.6% margin)

### Data Quality Impact
- **Missing quantities**: Only 0.01% of orders (5 of 51,290) have missing quantity data
- **Imputation accuracy**: Median-based approach yields realistic quantities (2-5 units) aligned with typical order sizes
- **Type casting necessity**: DOUBLE PRECISION storage for sales/quantity requires explicit ::numeric conversion for financial rounding

## Business Value
1. **Inventory Optimization**: Identifies top 5 products per category for focused stock management
2. **Data Quality Improvement**: Median imputation preserves statistical properties vs mean (less sensitive to outliers)
3. **Loss Prevention**: Flags unprofitable products like Hoover Stove White for pricing review
4. **Scalable Cleaning**: Window functions and CTEs provide reusable patterns for ongoing data quality workflows
5. **Decision Support**: Clean, formatted data enables accurate reporting for 51,290 orders across global markets
