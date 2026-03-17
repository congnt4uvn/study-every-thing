# AWS Athena – Querying Data from S3

## Overview

**Amazon Athena** is a serverless, interactive query service that lets you analyze data stored in **Amazon S3** using standard **SQL** — without setting up or managing any server infrastructure.

---

## Key Concepts

| Term | Description |
|------|-------------|
| **Athena** | Serverless SQL query engine for S3 data |
| **S3 Bucket** | Object storage where your raw data lives |
| **Query Result Location** | A separate S3 bucket where Athena saves query output |
| **Database** | Logical container for tables in Athena |
| **Table** | Schema definition mapped to files in S3 |

---

## Step-by-Step: Using Athena to Query S3

### Step 1 – Set Up a Query Result Location

Before running any query, Athena requires an S3 bucket to store query results.

1. Open the **Athena Query Editor**.
2. Go to **Settings** → enter an S3 bucket path as the result location.
3. Tip: Use the S3 browser inside Athena settings to avoid typos when entering the bucket path.

```
s3://your-athena-results-bucket/
```

> Always include a **trailing slash** at the end of the S3 path.

---

### Step 2 – Create a Database

Run the following SQL in the Athena editor to create a new database:

```sql
CREATE DATABASE s3_access_logs_db;
```

After creation, the new database will appear in the left-hand panel of the Query Editor.

---

### Step 3 – Create a Table

Create a table that maps to the S3 access log files stored in your bucket.

```sql
CREATE EXTERNAL TABLE s3_access_logs (
  bucket_owner STRING,
  bucket       STRING,
  request_datetime STRING,
  remote_ip    STRING,
  requester    STRING,
  request_id   STRING,
  operation    STRING,
  key          STRING,
  request_uri  STRING,
  http_status  INT,
  error_code   STRING,
  bytes_sent   BIGINT,
  object_size  BIGINT,
  ...
)
ROW FORMAT ...
LOCATION 's3://your-source-bucket/';
```

> The table definition (with full `ROW FORMAT` and column list) comes directly from the **Amazon S3 + Athena documentation**. Only the `LOCATION` value needs to be customized.

- Set `LOCATION` to your source S3 bucket (the one that contains the actual data).
- Include the prefix (sub-folder) if your objects are not at the bucket root:
  ```
  LOCATION 's3://your-bucket/prefix/'
  ```

---

### Step 4 – Preview the Table

Once the table is created, you can quickly preview 10 rows:

- Click the **three-dot menu** next to the table name in the left panel.
- Select **Preview Table**.

This auto-generates and runs:

```sql
SELECT * FROM s3_access_logs LIMIT 10;
```

---

### Step 5 – Run Analytics Queries

#### Count Requests by HTTP Status and Operation

```sql
SELECT http_status, operation, request_uri, COUNT(*) AS request_count
FROM s3_access_logs
GROUP BY http_status, operation, request_uri
ORDER BY request_count DESC;
```

This helps you see a breakdown such as:
- `404` — Not Found errors (unexpected? investigate!)
- `200` — Successful requests
- `403` — **Unauthorized access attempts** (security concern)

#### Detect Unauthorized Access (403 Errors)

```sql
SELECT *
FROM s3_access_logs
WHERE http_status = 403;
```

Use this query to identify who might be trying to access your bucket without permission.

---

## Why Use Athena?

- **Serverless** — no infrastructure to set up or manage.
- **Pay-per-query** — charges based on data scanned.
- **Standard SQL** — easy ramp-up for anyone familiar with SQL.
- **Works directly on S3** — no ETL pipeline or data loading needed.
- **Scalable** — handles terabytes of data automatically.

---

## Common Use Cases

- Analyzing **S3 access logs** for security auditing.
- Running **ad-hoc analytics** on raw log or event data.
- Querying **CloudTrail**, **ELB**, or **VPC Flow Logs** stored in S3.
- Cost analysis and reporting on data stored in S3.

---

## Summary

```
S3 Bucket (raw data)
       ↓
  Create Database  →  CREATE DATABASE ...
       ↓
  Create Table     →  CREATE EXTERNAL TABLE ... LOCATION 's3://...'
       ↓
  Run SQL Queries  →  SELECT, GROUP BY, WHERE ...
       ↓
  Results saved to →  S3 Result Bucket
```

Athena makes it extremely easy to gain insights from data sitting in S3 using just SQL — no servers, no loading, no complexity.

---

## Practice Questions

1. What must you configure before running your first Athena query?
2. What SQL statement is used to create a new database in Athena?
3. How do you specify where the source data is located when creating a table?
4. What HTTP status code indicates an unauthorized access attempt in S3 logs?
5. Why is Athena described as "serverless"? What does this mean for you as a user?

---

*Source: AWS Athena – Querying S3 Data (Lecture Notes)*
