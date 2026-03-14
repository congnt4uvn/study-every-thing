# AWS Lambda Functions - Dependencies and Packaging

## Overview
This document covers how to work with external dependencies in AWS Lambda functions, moving beyond simple code to real-world applications.

## Key Concepts

### External Dependencies
In real-world Lambda functions, you often need:
- Extra libraries and packages
- X-Ray SDK for tracing
- Database clients
- Other third-party dependencies

### Packaging by Language

#### JavaScript/Node.js
- Use **NPM** for package management
- Dependencies are stored in `node_modules` directory
- Include `node_modules` with your code when packaging

#### Python
- Use **PIP** for package management
- Use target options to install dependencies
- Package dependencies alongside your Python code

#### Java
- Include relevant **.jar files**
- Bundle all dependencies with your application code

## Deployment Process

### Step 1: Package Your Code
- Combine your code and all dependencies together
- Create a **ZIP file** containing everything

### Step 2: Upload to Lambda
Two options depending on size:

1. **Direct Upload** (< 50 MB)
   - Upload the ZIP file directly to Lambda
   
2. **S3 Upload** (≥ 50 MB)
   - First upload to Amazon S3
   - Then reference the S3 location from Lambda

## Important Notes

### Native Libraries
- Must be compiled on **Amazon Linux**
- Ensure compatibility with Lambda runtime environment
- Use Lambda layers for reusable native dependencies

### AWS SDK
- **Pre-installed** in every Lambda function
- No need to package AWS SDK with your code
- Saves package size and upload time

## Best Practices
1. Keep package size minimal
2. Use Lambda Layers for shared dependencies
3. Remove unnecessary files before zipping
4. Test package locally before deployment
5. Monitor package size to stay under limits

## Summary
- Always zip code + dependencies together
- Choose upload method based on package size (50 MB threshold)
- Native libraries require Amazon Linux compilation
- AWS SDK comes pre-installed - no packaging needed
