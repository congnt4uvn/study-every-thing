# AWS Lambda and S3 Integration

## Overview
This guide demonstrates how to configure an AWS Lambda function to be triggered automatically when objects are uploaded to an S3 bucket.

## Prerequisites
- AWS Account with access to Lambda and S3 services
- Basic understanding of AWS services
- Permissions to create Lambda functions and S3 buckets

## Step-by-Step Tutorial

### 1. Create Lambda Function
1. Navigate to the AWS Lambda service
2. Create a new function named **Lambda-S3**
3. Select **Python 3.8** as the runtime
4. Click "Create function"

### 2. Create S3 Bucket
1. Navigate to the S3 service
2. Create a new bucket with a unique name (e.g., `demo-s3-event-stephane`)
3. **Important**: Ensure the bucket is in the same region as your Lambda function (e.g., Ireland)
4. Scroll down and click "Create Bucket"

### 3. Configure S3 Event Notification
1. Go to your newly created bucket
2. Navigate to the **Properties** tab
3. Scroll down to find **Event notifications** section
4. Click "Create event notification"
5. Configure the notification:
   - **Name**: invoke-lambda
   - **Prefix**: (leave empty for all objects)
   - **Suffix**: (leave empty for all objects)
   - **Event types**: Select "All object create events"
6. Set the destination:
   - Choose **Lambda function**
   - Select your Lambda function from the dropdown (Lambda-S3)
7. Save changes

### 4. Verify Integration
1. Refresh your Lambda function page
2. You should now see **S3** on the left side as a trigger
3. This confirms that S3 is configured to invoke your Lambda function

### 5. Modify Lambda Function
Update your Lambda function code to print the event data:

```python
import json

def lambda_handler(event, context):
    print(event)
    # Process the S3 event here
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

Deploy the changes.

### 6. Understanding Permissions
- Navigate to **Configuration** → **Permissions** in your Lambda function
- Review the IAM role and execution policies
- The Lambda function needs appropriate permissions to be invoked by S3

## Key Concepts

### S3 Event Notification
- S3 can send notifications when specific events occur in a bucket
- Supported destinations: Lambda, SNS, SQS
- Event types include: object creation, deletion, restoration, etc.

### Lambda Trigger
- S3 acts as an event source for Lambda
- When an object is uploaded, S3 automatically invokes the Lambda function
- The event object contains metadata about the S3 operation

### Region Consistency
- **Critical**: Lambda function and S3 bucket must be in the same AWS region
- Cross-region triggers are not directly supported

## Best Practices
1. Always test with small objects first
2. Monitor Lambda execution logs in CloudWatch
3. Set appropriate timeout values for your Lambda function
4. Consider error handling and retry logic
5. Be aware of Lambda concurrency limits when dealing with high-volume S3 uploads

## Common Use Cases
- Image/video processing upon upload
- Data validation and transformation
- File format conversion
- Triggering workflows based on file uploads
- Logging and auditing S3 operations

## Troubleshooting
- If the trigger doesn't appear, check IAM permissions
- Verify both services are in the same region
- Check CloudWatch logs for execution errors
- Ensure the Lambda function has proper execution role

## Additional Resources
- AWS Lambda Documentation
- AWS S3 Event Notifications Documentation
- AWS IAM Best Practices
