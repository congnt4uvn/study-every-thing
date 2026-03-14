# AWS Lambda - Logging, Monitoring, and Tracing

## Overview
This document covers how AWS Lambda handles logging, monitoring, and tracing capabilities.

## CloudWatch Logs Integration

Lambda has built-in integration with **CloudWatch Logs** where all Lambda execution logs are automatically stored.

### Requirements
- Lambda function must have an **execution role** with the correct IAM policy
- The policy must authorize the Lambda function to write to CloudWatch Logs
- This is included in the **Lambda basic execution role** by default

## CloudWatch Metrics

CloudWatch metrics can be viewed in:
- CloudWatch Metrics UI
- Lambda UI

### Available Metrics
The following metrics are available for Lambda functions:
- **Invocations** - Number of times the function is invoked
- **Duration** - Time the function takes to execute
- **Concurrent Executions** - Number of concurrent executions
- **Error Counts** - Number of errors
- **Success Rate** - Percentage of successful invocations
- **Throttles** - Number of throttled invocations
- **Async Delivery Failures** - Failures in asynchronous invocations
- **Iterator Age** - (For Kinesis/DynamoDB streams) How far behind the function is in reading the stream

## X-Ray Tracing

AWS X-Ray provides distributed tracing for Lambda functions.

### Setup Steps
1. **Enable Active Tracing** in your Lambda configuration
2. **Use X-Ray SDK** in your code
3. **Configure IAM Role** with the managed policy: `AWS X-Ray daemon write access`

### Environment Variables
The following environment variables are used to communicate with X-Ray:
- `_X_AMZN_TRACE_ID`
- `AWS_XRAY_CONTEXT_MISSING`
- `AWS_XRAY_DAEMON_ADDRESS` - Specifies the IP and port where the X-Ray daemon is running

These environment variables can be accessed like any other environment variables in Lambda.

### Important Notes
- X-Ray daemon runs automatically when active tracing is enabled
- The `AWS_XRAY_DAEMON_ADDRESS` variable is the most important one for exam purposes
- It contains the IP address and port of the X-Ray daemon

## Key Takeaways
- Lambda automatically logs to CloudWatch Logs (with proper IAM permissions)
- CloudWatch Metrics provide visibility into Lambda performance
- X-Ray tracing is easily enabled through Lambda configuration
- Proper IAM roles are required for both CloudWatch and X-Ray integration
