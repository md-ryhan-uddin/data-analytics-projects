# SQL Associate Practical Exam: Hotel Operations

## Overview
This project analyzes **LuxurStay Hotels** operational data to diagnose customer satisfaction issues affecting their international hotel chain. Following customer complaints about slow room service, the Head of Operations requires data-driven insights to identify underperforming branches and service types. The analysis demonstrates SQL data cleaning, multi-table joins, aggregation, and filtering techniques to pinpoint specific hotel-service combinations requiring operational improvements.

## Dataset
The hotel operations database contains **17,786 records** across 3 interconnected tables (customer feedback data only):

- **branch** (100 rows): Hotel properties with id, location (EMEA/NA/LATAM/APAC), total_rooms, staff_count, opening_date, target_guests (Business/Leisure)
  - **Data Quality Issues**: Invalid locations, out-of-range room counts (1-400 valid), missing staff counts, invalid opening dates (2000-2023 valid), missing/inconsistent target_guests
  
- **request** (17,682 rows): Service requests with id, service_id, branch_id, time_taken (minutes), request_time (timestamp), rating (1-5 scale)
  
- **service** (4 rows): Service catalog with id, description (Meal, Laundry, Maintenance, Room Service)

**Business Context**: LuxurStay targets 4.5+ customer satisfaction ratings across their global portfolio. Recent complaints indicate ratings have dropped below this threshold in specific branch-service combinations, threatening the brand's reputation for customer service excellence.

**Key Relationships**:
- `request.branch_id` → `branch.id`: Links service requests to hotel locations
- `request.service_id` → `service.id`: Categorizes requests by service type

## Technical Stack
- **Database**: PostgreSQL 15 (Docker container on port 5443)
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
   Loads 17,786 records (100 branches, 17,682 requests, 4 services)

4. **Run Analysis**:
   ```bash
   jupyter notebook notebook.ipynb
   ```

## Analysis Tasks

### Task 1: Data Cleaning - Branch Table Validation
**Objective**: Clean branch data according to strict specifications, handling invalid/missing values

**SQL Query**:
```sql
SELECT
    id,
    CASE 
        WHEN UPPER(TRIM(location)) IN ('EMEA','NA','LATAM','APAC') 
            THEN UPPER(TRIM(location))
        ELSE 'Unknown'
    END AS location,
    CASE 
        WHEN total_rooms BETWEEN 1 AND 400 THEN CAST(total_rooms AS INT)
        ELSE 100
    END AS total_rooms,
    CASE 
        WHEN staff_count IS NOT NULL THEN CAST(staff_count AS INT)
        ELSE CAST(ROUND((CASE WHEN total_rooms BETWEEN 1 AND 400 
                         THEN total_rooms ELSE 100 END) * 1.5) AS INT)
    END AS staff_count,
    CASE 
        WHEN opening_date ~ '^[0-9]+$'
             AND CAST(opening_date AS INT) BETWEEN 2000 AND 2023
            THEN CAST(opening_date AS INT)
        ELSE 2023
    END AS opening_date,
    CASE 
        WHEN UPPER(TRIM(target_guests)) = 'LEISURE' THEN 'Leisure'
        WHEN UPPER(TRIM(target_guests)) LIKE 'B%' THEN 'Business'
        ELSE 'Leisure'
    END AS target_guests
FROM branch;
```

**Key Techniques**:
- **Nested CASE Expressions**: Multi-level validation logic for location, room count, staff, opening date, target guests
- **String Functions**: UPPER(), TRIM() for normalization before validation
- **Regex Pattern Matching**: `opening_date ~ '^[0-9]+$'` validates numeric strings
- **Type Casting**: CAST() converts validated strings to INT for numeric fields
- **Business Rule Enforcement**: staff_count = total_rooms * 1.5 when missing, default 100 rooms, default 2023 opening

**Results**: Cleaned 100 hotel records
- **Location Distribution**: APAC, LATAM, EMEA, NA + "Unknown" for invalid entries
- **Room Range**: All validated to 1-400 rooms or defaulted to 100
- **Staff Formula**: Missing staff counts calculated as 150% of room capacity
- **Date Validation**: Invalid years defaulted to 2023 (most recent)
- **Target Guest Standardization**: Normalized to "Leisure" or "Business" with case consistency

### Task 2: Service Time Analysis
**Objective**: Calculate average and maximum response times per branch-service combination

**SQL Query**:
```sql
SELECT
    service_id,
    branch_id,
    ROUND(AVG(time_taken)::numeric, 2) AS avg_time_taken,
    MAX(time_taken) AS max_time_taken
FROM request
GROUP BY service_id, branch_id;
```

**Key Techniques**:
- **Multi-Column Grouping**: GROUP BY service_id, branch_id for dimensional analysis
- **Aggregate Functions**: AVG() for central tendency, MAX() for outlier detection
- **Type Casting**: `::numeric` conversion for PostgreSQL ROUND compatibility
- **Precision Control**: ROUND(..., 2) for 2-decimal financial/time reporting standards

**Results**: 385 branch-service combinations analyzed
- **Response Time Variance**: Branch 46 Service 2 averages 13.09 minutes (max 16), while Branch 46 Service 1 averages 2.08 minutes (max 4)
- **Service Type Impact**: Service types show distinct time profiles (Service 1 ~2-3 min, Service 2 ~13-14 min, Service 3 ~6-7 min, Service 4 ~9 min)
- **Maximum Deviations**: Max times often 2-5x higher than averages, indicating outlier requests needing investigation

