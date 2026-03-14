# AWS Lambda Environment Variables

## Overview
This guide demonstrates how to use environment variables in AWS Lambda functions to manage configuration settings.

## Objective
Learn how to pass and retrieve environment variables in Lambda functions without encryption (encryption will be covered in the security section).

## Step-by-Step Tutorial

### 1. Create a Lambda Function
- Function name: `lambda-config-demo`
- Runtime: Python 3.8
- Purpose: Practice using environment variables

### 2. Modify the Lambda Code

Import the required module:
```python
import os
```

Update the return statement to retrieve the environment variable:
```python
return os.getenv("ENVIRONMENT_NAME")
```

**Key Points:**
- `os.getenv()` retrieves environment variables
- `ENVIRONMENT_NAME` is the variable we'll create
- The function will retrieve and return the variable's value

### 3. Deploy the Changes
Save and deploy the function to apply the code modifications.

### 4. Configure Environment Variables

1. Navigate to the **Configuration** section of your Lambda function
2. Select **Environment variables** from the left-hand menu
3. Click **Edit** and add a new environment variable:
   - **Key**: `ENVIRONMENT_NAME`
   - **Value**: `dev` (or any value you want)

**Notes:**
- You can add multiple environment variables if needed
- Encryption configuration is available but will be covered in the security section
- For now, the environment variable remains unencrypted

## Key Concepts

### What are Environment Variables?
Configuration values that can be passed to Lambda functions without hardcoding them in the source code.

### Benefits
- Separate configuration from code
- Easy to modify without redeploying code
- Support different environments (dev, staging, prod)

### Security Consideration
Environment variables can be encrypted using AWS encryption services (covered in advanced security sections).

## Summary
This tutorial demonstrates the basic setup and usage of environment variables in AWS Lambda functions using Python 3.8 runtime.
