# Analyzing Unicorn Companies

A comprehensive data analytics project exploring high-growth unicorn companies using PostgreSQL, Python, and data analysis techniques to identify industry trends and investment opportunities.

![Investment Calculator](calculator.jpg)
*Analyzing trends in billion-dollar startups*

## 📊 Project Overview

This project analyzes a dataset of unicorn companies (private companies valued at $1 billion or more) to support an investment firm in making data-driven decisions. The analysis focuses on identifying which industries are producing the highest valuations and the rate at which new high-value companies are emerging during the years 2019-2021.

**Key Research Question:** Which industries have the most unicorns, and what are their average valuations over time?

## 🗃️ Dataset Description

The project includes four CSV datasets:

### `companies.csv`
- **company_id**: A unique ID for the company
- **company**: Name of the company
- **city**: City where the company is headquartered
- **country**: Country where the company is headquartered
- **continent**: Continent where the company is headquartered

### `dates.csv`
- **company_id**: A unique ID for the company
- **date_joined**: The date that the company became a unicorn
- **year_founded**: The year that the company was founded

### `funding.csv`
- **company_id**: A unique ID for the company
- **valuation**: Company value in US dollars
- **funding**: The amount of funding raised in US dollars
- **select_investors**: A list of key investors in the company

### `industries.csv`
- **company_id**: A unique ID for the company
- **industry**: The industry that the company operates in

## 🛠️ Technical Stack

- **Database**: PostgreSQL (Docker container)
- **Languages**: Python, SQL
- **Libraries**: pandas, psycopg2, python-dotenv, sqlalchemy
- **Environment**: Jupyter Notebook
- **Containerization**: Docker Compose

## 🚀 Getting Started

### Prerequisites
1. Docker and Docker Desktop installed and running
2. Python 3.7+ with pip

### Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with your PostgreSQL credentials:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=unicorns_db
```

3. Start PostgreSQL Docker container:
```bash
docker-compose up -d
```

4. Load data into PostgreSQL:
```bash
python load_data.py
```

5. Open and run the Jupyter notebook:
```bash
jupyter notebook notebook.ipynb
```

## 📁 Project Structure

```
Project Analyzing Unicorn Companies/
├── data/                           # CSV datasets
│   ├── companies.csv
│   ├── dates.csv
│   ├── funding.csv
│   └── industries.csv
├── load_data.py                   # Data loading script
├── notebook.ipynb                 # Main analysis notebook
├── docker-compose.yml             # Docker configuration
├── requirements.txt               # Python dependencies
├── calculator.jpg                 # Project image
├── .env                          # Environment variables (not tracked)
└── README.md                     # This file
```

## 🔍 Analysis Highlights

The notebook includes:

### 1. Database Connection and Setup
- Connection to PostgreSQL database using psycopg2
- Environment variable management for secure credentials
- Data validation and sample queries

### 2. Exploratory Data Analysis
- Examination of company distribution across continents
- Industry classification overview
- Data quality checks

### 3. Main Analysis: Top Industries by Unicorn Count (2019-2021)
Using a sophisticated SQL query with Common Table Expressions (CTEs):
- Identifies the top 3 industries by total unicorn count
- Calculates yearly statistics including:
  - Number of new unicorns per year
  - Average valuation in billions
- Groups results by industry and year
- Provides insights into industry trends over time

### Key Findings
The analysis reveals:
- **Fintech** leads with the highest number of unicorns (173 total across 2019-2021)
- **Internet software & services** is second with 152 unicorns
- **E-commerce & direct-to-consumer** ranks third with 75 unicorns
- 2021 saw the highest surge in unicorn formations
- Average valuations were higher in earlier years (2019-2020) compared to 2021

## 📈 SQL Query Methodology

The main analysis uses advanced SQL techniques:
- **Common Table Expressions (CTEs)** for modular query organization
- **Window Functions** with EXTRACT for date manipulation
- **Multiple JOINs** across four tables
- **Aggregation Functions** (COUNT, AVG, ROUND)
- **Subquery Filtering** to focus on top performers

## 🙏 Acknowledgments

- **DataCamp**: This project was originally completed as part of a DataCamp PostgreSQL course
- Dataset represents real-world unicorn companies as of 2021
- Investment analysis framework inspired by venture capital methodologies

---

*Part of my data analytics portfolio showcasing SQL, PostgreSQL, Python, and data analysis skills.*
