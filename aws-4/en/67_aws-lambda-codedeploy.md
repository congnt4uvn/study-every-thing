# AWS Lambda Deployment with CodeDeploy

## Overview
CodeDeploy integrates with AWS Lambda to automate traffic shifting for Lambda aliases, building on the Lambda versions and aliases feature. This is particularly useful when implementing the Serverless Application Model (SAM) framework.

## Traffic Shifting Concept
When upgrading a PROD alias from Lambda function Version 1 (V1) to Version 2 (V2), CodeDeploy gradually shifts traffic from 100% V1 to 100% V2 over time.

**Example Flow:**
- Start: 100% V1, 0% V2
- Step 1: 90% V1, 10% V2
- Step 2: 50% V1, 50% V2
- End: 0% V1, 100% V2

## Deployment Strategies

### 1. Linear Deployment
Gradually increases traffic by a fixed percentage every N minutes until reaching 100%.

**Available Options:**
- `Linear10PercentEvery3Minutes` - Increases traffic by 10% every 3 minutes
- `Linear10PercentEvery10Minutes` - Increases traffic by 10% every 10 minutes

### 2. Canary Deployment
Tests with X% of traffic, then switches to 100%.

**Available Options:**
- `Canary10Percent5Minutes` - Routes 10% traffic to V2 for 5 minutes, then switches to 100%
- `Canary10Percent30Minutes` - Routes 10% traffic to V2 for 30 minutes, then switches to 100%

### 3. AllAtOnce Deployment
Immediate traffic shift from V1 to V2.

**Characteristics:**
- ✅ Quickest deployment method
- ⚠️ Most dangerous - no gradual testing
- ❌ High risk if V2 hasn't been properly tested

## Rollback Mechanisms

### Health Checks
CodeDeploy supports pre and post traffic hooks to monitor Lambda function health during deployment.

### Failure Detection
- **Traffic Hooks** - Can detect and report failures during deployment
- **CloudWatch Alarms** - Can trigger when metrics indicate problems

### Automatic Rollback
When failures are detected through traffic hooks or CloudWatch alarms, CodeDeploy automatically performs a rollback to the previous stable version.

## Integration with SAM
The CodeDeploy feature is fully integrated within the SAM (Serverless Application Model) framework, allowing for practice and implementation of Lambda function deployments.

---

**Key Takeaways:**
- Always test new Lambda versions before production deployment
- Use Canary or Linear strategies for safer deployments
- Set up proper monitoring and CloudWatch alarms
- Configure traffic hooks for automatic health checking
- AllAtOnce should only be used when confident in the new version
