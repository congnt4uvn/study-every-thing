# AWS DynamoDB Streams - Study Guide

## Overview

DynamoDB Streams is a feature that captures an ordered list of item-level modifications (create, update, delete) happening within a DynamoDB table.

## Key Concepts

### What are DynamoDB Streams?

- **Ordered stream** of item-level modifications in a table
- Captures all changes: inserts, updates, and deletes
- Represents a time-ordered sequence of modifications

### Stream Destinations

Stream records can be sent to multiple AWS services:

1. **Kinesis Data Streams (KDS)**
   - Forward DynamoDB Streams to Kinesis for further processing

2. **AWS Lambda Functions**
   - Read directly from DynamoDB Streams
   - Enable serverless event-driven processing

3. **Kinesis Client Library (KCL) Applications**
   - Custom applications can consume stream data directly

## Important Limitations

- **Data Retention**: 24 hours only
- **Action Required**: Persist data to durable storage (e.g., Kinesis Data Streams) or process quickly with Lambda/KCL

## Common Use Cases

### 1. Real-Time Reactions
React to changes in DynamoDB tables as they happen

### 2. User Engagement
- Send welcome emails to new users
- Trigger notifications based on data changes

### 3. Analytics
- Perform real-time analytics on data changes
- Stream data to analytics platforms

### 4. Data Transformation
- Create derivative tables in DynamoDB
- Transform and enrich data in real-time

### 5. Search Capabilities
- Send data to Amazon OpenSearch for indexing
- Enable full-text search on DynamoDB data

### 6. Global Tables
- Enable cross-region replication
- Foundation for DynamoDB Global Tables feature

## Architecture Example

```
Application
    ↓
  (create/update/delete)
    ↓
DynamoDB Table
    ↓
DynamoDB Stream
    ↓
Kinesis Data Streams (KDS)
    ↓
Kinesis Data Firehose
    ↓
Amazon Redshift (Analytics)
```

**Flow Description:**
1. Application performs CRUD operations on DynamoDB table
2. Changes appear in DynamoDB Stream
3. Stream is forwarded to Kinesis Data Streams
4. Kinesis Data Firehose processes the stream
5. Data is loaded into Amazon Redshift for analytics queries

## Best Practices

- ✅ Process streams within 24-hour retention window
- ✅ Use Lambda for simple event-driven processing
- ✅ Forward to Kinesis Data Streams for longer retention
- ✅ Implement error handling and retry logic
- ✅ Monitor stream processing with CloudWatch

## Study Tips

- Understand the 24-hour retention limitation
- Know the different consumption methods (Lambda, KDS, KCL)
- Be familiar with common use cases for exam scenarios
- Remember that streams are required for Global Tables

---

**Related AWS Services:**
- Amazon DynamoDB
- AWS Lambda
- Amazon Kinesis Data Streams
- Amazon Kinesis Data Firehose
- Amazon OpenSearch
- Amazon Redshift
