# Evaluate a Manufacturing Process

A statistical process control (SPC) project using PostgreSQL window functions to monitor and analyze manufacturing quality. This project implements data-driven quality control to identify when manufacturing processes fall outside acceptable ranges and require adjustment.

![Manufacturing Gears](manufacturing.jpg)
*Implementing statistical process control for manufacturing quality*

## 📊 Project Overview

This project supports a manufacturing team implementing **Statistical Process Control (SPC)** - an established strategy that uses statistical methods to monitor and control manufacturing processes. The analysis determines whether parts fall within acceptable quality ranges defined by Upper Control Limits (UCL) and Lower Control Limits (LCL).

**Key Objectives:**
- Monitor manufacturing process quality using historical data
- Calculate control limits for acceptable part dimensions
- Identify measurements that fall outside control limits (alerts)
- Enable data-driven process adjustments for consistent quality

## 🗃️ Dataset Description

Two CSV datasets with **500 manufacturing measurements** each:

### `manufacturing_parts.csv`
Main production data table:
- **index**: Record index
- **item_no**: Unique item number
- **length**: Part length measurement
- **width**: Part width measurement  
- **height**: Part height measurement
- **operator**: Operating machine identifier (Op-1, Op-2, etc.)

### `parts.csv`
Reference parts specification table with same structure for validation

## 📐 Statistical Process Control Methodology

### Control Limit Formulas

The acceptable range is defined using statistical formulas:

**Upper Control Limit (UCL)**:
$$UCL = avg\\_height + 3 \times \frac{stddev\\_height}{\sqrt{5}}$$

**Lower Control Limit (LCL)**:
$$LCL = avg\\_height - 3 \times \frac{stddev\\_height}{\sqrt{5}}$$

### Quality Assessment
- **In Control**: Parts with measurements between LCL and UCL
- **Out of Control** (Alert): Parts exceeding UCL or below LCL require process adjustment
- **Rolling Window**: Uses 5-measurement windows for statistical stability

## 🛠️ Technical Stack

- **Database**: PostgreSQL (Docker container)
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
cd "Project Evaluate a Manufacturing Process"
```

2. **Configure environment variables**:
The `.env` file contains database credentials:
```env
DB_HOST=localhost
DB_PORT=5434
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=manufacturing_db
```

3. **Start PostgreSQL Docker container**:
```bash
docker-compose up -d
```

4. **Load manufacturing data**:
```bash
python load_data.py
```

5. **Open and run the Jupyter notebook**:
```bash
jupyter notebook notebook.ipynb
```

## 📁 Project Structure

```
Project Evaluate a Manufacturing Process/
├── data/                              # CSV datasets (gitignored)
│   ├── manufacturing_parts.csv        # Main production data (500 parts)
│   └── parts.csv                      # Reference specifications
├── notebook.ipynb                     # SPC analysis notebook
├── load_data.py                       # Data loading script
├── docker-compose.yml                 # Database container
├── manufacturing.jpg                  # Project illustration
├── .env                              # Environment variables (not tracked)
└── README.md                         # This file
```

## 🔍 Analysis Highlights

### SQL Window Functions Used

The analysis leverages advanced PostgreSQL window functions:

```sql
WITH stats AS (
    SELECT
        operator,
        item_no,
        height,
        ROW_NUMBER() OVER (PARTITION BY operator ORDER BY item_no),
        AVG(height) OVER (
            PARTITION BY operator
            ORDER BY item_no
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) AS avg_height,
        STDDEV(height) OVER (
            PARTITION BY operator
            ORDER BY item_no
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) AS stddev_height
    FROM manufacturing_parts
)
SELECT
    operator,
    height,
    avg_height,
    (avg_height + 3 * stddev_height) AS ucl,
    (avg_height - 3 * stddev_height) AS lcl,
    CASE
        WHEN height > (avg_height + 3 * stddev_height)
          OR height < (avg_height - 3 * stddev_height)
        THEN TRUE ELSE FALSE
    END AS alert
FROM stats
WHERE window_count = 5
ORDER BY item_no;
```

### Key Features

1. **Window Functions**: 
   - `ROW_NUMBER()` for sequential numbering
   - `AVG()` for rolling average calculations
   - `STDDEV()` for rolling standard deviation
   - `ROWS BETWEEN` for 5-measurement windows

2. **Statistical Calculations**:
   - Rolling averages using 5-measurement windows
   - Standard deviation for process variability
   - Dynamic UCL/LCL calculation per window

3. **Alert System**:
   - CASE statement for out-of-control detection
   - Boolean alerts for immediate identification
   - Operator-specific monitoring

### Analysis Insights

- **Process Stability**: Identifies when manufacturing drift occurs
- **Operator Performance**: Compares quality across different operators
- **Preventive Action**: Flags issues before major quality problems
- **Continuous Improvement**: Provides data for process optimization

## 📈 SQL Techniques Demonstrated

- ✅ **Window Functions**: Advanced partitioning and ordering
- ✅ **Rolling Calculations**: ROWS BETWEEN for moving windows
- ✅ **Statistical Functions**: AVG(), STDDEV(), COUNT()
- ✅ **Common Table Expressions (CTEs)**: Complex query organization
- ✅ **Conditional Logic**: CASE statements for business rules
- ✅ **Subqueries**: Nested SELECT statements
- ✅ **Partitioning**: PARTITION BY for operator-level analysis

## 🎯 Key Takeaways

This project demonstrates:
- ✅ **Statistical Process Control** implementation using SQL
- ✅ **Quality Management** through data-driven insights
- ✅ **Advanced Window Functions** for rolling statistics
- ✅ **Manufacturing Analytics** for process improvement
- ✅ **PostgreSQL Proficiency** with complex analytical queries

## 📚 Business Value

- **Quality Assurance**: Early detection of manufacturing issues
- **Cost Reduction**: Minimize defects and waste
- **Process Optimization**: Data-driven improvement decisions
- **Regulatory Compliance**: Documented quality control methodology
- **Predictive Maintenance**: Identify equipment drift before failure

---

*Part of my data analytics portfolio showcasing PostgreSQL, SQL window functions, and statistical process control.*
