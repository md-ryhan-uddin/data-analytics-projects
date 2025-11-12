# Exploring London's Travel Network

![Tower Bridge](london.jpg)

## Overview

This project analyzes Transport for London (TfL) public transport journey data from 2010-2022, exploring ridership patterns across London's diverse transport network. London's transport system serves over 8.5 million residents speaking 300+ languages across 32 boroughs spanning 606 square miles. Since 2000, TfL has managed an integrated network including the Underground, Overground, DLR, buses, trams, river services, and the Emirates Airline cable car.

The analysis reveals fascinating insights into London's transport usage, from identifying the most popular transport types to uncovering the dramatic impact of the COVID-19 pandemic on Underground ridership (77% decline in 2020) and peak Emirates Airline usage during the 2012 Olympic Games.

## Dataset Description

The project uses a single comprehensive dataset covering all TfL transport types:

### journeys table
- **month**: Month in number format (1 = January)
- **year**: Year of the journey data
- **days**: Number of days in the given month
- **report_date**: Date that the data was reported (DATE format)
- **journey_type**: Method of transport used (Underground & DLR, Bus, Tram, Overground, Emirates Airline, TfL Rail)
- **journeys_millions**: Millions of journeys, measured in decimals (FLOAT)
- **Total records**: 936 monthly journey records (2010-2022)

## Technical Stack

- **Database**: PostgreSQL 15-alpine (Docker container)
- **Data Loading**: Python 3.12+ with pandas, SQLAlchemy, psycopg2
- **Analysis**: Jupyter Notebook with pandas for SQL query execution
- **Environment**: Docker Compose for containerized PostgreSQL
- **Libraries**: pandas>=2.0.0, psycopg2-binary>=2.9.11, python-dotenv>=1.0.0, sqlalchemy>=2.0.0

## Installation & Setup

1. **Start PostgreSQL container:**
   ```bash
   cd "Project Exploring London's Travel Network"
   docker-compose up -d
   ```

2. **Configure environment:**
   - Database runs on `localhost:5439`
   - Database name: `tfl`
   - Credentials configured in `.env` file

3. **Load data:**
   ```bash
   python load_data.py
   ```
   This loads TFL.JOURNEYS.csv (936 records) into PostgreSQL with normalized column names.

4. **Run analysis:**
   Open `notebook.ipynb` in Jupyter and execute all cells to perform transport analysis.

## Analysis Tasks

### Task 1: Most Popular Transport Types
Identify which transport methods have the highest total ridership:

```sql
SELECT 
    journey_type,
    ROUND(CAST(SUM(journeys_millions) AS NUMERIC), 2) AS total_journeys_millions
FROM journeys
GROUP BY journey_type
ORDER BY total_journeys_millions DESC;
```

**Key Findings:**
1. **Bus**: 24,905.19 million journeys (59% of total) - Most popular transport mode
2. **Underground & DLR**: 15,020.47 million journeys (36% of total) - Second most used
3. **Overground**: 1,666.85 million journeys (4% of total)
4. **TfL Rail**: 411.31 million journeys (1% of total)
5. **Tram**: 314.69 million journeys (<1% of total)
6. **Emirates Airline**: 14.58 million journeys (<0.1% of total) - Least popular

### Task 2: Emirates Airline Popularity Peak
Analyze when the Emirates Airline cable car experienced its highest usage:

```sql
SELECT 
    month,
    year,
    ROUND(CAST(journeys_millions AS NUMERIC), 2) AS rounded_journeys_millions
FROM journeys
WHERE journey_type ILIKE 'Emirates Airline%'
  AND journeys_millions IS NOT NULL
ORDER BY rounded_journeys_millions DESC
LIMIT 5;
```

**Key Findings:**
- **Peak month**: May 2012 (0.53 million journeys) - 2012 London Olympic Games preparation
- **Second peak**: June 2012 (0.38 million journeys) - Olympics opening month
- **Third peak**: April 2012 (0.24 million journeys) - Olympic lead-up
- **Pattern**: Emirates Airline saw dramatic spike during 2012 Olympics, then stabilized at much lower levels
- **Context**: The cable car opened in June 2012 as transport infrastructure for the Olympics

### Task 3: Underground & DLR Ridership Trends
Examine least and most popular years for Underground & DLR usage:

```sql
SELECT
    year,
    journey_type,
    ROUND(CAST(SUM(journeys_millions) AS NUMERIC), 2) AS total_journeys_millions
FROM journeys
WHERE journey_type = 'Underground & DLR'
GROUP BY year, journey_type
ORDER BY total_journeys_millions ASC
LIMIT 5;
```

