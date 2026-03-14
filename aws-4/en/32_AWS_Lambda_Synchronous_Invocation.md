# AWS Lambda - Synchronous Invocation

## Overview

This document covers the synchronous invocation pattern for AWS Lambda functions.

## What is Synchronous Invocation?

Synchronous invocation means you're **waiting for the results**, and the result will be returned to you directly. This is the invocation type we use when:

- Using the AWS CLI
- Using the AWS SDK
- Working with API Gateway
- Using Application Load Balancer

## Key Characteristics

### Direct Response
- You wait for the function to complete
- The result is returned immediately
- The client receives the response directly

### Error Handling
- Errors must be handled on the **client side**
- If a Lambda function fails, the client must decide what to do
- The client is responsible for retry logic
- Exponential backoff strategies should be implemented by the client

## Example Flow

### Simple CLI/SDK Invocation
```
Client → Lambda Function → Response back to Client
```

### API Gateway Pattern
```
Client → API Gateway → Lambda Function
                    ↓
Client ← API Gateway ← Response
```

The client invokes the API Gateway, which proxies the request to Lambda. Lambda processes the request and returns the response through API Gateway back to the client. Throughout this process, the client is waiting for the response.

## Services That Use Synchronous Invocation

### Services Covered in This Course (Bold)
- **Elastic Load Balancing (Application Load Balancer)**
- **API Gateway**
- **CloudFront (Lambda@Edge)**
- **Amazon Cognito**
- **AWS Step Functions**

### Other Services (Not Covered)
- Amazon S3 Batch
- Amazon Lex
- Amazon Alexa
- Amazon Kinesis Data Firehose

## When to Use Synchronous Invocation

Use synchronous invocation when:
- You need immediate response from the function
- The operation is user-invoked
- You need to wait for the result before proceeding
- Your application requires direct feedback

## Best Practices

1. **Implement retry logic** on the client side
2. **Use exponential backoff** for failed requests
3. **Handle timeouts** appropriately
4. **Monitor function duration** to optimize user experience
5. **Consider error handling** at the application level

## Summary

Synchronous invocation is a straightforward pattern where the client waits for Lambda to complete execution and return a result. Error handling is the client's responsibility, making it important to implement robust retry mechanisms and error handling logic in your application.
