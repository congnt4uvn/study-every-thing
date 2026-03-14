# AWS Lambda Concurrency Study Guide

## Overview
This document covers AWS Lambda concurrency settings and configuration, including reserved concurrency and provisioned concurrency.

## Lambda Concurrency Basics

### Unreserved Account Concurrency
- Default concurrency setting for Lambda functions
- By default: **1000 concurrent executions** per account
- Shared across all Lambda functions in the account
- Can be used by any function that doesn't have reserved concurrency

### Reserved Concurrency
Reserved concurrency allocates a specific number of concurrent executions for a Lambda function.

#### How It Works
- You can set a specific concurrency limit for a function
- Example: Setting reserved concurrency to **20** for a function
  - This function gets 20 guaranteed concurrent executions
  - Account unreserved concurrency becomes: 1000 - 20 = **980**
  - Other functions share the remaining 980 concurrent executions

#### Testing Throttling
- Set reserved concurrency to **0** to test throttling behavior
- Function will always be throttled
- Useful for testing error handling in applications
- Error returned: "Exceeded rate" from the invoke API action

#### Configuration Steps
1. Navigate to Lambda function configuration
2. Select **Concurrency** tab on the left side
3. Click **Edit**
4. Choose between:
   - Use unreserved account concurrency
   - Reserve concurrency (specify number)
5. Save changes

## Provisioned Concurrency

### Purpose
- Eliminates **cold starts** in Lambda functions
- Cold starts occur when application first initializes
- Takes time to start up the execution environment

### How It Works
- Keeps a warm pool of initialized function instances
- Reduces latency for function invocations
- Instances are pre-initialized and ready to respond immediately

### Configuration
- Add provisioned concurrency configuration
- Can be set for:
  - **Alias** - named pointer to a function version
  - **Version** - immutable snapshot of function code and configuration
- Specify the number of provisioned concurrent executions needed

## Best Practices

1. **Monitor Your Concurrency Usage**
   - Track how many concurrent executions your functions need
   - Adjust reserved concurrency based on actual usage patterns

2. **Test Throttling Scenarios**
   - Set concurrency to 0 to test application behavior under throttling
   - Implement proper error handling for rate exceeded errors

3. **Use Provisioned Concurrency for Latency-Sensitive Applications**
   - Recommended for applications that require consistent low latency
   - Trade-off: Higher cost for always-ready instances

4. **Balance Between Functions**
   - Remember: Reserved concurrency reduces available concurrency for other functions
   - Plan concurrency allocation across all functions in your account

## Key Takeaways

- **Unreserved Concurrency**: Default shared pool (1000 per account)
- **Reserved Concurrency**: Dedicated allocation for specific functions
- **Provisioned Concurrency**: Pre-warmed instances to eliminate cold starts
- **Testing**: Set concurrency to 0 to test throttling behavior
- **Configuration**: Accessible in Lambda console under Concurrency tab

## Common Error Messages

**"Calling the invoke API action failed because we have exceeded the rate"**
- Occurs when function exceeds its reserved concurrency limit
- Or when account reaches unreserved concurrency limit
- Solution: Increase reserved concurrency or use unreserved account concurrency
