# AWS Lambda Destinations

## Overview
Lambda Destinations is a feature introduced in November 2019 that allows you to send the results of asynchronous Lambda invocations to various AWS services.

## Problem Statement
Before Lambda Destinations, it was difficult to:
- Track whether asynchronous invocations or event mappers succeeded or failed
- Retrieve data from these operations
- Handle results systematically

## Solution: Lambda Destinations
Lambda Destinations allows you to send the result of an asynchronous invocation or the failure of an event mapper to specific AWS services.

## Asynchronous Invocations

### Destination Options
You can define destinations for both:
- **Successful events** - when processing completes successfully
- **Failed events** - when processing fails

### Supported Targets
- **Amazon SQS** (Simple Queue Service)
- **Amazon SNS** (Simple Notification Service)
- **AWS Lambda** (another Lambda function)
- **Amazon EventBridge** (CloudWatch Events)

### Example Flow
```
S3 Event → Lambda Function (async)
  ├─ Success → Destination (SQS/SNS/Lambda/EventBridge)
  └─ Failure → Destination (SQS/SNS/Lambda/EventBridge)
```

## Destinations vs Dead Letter Queues (DLQ)

### Dead Letter Queues (DLQ) - Legacy Approach
- Only handles **failed** events
- Limited targets: SQS and SNS only

### Lambda Destinations - Recommended Approach
- Handles both **successful** and **failed** events
- More target options: SQS, SNS, Lambda, and EventBridge
- Can be used alongside DLQ (but destinations are preferred)

**Recommendation:** Use Lambda Destinations instead of DLQ for new implementations.

## Event Source Mapping

### Use Case
When an event batch from streaming sources cannot be processed and gets discarded.

### Supported Targets (for failures only)
- Amazon SQS
- Amazon SNS

### Example Flow
```
Kinesis Data Stream → Event Source Mapping → Lambda
  └─ Processing Failure → Destination (SQS/SNS)
```

### Behavior
Instead of blocking the entire stream processing, failed batches are sent to the configured destination, allowing the stream to continue processing new records.

## Key Benefits
1. **Better observability** - Track both successes and failures
2. **More flexibility** - Multiple destination options
3. **Improved error handling** - Prevent stream blocking
4. **Modern architecture** - Newer and more feature-rich than DLQ

## Best Practices
- Use Destinations instead of DLQ for new implementations
- Configure separate destinations for success and failure scenarios
- For streaming sources (Kinesis, DynamoDB Streams), configure failure destinations to prevent blocking
- Consider using EventBridge for complex event routing scenarios

## Study Tips
- Understand the difference between asynchronous invocations and event source mappings
- Remember that Destinations support 4 targets while DLQ only supports 2
- Practice configuring destinations in the AWS Console or using Infrastructure as Code (CloudFormation/Terraform)
