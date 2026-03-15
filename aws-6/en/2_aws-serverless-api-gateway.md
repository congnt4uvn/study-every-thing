# AWS Serverless - API Gateway Study Guide

## Overview

This document covers AWS serverless architecture focusing on API Gateway, Lambda functions, and DynamoDB integration.

## Serverless Journey So Far

### Core Components
- **Lambda Functions**: Serverless compute service
- **DynamoDB**: NoSQL database for API backend
- **CRUD Operations**: Create, Read, Update, Delete operations on tables

## Invoking Lambda Functions

### Methods to Invoke Lambda Functions

1. **Direct Client Invocation**
   - Client directly invokes Lambda function
   - Requires IAM permissions
   - Not recommended for public APIs

2. **Application Load Balancer (ALB)**
   - Acts as intermediary between client and Lambda
   - Exposes Lambda function as HTTP endpoint
   - Basic HTTP functionality

3. **API Gateway** (Recommended)
   - Serverless offering from AWS
   - Creates REST APIs that are public and accessible
   - Client talks to API Gateway, which proxies requests to Lambda functions

## Why Use API Gateway?

### Advantages Over ALB

API Gateway provides much more than just an HTTP endpoint:

- **Authentication & Authorization**: Multiple security options
- **Usage Plans**: Control API access and quotas
- **Development Stages**: Manage dev, test, and production environments
- **API Versioning**: Support multiple API versions without breaking clients
- **Request Throttling**: Protect against excessive requests
- **API Keys**: Manage client access
- **Request/Response Transformation**: Validate and transform data
- **Caching**: Cache API responses for better performance
- **SDK Generation**: Automatically generate client SDKs
- **WebSocket Support**: Real-time streaming capabilities
- **Standards Support**: Import/export using Swagger or OpenAPI 3.0

## Full Serverless Application

**API Gateway + Lambda = Complete Serverless Solution**

Benefits:
- No infrastructure to manage
- Automatic scaling
- Pay-per-use pricing model
- High availability built-in

## API Gateway Integrations

### 1. Lambda Function Integration (Most Common)
- Invoke Lambda functions
- Easiest way to expose REST API
- Full serverless application
- Backend powered by Lambda

### 2. HTTP Integration
- Expose any HTTP endpoint in the backend
- Examples:
  - On-premises HTTP APIs
  - Application Load Balancer in cloud
  
**Use Cases:**
- Leverage rate limiting
- Add caching
- Implement user authentication
- Manage API keys

### 3. AWS Service Integration
- Expose any AWS API through API Gateway
- Direct integration with AWS services

**Examples:**
- Start Step Function workflows
- Post messages to SQS
- Stream data to Kinesis

**Use Cases:**
- Add authentication layer
- Deploy APIs publicly
- Implement rate control
- Avoid exposing AWS credentials

## Practical Example: Kinesis Data Streams

### Scenario
Send data to Kinesis Data Streams securely without AWS credentials

### Architecture
```
Clients → API Gateway → Kinesis Data Streams
```

### Benefits
- Secure data ingestion
- No AWS credentials needed for clients
- Authentication handled by API Gateway
- Rate limiting and monitoring

## Key Takeaways

1. API Gateway is the preferred method for exposing Lambda functions publicly
2. Provides enterprise-grade features (security, throttling, caching)
3. Supports multiple integration types (Lambda, HTTP, AWS Services)
4. Essential component for full serverless applications
5. Can act as a secure proxy to AWS services

## Next Steps

- Explore API Gateway deployment stages
- Learn about API Gateway security models
- Practice creating REST APIs with Lambda backend
- Understand request/response transformations
- Implement caching strategies
