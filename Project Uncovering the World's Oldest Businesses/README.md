# Uncovering the World's Oldest Businesses# Uncovering the World's Oldest Businesses



![Staffelter Hof Winery](MKn_Staffelter_Hof.jpeg)A comprehensive data analytics project exploring the world's oldest businesses using PostgreSQL, Python, and data visualization techniques.



## Overview![Staffelter Hof Winery](MKn_Staffelter_Hof.jpeg)

*Staffelter Hof Winery - Germany's oldest business, established in 862*

This project analyzes the world's oldest businesses across nearly every country, exploring what characteristics enable businesses to endure for centuries or even millennia. Using historical data compiled by BusinessFinancing.co.uk, we investigate the oldest business on each continent, identify countries lacking business data, and determine which business categories have proven most resilient over time.

## 📊 Project Overview

The analysis reveals fascinating insights into business longevity, from Japan's Kongō Gumi construction company founded in 578 CE to modern postal services established in the 1800s. By combining data from multiple CSV files using advanced SQL joins and window functions, we uncover patterns in business survival across different continents and industry categories.

This project analyzes a dataset of the oldest companies still operating in nearly every country around the world. The analysis explores what characteristics enable businesses to survive through centuries of dramatic historical changes, from empires to world wars.

## Dataset Description

**Key Research Question:** What factors allow businesses to stand the test of time?

The project uses four interconnected CSV datasets:

## 🗃️ Dataset Description

### businesses.csv & new_businesses.csv

- **business**: Name of the business (varchar)The project includes four cleaned CSV datasets:

- **year_founded**: Year the business was founded (int)

- **category_code**: Code for the business category (varchar)### `businesses.csv` & `new_businesses.csv`

- **country_code**: ISO 3166-1 three-letter country code (char)- **business**: Name of the business

- **Total records**: 163 businesses + 2 new businesses- **year_founded**: Year the business was founded

- **category_code**: Business category code

### countries.csv- **country_code**: ISO 3166-1 three-letter country code

- **country_code**: ISO 3166-1 three-letter country code (varchar)

- **country**: Name of the country (varchar)### `countries.csv`

- **continent**: Name of the continent (varchar)- **country_code**: ISO 3166-1 three-letter country code

- **Total records**: 195 countries- **country**: Name of the country

- **continent**: Continent where the country is located

### categories.csv

- **category_code**: Code for the business category (varchar)### `categories.csv`

- **category**: Description of the business category (varchar)- **category_code**: Business category code

- **Total records**: 19 business categories- **category**: Description of the business category



## Technical Stack## 🛠️ Technical Stack



- **Database**: PostgreSQL 15-alpine (Docker container)- **Database**: PostgreSQL

- **Data Loading**: Python 3.12+ with pandas, SQLAlchemy, psycopg2- **Languages**: Python, SQL

- **Analysis**: Jupyter Notebook with pandas for SQL query execution- **Libraries**: pandas, sqlalchemy, psycopg2, python-dotenv

- **Environment**: Docker Compose for containerized PostgreSQL- **Environment**: Jupyter Notebook

- **Libraries**: pandas>=2.0.0, psycopg2-binary>=2.9.11, python-dotenv>=1.0.0, sqlalchemy>=2.0.0- **Visualization**: matplotlib, seaborn (implied from analysis)



## Installation & Setup## 🚀 Getting Started



1. **Start PostgreSQL container:**### Prerequisites

   ```bash1. PostgreSQL installed and running

   cd "Project Uncovering the World's Oldest Businesses"2. Python 3.7+ with pip

   docker-compose up -d

   ```### Installation



2. **Configure environment:**1. Install required packages:

   - Database runs on `localhost:5438````bash

   - Database name: `Oldest_Businesses_DB`pip install -r requirements.txt

   - Credentials configured in `.env` file```



3. **Load data:**2. Set up environment variables:

   ```bashCreate a `.env` file with your PostgreSQL credentials:

   python load_csvs_to_postgres.py```env

   ```DB_HOST=localhost

   This loads all 4 CSV files into PostgreSQL tables with normalized column names.DB_PORT=5432

DB_USER=postgres

4. **Run analysis:**DB_PASS=your_password

   Open `notebook.ipynb` in Jupyter and execute all cells to perform the historical business analysis.DB_NAME=Oldest_Businesses_DB

```

## Analysis Tasks

3. Load data into PostgreSQL:

### Task 1: Oldest Business Per Continent```bash

Identify the single oldest business on each continent using window functions:python load_csvs_to_postgres.py

```

```sql

WITH ranking AS (4. Open and run the Jupyter notebook:

    SELECT continent, country, business, year_founded,```bash

        ROW_NUMBER() OVER (jupyter notebook notebook.ipynb

            PARTITION BY c.continent```

            ORDER BY b.year_founded ASC

        ) AS rn## 📁 Project Structure

    FROM businesses AS b

    LEFT JOIN countries AS c ON b.country_code = c.country_code```

)Uncovering the World's Oldest Businesses/

SELECT continent, country, business, year_founded├── data/                           # CSV datasets

FROM ranking│   ├── businesses.csv

WHERE rn = 1│   ├── categories.csv

ORDER BY year_founded;│   ├── countries.csv

```│   └── new_businesses.csv

├── load_csvs_to_postgres.py       # Data loading script

**Key Findings:**├── notebook.ipynb                 # Main analysis notebook

- **Asia**: Kongō Gumi (Japan, 578 CE) - Construction company├── requirements.txt               # Python dependencies

- **Europe**: St. Peter Stifts Kulinarium (Austria, 803 CE) - Restaurant├── MKn_Staffelter_Hof.jpeg       # Project image

