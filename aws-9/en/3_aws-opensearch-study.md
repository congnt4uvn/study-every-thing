# AWS Study Notes: Amazon OpenSearch Service

## 1) What Is Amazon OpenSearch Service?
Amazon OpenSearch Service is AWS managed search and analytics service.
It is the successor to Amazon Elasticsearch Service.

## 2) Why Use OpenSearch?
OpenSearch is useful when you need:
- Full-text search across many fields
- Partial match search (for example, searching by part of a product name)
- Fast analytics on indexed data

Compared to DynamoDB:
- DynamoDB query is mainly by primary key or indexes
- OpenSearch supports flexible searching across documents and fields

## 3) Provisioning Models
You can deploy OpenSearch in two ways:
- Managed clusters: you choose and run provisioned instances
- Serverless: AWS handles scaling and operations automatically

## 4) Query Language and SQL
- OpenSearch has its own query language
- SQL is not native by default
- SQL compatibility can be enabled with a plugin

## 5) Data Ingestion Sources
Common data sources into OpenSearch:
- Amazon Kinesis Data Firehose
- AWS IoT
- Amazon CloudWatch Logs
- Custom applications

## 6) Security Features
OpenSearch can integrate with:
- Amazon Cognito
- AWS IAM

Encryption support:
- Encryption at rest
- Encryption in transit (in-flight encryption)

## 7) Visualization and Analytics
Use OpenSearch Dashboards to:
- Build visualizations
- Explore and analyze indexed data

## 8) Common Architecture Patterns

### Pattern A: DynamoDB + OpenSearch for Search
1. Application writes data to DynamoDB
2. DynamoDB Streams captures changes
3. AWS Lambda reads stream events
4. Lambda indexes data into OpenSearch in near real time
5. Application searches in OpenSearch and gets item ID
6. Application reads full item from DynamoDB

Why this pattern is common:
- DynamoDB remains source of truth
- OpenSearch provides rich search capabilities

### Pattern B: CloudWatch Logs to OpenSearch
Option 1 (real time):
- CloudWatch Logs Subscription Filter -> AWS managed Lambda -> OpenSearch

Option 2 (near real time):
- CloudWatch Logs Subscription Filter -> Kinesis Data Firehose -> OpenSearch

### Pattern C: Kinesis to OpenSearch
Option 1 (near real time):
- Kinesis Data Streams -> Kinesis Data Firehose -> (optional Lambda transform) -> OpenSearch

Option 2 (real time with custom code):
- Kinesis Data Streams -> custom Lambda consumer -> OpenSearch

## 9) Real-Time vs Near Real-Time
- Lambda stream processing is commonly real time
- Firehose delivery is typically near real time (buffered)

## 10) Exam and Interview Key Points
- OpenSearch is for search plus analytics
- Often paired with DynamoDB, not a full replacement
- DynamoDB stores primary data; OpenSearch indexes searchable views
- Firehose is simpler, near real time
- Lambda gives more control and can be fully real time
- Dashboards is used for visualization

## 11) Quick Review Questions
1. Why keep DynamoDB as source of truth when using OpenSearch?
2. What is the difference between Firehose and Lambda ingestion?
3. Which service would you use for partial text search?
4. When would serverless OpenSearch be a better choice?

## 12) One-Line Summary
Use Amazon OpenSearch Service when your application needs powerful search and analytics, while keeping your primary data in systems like DynamoDB.