# AWS SAM Policy Templates

## Overview
SAM (Serverless Application Model) policy templates are a list of predefined templates that you can apply to grant permissions to your Lambda functions. These templates make it easier to define what your Lambda function can do without worrying about complex IAM role provisioning.

## Key Concepts
- **Purpose**: Simplify permission management for Lambda functions
- **Benefit**: Group related permissions into easy-to-understand templates
- **Usage**: Apply templates instead of manually creating IAM roles

## Important SAM Policy Templates

### 1. S3ReadPolicy
- **Function**: Provides read-only permissions to objects in S3
- **Use Case**: When your Lambda function needs to read data from S3 buckets

### 2. SQSPollerPolicy
- **Function**: Allows your Lambda function to poll an SQS queue
- **Use Case**: When your Lambda needs to receive messages from SQS

### 3. DynamoDBCrudPolicy
- **Function**: Enables Create, Read, Update, Delete (CRUD) operations on DynamoDB tables
- **Use Case**: When your Lambda needs full access to manage DynamoDB data

## Implementation Example

```yaml
MyFunction:
  Type: AWS::Serverless::Function
  Properties:
    Runtime: python2.7
    Policies:
      - SQSPollerPolicy:
          QueueName: !GetAtt MyQueue.QueueName
```

## How It Works
1. Define the policy template in your SAM template (e.g., `SQSPollerPolicy`)
2. Specify the required parameters (e.g., queue name)
3. SAM framework automatically transforms it into an IAM policy
4. The policy is attached to your Lambda function

## Exam Tips
- Policy template names are self-explanatory
- Know the three main examples: S3ReadPolicy, SQSPollerPolicy, DynamoDBCrudPolicy
- Understand that CRUD means Create, Read, Update, Delete
- SAM templates simplify IAM role management

## Additional Resources
- [Full list of SAM Policy Templates](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-templates.html)
