# AWS Lambda and EventBridge Integration

## Overview
This guide demonstrates how to integrate AWS Lambda with Amazon EventBridge to automatically invoke Lambda functions on a schedule or based on events.

## Creating a Lambda Function

1. **Create a new Lambda function**
   - Function name: `lambda-demo-eventbridge`
   - Runtime: Python 3.9
   - The function will be invoked by EventBridge

## EventBridge Configuration

### Creating an EventBridge Rule

1. **Navigate to EventBridge Console**
   - Go to **Rules** section
   - Create a new rule

2. **Rule Configuration**
   - Rule name: `InvokeLambdaEveryMinute`
   - Event bus: Default Event bus

3. **Rule Types**
   
   **Option 1: Event Pattern**
   - Use this to match events happening within AWS
   - Examples:
     - Code committed to CodeCommit
     - EC2 instance terminated
     - Other AWS service events
   
   **Option 2: Schedule** (Used in this demo)
   - Triggers function on a regular schedule
   - Can use Cron expressions or fixed intervals

### Setting Up the Schedule

1. **Schedule Pattern Options**
   - **Cron expression**: For complex scheduling patterns
   - **Fixed-rate schedule**: For regular intervals (e.g., every 1 minute)

2. **Configuration**
   - Set schedule to run every 1 minute
   - Click **Next**

### Configuring the Target

1. **Select Target Type**
   - Choose **Lambda function**

2. **Select Lambda Function**
   - Function: `lambda-demo-eventbridge`

3. **Additional Settings** (Optional)
   - Specific version or alias
   - Dead-letter queue configuration
   - Maximum retry attempts
   - Other advanced settings

## Key Concepts

### EventBridge vs EventBridge Scheduler
- **EventBridge Rules**: Traditional rule-based invocations
- **EventBridge Scheduler**: New service with enhanced scheduling capabilities
- Both provide similar functionality with different interfaces

### Resource Policies
EventBridge automatically manages the necessary permissions to invoke your Lambda function through resource policies.

## Use Cases

- **Scheduled Tasks**: Running Lambda functions at regular intervals
- **Event-Driven Architecture**: Responding to AWS service events
- **Automation**: Triggering workflows based on AWS infrastructure changes
- **Monitoring and Alerts**: Processing events and sending notifications

## Best Practices

1. **Error Handling**: Configure dead-letter queues for failed invocations
2. **Retry Logic**: Set appropriate maximum retry attempts
3. **Monitoring**: Use CloudWatch to monitor function invocations
4. **Version Control**: Use Lambda versions and aliases for production deployments
5. **Testing**: Test your EventBridge rules thoroughly before production use

## Additional Resources

- AWS Lambda Documentation
- Amazon EventBridge Documentation
- EventBridge Scheduler Documentation
