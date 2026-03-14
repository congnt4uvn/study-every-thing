# AWS Serverless Architecture - Study Guide

## What is Serverless?

Serverless is a modern cloud computing approach where developers don't have to manage servers. It's important to understand that **serverless doesn't mean there are no servers** - it just means you don't see them or provision them manually.

### Key Concepts

- **No Server Management**: Developers deploy code without managing infrastructure
- **Function as a Service (FaaS)**: Initially, serverless meant deploying functions
- **Broader Scope**: Now includes any remotely managed service where you don't provision servers

## AWS Serverless Services

### Core Services

1. **AWS Lambda**
   - Pioneer of serverless computing
   - Execute code without provisioning servers
   - Pay only for compute time used

2. **Amazon DynamoDB**
   - Fully managed NoSQL database
   - Automatic scaling
   - Store and retrieve data seamlessly

3. **API Gateway**
   - Create, publish, and manage REST APIs
   - Invoke Lambda functions
   - Handle API requests at scale

4. **Amazon Cognito**
   - User identity and authentication
   - Secure user login and management
   - Identity storage for applications

5. **Amazon S3**
   - Static content storage
   - Website hosting
   - Scalable object storage

6. **Amazon CloudFront**
   - Content Delivery Network (CDN)
   - Deliver static content globally
   - Works with S3 for website delivery

### Additional Serverless Services

- **Amazon SNS** (Simple Notification Service)
  - Messaging and notifications
  - No server management required
  - Automatic scaling

- **Amazon SQS** (Simple Queue Service)
  - Message queuing
  - Decouples application components
  - Scales automatically

- **Amazon Kinesis Data Firehose**
  - Real-time data streaming
  - Automatic scaling
  - Fully managed service

## Reference Serverless Architecture

A typical serverless application flow in AWS:

```
Users → CloudFront + S3 (static content)
  ↓
Cognito (authentication/login)
  ↓
API Gateway (REST API)
  ↓
Lambda Functions (business logic)
  ↓
DynamoDB (data storage)
```

## Benefits of Serverless

- **No Infrastructure Management**: Focus on code, not servers
- **Automatic Scaling**: Services scale based on demand
- **Cost Effective**: Pay only for what you use
- **Faster Development**: Deploy code quickly
- **High Availability**: Built-in redundancy

## Study Focus Areas

1. Understanding Lambda function deployment and execution
2. DynamoDB table design and operations
3. API Gateway configuration and integration
4. Cognito user pool management
5. S3 bucket policies and static website hosting
6. Integration patterns between serverless services
7. Cost optimization strategies
8. Security best practices for serverless applications

---

*Study Notes: AWS Serverless Services*
