# AWS Lambda Concurrency and Throttling

## Overview

Lambda functions can scale automatically to handle varying loads. Understanding concurrency and throttling is crucial for building reliable serverless applications.

## Lambda Concurrency

### What is Concurrency?

- **Concurrency** refers to the number of Lambda function instances running simultaneously
- Lambda can scale quickly and easily to handle increased load
- At low scale: may have 2 concurrent executions
- At high scale: can reach up to 1,000 concurrent executions by default

### Reserved Concurrency

- **Purpose**: Limit the number of concurrent executions for a specific Lambda function
- **Level**: Set at the function level
- **Benefit**: Prevents a single function from consuming all available concurrency

**Important**: The 1,000 concurrent execution limit applies to **all functions** in your AWS account. If one function consumes all concurrency, other functions will be throttled.

## Throttling

### What is Throttling?

When invocations exceed the concurrency limit, Lambda triggers a **throttle**.

### Throttle Behavior by Invocation Type

#### Synchronous Invocation
- Returns **Throttle Error 429**
- Caller must handle the error and retry

#### Asynchronous Invocation
- Automatically retries
- Event goes to Dead Letter Queue (DLQ) after exhausting retries

### Requesting Higher Limits

If you need more than 1,000 concurrent executions, open a support ticket with AWS to request a higher limit.

## Common Concurrency Issues

### Scenario: One Function Monopolizes Concurrency

**Setup:**
- Application 1: Load balancer → Lambda Function
- Application 2: Few users → API Gateway → Lambda Function  
- Application 3: SDK/CLI → Lambda Function

**Problem:**
When Application 1 experiences a spike (e.g., promotion), it may consume all 1,000 concurrent executions, causing Applications 2 and 3 to be throttled.

**Solution:**
Set reserved concurrency for each function to ensure fair resource allocation.

## Asynchronous Invocations and Throttling

### Example: S3 Event Notifications

**Flow:**
1. Multiple files uploaded to S3 bucket simultaneously
2. Each upload triggers a Lambda function
3. If concurrency limit is reached, additional requests are throttled

### Retry Mechanism

For asynchronous invocations with throttling errors (429) or system errors (5xx):
- Lambda returns the event to an **internal event queue**
- Attempts to run the function again for **up to 6 hours**
- Retry interval increases exponentially: 1 second → maximum of 5 minutes
- Allows Lambda to eventually find available concurrency

## Cold Starts

### What is a Cold Start?

- Occurs when a new Lambda function instance is created
- Code must be loaded and initialization code (outside handler) must run
- First request has **higher latency** than subsequent requests

### Impact

- Large initialization (many dependencies, database connections, SDK creation) takes time
- Users may experience delays (e.g., 3 seconds)
- Can negatively impact user experience

## Provisioned Concurrency

### Solution to Cold Starts

**Provisioned Concurrency** allocates concurrency **before** the function is invoked:
- Cold start is eliminated
- All invocations have consistently low latency
- Can be managed using **Application Auto Scaling** (schedule or target tracking)

### VPC Cold Start Improvements

**Historical Note**: Lambda functions in VPC used to have severe cold start issues.

**Important Update** (October/November 2019): AWS dramatically reduced cold start impact for Lambda functions in VPC. Modern Lambda functions have minimal VPC cold start issues.

## Key Concepts Summary

| Concept | Description |
|---------|-------------|
| **Concurrent Executions** | Number of Lambda instances running simultaneously |
| **Reserved Concurrency** | Limit set at function level to cap concurrent executions |
| **Throttling** | Occurs when invocations exceed concurrency limits |
| **Cold Start** | Initial latency when new instance is created |
| **Provisioned Concurrency** | Pre-allocated capacity to eliminate cold starts |

## Best Practices

1. **Set Reserved Concurrency** for critical functions to prevent throttling
2. **Monitor Concurrency** across all functions in your account
3. **Use Provisioned Concurrency** for latency-sensitive applications
4. **Implement DLQ** for asynchronous invocations
5. **Request Higher Limits** when needed through AWS support

## Additional Resources

For detailed diagrams explaining reserved concurrency and provisioned concurrency, refer to AWS documentation and official blog posts.

---

**Study Tip**: Understanding the difference between reserved concurrency (limiting maximum) and provisioned concurrency (pre-warming instances) is crucial for AWS certification exams.
