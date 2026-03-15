# AWS Lambda Stage Variables with API Gateway

## Overview
This tutorial covers how to use stage variables in API Gateway to dynamically invoke different Lambda function versions and aliases. This is a powerful pattern for managing multiple environments (DEV, TEST, PROD) with a single API Gateway configuration.

## Key Concepts

### Lambda Versions
- **Versions** are immutable snapshots of your Lambda function code
- Each version has a unique version number (v1, v2, etc.)
- The **$LATEST** version represents the current editable version
- Versions allow you to maintain multiple stable releases

### Lambda Aliases
- **Aliases** are pointers to specific Lambda versions
- They provide a level of abstraction between your API and function versions
- Common alias naming conventions: DEV, TEST, PROD
- Aliases can be updated to point to different versions

### Stage Variables
- Stage variables are key-value pairs in API Gateway
- They allow you to parameterize your API configuration
- Use case: Switch between Lambda aliases based on the deployment stage

## Tutorial Steps

### 1. Create a Lambda Function
```
Function name: api-gateway-stage-variables-get
Runtime: Python 3.11
```

### 2. Create Multiple Versions

**Version 1:**
```python
# Lambda code
return "Hello from Lambda v1"
```
- Deploy the code
- Test it
- Publish as Version 1

**Version 2:**
```python
# Lambda code
return "Hello from Lambda v2"
```
- Update the code
- Deploy and test
- Publish as Version 2

**Latest (DEV):**
```python
# Lambda code
return "Hello from Lambda in DEV"
```
- Update the code
- Deploy and test
- Do NOT publish (remains as $LATEST)

### 3. Create Aliases

| Alias | Points To | Purpose |
|-------|-----------|---------|
| **DEV** | $LATEST | Development - always uses latest code |
| **TEST** | Version 2 | Testing - uses newest published version |
| **PROD** | Version 1 | Production - uses most stable version |

### 4. Configure API Gateway

1. Create a resource named "stage variables"
2. Create a GET method for the Lambda function
3. Enable Lambda proxy integration
4. Use the Lambda ARN with stage variable:
   ```
   arn:aws:lambda:region:account-id:function:api-gateway-stage-variables-get:${stageVariables.LambdaAlias}
   ```

### 5. Set Permissions

When using stage variables, you need to grant API Gateway permission to invoke each alias:
```bash
# Run this command in CloudShell for each alias
aws lambda add-permission \
  --function-name <function-name>:<alias> \
  --statement-id apigateway-access \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com
```

## Benefits

1. **Environment Management**: Single API configuration for multiple environments
2. **Version Control**: Easy rollback by updating alias pointers
3. **Testing**: Test new versions in isolation before promoting to production
4. **Flexibility**: Change backend Lambda versions without modifying API Gateway

## Best Practices

- Use semantic versioning for Lambda versions
- Keep PROD pointing to the most stable, tested version
- Use DEV for ongoing development
- Promote versions through TEST before reaching PROD
- Document what each alias and version contains

## Summary

Stage variables in API Gateway combined with Lambda aliases provide a robust deployment strategy. This pattern enables:
- Blue-green deployments
- Canary releases
- Environment-specific routing
- Version management without API redeployment
