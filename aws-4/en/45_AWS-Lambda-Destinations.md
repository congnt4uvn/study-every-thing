# AWS Lambda Destinations

## Overview
Lambda Destinations is a feature that allows you to route the results of asynchronous Lambda function invocations to different AWS services based on success or failure conditions.

## Key Concepts

### What are Lambda Destinations?
- **Destinations** are AWS services that receive the result of a Lambda function execution
- Can be configured for both **successful** and **failed** invocations
- Supported for asynchronous invocations and stream-based invocations

### Supported Destination Types
- **SQS Queue** - Simple Queue Service
- **SNS Topic** - Simple Notification Service
- **Lambda Function** - Another Lambda function
- **EventBridge** - Event bus for event-driven architectures

## Practical Example: Configuring SQS Destinations

### Step 1: Create SQS Queues
Create two queues to handle different outcomes:

1. **Success Queue**: `S3-success`
   - Receives messages when Lambda executes successfully
   
2. **Failure Queue**: `S3-failure`
   - Receives messages when Lambda execution fails

### Step 2: Configure Lambda Function
1. Navigate to your Lambda function (e.g., `lambda-S3-function`)
2. Go to **Configuration** tab
3. Select **Destinations**
4. Click **Add destination**

### Step 3: Add Failure Destination
- **Source type**: Asynchronous invocation
- **Condition**: On failure
- **Destination type**: SQS queue
- **Destination**: Select `S3-failure` queue

### Step 4: Add Success Destination
- **Source type**: Asynchronous invocation
- **Condition**: On success
- **Destination type**: SQS queue
- **Destination**: Select `S3-success` queue

## IAM Permissions

### Automatic Permission Addition
When you configure a destination through the Lambda console, it automatically adds the required IAM permissions to the Lambda execution role.

### Required Permissions
The execution role needs permission to send messages to the destination service. For SQS, this includes:
- `sqs:SendMessage` permission
- Resource ARN of the destination queue

### Verification
You can verify the permissions by:
1. Opening the Lambda function configuration
2. Going to **Permissions** tab
3. Clicking on the **Execution role**
4. Reviewing the IAM policies attached

Example policy name: `AmazonLambdaSQSQueueDestinationExecutionRole`

## Use Cases

### When to Use Destinations
- **Error Handling**: Route failed executions to a dead-letter queue for analysis
- **Success Tracking**: Send successful execution details to monitoring systems
- **Workflow Orchestration**: Chain Lambda functions together
- **Audit Logging**: Keep records of all invocations

### Alternative Invocation Types
- **Asynchronous Invocation**: Lambda queues the event and immediately returns success
- **Stream Invocation**: For Kinesis or DynamoDB streams mapped to Lambda functions

## Best Practices
1. Always configure both success and failure destinations for critical workflows
2. Monitor your destination queues regularly
3. Use appropriate retry configurations for failed invocations
4. Test IAM permissions before deploying to production
5. Consider using EventBridge for complex routing scenarios

## Additional Resources
- AWS Lambda Destinations Documentation
- SQS Queue Configuration Best Practices
- Lambda Error Handling Patterns