- **North America**: La Casa de Moneda de México (Mexico, 1534) - Mint├── .env                          # Environment variables (not tracked)

- **South America**: Casa Nacional de Moneda (Peru, 1565) - Mint├── .gitignore                    # Git ignore file

- **Africa**: Mauritius Post (Mauritius, 1772) - Postal service└── README.md                     # This file

- **Oceania**: Australia Post (Australia, 1809) - Postal service```



### Task 2: Countries Without Business Data## 🔍 Analysis Highlights

Determine how many countries per continent lack historical business data, including new_businesses:

The notebook includes:

```sql- Data exploration and cleaning

WITH all_businesses AS (- Multi-table joins using SQL

    SELECT DISTINCT country_code FROM businesses- Historical business trend analysis

    UNION- Continental and country-level comparisons

    SELECT DISTINCT country_code FROM new_businesses- Insights into business longevity factors

),

missing_countries AS (## 🙏 Acknowledgments

    SELECT c.continent, c.country_code

    FROM countries c- **DataCamp**: This project was originally completed as part of a DataCamp course/project

    LEFT JOIN all_businesses a ON c.country_code = a.country_code- Dataset provided by BusinessFinancing.co.uk

    WHERE a.country_code IS NULL- Image credit: Martin Kraft (Wikimedia Commons)

)- Inspired by the fascinating history of businesses that have survived centuries

SELECT continent, COUNT(DISTINCT country_code) AS countries_without_businesses

FROM missing_countries---

GROUP BY continent

ORDER BY continent;*Part of my data analytics portfolio showcasing SQL, PostgreSQL, and Python skills.*

```

**Key Findings:**
- **Total countries without data**: 31 out of 195 countries (15.9%)
- **Oceania**: 10 countries missing (highest)
- **Asia**: 7 countries missing
- **North America**: 5 countries missing
- **Africa, Europe, South America**: 3 countries each missing

### Task 3: Most Resilient Business Categories
Analyze which business categories have proven best suited to last over centuries:

```sql
SELECT c.continent, cat.category, MIN(b.year_founded) AS year_founded
FROM businesses b
JOIN countries c ON b.country_code = c.country_code
JOIN categories cat ON b.category_code = cat.category_code
WHERE b.year_founded IS NOT NULL
GROUP BY c.continent, cat.category
ORDER BY year_founded;
```

**Key Findings by Category (oldest foundation year):**
1. **Construction** (578 CE) - 2 businesses
2. **Cafés, Restaurants & Bars** (803 CE) - 6 businesses
3. **Distillers, Vintners, & Breweries** (862 CE) - 22 businesses (most prevalent!)
4. **Manufacturing & Production** (864 CE) - 15 businesses
5. **Banking & Finance** (1565 CE) - 37 businesses (largest category)

## SQL Techniques Demonstrated

- **Window Functions**: `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` for ranking oldest businesses per continent
- **Common Table Expressions (CTEs)**: Multi-level CTEs for combining datasets and filtering results
- **Set Operations**: `UNION` to merge businesses and new_businesses datasets
- **Advanced Joins**: 
  - `LEFT JOIN` to identify missing data (countries without businesses)
  - Multiple `JOIN` operations combining 4 tables
- **Aggregate Functions**: `MIN()`, `COUNT(DISTINCT)` for statistical analysis
- **Subquery Patterns**: Using CTEs to create intermediate result sets
- **Data Normalization**: Automated column name cleaning (lowercase, underscores) during data loading

## Skills Demonstrated

✅ **Data Integration**: Combining multiple CSV files with foreign key relationships  
✅ **Historical Data Analysis**: Working with temporal data spanning 1,400+ years  
✅ **Window Functions**: Advanced ranking techniques with PARTITION BY  
✅ **CTE Mastery**: Complex multi-level common table expressions  
✅ **Database Design**: Normalized schema with proper relationships  
✅ **Docker Containerization**: PostgreSQL deployment with Docker Compose  
✅ **ETL Pipeline**: Automated data loading with SQLAlchemy and pandas  
✅ **Data Quality**: Identifying missing data and coverage gaps across continents  

## Key Business Insights

1. **Construction & Hospitality Dominate Ancient Business**: The oldest businesses are in construction (578 CE) and restaurants/bars (803 CE), suggesting essential services and craftsmanship have timeless value.

2. **Distilleries Show Remarkable Longevity**: With 22 businesses and origins dating to 862 CE, the alcohol production industry demonstrates exceptional staying power across generations.

3. **Postal Services as Government-Backed Survivors**: Many of the oldest businesses in Africa and Oceania are postal services (1772-1809), often benefiting from government support and monopoly status.

4. **Banking & Finance Lead in Quantity**: Despite not being the oldest category, Banking & Finance has the most surviving businesses (37), indicating modern financial systems' importance.

5. **Geographic Disparity in Data**: 31 countries (15.9%) lack business data, with Oceania showing the largest gaps, highlighting potential research opportunities or data collection challenges.

## Business Value

This analysis provides valuable insights for:
- **Entrepreneurs**: Understanding which industries have proven resilient over centuries
- **Investors**: Identifying sectors with demonstrated longevity potential
- **Economic Historians**: Mapping the evolution of global commerce and trade
- **Business Strategy**: Learning from businesses that have survived wars, economic changes, and technological disruptions
- **Cultural Preservation**: Recognizing businesses as cultural heritage and historical artifacts

---

**Note**: The database contains 163 businesses from the main dataset plus 2 additional businesses from new_businesses.csv, representing nearly every country globally. Missing data for 31 countries presents opportunities for future research and data collection efforts.
