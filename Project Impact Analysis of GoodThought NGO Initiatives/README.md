# Impact Analysis of GoodThought NGO Initiatives

## Overview
This project analyzes **GoodThought NGO's** humanitarian efforts from 2010 to 2023, focusing on the intersection of funding, regional distribution, and social impact. Using PostgreSQL and window functions, the analysis identifies high-performing assignments, evaluates donor contributions across regions, and ranks projects by impact scores to guide data-driven decision-making for future initiatives.

## Dataset
The GoodThought database contains **15,000 records** across 3 interconnected tables:

- **assignments** (5,000 rows): Project details with assignment_id, assignment_name, start_date, end_date, budget, region (East/West/North/South), impact_score (0-10 scale measuring social benefit)
- **donations** (5,000 rows): Financial contributions with donation_id, donor_id, amount, donation_date, assignment_id (links donations to specific projects)
- **donars** (5,000 rows): Donor profiles with donor_id, donor_name, donor_type (Individual vs Organization)

**Key Relationships**:
- `donations.assignment_id` → `assignments.assignment_id`: Links funding to projects
- `donations.donor_id` → `donars.donor_id`: Connects donations to donor profiles

**Business Context**: GoodThought operates across 4 geographic regions, implementing projects in education, healthcare, and sustainable development. Impact scores measure social benefit on a 0-10 scale, guiding resource allocation decisions.

## Technical Stack
- **Database**: PostgreSQL 15 (Docker container on port 5442)
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
   Loads 15,000 records (5,000 assignments, 5,000 donations, 5,000 donors)

4. **Run Analysis**:
   ```bash
   jupyter notebook notebook.ipynb
   ```

## Analysis Tasks

### Task 1: Highest Donation Assignments by Donor Type
**Objective**: Identify top 5 assignments by total funding, segmented by donor type (Individual vs Organization)

**SQL Query**:
```sql
SELECT
    a.assignment_name,
    a.region,
    ROUND(SUM(d.amount)::numeric, 2) AS rounded_total_donation_amount,
    dn.donor_type
FROM
    donations d
JOIN assignments a ON d.assignment_id = a.assignment_id
JOIN donars dn ON d.donor_id = dn.donor_id
GROUP BY
    a.assignment_name, a.region, dn.donor_type
ORDER BY
    rounded_total_donation_amount DESC
LIMIT 5;
```

**Key Techniques**:
- **Multi-Table JOIN**: Combines donations, assignments, and donars for comprehensive funding view
- **Aggregate Functions**: SUM() calculates total donations per assignment-donor_type combination
- **Type Casting**: `::numeric` conversion for PostgreSQL ROUND compatibility
- **GROUP BY**: Multi-column grouping by assignment_name, region, donor_type for granular analysis

**Results**: Top 5 funded assignments
1. **Assignment_3033** (East, Individual): $3,840.66 total donations
2. **Assignment_300** (West, Organization): $3,133.98 total donations
3. **Assignment_4114** (North, Organization): $2,778.57 total donations
4. **Assignment_1765** (West, Organization): $2,626.98 total donations
5. **Assignment_268** (East, Individual): $2,488.69 total donations

**Insight**: Individual donors lead funding in East region, while Organizations dominate in West/North

### Task 2: Top Regional Impact Assignments
**Objective**: Identify highest-impact assignment per region using window functions

**SQL Query**:
```sql
WITH assignment_donations AS (
    SELECT
        a.assignment_id,
        a.assignment_name,
        a.region,
        a.impact_score,
        COUNT(d.donation_id) AS num_total_donations
    FROM
        assignments a
    JOIN donations d ON a.assignment_id = d.assignment_id
    GROUP BY
        a.assignment_id, a.assignment_name, a.region, a.impact_score
),
ranked_assignments AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY impact_score DESC) AS rank
    FROM assignment_donations
)
SELECT
    assignment_name,
    region,
    impact_score,
    num_total_donations
FROM ranked_assignments
WHERE rank = 1
ORDER BY region ASC;
```

**Key Techniques**:
- **Common Table Expressions (CTEs)**: Two-stage query structure for clarity
- **Window Functions**: ROW_NUMBER() OVER (PARTITION BY region ORDER BY impact_score DESC) ranks assignments within each region
- **Aggregate with JOIN**: COUNT(donation_id) calculates funding activity per assignment
- **PARTITION BY**: Isolates ranking within regional boundaries

**Results**: Top impact assignment per region (4 regions)
- **East**: Assignment_316 (10.00 impact, 2 donations)
- **North**: Assignment_2253 (9.99 impact, 1 donation)
- **South**: Assignment_3547 (10.00 impact, 1 donation)
- **West**: Assignment_3764 (9.99 impact, 1 donation)

**Insight**: Perfect/near-perfect impact scores (9.99-10.00) achieved across all regions, but donation counts vary (East receives 2x more donations than other regions for top project)

## SQL Techniques Demonstrated
- **Multi-Table JOINs**: Three-way joins (donations → assignments → donars) for holistic analysis
- **Aggregate Functions**: SUM() for funding totals, COUNT() for donation frequency, ROUND() for financial precision
- **Common Table Expressions (CTEs)**: Multi-stage query decomposition for complex window function operations
- **Window Functions**: ROW_NUMBER() OVER (PARTITION BY...) for regional ranking without losing detail
- **Type Casting**: `::numeric` for proper ROUND function behavior in PostgreSQL
- **Grouping & Ordering**: Multi-column GROUP BY for dimensional analysis, ORDER BY for result presentation

## Skills Demonstrated
- Relational database query design with multi-table joins
- Window function mastery for regional partitioning and ranking
- Statistical aggregation (SUM, COUNT) for business metrics
- Data-driven decision support for nonprofit resource allocation
- Financial data formatting with ROUND for reporting standards

## Business Insights

### Funding Patterns
- **Individual vs Organization Donors**: Top 5 assignments split 40% Individual (2 projects) vs 60% Organization (3 projects), suggesting organizational donors provide slightly larger contributions
- **Regional Concentration**: East region appears twice in top 5 (Assignment_3033, Assignment_268), indicating higher funding activity
- **Donation Size**: Average top donation ~$2,974 (total $14,869 / 5 assignments), showing substantial donor engagement

### Impact Distribution
- **Perfect Impact Scores**: 2 of 4 regions (East, South) achieve perfect 10.00 impact scores
- **Near-Perfect Performance**: North and West reach 9.99 impact, suggesting consistent high-quality project execution across all regions
- **Funding Efficiency**: Assignment_316 (East) achieves perfect 10.00 impact with only 2 donations, demonstrating efficient resource utilization vs other regions requiring 1 donation for similar impact

### Strategic Implications
- **East Region Success**: Leads in both funding (2 top-5 assignments) and impact (perfect 10.00 score), suggesting best practices for replication
- **Single-Donation Projects**: 3 of 4 top-impact assignments achieved with 1 donation, indicating potential for high-impact low-cost initiatives
- **Donor Type Strategy**: Organizations dominate 60% of top funding, warranting targeted corporate engagement programs

## Business Value
1. **Resource Allocation**: Identifies high-impact regions (East) for expanded investment
2. **Donor Engagement**: Reveals Individual vs Organization funding patterns to tailor fundraising strategies
3. **Impact Benchmarking**: 9.99-10.00 impact scores set performance standards for future assignments
4. **Regional Equity**: Window functions expose funding disparities (East receives 2x donations), guiding equitable distribution efforts
5. **Efficiency Insights**: Single-donation high-impact projects suggest scalable low-cost intervention models for replication
