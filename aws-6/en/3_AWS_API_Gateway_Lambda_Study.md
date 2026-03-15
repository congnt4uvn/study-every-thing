# AWS API Gateway and Lambda Integration Study Guide

## Overview
This guide covers the fundamentals of AWS API Gateway integration with Lambda functions, demonstrating how to create RESTful APIs that trigger serverless functions.

## API Gateway API Types

AWS API Gateway offers several API types:

1. **HTTP APIs** - Lightweight, low-latency RESTful APIs
2. **WebSocket APIs** - For real-time two-way communication
3. **REST APIs** - Full-featured APIs (public or private)

This guide focuses on **REST APIs**.

## API Endpoint Types

When creating a REST API, you can choose from three endpoint types:

### Regional
- Deployed in a single AWS region
- Best for applications serving users in a specific geographic area
- Lower latency for regional users

### Edge-Optimized
- Deployed across multiple edge locations using CloudFront
- API still lives in one region but distributed at the edge
- Best for geographically distributed users
- Automatic routing to nearest edge location

### Private
- Only accessible within your VPC
- Not exposed to the public internet
- Best for internal applications and microservices

## Integration Types

API Gateway supports five integration types:

1. **Lambda Function** - Invoke AWS Lambda functions
2. **HTTP** - Forward requests to HTTP endpoints
3. **Mock** - Return responses without backend integration (useful for testing)
4. **AWS Service** - Directly integrate with AWS services (any service, any region)
5. **VPC Link** - Connect to private resources in your VPC

## Creating a Lambda Function for API Gateway

### Basic Lambda Function Structure

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda',
        'headers': {
            'Content-Type': 'application/json'
        }
    }
```

### Key Components:
- **statusCode**: HTTP status code (200 for success)
- **body**: Response content
- **headers**: HTTP headers (Content-Type specifies response format)

## Step-by-Step Integration Process

### 1. Create API in API Gateway
- Choose REST API type
- Select endpoint type (Regional, Edge-optimized, or Private)
- Name your API (e.g., "MyFirstAPI")

### 2. Create Method
- Click "Create method"
- Choose HTTP verb (GET, POST, PUT, DELETE, etc.)
- Select integration type (Lambda Function)

### 3. Create Lambda Function
- Navigate to AWS Lambda console
- Create new function (e.g., "api-gateway-route-gets")
- Choose runtime (Python 3.11 or other supported runtimes)
- Deploy function code

### 4. Connect API Gateway to Lambda
- Copy Lambda function ARN (Amazon Resource Name)
- Paste ARN in API Gateway integration settings
- Enable **Lambda Proxy Integration** to pass full request/response

## Lambda Proxy Integration

When enabled, Lambda Proxy Integration:
- Passes complete request details to Lambda (headers, query params, body, etc.)
- Expects Lambda to return properly formatted HTTP response
- Simplifies request/response handling

## Configuration Options

### Timeout Settings
- Default timeout can be configured
- Important for long-running operations
- Balance between user experience and cost

## Testing Your Integration

### Test in Lambda Console
1. Create test event
2. Configure event payload
3. Save and execute test
4. Verify response (status code, body, headers)

### Test in API Gateway
1. Use built-in test feature
2. Send sample requests
3. Verify integration works end-to-end

## Best Practices

1. **Use Lambda Proxy Integration** - Simplifies request/response handling
2. **Set Appropriate Timeouts** - Balance performance and cost
3. **Choose Right Endpoint Type** - Based on user geography
4. **Return Proper Status Codes** - Follow HTTP standards
5. **Include Content-Type Headers** - Ensure clients parse responses correctly
6. **Test Thoroughly** - Test both Lambda and API Gateway separately

## Common Use Cases

- **RESTful APIs** - CRUD operations for web/mobile apps
- **Webhooks** - Receive events from external services
- **Microservices** - Build scalable, serverless architecture
- **API Backends** - Power mobile and web applications
- **Data Processing** - Trigger data transformations via HTTP requests

## Key Takeaways

- API Gateway provides multiple API types and endpoint configurations
- Lambda functions can be easily integrated as backend services
- Proxy integration simplifies request/response handling
- You can expose any AWS service through API Gateway
- Regional endpoint type is suitable for region-specific applications
- Proper testing at each layer ensures reliable integration

## Next Steps

1. Experiment with different HTTP methods (POST, PUT, DELETE)
2. Add request validation and transformation
3. Implement authentication and authorization
4. Set up custom domain names
5. Enable API caching for performance
6. Configure throttling and usage plans
7. Monitor with CloudWatch logs and metrics
