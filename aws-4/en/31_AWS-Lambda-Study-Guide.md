# AWS Lambda Study Guide

## Introduction to Lambda

AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers.

## Getting Started with Lambda Console

To access the Lambda practice interface:
1. Go to the Lambda console
2. Navigate to `/begin` in the URL
3. This provides a helpful UI to understand how Lambda works

## Lambda Function Basics

### Supported Programming Languages

Lambda functions can be written in multiple languages:
- .NET
- Java
- Node.js
- Python
- Ruby
- Custom runtime (for other languages)

### Example: Hello World

When you create a basic Node.js Lambda function and click **Run**, it executes and returns:
```
"Hello from Lambda."
```

## Event-Driven Architecture

### Lambda Event Sources

Lambda responds to various event triggers:
- **Streaming analytics** - Processing real-time data streams
- **Mobile applications** - Mobile phone and IoT backend events
- **S3 buckets** - Photos or files being uploaded
- **IoT devices** - Camera and sensor data

### Automatic Scaling

Lambda scales automatically based on demand:
- Initially runs with minimal resources (one pair of cogs)
- As more events arrive, Lambda scales up seamlessly
- Can scale to 8-9 instances or more
- **No server management required** - scaling happens automatically

## Cost Considerations

### Pricing Model

- **Free Tier**: Generous free tier for initial invocations
- **Pay-per-use**: Costs accumulate based on:
  - Number of invocations
  - Execution duration
  - Allocated memory

### Cost Optimization Tips

- Lambda can be a **cost-effective service**
- Important to estimate your workload
- Monitor invocation patterns to predict costs
- Review free tier limits regularly

## Creating Your First Lambda Function

### Steps to Create

1. Click **Create a Function** in the Lambda console
2. Choose to use a **blueprint**
3. Select the **hello-world** blueprint
4. Configure and deploy

## Key Takeaways

✓ Lambda provides serverless computing without infrastructure management

✓ Supports multiple programming languages

✓ Automatically scales based on demand

✓ Event-driven architecture enables real-time processing

✓ Cost-effective for many workloads with proper planning

---

**Next Steps**: Practice creating Lambda functions with different blueprints and event sources to understand its full capabilities.
