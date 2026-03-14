# AWS Lambda with SQS Event Mapper

## Overview
This guide covers how to set up AWS Lambda with SQS (Simple Queue Service) as an event mapper, allowing Lambda functions to automatically process messages from SQS queues.

## Prerequisites
- AWS Account with appropriate permissions
- Basic understanding of AWS Lambda
- Familiarity with SQS concepts

## Step-by-Step Tutorial

### 1. Create Lambda Function
- Navigate to AWS Lambda console
- Click "Create function"
- Function name: `lambda-SQS`
- Runtime: Python 3.8 (or your preferred version)
- Click "Create function"

### 2. Create SQS Queue
- Navigate to Amazon SQS console
- Click "Create queue"
- Queue name: `lambda-demo-SQS`
- Queue type: Standard queue
- Scroll down and click "Create queue"

### 3. Configure Lambda Trigger
1. In your Lambda function, click "Add trigger"
2. Select **SQS** from the list of available triggers
3. Choose the SQS queue: `lambda-demo-SQS`
4. Configure batch settings:
   - **Batch size**: Number of messages to receive in a single batch (1 to max allowed)
   - **Batch window**: Time in seconds to gather records before invoking the function
5. Enable the trigger
6. Click "Add"

### 4. Common Issue: IAM Permissions
When adding the SQS trigger, you may encounter an error:

**Error**: "The execution role does not have permissions to call ReceiveMessage on SQS"

**Solution**: The Lambda execution role needs the following permission:
- `sqs:ReceiveMessage`
- `sqs:DeleteMessage`
- `sqs:GetQueueAttributes`

Add these permissions to the Lambda execution role's IAM policy.

## Key Concepts

### Batch Processing
- **Batch Size**: Controls how many messages Lambda receives at once
- **Batch Window**: Allows Lambda to wait and collect more messages for efficient processing
- Larger batches reduce the number of Lambda invocations

### Event Mappers
AWS Lambda supports various event mappers including:
- Amazon SQS
- Amazon Kinesis
- Amazon DynamoDB Streams
- Amazon MSK (Managed Streaming for Apache Kafka)
- Partner event sources

## Best Practices
1. Configure appropriate batch sizes based on your processing needs
2. Set reasonable batch windows to balance latency and efficiency
3. Ensure proper IAM permissions before enabling triggers
4. Monitor Lambda metrics and SQS queue depth
5. Implement error handling and dead-letter queues

## Summary
This tutorial demonstrates how to connect AWS Lambda with SQS using event mappers, enabling serverless message processing at scale.
