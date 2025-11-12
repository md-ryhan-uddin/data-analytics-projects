# Analyzing Motorcycle Part Sales

![Parked motorcycle](motorcycle.jpg)

## Overview

This project analyzes sales data for a motorcycle parts company operating three warehouses across a region. The analysis focuses on calculating net revenue for wholesale orders, accounting for different payment method fees, and examining revenue patterns across product lines, months, and warehouse locations.

The company serves both retail and wholesale customers, offering six major product lines (Frame & Body, Suspension & Traction, Braking System, Electrical System, Engine, and Miscellaneous parts). With payment methods including credit cards (3% fee), bank transfers (1% fee), and cash (0% fee), understanding net revenue after payment processing fees is critical for accurate profitability assessment.

## Dataset Description

### sales table
- **order_number**: Unique order identifier (VARCHAR)
- **date**: Date of the order, June-August 2021 (DATE)
- **warehouse**: Order fulfillment location - North, Central, or West (VARCHAR)
- **client_type**: Customer segment - Retail or Wholesale (VARCHAR)
- **product_line**: Type of motorcycle part ordered (VARCHAR)
- **quantity**: Number of products in the order (INT)
- **unit_price**: Price per individual product in dollars (FLOAT)
- **total**: Total order value in dollars (FLOAT)
- **payment**: Payment method - Credit card, Transfer, or Cash (VARCHAR)
- **payment_fee**: Processing fee as percentage of total (FLOAT) - 0.00 (Cash), 0.01 (Transfer), 0.03 (Credit card)
- **Total records**: 1,000 orders (225 wholesale, 775 retail)

## Technical Stack

- **Database**: PostgreSQL 15-alpine (Docker container)
- **Data Loading**: Python 3.12+ with pandas, SQLAlchemy, psycopg2
- **Analysis**: Jupyter Notebook with pandas for SQL query execution
- **Environment**: Docker Compose for containerized PostgreSQL
- **Libraries**: pandas>=2.0.0, psycopg2-binary>=2.9.11, python-dotenv>=1.0.0, sqlalchemy>=2.0.0

## Installation & Setup

1. **Start PostgreSQL container:**
   ```bash
   cd "Project Analyzing Motorcycle Part Sales"
   docker-compose up -d
   ```

2. **Configure environment:**
   - Database runs on `localhost:5440`
   - Database name: `motorcycle_sales_db`
   - Credentials configured in `.env` file

3. **Load data:**
   ```bash
   python load_data.py
   ```
   This loads sales.csv (1,000 orders) into PostgreSQL with normalized column names.

4. **Run analysis:**
   Open `notebook.ipynb` in Jupyter and execute all cells to perform net revenue analysis.

## Analysis Task: Wholesale Net Revenue by Product Line, Month, and Warehouse

Calculate net revenue (total sales minus payment processing fees) for wholesale orders, grouped by product line, month, and warehouse:

```sql
SELECT
    product_line,
    CASE EXTRACT(MONTH FROM date)
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
    END AS month,
    warehouse,
    ROUND(CAST(SUM(total) - SUM(total * payment_fee) AS NUMERIC), 2) AS net_revenue
FROM sales
WHERE client_type = 'Wholesale'
GROUP BY
    product_line,
    EXTRACT(MONTH FROM date),
    warehouse
ORDER BY
    product_line,
    EXTRACT(MONTH FROM date),
    net_revenue DESC;
```

### Key Findings

**Wholesale Revenue Overview:**
- **Total wholesale orders**: 225 orders (22.5% of all orders)
- **Total wholesale revenue**: $159,642.33 (55.2% of total company revenue)
- **Total net revenue** (after payment fees): ~$158,045.91
- **Average payment fee impact**: ~$1,596.42 (1.0% reduction)

**Top Product Lines by Net Revenue (Wholesale):**
1. **Frame & Body**: $39,083.11 net revenue (38 orders) - Highest revenue per order
2. **Suspension & Traction**: $37,912.32 net revenue (51 orders) - Most orders
3. **Braking System**: $22,899.59 net revenue (55 orders) - Second most orders
4. **Electrical System**: $21,536.87 net revenue (38 orders)
5. **Engine**: $21,023.69 net revenue (13 orders) - Highest revenue per order ($1,617)
6. **Miscellaneous**: $15,590.33 net revenue (30 orders)

