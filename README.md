# SQL ↔ Pandas ↔ PySpark Cheat Sheet

**Beginner → Intermediate → Advanced**

---

## Table of Contents

1. [Data Loading](#1-load-data)
2. [Selecting Columns](#2-select-columns)
3. [Filtering Rows](#3-filter-rows)
4. [Multiple Conditions](#4-multiple-conditions)
5. [Sort](#5-sort)
6. [Top N](#6-top-n)
7. [Create New Column](#7-create-new-column)
8. [String Functions](#8-string-functions)
9. [Date Functions](#9-date-functions)
10. [DISTINCT](#10-distinct)
11. [Aggregations](#11-aggregations)
12. [GROUP BY](#12-group-by)
13. [HAVING](#13-having)
14. [Joins](#14-joins)
15. [UNION](#15-union)
16. [NULL Handling](#16-null-handling)
17. [CASE WHEN](#17-case-when)
18. [Window Functions](#18-window-functions)
19. [RANK](#19-rank)
20. [DENSE_RANK](#20-dense_rank)
21. [LAG](#21-lag)
22. [LEAD](#22-lead)
23. [Running Total](#23-running-total)
24. [CTE](#24-cte)
25. [Subquery](#25-subquery)
26. [Pivot](#26-pivot)
27. [Unpivot](#27-unpivot)
28. [Duplicate Removal](#28-duplicate-removal)
29. [Regex](#29-regex)
30. [Explode Arrays](#30-explode-arrays)
31. [JSON Parsing](#31-json-parsing)
32. [Sampling](#32-sampling)
33. [Set Operations](#33-set-operations)
34. [Arrays](#34-arrays)
35. [Struct](#35-struct)
36. [Performance Optimization](#36-performance-optimization)
37. [Read Files](#37-read-files)
38. [Write Files](#38-write-files)
39. [Common PySpark Optimizations](#39-common-pyspark-optimizations)
40. [Advanced Topics](#40-advanced-topics)
41. [Interview Topics Checklist](#interview-topics-checklist)

---

## 1. Load Data

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `CREATE TABLE` | `pd.read_csv()` | `spark.read.csv()` |
| `SELECT * FROM table` | `df` | `df.show()` |

```python
# Pandas
df = pd.read_csv("file.csv")

# PySpark
df = spark.read.option("header", True).csv("file.csv")
```

---

## 2. Select Columns

**SQL**
```sql
SELECT name, salary
FROM employees;
```

**Pandas**
```python
df[['name', 'salary']]
```

**PySpark**
```python
df.select("name", "salary")
```

---

## 3. Filter Rows

**SQL**
```sql
SELECT *
FROM employees
WHERE salary > 50000;
```

**Pandas**
```python
df[df['salary'] > 50000]
```

**PySpark**
```python
df.filter(df.salary > 50000)
```

### IN / NOT IN

**SQL**
```sql
WHERE department IN ('IT', 'HR')
WHERE department NOT IN ('IT', 'HR')
```

**Pandas**
```python
df[df['department'].isin(['IT', 'HR'])]
df[~df['department'].isin(['IT', 'HR'])]
```

**PySpark**
```python
df.filter(col("department").isin("IT", "HR"))
df.filter(~col("department").isin("IT", "HR"))
```

### BETWEEN

**SQL**
```sql
WHERE salary BETWEEN 50000 AND 100000
```

**Pandas**
```python
df[df['salary'].between(50000, 100000)]
```

**PySpark**
```python
df.filter(col("salary").between(50000, 100000))
```

### LIKE / Contains

**SQL**
```sql
WHERE name LIKE 'A%'
```

**Pandas**
```python
df[df['name'].str.startswith('A')]
df[df['name'].str.contains('pattern')]   # supports regex
```

**PySpark**
```python
df.filter(col("name").like("A%"))
df.filter(col("name").rlike("pattern"))  # regex
```

### IS NULL / IS NOT NULL

**SQL**
```sql
WHERE salary IS NULL
WHERE salary IS NOT NULL
```

**Pandas**
```python
df[df['salary'].isna()]
df[df['salary'].notna()]
```

**PySpark**
```python
df.filter(col("salary").isNull())
df.filter(col("salary").isNotNull())
```

---

## 4. Multiple Conditions

**SQL**
```sql
WHERE salary > 50000
AND department = 'IT'
```

**Pandas**
```python
df[(df.salary > 50000) &
   (df.department == "IT")]
```

**PySpark**
```python
df.filter(
    (col("salary") > 50000) &
    (col("department") == "IT")
)
```

---

## 5. Sort

**SQL**
```sql
ORDER BY salary DESC;
```

**Pandas**
```python
df.sort_values("salary", ascending=False)
```

**PySpark**
```python
df.orderBy(col("salary").desc())
```

### Multiple Columns / Mixed Directions

**SQL**
```sql
ORDER BY department ASC, salary DESC
```

**Pandas**
```python
df.sort_values(['department', 'salary'], ascending=[True, False])
```

**PySpark**
```python
df.orderBy(col("department").asc(), col("salary").desc())
```

### Nulls First / Last

**SQL**
```sql
ORDER BY salary DESC NULLS LAST
```

**Pandas**
```python
df.sort_values("salary", ascending=False, na_position='last')
```

**PySpark**
```python
df.orderBy(col("salary").desc_nulls_last())
```

---

## 6. Top N

**SQL**
```sql
SELECT *
FROM employees
LIMIT 10;
```

**Pandas**
```python
df.head(10)
```

**PySpark**
```python
df.limit(10)
```

---

## 7. Create New Column

**SQL**
```sql
SELECT salary * 1.1 AS new_salary
FROM employees;
```

**Pandas**
```python
df['new_salary'] = df.salary * 1.1
```

**PySpark**
```python
df.withColumn("new_salary", col("salary") * 1.1)
```

---

## 8. String Functions

| Operation | SQL | Pandas | PySpark |
|-----------|-----|--------|---------|
| Upper | `UPPER()` | `.str.upper()` | `upper()` |
| Lower | `LOWER()` | `.str.lower()` | `lower()` |
| Length | `LENGTH()` | `.str.len()` | `length()` |
| Trim | `TRIM()` | `.str.strip()` | `trim()` |
| Left trim | `LTRIM()` | `.str.lstrip()` | `ltrim()` |
| Right trim | `RTRIM()` | `.str.rstrip()` | `rtrim()` |
| Substring | `SUBSTR(col,1,3)` | `.str.slice(0,3)` | `substring(col,1,3)` |
| Replace | `REPLACE()` | `.str.replace()` | `regexp_replace()` |
| Concat | `CONCAT(a, b)` | `df['a'] + df['b']` | `concat(col('a'), col('b'))` |
| Split | `SPLIT_PART(col,',',1)` | `.str.split(',')` | `split(col, ',')` |
| Pad left | `LPAD(col,10,'0')` | `.str.zfill(10)` | `lpad(col, 10, '0')` |
| Pad right | `RPAD(col,10,' ')` | `.str.ljust(10)` | `rpad(col, 10, ' ')` |
| Position | `INSTR(col,'a')` | `.str.find('a')` | `instr(col, 'a')` |
| Starts with | `col LIKE 'A%'` | `.str.startswith('A')` | `.startswith('A')` |
| Ends with | `col LIKE '%A'` | `.str.endswith('A')` | `.endswith('A')` |

---

## 9. Date Functions

### Current Date

**SQL**
```sql
CURRENT_DATE
```

**Pandas**
```python
pd.Timestamp.today()
```

**PySpark**
```python
current_date()
```

### Date Difference

**SQL**
```sql
DATEDIFF(day, date1, date2)
```

**Pandas**
```python
(df.date2 - df.date1).dt.days
```

**PySpark**
```python
datediff("date2", "date1")
```

### Extract Parts

| Part | SQL | Pandas | PySpark |
|------|-----|--------|---------|
| Year | `YEAR(date)` | `df['date'].dt.year` | `year(col("date"))` |
| Month | `MONTH(date)` | `df['date'].dt.month` | `month(col("date"))` |
| Day | `DAY(date)` | `df['date'].dt.day` | `dayofmonth(col("date"))` |
| Hour | `HOUR(date)` | `df['date'].dt.hour` | `hour(col("date"))` |
| Day of week | `DAYOFWEEK(date)` | `df['date'].dt.dayofweek` | `dayofweek(col("date"))` |
| Quarter | `QUARTER(date)` | `df['date'].dt.quarter` | `quarter(col("date"))` |

### Date Add / Subtract

**SQL**
```sql
DATE_ADD(date, 7)
DATE_SUB(date, 7)
```

**Pandas**
```python
df['date'] + pd.Timedelta(days=7)
df['date'] - pd.Timedelta(days=7)
```

**PySpark**
```python
date_add(col("date"), 7)
date_sub(col("date"), 7)
```

### Format Date

**SQL**
```sql
DATE_FORMAT(date, '%Y-%m')
```

**Pandas**
```python
df['date'].dt.strftime('%Y-%m')
```

**PySpark**
```python
date_format(col("date"), "yyyy-MM")
```

---

## 10. DISTINCT

**SQL**
```sql
SELECT DISTINCT department
FROM employees;
```

**Pandas**
```python
df['department'].drop_duplicates()
```

**PySpark**
```python
df.select("department").distinct()
```

---

## 11. Aggregations

| Aggregation | SQL | Pandas | PySpark |
|-------------|-----|--------|---------|
| Count | `COUNT(*)` | `df.shape[0]` | `df.count()` |
| Count column | `COUNT(salary)` | `df['salary'].count()` | `count("salary")` |
| Count distinct | `COUNT(DISTINCT dept)` | `df['dept'].nunique()` | `countDistinct("dept")` |
| Sum | `SUM(salary)` | `df['salary'].sum()` | `sum("salary")` |
| Avg | `AVG(salary)` | `df['salary'].mean()` | `avg("salary")` |
| Min | `MIN(salary)` | `df['salary'].min()` | `min("salary")` |
| Max | `MAX(salary)` | `df['salary'].max()` | `max("salary")` |
| Std dev | `STDDEV(salary)` | `df['salary'].std()` | `stddev("salary")` |
| Variance | `VARIANCE(salary)` | `df['salary'].var()` | `variance("salary")` |

### Conditional Count

**SQL**
```sql
COUNT(CASE WHEN salary > 100000 THEN 1 END) AS high_earners
```

**Pandas**
```python
(df['salary'] > 100000).sum()
```

**PySpark**
```python
count(when(col("salary") > 100000, 1)).alias("high_earners")
```

---

## 12. GROUP BY

### Single Column

**SQL**
```sql
SELECT department, AVG(salary)
FROM employees
GROUP BY department;
```

**Pandas**
```python
df.groupby('department')['salary'].mean()
```

**PySpark**
```python
df.groupBy("department").agg(avg("salary"))
```

### Multiple Columns

**SQL**
```sql
SELECT department, gender, AVG(salary)
FROM employees
GROUP BY department, gender;
```

**Pandas**
```python
df.groupby(['department', 'gender'])['salary'].mean()
```

**PySpark**
```python
df.groupBy("department", "gender").agg(avg("salary"))
```

### Multiple Aggregations

**SQL**
```sql
SELECT department,
       AVG(salary)  AS avg_sal,
       MAX(salary)  AS max_sal,
       COUNT(*)     AS headcount
FROM employees
GROUP BY department;
```

**Pandas**
```python
df.groupby('department').agg(
    avg_sal=('salary', 'mean'),
    max_sal=('salary', 'max'),
    headcount=('salary', 'count')
).reset_index()
```

**PySpark**
```python
df.groupBy("department").agg(
    avg("salary").alias("avg_sal"),
    max("salary").alias("max_sal"),
    count("*").alias("headcount")
)
```

### Multiple Columns + Multiple Aggregations

**SQL**
```sql
SELECT department, gender,
       AVG(salary) AS avg_sal,
       MIN(salary) AS min_sal,
       MAX(salary) AS max_sal
FROM employees
GROUP BY department, gender;
```

**Pandas**
```python
df.groupby(['department', 'gender']).agg(
    avg_sal=('salary', 'mean'),
    min_sal=('salary', 'min'),
    max_sal=('salary', 'max')
).reset_index()
```

**PySpark**
```python
df.groupBy("department", "gender").agg(
    avg("salary").alias("avg_sal"),
    min("salary").alias("min_sal"),
    max("salary").alias("max_sal")
)
```

---

## 13. HAVING

**SQL**
```sql
GROUP BY department
HAVING AVG(salary) > 60000
```

**Pandas**
```python
df.groupby("department").salary.mean()\
  .loc[lambda x: x > 60000]
```

**PySpark**
```python
df.groupBy("department")\
  .agg(avg("salary").alias("avg_sal"))\
  .filter(col("avg_sal") > 60000)
```

---

## 14. Joins

### Inner Join

**SQL**
```sql
SELECT *
FROM emp e
INNER JOIN dept d ON e.dept_id = d.dept_id;
```

**Pandas**
```python
pd.merge(emp, dept, on='dept_id')
```

**PySpark**
```python
emp.join(dept, "dept_id", "inner")
```

### Left Join

```python
# Pandas
pd.merge(emp, dept, on='dept_id', how='left')

# PySpark
emp.join(dept, "dept_id", "left")
```

### Right Join

```python
# Pandas
pd.merge(emp, dept, on='dept_id', how='right')

# PySpark
emp.join(dept, "dept_id", "right")
```

### Full Outer Join

```python
# Pandas
pd.merge(emp, dept, on='dept_id', how='outer')

# PySpark
emp.join(dept, "dept_id", "outer")
```

### Join on Multiple Keys

**SQL**
```sql
JOIN dept d ON e.dept_id = d.dept_id
          AND e.location = d.location
```

**Pandas**
```python
pd.merge(emp, dept, on=['dept_id', 'location'])
```

**PySpark**
```python
emp.join(dept, ["dept_id", "location"], "inner")
```

### Join on Different Column Names

**SQL**
```sql
JOIN dept d ON e.dept_id = d.id
```

**Pandas**
```python
pd.merge(emp, dept, left_on='dept_id', right_on='id')
```

**PySpark**
```python
emp.join(dept, emp.dept_id == dept.id, "inner")
```

---

## 15. UNION

**SQL**
```sql
UNION ALL
```

**Pandas**
```python
pd.concat([df1, df2])
```

**PySpark**
```python
df1.union(df2)
```

---

## 16. NULL Handling

### COALESCE

**SQL**
```sql
COALESCE(col, 0)
```

**Pandas**
```python
df['col'].fillna(0)
df.fillna({'salary': 0, 'name': 'Unknown'})  # per column
```

**PySpark**
```python
coalesce(col("x"), lit(0))
```

### NULLIF

**SQL**
```sql
NULLIF(col, 0)   -- returns NULL if col = 0
```

**Pandas**
```python
df['col'].replace(0, None)
```

**PySpark**
```python
nullif(col("x"), lit(0))
```

### IS NULL Check / Drop

**SQL**
```sql
SELECT * FROM emp WHERE salary IS NULL
```

**Pandas**
```python
df[df['salary'].isna()]          # filter nulls
df.dropna(subset=['salary'])     # drop rows where salary is null
df.dropna()                      # drop rows with any null
df.isnull().sum()                # count nulls per column
```

**PySpark**
```python
df.filter(col("salary").isNull())
df.dropna(subset=["salary"])
df.dropna()
```

---

## 17. CASE WHEN

**SQL**
```sql
CASE
  WHEN salary > 100000 THEN 'High'
  ELSE 'Low'
END
```

**Pandas (native)**
```python
# Single condition
df['level'] = df['salary'].where(df['salary'] <= 100000, 'High').mask(df['salary'] > 100000, 'High')

# Cleaner with apply
df['level'] = df['salary'].apply(lambda x: 'High' if x > 100000 else 'Low')
```

**NumPy (inside Pandas) — single condition**
```python
import numpy as np
df['level'] = np.where(df.salary > 100000, 'High', 'Low')
```

**NumPy — multiple branches (equivalent to multi-WHEN)**
```python
conditions = [
    df.salary > 100000,
    df.salary >= 50000,
]
choices = ['High', 'Medium']
df['level'] = np.select(conditions, choices, default='Low')
```

**PySpark**
```python
# Single condition
when(col("salary") > 100000, "High").otherwise("Low")

# Multiple branches
when(col("salary") > 100000, "High")\
  .when(col("salary") >= 50000, "Medium")\
  .otherwise("Low")
```

---

## 18. Window Functions

### Window Definition

**SQL**
```sql
OVER (PARTITION BY dept ORDER BY salary DESC)
```

**PySpark**
```python
from pyspark.sql.window import Window
w = Window.partitionBy("dept").orderBy(desc("salary"))

# With frame spec
w_rows = Window.partitionBy("dept").orderBy("date")\
               .rowsBetween(Window.unboundedPreceding, Window.currentRow)

w_range = Window.partitionBy("dept").orderBy("salary")\
                .rangeBetween(-1000, 1000)
```

### Frame Spec (SQL)

The frame clause defines which rows relative to the current row are included in the window calculation.

**Syntax**
```sql
OVER (
  PARTITION BY col
  ORDER BY col
  {ROWS | RANGE} BETWEEN frame_start AND frame_end
)
```

**Frame boundaries**

| Boundary | Meaning |
|----------|---------|
| `UNBOUNDED PRECEDING` | First row of the partition |
| `N PRECEDING` | N rows before current row |
| `CURRENT ROW` | Current row |
| `N FOLLOWING` | N rows after current row |
| `UNBOUNDED FOLLOWING` | Last row of the partition |

**ROWS vs RANGE**

| Mode | Behaviour |
|------|-----------|
| `ROWS` | Physical offset — counts exact rows |
| `RANGE` | Logical offset — includes all rows with the same ORDER BY value as the boundary row (handles ties) |

**Examples**

```sql
-- Running total (start of partition → current row)
SUM(sales) OVER (
  PARTITION BY dept ORDER BY date
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- 7-day moving average (6 rows back + current)
AVG(sales) OVER (
  ORDER BY date
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)

-- Centred 3-row window (1 before, current, 1 after)
AVG(sales) OVER (
  ORDER BY date
  ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
)

-- Entire partition (same result as no frame clause)
SUM(sales) OVER (
  PARTITION BY dept
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)

-- From current row to end of partition
SUM(sales) OVER (
  PARTITION BY dept ORDER BY date
  ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
)

-- RANGE example: includes all rows with the same date as current row
SUM(sales) OVER (
  PARTITION BY dept ORDER BY date
  RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

### ROW_NUMBER

**SQL**
```sql
ROW_NUMBER() OVER (
  PARTITION BY dept
  ORDER BY salary DESC
)
```

**Pandas**
```python
df.sort_values(['dept', 'salary'], ascending=[True, False])\
  .groupby('dept').cumcount() + 1
```

**PySpark**
```python
w = Window.partitionBy("dept").orderBy(desc("salary"))
row_number().over(w)
```

---

## 19. RANK

**SQL**
```sql
RANK() OVER (PARTITION BY dept ORDER BY salary DESC)
```

**Pandas**
```python
df.groupby('dept')['salary'].rank(method='min', ascending=False)
```

**PySpark**
```python
rank().over(w)
```

---

## 20. DENSE_RANK

**SQL**
```sql
DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC)
```

**Pandas**
```python
df.groupby('dept')['salary'].rank(method='dense', ascending=False)
```

**PySpark**
```python
dense_rank().over(w)
```

---

## 21. LAG

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `LAG(salary)` | `df['salary'].shift(1)` | `lag("salary", 1).over(w)` |

---

## 22. LEAD

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `LEAD(salary)` | `df['salary'].shift(-1)` | `lead("salary", 1).over(w)` |

---

## 23. Running Total / Cumulative Functions

| Function | SQL | Pandas | PySpark |
|----------|-----|--------|---------|
| Running sum | `SUM(sales) OVER (ORDER BY date)` | `df['sales'].cumsum()` | `sum("sales").over(w)` |
| Running max | `MAX(sales) OVER (ORDER BY date)` | `df['sales'].cummax()` | `max("sales").over(w)` |
| Running min | `MIN(sales) OVER (ORDER BY date)` | `df['sales'].cummin()` | `min("sales").over(w)` |
| Running avg | `AVG(sales) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` | `df['sales'].expanding().mean()` | `avg("sales").over(w_rows)` |

### Moving / Rolling Average

**SQL**
```sql
AVG(sales) OVER (
  ORDER BY date
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

**Pandas**
```python
df['sales'].rolling(window=7).mean()
```

**PySpark**
```python
w7 = Window.orderBy("date").rowsBetween(-6, 0)
avg("sales").over(w7)
```

---

## 24. CTE

**SQL**
```sql
WITH temp AS (
  SELECT * FROM emp
)
SELECT * FROM temp;
```

**Pandas**
```python
temp = df.copy()
```

**PySpark**
```python
temp = df
```

---

## 25. Subquery

**SQL**
```sql
WHERE salary > (SELECT AVG(salary) FROM emp)
```

**Pandas**
```python
avg = df.salary.mean()
df[df.salary > avg]
```

**PySpark**
```python
avg_salary = df.agg(avg("salary")).collect()[0][0]
df.filter(col("salary") > avg_salary)
```

---

## 26. Pivot

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `PIVOT()` | `pivot_table()` | `groupBy().pivot()` |

---

## 27. Unpivot

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `UNPIVOT()` | `melt()` | `stack()` |

---

## 28. Duplicate Removal

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `SELECT DISTINCT *` | `drop_duplicates()` | `dropDuplicates()` |

---

## 29. Regex

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `REGEXP_LIKE()` | `str.contains()` | `rlike()` |

---

## 30. Explode Arrays

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `UNNEST()` | `explode()` | `explode()` |

---

## 31. JSON Parsing

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `JSON_VALUE()` | `json_normalize()` | `from_json()` |

---

## 32. Sampling

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `TABLESAMPLE(10 PERCENT)` | `sample(frac=0.1)` | `sample(0.1)` |

---

## 33. Set Operations

### INTERSECT

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `INTERSECT` | `pd.merge(df1, df2)` | `df1.intersect(df2)` |

### EXCEPT

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `EXCEPT` | `pd.merge(df1, df2, how='left', indicator=True).query('_merge=="left_only"').drop('_merge', axis=1)` | `df1.exceptAll(df2)` |

---

## 34. Arrays

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `ARRAY_AGG()` | `groupby().agg(list)` | `collect_list()` |

---

## 35. Struct

**PySpark**
```python
struct(col("name"), col("salary"))
```

---

## 36. Performance Optimization

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `CREATE INDEX` | `astype("category")` | `cache()` |
| `ANALYZE TABLE` | vectorization | `persist()` |
| `PARTITION` | `query()` | `broadcast()` |
| | | `repartition()` |
| | | `coalesce()` |
| | | `partitionBy()` |

---

## 37. Read Files

| Format | Pandas | PySpark |
|--------|--------|---------|
| CSV | `pd.read_csv()` | `spark.read.csv()` |
| JSON | `pd.read_json()` | `spark.read.json()` |
| Parquet | `pd.read_parquet()` | `spark.read.parquet()` |

---

## 38. Write Files

| Format | Pandas | PySpark |
|--------|--------|---------|
| CSV | `df.to_csv()` | `df.write.csv()` |
| Parquet | `df.to_parquet()` | `df.write.parquet()` |
| Delta Lake | — | `df.write.format("delta")` |

---

## 39. Common PySpark Optimizations

```python
df.cache()            # Cache in memory
df.persist()          # Persist with storage level
broadcast(df2)        # Broadcast join for small tables
df.repartition(10)    # Increase partitions
df.coalesce(2)        # Reduce partitions
```

---

## 40. Advanced Topics

### Cumulative Average

**SQL**
```sql
AVG(sales) OVER (
  ORDER BY date
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

### NTILE

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `NTILE(4)` | `pd.qcut(df['salary'], q=4, labels=False) + 1` | `ntile(4).over(w)` |

### Percent Rank

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `PERCENT_RANK()` | `df['salary'].rank(pct=True)` | `percent_rank().over(w)` |

### CUME_DIST

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `CUME_DIST()` | `df['salary'].rank(pct=True, method='max')` | `cume_dist().over(w)` |

---

## Interview Topics Checklist

### Beginner
- [ ] SELECT
- [ ] WHERE
- [ ] ORDER BY
- [ ] GROUP BY
- [ ] HAVING
- [ ] DISTINCT
- [ ] CASE WHEN
- [ ] JOINS

### Intermediate
- [ ] Window functions
- [ ] CTE
- [ ] Subqueries
- [ ] UNION
- [ ] Pivot
- [ ] Date functions
- [ ] String functions

### Advanced
- [ ] Ranking functions
- [ ] LAG / LEAD
- [ ] Running totals
- [ ] JSON handling
- [ ] Arrays and Structs
- [ ] Explode
- [ ] Broadcast joins
- [ ] Partitioning
- [ ] Repartition vs Coalesce
- [ ] Caching
- [ ] Persistence
- [ ] Catalyst Optimizer
- [ ] Lazy Evaluation
- [ ] Narrow vs Wide Transformations
- [ ] Shuffle
- [ ] Skew handling
- [ ] Bucketing
- [ ] Delta Lake
- [ ] AQE (Adaptive Query Execution)
