# AWS Lambda Best Practices

## Overview
This document covers essential best practices for AWS Lambda that are important for the AWS certification exam.

## Key Best Practices

### 1. Optimize Function Handler Performance
**Heavy-duty work should be performed outside the function handler** to minimize execution time.

This includes:
- **Database connections** - Initialize connections outside the handler
- **AWS SDK initialization** - Set up SDK clients outside the handler
- **Dependencies and datasets** - Build and load these outside the handler

**Why?** Lambda reuses execution environments, so code outside the handler only runs once during cold starts, improving overall performance.

### 2. Use Environment Variables
Environment variables should be used for values that change over time:
- Database connection strings
- S3 bucket names
- Configuration parameters
- Any dynamic values

**Important:** Never hardcode these values in your code!

### 3. Secure Sensitive Data
For passwords and sensitive values:
- Use environment variables
- **Encrypt them with AWS KMS** for added security
- Never store credentials in plain text

### 4. Minimize Deployment Package Size
Keep your deployment package as small as possible:
- Include only runtime necessities
- Break down large functions into smaller ones
- Remember Lambda's package size limits
- Use **Lambda Layers** to reuse common libraries across multiple functions

### 5. Avoid Recursive Code
**Never have a Lambda function call itself!**
- This can lead to uncontrolled execution
- Results in very high costs
- Can quickly exhaust concurrency limits
- Considered a disaster scenario

## Summary
Following these best practices will help you:
- Improve Lambda performance
- Reduce costs
- Enhance security
- Pass the AWS certification exam

## Exam Tips
- Understand the rationale behind each best practice
- Know when to use Lambda Layers
- Remember the importance of KMS encryption for sensitive data
- Be aware of Lambda's limits and constraints
