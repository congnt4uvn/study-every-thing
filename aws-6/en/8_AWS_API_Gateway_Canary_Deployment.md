# AWS API Gateway Canary Deployment

## Overview
Canary deployment is a strategy in AWS API Gateway that allows you to test new API versions by gradually rolling them out to a small percentage of users before deploying to all users. This minimizes the risk of introducing breaking changes.

## Key Concepts

### What is a Canary Deployment?
- A deployment strategy that routes a percentage of traffic to a new version while keeping the rest on the stable version
- Allows safe testing of new changes in production
- Can be promoted to full deployment or rolled back if issues arise

### Lambda Function Versions
- Lambda functions can have multiple versions (v1, v2, etc.)
- Each version can be independently invoked
- Versions are specified using a colon notation (e.g., `function-name:1`)

## Step-by-Step Demo

### 1. Create API Gateway Resource
1. Create a new resource called `canary-demo`
2. Add a GET method with Lambda function integration
3. Enable Lambda proxy integration
4. Link to Lambda function `stage-variables-get`

### 2. Configure Lambda Version
- Point to version 1 by adding `:1` to the Lambda function name
- Version 1 returns: "Hello from Lambda v1"
- Version 2 returns: "Hello from Lambda v2"

### 3. Test Initial Setup
```
GET /canary-demo
Response: "Hello from Lambda v1"
```

### 4. Deploy to Stage
1. Deploy API to a new stage
2. Name the stage "canary"
3. Test the invoke URL: `/canary/canary-demo`
4. Verify response: "Hello from Lambda v1"

### 5. Create Canary Deployment
1. Navigate to the Canary tab in the stage
2. Click "Create Canary"
3. Set distribution percentage:
   - **For demo**: 50% canary / 50% current stage
   - **For production**: Typically 10-20% for canary
4. Create the canary

### 6. Update to Version 2
1. Go back to Resources
2. Select the GET method on `canary-demo`
3. Edit the integration request
4. Change from version 1 (`:1`) to version 2 (`:2`)
5. Save changes
6. Test: Should now return "Hello from Lambda v2"

### 7. Deploy to Canary
1. Deploy API
2. Select the "Canary" stage
3. Complete deployment

### 8. Test Canary Distribution
- Navigate to the invoke URL and refresh multiple times
- Observe alternating responses:
  - "Hello from Lambda v1" (50% of requests)
  - "Hello from Lambda v2" (50% of requests)
- This confirms the canary is routing traffic between versions

### 9. Promote Canary
1. Once testing is complete and v2 is verified
2. Click "Promote Canary"
3. This updates the entire stage to the canary deployment
4. All traffic (100%) now goes to version 2
5. Test: All requests return "Hello from Lambda v2"

## Summary

**Canary Deployment Workflow:**
1. Modify your API resource/method
2. Create a canary in your stage with desired traffic percentage
3. Deploy changes to the canary
4. Test with the split traffic distribution
5. Promote canary to production (100% traffic) when ready

**Benefits:**
- Minimized risk when deploying changes
- Ability to test in production with real traffic
- Easy rollback if issues are detected
- Gradual migration path for API updates

**Best Practices:**
- Start with a small percentage (5-10%) for critical APIs
- Monitor metrics during canary deployment
- Use CloudWatch to track errors and latency
- Set a time limit for canary testing before promoting or rolling back
