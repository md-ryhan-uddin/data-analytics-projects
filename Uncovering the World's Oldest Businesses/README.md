# Uncovering the World's Oldest Businesses

A comprehensive data analytics project exploring the world's oldest businesses using PostgreSQL, Python, and data visualization techniques.

![Staffelter Hof Winery](MKn_Staffelter_Hof.jpeg)
*Staffelter Hof Winery - Germany's oldest business, established in 862*

## 📊 Project Overview

This project analyzes a dataset of the oldest companies still operating in nearly every country around the world. The analysis explores what characteristics enable businesses to survive through centuries of dramatic historical changes, from empires to world wars.

**Key Research Question:** What factors allow businesses to stand the test of time?

## 🗃️ Dataset Description

The project includes four cleaned CSV datasets:

### `businesses.csv` & `new_businesses.csv`
- **business**: Name of the business
- **year_founded**: Year the business was founded
- **category_code**: Business category code
- **country_code**: ISO 3166-1 three-letter country code

### `countries.csv`
- **country_code**: ISO 3166-1 three-letter country code
- **country**: Name of the country
- **continent**: Continent where the country is located

### `categories.csv`
- **category_code**: Business category code
- **category**: Description of the business category

## 🛠️ Technical Stack

- **Database**: PostgreSQL
- **Languages**: Python, SQL
- **Libraries**: pandas, sqlalchemy, psycopg2, python-dotenv
- **Environment**: Jupyter Notebook
- **Visualization**: matplotlib, seaborn (implied from analysis)

## 🚀 Getting Started

### Prerequisites
1. PostgreSQL installed and running
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
DB_PASS=your_password
DB_NAME=Oldest_Businesses_DB
```

3. Load data into PostgreSQL:
```bash
python load_csvs_to_postgres.py
```

4. Open and run the Jupyter notebook:
```bash
jupyter notebook notebook.ipynb
```

## 📁 Project Structure

```
Uncovering the World's Oldest Businesses/
├── data/                           # CSV datasets
│   ├── businesses.csv
│   ├── categories.csv
│   ├── countries.csv
│   └── new_businesses.csv
├── load_csvs_to_postgres.py       # Data loading script
├── notebook.ipynb                 # Main analysis notebook
├── requirements.txt               # Python dependencies
├── MKn_Staffelter_Hof.jpeg       # Project image
├── .env                          # Environment variables (not tracked)
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```

## 🔍 Analysis Highlights

The notebook includes:
- Data exploration and cleaning
- Multi-table joins using SQL
- Historical business trend analysis
- Continental and country-level comparisons
- Insights into business longevity factors

## 🙏 Acknowledgments

- **DataCamp**: This project was originally completed as part of a DataCamp course/project
- Dataset provided by BusinessFinancing.co.uk
- Image credit: Martin Kraft (Wikimedia Commons)
- Inspired by the fascinating history of businesses that have survived centuries

---

*Part of my data analytics portfolio showcasing SQL, PostgreSQL, and Python skills.*