**Warehouse Distribution (48 product-month-warehouse combinations):**
- Net revenue distributed across **3 warehouses** (North, Central, West)
- Revenue varies by **3 months** (June, July, August 2021)
- Each product line analyzed across **6 dimensions** (6 products × 3 months × 3 warehouses = 54 possible combinations)

**Payment Fee Impact:**
- Wholesale customers prefer **Transfer** payments (1% fee) and **Cash** (0% fee)
- Credit card usage (3% fee) less common in wholesale segment
- Payment fee deductions average **1% of gross revenue**, preserving 99% as net revenue

## SQL Techniques Demonstrated

- **CASE Expressions**: Converting month numbers to readable names using EXTRACT(MONTH FROM date)
- **Date Functions**: EXTRACT() to parse month from DATE column
- **Aggregate Functions**: SUM() for calculating totals across orders
- **Mathematical Operations**: Subtracting payment fees (total - total * payment_fee) for net revenue
- **Type Casting**: CAST(... AS NUMERIC) for precise decimal calculations with ROUND
- **WHERE Filtering**: Isolating wholesale orders with client_type = 'Wholesale'
- **GROUP BY Clauses**: Multi-dimensional grouping by product_line, month, and warehouse
- **ORDER BY**: Sorting results by product line, chronological month, and descending net revenue

## Skills Demonstrated

✅ **Net Revenue Calculation**: Accounting for variable payment processing fees  
✅ **Multi-Dimensional Analysis**: Grouping by product, time period, and location  
✅ **Date Manipulation**: Extracting and formatting month data from DATE fields  
✅ **Business Profitability Analysis**: Understanding impact of payment methods on margins  
✅ **CASE Logic**: Implementing conditional transformations for readable output  
✅ **Aggregate Query Optimization**: Efficient GROUP BY with multiple dimensions  
✅ **Docker Containerization**: PostgreSQL deployment with Docker Compose  
✅ **ETL Pipeline**: Automated data loading with pandas and SQLAlchemy  

## Key Business Insights

1. **Wholesale Dominance**: Despite representing only 22.5% of orders (225/1,000), wholesale sales generate 55.2% of total revenue ($159,642 vs $129,471 retail), indicating higher average order values in the wholesale segment.

2. **Frame & Body Leadership**: Frame & Body parts lead wholesale net revenue at $39,083 (38 orders), averaging $1,028 per order, making them the most valuable wholesale product line.

3. **Engine Parts Premium**: Engine parts have the highest revenue per order ($1,617 from 13 orders totaling $21,024), suggesting these are high-value specialized components with lower order frequency but premium pricing.

4. **Minimal Payment Fee Impact**: Payment processing fees reduce gross revenue by only 1.0% ($1,596 on $159,642), indicating wholesale customers predominantly use low-fee payment methods (Transfer at 1% or Cash at 0%) rather than credit cards (3% fee).

5. **Balanced Warehouse Distribution**: With 48 product-month-warehouse combinations generating revenue, the analysis reveals balanced distribution across all three warehouses (North, Central, West), suggesting effective geographic market coverage without over-reliance on a single location.

6. **Seasonal Consistency**: The 3-month period (June-August 2021) shows consistent wholesale ordering patterns across all product lines, indicating stable B2B relationships without major seasonal fluctuations during summer months.

## Business Value

This analysis provides valuable insights for:
- **Financial Planning**: Accurate net revenue calculations accounting for payment processing costs
- **Product Strategy**: Identifying high-value wholesale product lines (Frame & Body, Suspension & Traction)
- **Warehouse Optimization**: Understanding revenue distribution across three warehouse locations
- **Payment Terms Negotiation**: Quantifying the cost impact of different payment methods
- **Inventory Management**: Prioritizing stock levels for high-revenue wholesale products
- **Sales Forecasting**: Establishing baseline monthly revenue patterns by product line and location
- **Margin Analysis**: Measuring true profitability after payment processing fees

---

**Note**: The dataset contains 1,000 orders from June-August 2021, with wholesale orders ($159,642 revenue) outperforming retail orders ($129,471 revenue) despite fewer transactions, demonstrating the strategic importance of the wholesale segment. Payment processing fees average 1% of wholesale revenue, a relatively low friction cost that preserves 99% of gross sales as net revenue.
