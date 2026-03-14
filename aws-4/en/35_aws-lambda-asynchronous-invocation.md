# AWS Lambda - Asynchronous Invocation

## Overview

AWS Lambda supports different invocation types. This document focuses on **asynchronous invocations**, which differ from synchronous invocations in how events are processed and handled.

## What is Asynchronous Invocation?

Asynchronous invocation is used when AWS services invoke Lambda functions behind the scenes without waiting for an immediate response.

### Services that Use Asynchronous Invocation

- **Amazon S3** - S3 event notifications for new files
- **Amazon SNS** - SNS topics
- **Amazon CloudWatch Events** - Event-driven triggers
- And more...

## How It Works

### Example: S3 Bucket Event Flow

1. **Event Trigger**: A new file is uploaded to an S3 bucket
2. **S3 Event Notification**: S3 generates an event notification
3. **Lambda Service**: The event is sent to the Lambda service
4. **Internal Event Queue**: Events are placed in an internal event queue
5. **Processing**: Lambda function reads and processes events from the queue

```
S3 Bucket → S3 Event Notification → Lambda Service → Event Queue → Lambda Function
```

## Retry Mechanism

When things go wrong, Lambda automatically retries failed invocations:

- **Total Attempts**: 3 tries
- **First Try**: Immediate
- **Second Try**: 1 minute after the first
- **Third Try**: 2 minutes after the second

### Important Considerations

⚠️ **Lambda functions may process the same event multiple times** due to retries.

## Idempotency

### What is Idempotency?

**Idempotency** means that processing the same event multiple times produces the same result.

### Why It Matters

- Retries can cause duplicate processing
- Non-idempotent functions may cause issues (e.g., duplicate database entries, multiple charges)
- Your Lambda function **should be idempotent** to handle retries safely

### Observability

When retries occur, you will see:
- **Duplicate log entries** in CloudWatch Logs
- Multiple execution records for the same event

## Dead Letter Queue (DLQ)

### Purpose

After all retry attempts are exhausted, failed events can be sent to a Dead Letter Queue for further processing.

### Supported DLQ Services

- **Amazon SQS** - Simple Queue Service
- **Amazon SNS** - Simple Notification Service

### How to Use DLQ

1. Define a DLQ (SQS queue or SNS topic)
2. Configure your Lambda function to use the DLQ
3. Failed events will be sent to the DLQ after all retries fail
4. Process or investigate failed events later

## Key Takeaways

✅ Asynchronous invocations use an internal event queue
✅ Lambda automatically retries failed events 3 times
✅ Always design Lambda functions to be idempotent
✅ Configure a DLQ to handle permanently failed events
✅ Monitor CloudWatch Logs for duplicate entries indicating retries

## Best Practices

1. **Design for Idempotency**: Ensure your function can safely process the same event multiple times
2. **Implement DLQ**: Always configure a Dead Letter Queue to capture failed events
3. **Monitor Retries**: Watch CloudWatch Logs for patterns indicating persistent failures
4. **Handle Errors Gracefully**: Implement proper error handling to minimize retry scenarios
5. **Set Appropriate Timeouts**: Configure function timeout to prevent unnecessary retries

---

*Study Material - AWS Lambda Asynchronous Invocation*
