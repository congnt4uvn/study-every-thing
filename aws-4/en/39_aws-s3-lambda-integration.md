# AWS S3 Event Notifications with Lambda Integration

## Overview
S3 event notifications provide a way to get notified whenever specific actions occur on objects in your S3 bucket. This integration with Lambda enables powerful event-driven architectures.

## S3 Event Notifications

### What Are S3 Event Notifications?
S3 event notifications allow you to receive alerts when:
- An object is **created**
- An object is **removed**
- An object is **restored**
- **Replication** is happening

### Filtering Options
- **Prefix filtering**: Filter by object path prefix
- **Suffix filtering**: Filter by file extension or suffix

### Classic Use Case
**Thumbnail Generation**: Automatically generate thumbnail images for every image uploaded to Amazon S3.

## Integration Patterns

### 1. S3 → SNS → SQS (Fan-out Pattern)
- S3 sends events to an SNS topic
- SNS fans out to multiple SQS queues
- Multiple consumers can process the same event

### 2. S3 → SQS → Lambda
- S3 sends events to an SQS queue
- Lambda function reads directly from the SQS queue
- Provides buffering and retry capabilities

### 3. S3 → Lambda (Direct Invocation)
- S3 event notification directly invokes Lambda function
- **Asynchronous invocation**
- Simplest integration pattern

## Error Handling
- Configure a **Dead-Letter Queue (DLQ)** using SQS
- Captures failed invocations for later analysis
- Prevents event loss

## Important Considerations

### Event Delivery Time
- Typically delivers events in **seconds**
- Can sometimes take **a minute or longer**
- Plan for eventual consistency

### Versioning for Reliability
⚠️ **Critical**: Enable versioning on your S3 bucket to prevent event loss.

**Why?** If two writes occur on the same object at the exact same time:
- **Without versioning**: You may receive only ONE notification instead of TWO
- **With versioning**: Each write creates a unique version, ensuring all notifications are sent

## Simple Architecture Pattern

```
S3 Bucket (New File Event)
    ↓
Lambda Function (Process File)
    ↓
Data Storage
    ├── DynamoDB Table
    └── RDS Database
```

### Workflow
1. New file uploaded to S3 bucket
2. S3 triggers event notification
3. Lambda function automatically invoked
4. Lambda processes the file
5. Data inserted into DynamoDB or RDS database

## Best Practices
- ✅ Always enable S3 bucket versioning
- ✅ Configure DLQ for failed processing
- ✅ Use appropriate filtering to reduce unnecessary invocations
- ✅ Monitor Lambda execution metrics
- ✅ Implement idempotent Lambda functions (handle duplicate events gracefully)

## Key Takeaways
- S3 event notifications enable real-time, event-driven processing
- Multiple integration patterns available (direct Lambda, via SNS, via SQS)
- Versioning is crucial for event reliability
- Asynchronous invocation provides scalability but requires proper error handling
