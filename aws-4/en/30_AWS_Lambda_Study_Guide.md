# AWS Lambda Study Guide

## What is AWS Lambda?

AWS Lambda is a serverless computing service that lets you run code without provisioning or managing servers.

## EC2 vs Lambda Comparison

### Amazon EC2
- **Virtual servers** in the cloud
- Must be **provisioned** with specific memory and CPU
- **Continuously running** regardless of usage
- Requires **Auto Scaling groups** for scaling
- Need to manually manage starting/stopping for optimization

### AWS Lambda
- **Virtual functions** - no servers to manage
- Just provision the code and functions run automatically
- **Limited by time** - up to 15 minutes per execution
- **Run on demand** - only runs when invoked
- **Automated scaling** - AWS automatically provisions more functions as needed

## Key Benefits of AWS Lambda

### 1. Cost Efficiency
- **Pay only for what you use**
  - Number of requests (invocations)
  - Compute time (duration)
- **Generous free tier**
  - 1 million Lambda requests per month
  - 400,000 GB-seconds of compute time

### 2. No Server Management
- No need to provision or maintain servers
- Focus on code, not infrastructure

### 3. Automatic Scaling
- Scales automatically based on demand
- Handles increased concurrency without manual intervention

### 4. On-Demand Execution
- Functions only run when invoked
- No billing when functions are idle
- Huge shift from traditional always-on EC2 instances

### 5. AWS Integration
- Integrated with many AWS services
- Easy to build complex serverless architectures

## Use Cases for Lambda
- Event-driven applications
- Real-time file processing
- APIs and microservices
- Data transformation
- Scheduled tasks
- IoT backends

## Key Takeaways
✓ Serverless computing - no server management required  
✓ Cost-effective - pay per execution  
✓ Automatic scaling  
✓ Short executions (up to 15 minutes)  
✓ Seamless AWS service integration
