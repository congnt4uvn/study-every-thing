# AWS Study Guide: DynamoDB Streams with Lambda Triggers

## Overview
This guide covers how to enable and configure DynamoDB Streams to trigger AWS Lambda functions for real-time data processing.

## What are DynamoDB Streams?

DynamoDB Streams captures time-ordered sequence of item-level modifications in any DynamoDB table and stores this information in a log for up to 24 hours. Applications can access this log and view the data items as they appeared before and after modification.

## Key Concepts

### 1. Enabling DynamoDB Streams

**Steps:**
1. Navigate to your DynamoDB table (e.g., `users_post` table)
2. Go to **Exports and Streams** tab
3. Find **DynamoDB stream details**
4. Click **Enable stream**

### 2. Stream View Types

When enabling a stream, you can choose what information to write:

- **Keys only** - Only the key attributes of the modified item
- **New image** - The entire item after it was modified
- **Old image** - The entire item before it was modified
- **New and old images** - Both the new and old images of the item (recommended for maximum information)

### 3. Creating Lambda Triggers

Once the stream is enabled, you can create triggers that invoke Lambda functions automatically when items are modified.

**Steps to create a trigger:**

1. Scroll to the **Trigger** section in the stream details
2. Click **Create trigger**
3. Select or create a Lambda function

### 4. Lambda Function Setup

**Using a Blueprint:**
- Search for "DynamoDB" in blueprints
- Select **DynamoDB process stream Python**
- This blueprint logs all updates made to a table

**Configuration:**
- **Function name**: e.g., `Lambda-demo-DynamoDB-stream`
- **Execution role**: Create new role with basic Lambda permissions
  - **Important**: Edit the role to add permissions to read from DynamoDB
  
**Trigger Configuration:**
- **DynamoDB table**: Select your table (e.g., `users_post`)
- **Batch size**: 100 (how many records to read at a time)
- **Batch window**: Time to gather records before invoking function (for efficiency)
- **Starting position**: Where to start reading (TRIM_HORIZON or LATEST)

## Use Cases

- **Real-time analytics**: Process data changes in real-time
- **Data replication**: Replicate data to other databases or services
- **Notifications**: Send notifications when specific items change
- **Auditing**: Track all changes to database items
- **Cross-region replication**: Keep multiple regions in sync

## Best Practices

1. **Choose appropriate stream view type** based on your needs
2. **Configure proper IAM permissions** for Lambda to read streams
3. **Set appropriate batch size** to balance throughput and cost
4. **Handle errors gracefully** with proper error handling in Lambda
5. **Monitor stream metrics** using CloudWatch
6. **Consider batch window** for cost optimization

## Important Permissions

The Lambda execution role needs:
- `dynamodb:GetRecords`
- `dynamodb:GetShardIterator`
- `dynamodb:DescribeStream`
- `dynamodb:ListStreams`

## Summary

DynamoDB Streams with Lambda triggers provides a powerful way to react to data changes in real-time. By configuring streams correctly and setting up Lambda functions with proper permissions, you can build event-driven architectures that scale automatically.
