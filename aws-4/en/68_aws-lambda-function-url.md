# AWS Lambda Function URL Study Guide

## Overview
AWS Lambda Function URLs provide a dedicated HTTP(S) endpoint for your Lambda function, allowing you to invoke it directly without needing API Gateway.

## Step-by-Step Tutorial

### 1. Create Lambda Function
- Function name: `lambda-demo-url`
- Runtime: Python 3.9
- Click **Create function**

### 2. Test the Function
1. Click on **Test**
2. Create a new Test Event
3. Add a name: `test`
4. Click **Save**
5. Run the test

**Expected Response:**
```json
{
  "statusCode": 200,
  "body": "Hello from Lambda"
}
```

### 3. Publish a Version
1. Click **Publish new version**
2. Version name: `version 1`
3. This creates an immutable version of your function

### 4. Create an Alias
1. Create a new alias
2. Alias name: `dev`
3. Point it to `version 1`
4. Click **Save**

> **Note:** The alias `dev` now points to version 1

### 5. Create Function URL
1. Scroll down or select **Function URL** from the left-hand side menu
2. Click **Create Function URL**

#### Configuration Options:

**Authentication Type:**
- **IAM** - Requires AWS credentials
- **NONE** - Public access (choose this option)

**Resource Policy:**
- Automatically created when using NONE authentication
- Allows anyone to access the Lambda Function URL
- AuthType is set to NONE

**CORS (Optional):**
- Configure Cross-Origin Resource Sharing if needed
- Specify allowed origins
- Specify exposed headers
- Not required for basic setup

### 6. Access Your Function
1. Copy the Function URL (this URL remains permanent for the alias)
2. Open the URL in a web browser
3. You should see: `Hello from Lambda`

## Key Concepts

### Function URL Benefits
- Direct HTTP(S) endpoint for Lambda
- No need for API Gateway
- Permanent URL for each alias
- Simple authentication options

### Authentication Types
- **IAM**: Secure access with AWS credentials
- **NONE**: Public access (requires resource policy)

### Resource Policy
- Automatically created with Function URL
- Controls access to your Lambda function
- Ensures proper security configuration

### CORS Configuration
- Allows cross-origin requests
- Configure allowed origins
- Configure exposed headers
- Optional for basic scenarios

## Best Practices
1. Use aliases to manage different environments (dev, staging, prod)
2. Choose appropriate authentication type based on use case
3. Configure CORS only when needed
4. Test the function before publishing versions
5. Use versioning for production deployments

## Common Use Cases
- Webhooks
- Simple REST APIs
- Microservices
- Public endpoints
- Integration with external services
