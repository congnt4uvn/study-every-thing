# AWS SAM and CodeDeploy Integration

## Overview

This document covers how AWS CodeDeploy integrates with the Serverless Application Model (SAM) framework to safely deploy and update Lambda functions using traffic shifting features.

## Key Concepts

### CodeDeploy with SAM Framework

SAM uses CodeDeploy to update Lambda functions, leveraging:
- **Traffic shifting** with Lambda aliases
- **Pre and post-traffic hooks** using Lambda functions to validate deployments
- **Automated rollbacks** triggered by CloudWatch alarms

### Deployment Workflow

1. **Initial State**: Lambda alias points to v1 of the function
2. **Trigger Deployment**: Via CI/CD pipeline or SAM framework
3. **Pre-Traffic Hook** (Optional): Lambda function runs tests before traffic shift
4. **Traffic Shifting**: Gradual shift of traffic from v1 to v2 according to strategy
5. **Monitoring** (Optional): CloudWatch alarms monitor deployment health
6. **Post-Traffic Hook** (Optional): Lambda function runs tests after traffic shift
7. **Completion**: Alias fully points to v2, v1 is deprecated

## SAM Configuration

### Key YAML Components

#### AutoPublishAlias

```yaml
AutoPublishAlias: live
```

- Helps SAM detect when new code is deployed
- Creates a new Lambda version with the latest code
- Automatically updates the alias to point to the new version

#### DeploymentPreference

Controls the deployment strategy and monitoring:

```yaml
DeploymentPreference:
  Type: Canary10Percent10Minutes
  Alarms:
    - MyCloudWatchAlarm
  Hooks:
    PreTraffic: !Ref PreTrafficHookFunction
    PostTraffic: !Ref PostTrafficHookFunction
```

### Deployment Types

1. **Canary**: Shifts a percentage of traffic, then waits before shifting remaining traffic
   - Example: `Canary10Percent10Minutes` - 10% traffic for 10 minutes, then 100%

2. **Linear**: Gradually increases traffic at regular intervals
   - Example: `Linear10PercentEvery10Minutes` - increases by 10% every 10 minutes

3. **AllAtOnce**: Immediately shifts all traffic to the new version

### Components

#### Alarms
- List of CloudWatch alarms to monitor during deployment
- Can trigger automatic rollback if thresholds are breached
- Example: Monitoring error rates on the new version

#### Hooks
- **PreTraffic**: Lambda function executed before traffic shifting begins
- **PostTraffic**: Lambda function executed after traffic shifting completes
- Used for custom validation and testing

## Practical Implementation

### Setup Steps

1. Create SAM application directory:
   ```bash
   mkdir sam-codedeploy
   cd sam-codedeploy
   ```

2. Initialize SAM application:
   ```bash
   sam init
   ```
   - Select Python runtime (e.g., Python 3.7)
   - Choose "Hello World Example" template
   - Name the project (e.g., sam-app)

3. Build the SAM application:
   ```bash
   cd sam-app
   sam build
   ```

4. Configure CodeDeploy in `template.yaml`:
   - Add `AutoPublishAlias` property
   - Configure `DeploymentPreference` settings
   - Define alarms and hooks as needed

### Template Structure

The SAM template includes:
- `Serverless::Function` resource definition
- Function handler (e.g., `app.py` returning "hello world")
- Outputs for function ARN and API endpoints
- CodeDeploy configuration integrated into the function definition

## Best Practices

- **Use Alarms**: Always configure CloudWatch alarms to monitor deployment health
- **Test Hooks**: Implement pre and post-traffic hooks for critical applications
- **Choose Appropriate Strategy**: Select deployment type based on risk tolerance
- **Monitor Metrics**: Watch for errors, latency, and throttling during deployments
- **Plan Rollbacks**: Ensure rollback mechanisms are tested and functional

## Benefits

- **Safe Deployments**: Gradual traffic shifting reduces risk
- **Automated Testing**: Hooks enable automated validation
- **Quick Rollback**: Automatic rollback on alarm triggers
- **Version Control**: Maintains multiple Lambda versions during transition
- **Monitoring Integration**: CloudWatch alarms provide deployment visibility

## Summary

SAM and CodeDeploy integration provides a robust framework for safely deploying Lambda function updates with built-in traffic management, testing hooks, and automated rollback capabilities. This approach minimizes deployment risks and ensures application stability during updates.
