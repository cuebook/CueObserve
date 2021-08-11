# Data Sources

Below are sample dataset queries for different data warehouses and databases.

## BigQuery

```sql
SELECT
TIMESTAMP_TRUNC(CreatedTS, DAY) as OrderDate, -- HOUR or DAY granularity
City, State, -- dimensions
COUNT(1) as Orders, SUM(IFNULL(Order_Amount,0)) as OrderAmount -- measures
FROM ORDERS
WHERE CreatedTS >= TIMESTAMP_SUB(TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), DAY), INTERVAL 400 DAY)  -- limit historical data to use for forecasting
GROUP BY 1, 2, 3
ORDER BY 1
```

## Redshift

```sql
SELECT
DATE_TRUNC('day', CreatedTS) as OrderDate, -- 'hour' or 'day' granularity
City, State, -- dimensions
COUNT(1) as Orders, SUM(NVL(Order_Amount,0)) as OrderAmount -- measures
FROM ORDERS
WHERE CreatedTS >= DATE_TRUNC('day', SYSDATE) - INTERVAL '400 days'  -- limit historical data to use for forecasting
GROUP BY 1, 2, 3
ORDER BY 1
```

## Snowflake

```sql
SELECT
DATE_TRUNC('DAY', CreatedTS) as OrderDate, -- 'HOUR' or 'DAY' granularity
City, State, -- dimensions
COUNT(1) as Orders, SUM(IFNULL(Order_Amount,0)) as OrderAmount -- measures
FROM ORDERS
WHERE CreatedTS >= DATE_TRUNC('DAY', CURRENT_TIMESTAMP) - INTERVAL '400 days'  -- limit historical data to use for forecasting
GROUP BY 1, 2, 3
ORDER BY 1
```

## Postgres

```sql
SELECT
DATE_TRUNC('day', CreatedTS) as OrderDate, -- 'hour' or 'day' granularity
City, State, -- dimensions
COUNT(1) as Orders, SUM(COALESCE(Order_Amount,0)) as OrderAmount -- measures
FROM ORDERS
WHERE CreatedTS >= DATE_TRUNC('day', now()) - INTERVAL '400 days' -- limit historical data to use for forecasting
GROUP BY 1, 2, 3
ORDER BY 1
```

## MySQL

### Hourly granularity

```sql
SELECT
DATE_FORMAT(CreatedTS, '%Y-%m-%d %H') as OrderDate,
City, State, -- dimensions
COUNT(1) as Orders, SUM(IFNULL(Order_Amount,0)) as OrderAmount -- measures
FROM ORDERS
WHERE CreatedTS >= DATE_SUB(DATE_FORMAT(now(), '%Y-%m-%d %H'), INTERVAL 21 DAY) -- limit historical data to use for forecasting
GROUP BY 1, 2, 3
ORDER BY 1
```

### Daily granularity

```sql
SELECT
DATE(CreatedTS) as OrderDate,
City, State, -- dimensions
COUNT(1) as Orders, SUM(IFNULL(Order_Amount,0)) as OrderAmount -- measures
FROM ORDERS
WHERE CreatedTS >= DATE_SUB(CURDATE(), INTERVAL 400 DAY) -- limit historical data to use for forecasting
GROUP BY 1, 2, 3
ORDER BY 1
```

## Druid

```sql
SELECT
DATE_TRUNC('DAY', __time) as OrderDate, -- 'HOUR' or 'DAY' granularity
City, State, -- dimensions
SUM("count") as Orders, SUM(Order_Amount) as OrderAmount -- measures
FROM ORDERS
WHERE __time >= CURRENT_TIMESTAMP - INTERVAL '13' MONTH -- limit historical data to use for forecasting
GROUP BY 1, 2, 3
ORDER BY 1
```

