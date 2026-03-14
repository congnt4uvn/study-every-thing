# AWS Lambda Deployment with CloudFormation

## Overview
This document covers how to deploy AWS Lambda functions using CloudFormation templates.

## Deployment Methods

### 1. Inline Method

**Description:**
- Define Lambda function code directly within the CloudFormation template
- Use the `Code.ZipFile` property

**Advantages:**
- Simple and straightforward
- Code is visible in the template
- No external dependencies needed

**Limitations:**
- Only for very simple functions
- Cannot include function dependencies
- Not suitable for complex applications

**Example Structure:**
```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Code:
        ZipFile: |
          # Your Lambda code here
```

### 2. S3 Zip File Method

**Description:**
- Store Lambda function as a zip file in Amazon S3
- Reference the S3 location in CloudFormation template

**Requirements:**
- Lambda function zip must be stored in Amazon S3
- Must specify S3 location in CloudFormation code

**Key Properties:**
- **S3Bucket**: The bucket containing the zip file
- **S3Key**: The full path to your zip file in S3
- **S3ObjectVersion**: Version ID (if using versioned bucket)

**Best Practices:**
- Enable versioning on S3 bucket (recommended)
- Update S3ObjectVersion when code changes
- This ensures CloudFormation detects and applies updates

**Update Behavior:**
- If you update code in S3 but don't update S3Bucket, S3Key, or S3ObjectVersion in the template, CloudFormation **will not** update the function
- Versioning helps CloudFormation track changes and update properly

### 3. Multi-Account Deployment

**Scenario:**
Deploy Lambda function from one AWS account to multiple other accounts.

**Setup:**
- Account 1: Contains S3 bucket with Lambda code
- Account 2 & 3: Target accounts for deployment

**Process:**
1. Launch CloudFormation in Account 2
2. Reference S3 bucket from Account 1
3. Ensure proper cross-account access permissions

**Key Consideration:**
- Account 2 must have access to Account 1's S3 bucket
- Configure appropriate IAM policies and bucket policies

## Summary

| Method | Use Case | Dependencies | Complexity |
|--------|----------|--------------|------------|
| Inline | Simple functions | Not supported | Low |
| S3 Zip | Production use | Supported | Medium |
| Multi-Account | Enterprise deployment | Supported | High |

## Important Notes

- For production environments, use S3 zip method with versioning
- Always enable S3 bucket versioning for better change tracking
- Cross-account deployments require careful IAM configuration
- Update S3ObjectVersion in template when deploying new code versions
