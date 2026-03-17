# Amazon Athena — Study Notes

---

## What is Amazon Athena?

**Amazon Athena** is a **serverless query service** that lets you analyze data stored in **Amazon S3 buckets** using standard **SQL**.

- Built on the **Presto engine**
- No infrastructure to provision or manage
- Works directly on data in S3 — no data movement required

---

## Supported File Formats

| Format   | Notes                          |
|----------|--------------------------------|
| CSV      | Common flat-file format        |
| JSON     | Semi-structured data           |
| ORC      | Columnar — recommended         |
| Avro     | Row-based binary format        |
| Parquet  | Columnar — recommended ★       |

> **Tip:** Apache **Parquet** and **ORC** are the recommended formats for best performance and cost savings.

---

## Pricing

- **Pay per query** — fixed price per **terabyte of data scanned**
- Reducing the amount of data scanned = lower cost

---

## Common Use Cases

- Ad hoc queries
- Business intelligence (BI), analytics, and reporting
- Log analysis from AWS services:
  - VPC Flow Logs
  - Load Balancer Logs
  - AWS CloudTrail Trails

> **Exam Tip:** When you see *"analyze data in S3 using a serverless SQL engine"* → think **Athena**.

---

## Integration — Amazon QuickSight

```
Amazon QuickSight  ──►  Amazon Athena  ──►  Amazon S3
```

Athena is commonly paired with **Amazon QuickSight** to build reports and dashboards.

---

## Performance Improvements

### 1. Use Columnar Data Formats
- Use **Apache Parquet** or **ORC**
- Only the columns you query are scanned → **huge cost and performance improvement**
- Use **AWS Glue** (ETL) to convert CSV → Parquet

### 2. Compress Data
- Compress files to reduce the amount of data scanned
- Supported compression codecs: GZIP, SNAPPY, ZSTD, etc.

### 3. Partition Datasets in S3
Organize data in S3 using a path structure that maps to columns:

```
s3://my-bucket/flight-data/year=1991/month=01/day=01/
```

- Athena uses the partition path to **skip irrelevant folders**
- Filter by year/month/day → only scans the matching partition
- Dramatically reduces data scanned

### 4. Use Larger Files
- Prefer files **≥ 128 MB**
- Many small files → high overhead for Athena
- Larger files → easier and faster to scan

---

## Federated Query

Athena can query data **beyond S3** — any relational, non-relational, or custom data source.

### How it works

```
Amazon Athena
    │
    ▼
Lambda Function (Data Source Connector)  ──►  External Data Source
```

Each **Data Source Connector** is a **Lambda function** that runs federated queries against other services.

### Supported Sources (examples)

| AWS Services          | On-Premises / Other |
|-----------------------|---------------------|
| ElastiCache           | HBase on EMR        |
| Amazon DynamoDB       | Any on-premises DB  |
| Amazon RDS / Aurora   | SQL Server / MySQL  |
| Amazon Redshift       |                     |
| DocumentDB            |                     |
| CloudWatch Logs       |                     |

- Query results can be **stored back in Amazon S3** for later analysis.

---

## Summary Table

| Feature              | Detail                                                  |
|----------------------|---------------------------------------------------------|
| Type                 | Serverless query service                                |
| Language             | Standard SQL                                            |
| Engine               | Presto                                                  |
| Data source          | Amazon S3 (primary) + federated sources                 |
| Best formats         | Apache Parquet, ORC                                     |
| Pricing model        | Per TB scanned                                          |
| ETL companion        | AWS Glue                                                |
| BI companion         | Amazon QuickSight                                       |
| Federated connector  | AWS Lambda (Data Source Connector)                      |

---

## Key Exam Points

1. **Serverless** — no database to provision
2. Use **Parquet/ORC** for cost and performance
3. Use **Glue** to convert data formats (e.g., CSV → Parquet)
4. **Partition** S3 data to minimize scans
5. Use **larger files** (≥ 128 MB) for efficiency
6. **Federated Query** via Lambda connectors can reach any data source
7. Results of federated queries are saved to **S3**
