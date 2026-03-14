# AWS Lambda - Synchronous Invocations

## Overview
Synchronous invocations in AWS Lambda occur when the caller waits for the function to complete and receive the result immediately.

## Key Concepts

### What is Synchronous Invocation?
- The caller waits for the Lambda function to complete execution
- Results are returned directly to the caller
- If execution takes 2 minutes, you wait 2 minutes for the response
- Common when testing functions through the AWS Console UI

## Testing Methods

### 1. AWS Console UI
- Navigate to your Lambda function
- Use the "Test" button
- This performs a synchronous invocation
- Results appear directly in the console window

### 2. AWS CLI (Command Line Interface)

#### Setup
You can use:
- **AWS CloudShell** (available in supported regions)
- **Local Terminal** with AWS CLI installed

#### Verify CLI Version
```bash
aws --version
```
Expected: AWS CLI version 2.x

#### List Lambda Functions
```bash
aws lambda list-functions
```

**Note:** If using CLI in your local terminal (not CloudShell), add the region flag:
```bash
aws lambda list-functions --region eu-west-1
```

#### Invoke Lambda Function Synchronously
```bash
aws lambda invoke \
  --function-name hello-world \
  --payload '{"key": "value"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```

**Important Notes:**
- Remove the `--region` argument if using CloudShell (region is auto-detected)
- For CLI v1, the command syntax may differ slightly
- The response is written to the specified file (`response.json`)

## Common Issues

### Function Not Found Error
- Verify the function name is correct
- Ensure you're in the correct region
- Check that the function exists in your AWS account

## CLI Version Differences
- **CLI v2** (recommended): Current command syntax as shown above
- **CLI v1** (older): May have slightly different command structure
- Always use CLI v2 when possible

## Best Practices
1. Use CloudShell for quick testing without local setup
2. Always verify your region when using local CLI
3. Check CLI version to ensure compatibility with commands
4. Use synchronous invocations for immediate feedback and testing
5. Consider asynchronous invocations for long-running tasks

## Use Cases for Synchronous Invocations
- Interactive applications requiring immediate responses
- API Gateway integrations
- Testing and debugging Lambda functions
- Request-response workflows

---
*Study Notes: AWS Lambda Synchronous Invocations*
