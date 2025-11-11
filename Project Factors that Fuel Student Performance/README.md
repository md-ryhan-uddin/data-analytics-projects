# Factors that Fuel Student Performance

A comprehensive SQL analysis project investigating the key factors that influence student academic success. This project analyzes 6,607 student records to identify correlations between study habits, attendance, extracurricular activities, and exam performance using PostgreSQL.

![Student Exam Performance](exam_result.jpeg)
*Analyzing factors that drive student academic success*

## 📊 Project Overview

In today's competitive educational environment, understanding what truly impacts student success is crucial for educators, students, and policymakers. This project examines a rich dataset of student demographics, study habits, and performance metrics to uncover actionable insights.

**Key Objectives:**
- Identify study hour patterns that correlate with high exam scores
- Analyze the impact of extracurricular activities on academic performance
- Rank top-performing students using window functions
- Provide data-driven recommendations for student success

## 🗃️ Dataset Description

The `student_performance` table contains **6,607 student records** with 20 comprehensive attributes:

| Column | Definition | Data Type |
|--------|------------|-----------|
| `hours_studied` | Hours spent studying per week | `INTEGER` |
| `attendance` | Percentage of classes attended | `FLOAT` |
| `parental_involvement` | Level of parental engagement | `VARCHAR` (Low, Medium, High) |
| `access_to_resources` | Access to learning resources | `VARCHAR` (Low, Medium, High) |
| `extracurricular_activities` | Participation in activities | `VARCHAR` (Yes, No) |
| `sleep_hours` | Average hours of sleep per night | `FLOAT` |
| `previous_scores` | Prior academic scores | `INTEGER` |
| `motivation_level` | Student motivation level | `VARCHAR` (Low, Medium, High) |
| `internet_access` | Access to internet | `VARCHAR` (Yes, No) |
| `tutoring_sessions` | Number of tutoring sessions | `INTEGER` |
| `family_income` | Family income level | `VARCHAR` (Low, Medium, High) |
| `teacher_quality` | Quality of teachers | `VARCHAR` (Low, Medium, High) |
| `school_type` | Type of school | `VARCHAR` (Public, Private) |
| `peer_influence` | Peer influence type | `VARCHAR` (Positive, Negative, Neutral) |
| `physical_activity` | Hours of physical activity | `INTEGER` |
| `learning_disabilities` | Presence of learning disabilities | `VARCHAR` (Yes, No) |
| `parental_education_level` | Parents' education level | `VARCHAR` |
| `distance_from_home` | Distance to school | `VARCHAR` (Near, Moderate, Far) |
| `gender` | Student gender | `VARCHAR` (Male, Female) |
| `exam_score` | Final exam score | `FLOAT` |

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
cd "Project Factors that Fuel Student Performance"
```

2. **Configure environment variables**:
The `.env` file contains database credentials:
```env
DB_HOST=localhost
DB_PORT=5435
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=student_performance_db
```

3. **Start PostgreSQL Docker container**:
```bash
docker-compose up -d
```

4. **Load student performance data**:
```bash
python load_data.py
```

5. **Open and run the Jupyter notebook**:
```bash
jupyter notebook notebook.ipynb
```

## 📁 Project Structure

```
Project Factors that Fuel Student Performance/
├── data/                                    # Dataset directory (gitignored)
│   └── StudentPerformanceFactors.csv        # 6,607 student records
├── notebook.ipynb                           # Analysis notebook
├── load_data.py                             # Data loading script
├── docker-compose.yml                       # Database container config
├── exam_result.jpeg                         # Project illustration
├── .env                                    # Environment variables (not tracked)
└── README.md                               # This file
```

## 🔍 Analysis Highlights

### 1. Impact of Study Hours + Extracurricular Activities

Analyzes students who study >10 hours/week AND participate in extracurricular activities:

```sql
SELECT
    hours_studied,
    AVG(exam_score) AS avg_exam_score
FROM student_performance
WHERE
    hours_studied > 10
    AND extracurricular_activities = 'Yes'
    AND exam_score IS NOT NULL
GROUP BY hours_studied
ORDER BY hours_studied DESC;
```

**Key Insight**: Examines whether high study hours combined with extracurriculars leads to better outcomes.

### 2. Study Hours Range Analysis with CTEs

Uses Common Table Expressions to bucket study hours and find optimal ranges:

```sql
WITH buckets AS (
    SELECT
        CASE
            WHEN hours_studied BETWEEN 1 AND 5   THEN '1-5 hours'
            WHEN hours_studied BETWEEN 6 AND 10  THEN '6-10 hours'
            WHEN hours_studied BETWEEN 11 AND 15 THEN '11-15 hours'
            WHEN hours_studied >= 16             THEN '16+ hours'
            ELSE '0 or NULL'
        END AS hours_studied_range,
        exam_score
    FROM student_performance
    WHERE exam_score IS NOT NULL
)
SELECT
    hours_studied_range,
    AVG(exam_score) AS avg_exam_score
FROM buckets
WHERE hours_studied_range <> '0 or NULL'
GROUP BY hours_studied_range
ORDER BY avg_exam_score DESC;
```

**Key Insight**: Identifies the "sweet spot" for study hours that maximizes exam performance.

### 3. Top Student Ranking with Window Functions

Ranks students using `DENSE_RANK()` to identify top performers and their characteristics:

```sql
SELECT
    attendance,
    hours_studied,
    sleep_hours,
    tutoring_sessions,
    exam_score,
    DENSE_RANK() OVER (ORDER BY exam_score DESC) AS exam_rank
FROM student_performance
WHERE exam_score IS NOT NULL
ORDER BY exam_rank ASC
LIMIT 30;
```

**Key Insight**: Reveals patterns in attendance, study habits, and sleep among top 30 students.

## 📈 SQL Techniques Demonstrated

- ✅ **Window Functions**: `DENSE_RANK()` for ranking analysis
- ✅ **Common Table Expressions (CTEs)**: Complex query organization
- ✅ **CASE Statements**: Dynamic bucketing and categorization
- ✅ **Aggregate Functions**: `AVG()`, `GROUP BY` for statistical analysis
- ✅ **Filtering**: Multi-condition WHERE clauses
- ✅ **NULL Handling**: Proper NULL exclusion in analysis
- ✅ **Sorting**: `ORDER BY` for meaningful result presentation

## 🎯 Key Findings & Insights

This analysis reveals:
- ✅ **Optimal Study Patterns**: Identify the most effective study hour ranges
- ✅ **Extracurricular Impact**: Quantify how activities affect academic performance
- ✅ **Success Factors**: Characteristics shared by top-performing students
- ✅ **Attendance Correlation**: Relationship between class attendance and exam scores
- ✅ **Work-Life Balance**: Importance of sleep and physical activity

## 📚 Business Value

- **For Students**: Data-driven guidance on effective study strategies
- **For Educators**: Insights to support struggling students
- **For Policymakers**: Evidence for educational program design
- **For Parents**: Understanding factors that contribute to academic success
- **For Researchers**: Foundation for further educational studies

## 💡 Potential Extensions

- Correlation analysis between multiple factors
- Predictive modeling for at-risk student identification
- Comparative analysis by school type or demographics
- Time-series analysis if longitudinal data available
- Visualization dashboards for interactive exploration

---

*Part of my data analytics portfolio showcasing PostgreSQL, SQL analytics, and educational data analysis.*
