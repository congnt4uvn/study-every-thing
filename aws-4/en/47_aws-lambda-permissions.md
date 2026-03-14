# AWS Lambda Permissions Study Guide

## Overview
Every Lambda function must have an IAM role attached to it. Understanding the difference between execution roles and resource-based policies is crucial for working with AWS Lambda.

## Lambda Execution Roles

### Basic Execution Role
- Automatically attached to Lambda functions created through the console
- Provides permissions for the Lambda function to perform actions
- **Key permissions include:**
  - Create CloudWatch log groups
  - Send log events to CloudWatch Logs
  - This allows Lambda functions to write their execution logs

### Example: SQS Lambda Execution Role
When Lambda needs to poll SQS queues, the execution role must include:
- Receive messages from SQS
- Delete messages from SQS
- Get queue attributes

**Important:** In this pattern, Lambda is actively pulling data from SQS, not being invoked by it.

## Resource-Based Policies

Resource-based policies define **who can invoke** your Lambda function. These policies are attached directly to the Lambda function itself.

### S3 Trigger Example
When S3 invokes a Lambda function:
- The resource-based policy allows `s3.amazonaws.com` service to invoke the function
- Conditions specify:
  - Source account ID
  - Source ARN (the specific S3 bucket)
- **Pattern:** S3 pushes events to Lambda

### EventBridge Trigger Example
When EventBridge invokes a Lambda function:
- The resource-based policy allows `events.amazonaws.com` service to invoke the function
- Conditions specify:
  - Source ARN (the specific EventBridge rule)
- **Pattern:** EventBridge pushes events to Lambda

## Key Differences

| Aspect | Execution Role | Resource-Based Policy |
|--------|----------------|----------------------|
| **Purpose** | Permissions for Lambda to access other AWS services | Permissions for other services to invoke Lambda |
| **Direction** | Lambda → Other Services | Other Services → Lambda |
| **Example Use Cases** | Lambda reading from SQS, writing to DynamoDB | S3 triggering Lambda, EventBridge invoking Lambda |
| **Location** | IAM Roles section | Lambda function configuration |

## Important Patterns to Remember

### Push Model (Uses Resource-Based Policy)
- S3 → Lambda
- EventBridge → Lambda
- API Gateway → Lambda
- Services **invoke** Lambda directly

### Poll Model (Uses Execution Role)
- Lambda → SQS
- Lambda → Kinesis
- Lambda → DynamoDB Streams
- Lambda **polls** for data from these services

## Viewing Policies in AWS Console

### Execution Role
1. Navigate to Lambda function
2. Go to **Configuration** → **Permissions**
3. Click on the execution role name
4. View attached policies

### Resource-Based Policy
1. Navigate to Lambda function
2. Go to **Configuration** → **Permissions**
3. Scroll down to "Resource-based policy statements"
4. Click "View policy" to see the JSON

## Best Practices
- Always use the principle of least privilege
- Regularly audit Lambda execution roles
- Use resource-based policies for cross-account access
- Monitor CloudWatch Logs for permission-related errors
- Keep IAM policies specific to required actions only

## Summary
Understanding when to use execution roles versus resource-based policies is essential:
- **Execution roles** = What Lambda can do to other services
- **Resource-based policies** = What other services can do to Lambda

Remember: SQS is special because Lambda polls it, so it doesn't use resource-based policies but requires proper execution role permissions instead.
