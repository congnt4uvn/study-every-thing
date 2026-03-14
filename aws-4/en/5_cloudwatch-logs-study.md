# AWS Study Notes — CloudWatch Logs

## 1) What CloudWatch Logs is for
- **CloudWatch Logs** is a managed service to **store and manage application/service logs in AWS**.
- It is a central place to collect logs from many AWS services and your own workloads.

## 2) Core concepts
### Log group
- A **log group** is a logical container for logs.
- The name is **whatever you choose** (commonly an application name).

### Log stream
- Inside a log group, you have **log streams**.
- A log stream typically represents a **specific log source/instance**, such as:
  - an application instance,
  - a specific log file,
  - a specific container (for example in a cluster).

### Retention (expiration) policy
- You define how long logs are kept:
  - **Never expire** (indefinite retention), or
  - expire from **1 day up to 10 years**.

### Encryption
- Logs are **encrypted by default**.
- You can optionally configure **KMS encryption (customer-managed key)**.

## 3) Where logs can be sent (destinations)
CloudWatch Logs data can be delivered to:
- **Amazon S3** (batch export)
- **Kinesis Data Streams** (real-time streaming)
- **Kinesis Data Firehose** (near real-time delivery)
- **AWS Lambda**
- **Amazon OpenSearch Service**

## 4) How logs get into CloudWatch Logs (sources)
Ways to send logs:
- Using the **SDK**
- **CloudWatch Logs Agent** (older / deprecated)
- **CloudWatch Unified Agent** (recommended vs the older Logs Agent)

AWS services that commonly publish logs to CloudWatch Logs:
- **Elastic Beanstalk** (application logs)
- **ECS** (container logs)
- **AWS Lambda** (function logs)
- **VPC Flow Logs** (VPC network traffic metadata)
- **API Gateway** (API requests)
- **CloudTrail** (can send based on filter)
- **Route 53** (DNS query logs)

## 5) Querying logs: CloudWatch Logs Insights
**CloudWatch Logs Insights** is the query capability inside CloudWatch Logs.

What you do:
- Write a query in the **Logs Insights query language**
- Choose a **timeframe**
- Get results with **visualizations**, and see the **log lines** behind them

Helpful features:
- Many **console-provided sample queries** (recent events, errors/exceptions, IP filtering, etc.)
- Fields are **automatically discovered** from log events
- You can:
  - filter based on conditions,
  - compute aggregate statistics,
  - sort events,
  - limit results.
- Save queries and add to **CloudWatch Dashboards**.
- Query **multiple log groups at once**, even across **different accounts**.

Important limitation:
- Logs Insights is a **query engine, not a real-time engine** — it queries **historical data** when you run it.

## 6) Export vs subscription (batch vs real-time)
### Batch export to S3
- Export logs to **Amazon S3** in batch.
- Export can take **up to 12 hours**.
- API to start export: **`CreateExportTask`**.
- Not real-time / not near real-time.

### Real-time streaming: subscription filters
- Use **CloudWatch Logs subscription filters** for **real-time streaming**.
- Destinations can include:
  - **Kinesis Data Streams**
  - **Kinesis Data Firehose**
  - **AWS Lambda**
- You can set a **subscription filter** to select which log events are delivered.

## 7) Cross-account / cross-region log aggregation (high level)
You can aggregate logs from **multiple accounts and regions** into a common destination.

Typical flow described:
- CloudWatch Logs (multiple accounts/regions)
  → **Subscription filter**
  → **Destination** (represents a Kinesis Data Stream in a recipient account)
  → (optionally) **Kinesis Data Firehose**
  → **Amazon S3** (near real-time delivery)

Key building blocks:
- **Destination**: a virtual representation of the recipient’s Kinesis Data Stream.
- **Destination access policy**: allows the sender account to send to the destination.
- **IAM role (recipient account)**: permits putting records into Kinesis Data Stream.
- Trust/assume-role setup so the sender account can use that role.

## 8) Quick self-check (study prompts)
- Explain the difference between a **log group** and a **log stream**.
- When would you use **S3 export** vs a **subscription filter**?
- Why is Logs Insights considered **not real-time**?
- Name at least **4 AWS services** that can write logs to CloudWatch Logs.
- Describe the **cross-account streaming** pieces: destination, policy, role.

## 9) Mini flashcards
- **Retention range** → 1 day to 10 years (or never expire)
- **Batch export API** → `CreateExportTask`
- **Real-time delivery mechanism** → Subscription filter
- **Default encryption** → Enabled (optional KMS customer key)
