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
| Substring | `SUBSTR()` | `.str.slice()` | `substring()` |
| Replace | `REPLACE()` | `.str.replace()` | `regexp_replace()` |

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

### Count

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `COUNT(*)` | `df.shape[0]` | `df.count()` |

### Sum

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `SUM(salary)` | `df.salary.sum()` | `sum("salary")` |

### Avg

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `AVG(salary)` | `df.salary.mean()` | `avg("salary")` |

---

## 12. GROUP BY

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
df.fillna(0)
```

**PySpark**
```python
coalesce(col("x"), lit(0))
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

**Pandas**
```python
np.where(df.salary > 100000, 'High', 'Low')
```

**PySpark**
```python
when(col("salary") > 100000, "High").otherwise("Low")
```

---

## 18. Window Functions

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
df.sort_values(['dept', 'salary'], ascending=False)\
  .groupby('dept').cumcount() + 1
```

**PySpark**
```python
w = Window.partitionBy("dept").orderBy(desc("salary"))
row_number().over(w)
```

---

## 19. RANK

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `RANK()` | `rank()` | `rank().over(w)` |

---

## 20. DENSE_RANK

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `DENSE_RANK()` | `rank(method='dense')` | `dense_rank().over(w)` |

---

## 21. LAG

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `LAG(salary)` | `shift(1)` | `lag("salary", 1)` |

---

## 22. LEAD

| SQL | Pandas | PySpark |
|-----|--------|---------|
| `LEAD(salary)` | `shift(-1)` | `lead("salary", 1)` |

---

## 23. Running Total

**SQL**
```sql
SUM(sales) OVER (ORDER BY date)
```

**Pandas**
```python
df['sales'].cumsum()
```

**PySpark**
```python
sum("sales").over(w)
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
| `EXCEPT` | `concat + drop_duplicates` | `exceptAll()` |

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

| SQL | PySpark |
|-----|---------|
| `NTILE(4)` | `ntile(4).over(w)` |

### Percent Rank

| SQL | PySpark |
|-----|---------|
| `PERCENT_RANK()` | `percent_rank().over(w)` |

### CUME_DIST

| SQL | PySpark |
|-----|---------|
| `CUME_DIST()` | `cume_dist().over(w)` |

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