**Least Popular Years:**
1. **2020**: 310.18 million journeys (77% decline) - COVID-19 pandemic lockdowns
2. **2021**: 748.45 million journeys (46% decline) - COVID recovery period
3. **2022**: 1,064.86 million journeys (23% decline) - Partial return to normal
4. **2010**: 1,096.15 million journeys - Early in dataset
5. **2011**: 1,156.65 million journeys

**Most Popular Years:**
1. **2019**: 1,386.44 million journeys - Pre-pandemic peak
2. **2016**: 1,384.64 million journeys - Strong ridership year
3. **2018**: 1,382.42 million journeys - Consistent high usage
4. **2015**: 1,363.46 million journeys
5. **2017**: 1,362.29 million journeys

## SQL Techniques Demonstrated

- **Aggregate Functions**: `SUM()`, `COUNT()` for totaling journeys across time periods
- **Type Casting**: `CAST(... AS NUMERIC)` to ensure proper data types for ROUND function in PostgreSQL
- **ROUND Function**: Formatting decimal numbers for readability with proper casting
- **ILIKE Operator**: Case-insensitive pattern matching for transport type filtering
- **GROUP BY Clauses**: Aggregating data by transport type and year
- **ORDER BY with ASC/DESC**: Sorting results to find peaks and troughs
- **LIMIT Clause**: Restricting results to top N records
- **WHERE Filtering**: Isolating specific transport types and handling NULL values

## Skills Demonstrated

✅ **Time Series Analysis**: Analyzing ridership patterns across 12+ years  
✅ **Event Impact Analysis**: Quantifying COVID-19's effect on transport (77% decline)  
✅ **Aggregate Queries**: Summing millions of journey records across dimensions  
✅ **Data Type Management**: Proper casting for PostgreSQL numeric functions  
✅ **Transport Analytics**: Understanding modal share and usage patterns  
✅ **Docker Containerization**: PostgreSQL deployment with Docker Compose  
✅ **ETL Pipeline**: Automated data loading with pandas and SQLAlchemy  
✅ **Trend Identification**: Finding peaks (2012 Olympics) and troughs (2020 pandemic)  

## Key Business Insights

1. **Bus Dominance**: Buses account for nearly 60% of all TfL journeys (24.9 billion), demonstrating their critical role as London's transport backbone serving all 32 boroughs.

2. **COVID-19 Catastrophic Impact**: Underground & DLR ridership collapsed 77% in 2020 (from 1.39 billion to 310 million annual journeys), representing the most dramatic transport disruption in London's modern history.

3. **Olympics Infrastructure Reality**: Emirates Airline peaked at 0.53 million monthly journeys during the 2012 Olympics but quickly stabilized at much lower levels (<0.2 million/month), suggesting the £60 million cable car serves more as tourist attraction than essential transport.

4. **Pre-Pandemic Peak**: 2019 saw record Underground & DLR usage (1.39 billion journeys), marking the zenith before COVID-19 disrupted global urban transport patterns.

5. **Recovery Trajectory**: 2022 Underground ridership (1.06 billion) recovered to 77% of pre-pandemic levels, indicating persistent behavior changes in work-from-home culture and commuting patterns.

6. **Modal Share Stability**: The Bus/Underground ratio (60/36) remained remarkably consistent throughout the dataset, suggesting fundamental transport preferences driven by London's geography and infrastructure rather than temporary trends.

## Business Value

This analysis provides valuable insights for:
- **Transport Planners**: Understanding ridership patterns to optimize service frequency and capacity
- **Infrastructure Investment**: Data-driven decisions on which transport modes require capacity expansion
- **Policy Makers**: Quantifying the impact of major events (Olympics) and crises (COVID-19) on transport usage
- **Urban Development**: Informing transit-oriented development decisions based on modal share data
- **Revenue Forecasting**: Predicting fare income based on historical ridership trends and recovery patterns
- **Crisis Management**: Establishing baselines for future pandemic or disruption scenarios

---

**Note**: The dataset contains 936 monthly journey records across 6 transport types (Underground & DLR, Bus, Tram, Overground, Emirates Airline, TfL Rail) from 2010-2022, representing over 42 billion individual journeys on London's transport network. The dramatic COVID-19 impact on 2020-2022 data provides unique insights into transport resilience and recovery patterns.
