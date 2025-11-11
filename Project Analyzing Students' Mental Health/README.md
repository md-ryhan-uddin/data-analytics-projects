# Analyzing Students' Mental Health

A data analytics project investigating the mental health of international university students using PostgreSQL and statistical analysis. This study examines the relationship between length of stay, social connectedness, acculturative stress, and depression among international students.

![Mental Health Illustration](mentalhealth.jpg)
*Understanding mental health challenges faced by international students*

## 📊 Project Overview

This project analyzes survey data from a Japanese international university (2018) to explore whether studying abroad affects students' mental health. The research focuses on international students and investigates if the length of stay in a foreign country contributes to mental health outcomes.

**Key Research Questions:**
- Do international students experience higher rates of mental health difficulties?
- Does the length of stay correlate with depression scores?
- How do social connectedness and acculturative stress relate to mental health?

## 🗃️ Dataset Description

The `students.csv` dataset contains **286 student responses** with the following key variables:

| Field Name      | Description                                          |
|-----------------|------------------------------------------------------|
| `inter_dom`     | Student type (International or Domestic)             |
| `japanese_cate` | Japanese language proficiency level                  |
| `english_cate`  | English language proficiency level                   |
| `academic`      | Academic level (Undergraduate or Graduate)           |
| `age`           | Current age of student                               |
| `stay`          | Length of stay in years                              |
| `todep`         | Total PHQ-9 depression score                         |
| `tosc`          | Total Social Connectedness Scale (SCS) score         |
| `toas`          | Total Acculturative Stress Scale (ASISS) score       |

### Assessment Scales

- **PHQ-9 (Patient Health Questionnaire-9)**: Depression screening tool (0-27 scale)
  - Higher scores indicate more depressive symptoms
- **SCS (Social Connectedness Scale)**: Measures sense of belonging (8-48 scale)
  - Higher scores indicate better social connections
- **ASISS (Acculturative Stress Scale for International Students)**: Stress from cultural adaptation (36-180 scale)
  - Higher scores indicate more acculturative stress

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
cd "Project Analyzing Students' Mental Health"
```

2. **Environment setup** (if not using root venv):
```bash
pip install pandas psycopg2-binary python-dotenv sqlalchemy jupyter
```

3. **Configure environment variables**:
The `.env` file contains database credentials:
```env
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=students_mental_health_db
```

4. **Start PostgreSQL Docker container**:
```bash
docker-compose up -d
```

5. **Load data into PostgreSQL**:
```bash
python load_data.py
```

6. **Open and run the Jupyter notebook**:
```bash
jupyter notebook notebook.ipynb
```

## 📁 Project Structure

```
Project Analyzing Students' Mental Health/
├── students.csv                       # Survey dataset (286 students)
├── notebook.ipynb                     # Main analysis notebook
├── load_data.py                       # Data loading script
├── docker-compose.yml                 # Database container configuration
├── mentalhealth.jpg                   # Project illustration
├── .env                              # Environment variables (not tracked)
└── README.md                         # This file
```

## 🔍 Analysis Highlights

### Main Analysis Query
The core analysis uses SQL aggregation to examine mental health metrics by length of stay:

```sql
SELECT 
    stay,
    COUNT(inter_dom) AS count_int,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM students
WHERE inter_dom = 'Inter'
GROUP BY stay	
ORDER BY stay DESC;
```

### Key Findings

1. **Sample Size**: 286 international and domestic students surveyed
2. **Depression Scores**: International students show varying PHQ-9 scores based on length of stay
3. **Social Connectedness**: Longer stays tend to correlate with improved social connections
4. **Acculturative Stress**: Stress levels change as students adapt to the new cultural environment
5. **Length of Stay Impact**: Clear patterns emerge showing how duration affects mental health indicators

### Statistical Insights

- **SQL Aggregation**: GROUP BY and AVG functions to calculate mean scores
- **Filtering**: WHERE clause to isolate international students
- **Rounding**: ROUND function for cleaner presentation of averages
- **Ordering**: Results sorted by length of stay for trend analysis

## 📈 SQL Techniques Used

- **Aggregate Functions**: COUNT(), AVG(), ROUND()
- **Filtering**: WHERE clause for international students
- **Grouping**: GROUP BY to analyze by length of stay
- **Ordering**: ORDER BY for chronological presentation
- **Data Type Handling**: Proper numeric calculations

## 🎯 Key Takeaways

This analysis demonstrates:
- ✅ SQL proficiency for statistical analysis
- ✅ Understanding of mental health assessment scales
- ✅ Data-driven insights into student wellbeing
- ✅ PostgreSQL database management
- ✅ Research methodology and ethics considerations

## 🙏 Acknowledgments

- Original study conducted by a Japanese international university (2018)
- Research approved by ethical and regulatory boards
- Dataset provided for educational purposes
- Analysis framework based on clinical psychology assessment tools

---

*Part of my data analytics portfolio showcasing PostgreSQL, SQL, and statistical analysis skills.*
