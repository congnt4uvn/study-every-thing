# AWS Lambda Execution Roles and Permissions

## Overview

An IAM Role must be attached to your Lambda function to grant it permissions to access AWS services and resources.

## Managed Policies for Lambda

AWS provides several managed policies that can be reused for common Lambda scenarios:

- **AWSLambdaBasicExecutionRole** - Allows uploading logs to CloudWatch
- **AWSLambdaKinesisExecutionRole** - Enables reading from Kinesis streams
- **AWSLambdaDynamoDBExecutionRole** - Enables reading from DynamoDB streams
- **AWSLambdaSQSQueueExecutionRole** - Enables reading from SQS queues
- **AWSLambdaVPCAccessExecutionRole** - Allows deploying Lambda functions inside a VPC
- **AWSXRayDaemonWriteAccess** - Enables uploading trace data to X-Ray

## Custom Policies

You can create your own custom policies for Lambda functions based on specific requirements.

## Event Source Mapping

When using an event source mapping to invoke your function, Lambda reads the data from the event source. Therefore, you must use an execution role with permissions to read the event data.

When Lambda is invoked by other services directly (without event source mapping), you don't need specific IAM Role permissions for the invocation itself.

## Best Practice

**Create one Lambda execution role per function** to follow the principle of least privilege and maintain clear separation of permissions.

## Resource-Based Policies

Resource-based policies are used to give other AWS accounts or services permissions to invoke your Lambda function. This is similar to S3 bucket policies.

### Access Control Rule

An IAM principal can access your Lambda function if **one of the following** is true:

1. The IAM policy attached to the principal authorizes it
2. The resource-based policy on the Lambda function allows it

## Key Differences

- **Execution Role (IAM Role)**: Grants Lambda permissions to access other AWS services
- **Resource-Based Policy**: Grants other services/accounts permission to invoke Lambda

## Summary

- Attach IAM roles to Lambda functions for outbound permissions
- Use managed policies when possible
- Create one execution role per function as best practice
- Use resource-based policies for inbound access control
- Event source mappings require execution role permissions to read data
