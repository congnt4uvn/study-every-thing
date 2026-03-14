# AWS Lambda: Event and Context Objects

## Overview

Understanding the **event** and **context** objects is crucial when working with AWS Lambda functions. These two objects provide all the necessary information for your Lambda function to execute properly.

## Event Object

### What is the Event Object?

The event object is a JSON-formatted document that contains data for the function to process. It is created and passed by the invoking service (such as EventBridge, SQS, SNS, etc.) to your Lambda function.

### Key Characteristics

- **Format**: JSON-formatted document
- **Source**: Created by the invoking AWS service
- **Purpose**: Contains all the data and information needed for your Lambda function to process the event
- **Runtime Conversion**: Converted to appropriate data structures based on your runtime
  - For Python: Converted into a dictionary
  - For other languages: Converted to equivalent data structures

### Event Object Contents

The event object includes:
- Details about the event itself
- The source service that emitted the event
- The region where the event originated
- Service-specific data related to the event
- Any arguments or parameters from the invoking service

### Example Use Case

When EventBridge invokes your Lambda function:
1. EventBridge creates an event
2. The event is passed to your Lambda function
3. Your function receives it as the event object
4. Your function processes the data contained in the event

## Context Object

### What is the Context Object?

The context object provides metadata and methods about the Lambda function invocation itself and the runtime environment. It is passed to your Lambda function at runtime.

### Key Characteristics

- **Format**: Object with methods and properties
- **Source**: Automatically provided by AWS Lambda runtime
- **Purpose**: Provides metadata about the function execution environment
- **Timing**: Passed at runtime

### Context Object Contents

The context object includes:
- AWS request ID
- Function name
- Associated log group
- Memory limit (in megabytes)
- Runtime environment information
- Other invocation metadata

## Using Event and Context in Your Code

### Python Example

```python
def handler(event, context):
    # Access event data
    event_source = event.get('source')
    event_region = event.get('region')
    
    # Access context information
    request_id = context.aws_request_id
    function_name = context.function_name
    memory_limit = context.memory_limit_in_mb
    
    # Process your logic here
    print(f"Event source: {event_source}")
    print(f"Request ID: {request_id}")
    
    return {
        'statusCode': 200,
        'body': 'Success'
    }
```

## Key Differences

| Aspect | Event Object | Context Object |
|--------|--------------|----------------|
| **Purpose** | Contains event data to process | Contains metadata about invocation |
| **Source** | Invoking service (EventBridge, SQS, etc.) | AWS Lambda runtime |
| **Content** | Business/event data | Function execution metadata |
| **Format** | JSON (converted to runtime object) | Runtime object with methods |

## Summary

- **Event Object**: What to process (the data)
- **Context Object**: Information about the processing environment (the metadata)
- Both objects are complementary and essential for Lambda function execution
- Always available in your Lambda handler function