### Task 3: Target Hotels for Improvement
**Objective**: Identify Meal and Laundry service requests in EMEA and LATAM regions for management focus

**SQL Query**:
```sql
SELECT
    s.description,
    b.id AS id,
    b.location,
    r.id AS request_id,
    r.rating
FROM request r
JOIN service s ON r.service_id = s.id
JOIN branch b ON r.branch_id = b.id
WHERE s.description IN ('Meal', 'Laundry')
  AND b.location IN ('EMEA', 'LATAM');
```

**Key Techniques**:
- **Multi-Table INNER JOINs**: Combines request → service (description), request → branch (location)
- **IN Clause Filtering**: Efficient filtering for multiple values (2 services, 2 regions)
- **Column Aliasing**: `b.id AS id` for clearer output naming

**Results**: 5,047 target requests identified
- **Geographic Scope**: EMEA and LATAM regions only (excludes NA, APAC)
- **Service Focus**: Meal and Laundry services (excludes Maintenance, Room Service)
- **Rating Distribution**: Ratings span 1-5 scale, providing performance snapshot
- **Volume**: 5,047 requests represent ~28.5% of total 17,682 requests (significant subset for targeted improvements)

### Task 4: Underperforming Service-Branch Combinations
**Objective**: Identify all service-branch combinations with average ratings below 4.5 target

**SQL Query**:
```sql
SELECT
    service_id,
    branch_id,
    ROUND(AVG(rating)::numeric, 2) AS avg_rating
FROM request
GROUP BY service_id, branch_id
HAVING AVG(rating) < 4.5;
```

**Key Techniques**:
- **HAVING Clause**: Post-aggregation filtering (vs WHERE for pre-aggregation)
- **Aggregate Filter Logic**: AVG(rating) < 4.5 enforces business threshold
- **GROUP BY Dimensional Analysis**: service_id + branch_id isolates specific problem areas

**Results**: 215 underperforming combinations (55.8% of 385 total combinations)
- **Severe Underperformers**: Branch 8 Service 3 averages 3.38 (24.9% below target), Branch 1 Service 8 averages 3.64 (19.1% below target)
- **Marginal Failures**: Some combinations at 4.00 rating (11.1% below 4.5 target)
- **Failure Rate**: 215/385 = 55.8% of branch-service combinations fail to meet 4.5 target, indicating widespread service quality issues
- **Geographic/Service Patterns**: Requires cross-referencing with Task 3 results to identify if EMEA/LATAM or Meal/Laundry drive underperformance

## SQL Techniques Demonstrated
- **Data Cleaning & Validation**: Nested CASE expressions with regex, range checks, default value imputation
- **String Manipulation**: UPPER(), TRIM() for normalization, LIKE pattern matching for partial matches
- **Type Casting**: CAST() and `::numeric` for proper data types, ROUND() for precision control
- **Multi-Table JOINs**: INNER JOIN across request-service-branch relationships
- **Aggregate Functions**: AVG(), MAX() with GROUP BY for dimensional analysis
- **Filtering Logic**: WHERE for pre-aggregation, HAVING for post-aggregation, IN clause for multiple values
- **Business Rule Enforcement**: Calculated defaults (staff = rooms * 1.5), threshold filtering (rating < 4.5)

## Skills Demonstrated
- Data quality assessment and systematic cleaning strategies
- Multi-step validation logic with fallback defaults
- Relational database design understanding (foreign key relationships)
- Statistical aggregation for performance benchmarking
- Dimensional analysis for targeted operational improvements
- SQL query optimization with appropriate JOIN and filter placement

## Business Insights

### Data Quality Impact
- **Branch Data Issues**: Multiple data quality problems (invalid locations, out-of-range values, missing fields) required systematic cleaning before analysis
- **Validation Necessity**: Regex date validation, numeric range checks essential to prevent invalid data propagation

### Service Performance Crisis
- **Widespread Failure**: 55.8% of branch-service combinations fail 4.5 rating target, confirming management concerns
- **Service Time Variability**: 6x variance in average response times (2 min vs 13 min) suggests process standardization gaps
- **Geographic Concentration**: 5,047 EMEA/LATAM requests (28.5% of total) represent substantial improvement opportunity

### Operational Priorities
- **Critical Branches**: Branch 8, Branch 1 Service 8 show severe underperformance (3.38-3.64 ratings)
- **Service Type Focus**: Meal and Laundry in EMEA/LATAM warrant immediate operational review
- **Outlier Investigation**: Max times 2-5x higher than averages indicate process breakdowns needing root cause analysis

## Business Value
1. **Targeted Interventions**: Identifies 215 specific branch-service combinations for operational improvements vs blanket hotel-wide changes
2. **Data-Driven Decisions**: Quantifies underperformance (3.38-4.49 range) enabling prioritization by severity
3. **Regional Strategy**: EMEA/LATAM geographic focus concentrates resources on 28.5% of requests with documented issues
4. **Service Benchmarking**: Establishes time/rating benchmarks for each service type to guide performance standards
5. **Brand Protection**: Addresses customer satisfaction crisis before ratings decline further damages LuxurStay's premium brand positioning
