# AWS Lambda with Dependencies - Study Guide

## Overview
This guide covers creating and deploying AWS Lambda functions with external dependencies using CloudShell and NPM.

## Key Concepts

### AWS Lambda
- Serverless compute service
- Runs code without provisioning servers
- Can include external dependencies and packages

### CloudShell
- Browser-based terminal connected to your AWS account
- Pre-configured with AWS CLI and development tools
- NPM already installed for package management

### NPM (Node Package Manager)
- Manages packages and dependencies for Node.js
- Used to install required libraries for Lambda functions

## Step-by-Step Process

### 1. Access CloudShell
- Navigate to CloudShell in AWS Console
- Provides a terminal environment ready to use

### 2. Create Lambda Folder
```bash
mkdir lambda
cd lambda
```

### 3. Install Text Editor (Optional)
```bash
sudo yum install -y nano
```

### 4. Create index.js File
```bash
nano index.js
```

The Lambda function code includes:
- **X-Ray SDK Core**: For distributed tracing
- **AWS SDK**: To interact with AWS services (S3 in this case)
- **ListBuckets Operation**: Returns list of S3 buckets

### 5. Install Dependencies
```bash
npm install aws-xray-sdk
```

This command installs the X-Ray SDK locally, which will be bundled with the Lambda function for deployment.

## Key Components

### index.js
- Main Lambda function handler
- Requires `xray-sdk-core` for tracing
- Uses AWS SDK to communicate with Amazon S3
- Executes ListBuckets operation

### Dependencies
- `aws-xray-sdk`: Required for distributed tracing capabilities
- Must be packaged with the Lambda function for deployment

## Important Notes
- Dependencies must be installed locally before packaging
- CloudShell provides a convenient environment for Lambda development
- The function requires proper IAM permissions to access S3

## Learning Objectives
✓ Create Lambda functions with external dependencies  
✓ Use CloudShell for AWS development  
✓ Manage Node.js packages with NPM  
✓ Bundle dependencies with Lambda functions  
✓ Integrate AWS X-Ray for tracing  
✓ Work with AWS SDK in Lambda functions  

## Next Steps
- Package the Lambda function with dependencies
- Upload to AWS Lambda service
- Configure IAM roles and permissions
- Test the function execution
- Monitor with AWS X-Ray
