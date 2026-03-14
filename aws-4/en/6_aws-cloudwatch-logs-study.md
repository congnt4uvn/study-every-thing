# AWS CloudWatch Logs — Study Notes (Based on `file.txt`)

## 1) What CloudWatch Logs is
CloudWatch Logs is AWS’s service for **collecting, storing, searching, and analyzing log data** from AWS services and your own applications.

In the console you’ll typically work with:
- **Log groups**: high-level containers (often per app/service).
- **Log streams**: sequences of log events from a single source (e.g., one Lambda instance, one EC2 instance, one container task, etc.).

## 2) Log groups & log streams (key mental model)
- A **log group** can have many **log streams**.
- A **log stream** often maps to an individual producer.
- When using SSM Run Command, you may see streams that represent:
  - Different **instance IDs**
  - Separate output channels like **stdout** and **stderr**

Example pattern you may observe:
- Same Run Command ID across multiple instances
- Per instance you see both `stdout` and `stderr` streams

## 3) Reading and searching logs
Inside a log stream, you can:
- Browse log lines/events
- Search by keyword (e.g., `http`, `installing`) to find matching lines quickly

Tip: keyword search is a fast first step before moving to Insights queries.

## 4) Metric filters (turn log patterns into metrics)
A **metric filter** scans incoming log events in a log group and, on matches, **publishes metric data** to CloudWatch Metrics.

Typical workflow (console):
1. Open a log group
2. Create a **metric filter**
3. Provide a **filter pattern** (e.g., `installing`)
4. Test the pattern against sample logs to confirm matches
5. Configure metric publishing:
   - **Filter name** (e.g., `DemoMetricFilter`)
   - **Metric namespace** (custom, e.g., `DemoFilter`)
   - **Metric name** (e.g., `DemoMetric`)
   - **Metric value** (commonly `1` so you can count occurrences)

Notes:
- The metric may not appear/graph immediately if no new matching log events are arriving.
- Metric filters are a common way to measure errors, warnings, or important events emitted only in logs.

## 5) Alarms on metric filters
Once the metric exists, you can create a **CloudWatch Alarm**:
- Trigger when the metric is above/below a threshold
- Use it to alert (or automate) when specific log patterns happen too frequently

## 6) Subscription filters (stream logs out of CloudWatch Logs)
A **subscription filter** forwards matching log events to a destination such as:
- Amazon OpenSearch/Elasticsearch
- Amazon Kinesis Data Streams
- Amazon Kinesis Data Firehose
- AWS Lambda (custom processing)

Important limit (noted in the walkthrough):
- Up to **two subscription filters per log group**

## 7) Retention settings
You can control how long log events are kept:
- From **never expire** to a defined retention period (up to 120 months / 10 years in the console options shown)

Retention is an easy cost-control lever.

## 8) Exporting logs to Amazon S3
From a log group, you can **export data to S3**:
- Choose the time range to export
- Optionally filter by **log stream prefix**
- Select destination S3 bucket and bucket prefix

This is useful for long-term archiving or downstream analytics.

## 9) Encrypting log groups (KMS)
When creating a log group, you can specify a **KMS key**.
- If set, an encryption setting/KMS Key ID is shown for that log group.

## 10) CloudWatch Logs Insights (query language over logs)
Logs Insights provides a query language to explore logs across one or more log groups.

Key usage tips:
- Always check the **time range** (e.g., past 1 hour vs past 60 days) if you see no results.
- You can **export query results**.
- You can **save queries** for reuse.
- The console includes sample queries/use cases (e.g., latency stats for Lambda, top talkers for VPC Flow Logs).

## 11) Quick practice checklist
- Identify log groups created by services (Lambda, Glue, DataSync, SSM Run Command).
- Open a log group and understand its log streams (instance ID, stdout/stderr).
- Search within a stream for a keyword (e.g., `installing`).
- Create a metric filter that counts occurrences of a keyword.
- Create an alarm on that metric.
- Review subscription filter destinations and the “2 per log group” limit.
- Set retention on a test log group.
- Export a small time range to S3.
- Run a Logs Insights query, then expand the time range if needed.
