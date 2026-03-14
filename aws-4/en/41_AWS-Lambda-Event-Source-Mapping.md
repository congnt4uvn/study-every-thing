# AWS Lambda Event Source Mapping

## Overview

Event Source Mapping is one of the three ways Lambda can process events in AWS, alongside asynchronous and synchronous processing.

## Applicable Services

Event Source Mapping applies to:
- **Kinesis Data Streams**
- **SQS and SQS FIFO queues**
- **DynamoDB Streams**

## How It Works

### Core Concept

The common denominator of these services is that **records need to be polled from the source**. Lambda actively asks the service to retrieve records, rather than receiving them passively.

### Processing Flow

1. Lambda service is configured to read from a source (e.g., Kinesis)
2. An **Event Source Mapping** is created internally
3. Event Source Mapping polls the service (e.g., Kinesis)
4. Service returns a batch of records
5. Event Source Mapping invokes Lambda function **synchronously** with the event batch

```
[Kinesis] <-- polling -- [Event Source Mapping] --> [Lambda Function]
                                                      (synchronous invocation)
```

## Two Categories

### 1. Streams
Applies to:
- Kinesis Data Streams
- DynamoDB Streams

#### Stream Characteristics

- **Iterator per shard**: Event Source Mapping creates an iterator for each Kinesis shard or DynamoDB Stream shard
- **Processing order**: Items are processed in order at the shard level
- **Configurable start position**: 
  - Read only new items
  - Read from the beginning of the shard
  - Read from a specific timestamp
- **Non-destructive reads**: Processed items are NOT removed from streams, allowing other consumers to read the same data

### 2. Queues
Applies to:
- SQS
- SQS FIFO queues

## Key Points

✓ Lambda function is invoked **synchronously** with Event Source Mapping
✓ Lambda **polls** (pulls) data from the source rather than receiving push notifications
✓ Processing maintains order at the shard level for streams
✓ Data remains in streams after processing, enabling multiple consumers

## Use Cases

Event Source Mapping is ideal for:
- Processing streaming data from Kinesis
- Handling messages from SQS queues
- Reacting to database changes via DynamoDB Streams
- Scenarios requiring ordered processing per shard
- Multiple consumer patterns where data needs to persist after processing
