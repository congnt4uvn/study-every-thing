# AWS Lambda Configuration Study Guide

## Overview
This document covers key configuration options for AWS Lambda functions, focusing on memory, CPU, and timeout settings.

## Memory Configuration

### Memory Range
- **Minimum**: 128 MB
- **Maximum**: 10,240 MB (10 GB)
- Memory can be configured anywhere within this range

### Key Points
- More memory = More CPU power (proportional relationship)
- Higher memory = Higher costs
- **Important**: Monitor Lambda function memory usage to optimize costs
- Set memory according to actual needs - not too little (performance issues), not too much (over-billing)

## CPU Configuration

### Important Exam Topic ⚠️
**There is NO way to change CPU independently from memory in AWS Lambda**

- CPU is automatically allocated proportionally to memory
- To get faster CPU or more CPU cores: **Increase memory allocation**
- This is a very popular exam question

## Timeout Configuration

### What is Timeout?
- Defines how long the Lambda function can run before Lambda throws an error
- Default: Can be set to any value up to the maximum timeout (15 minutes)

### Example Scenario
- If timeout is set to **3 seconds**:
  - Lambda function with 2-second work duration: ✅ Succeeds
  - Lambda function with 5-second work duration: ❌ Fails (timeout error)

### Best Practice
- Set timeout based on expected function execution time
- Leave buffer room for variations in execution time
- Monitor actual execution durations to optimize timeout settings

## Hands-On Example

```python
import time

def lambda_handler(event, context):
    time.sleep(2)  # Simulates 2 seconds of work
    return "prod"
```

**Result**: Function completes successfully (~2000 milliseconds duration)

```python
import time

def lambda_handler(event, context):
    time.sleep(5)  # Simulates 5 seconds of work
    return "prod"
```

**Result**: Function fails if timeout is set to 3 seconds

## Summary
1. **Memory** controls both memory allocation and CPU power
2. **CPU** cannot be configured independently - adjust memory instead
3. **Timeout** prevents functions from running indefinitely
4. Always optimize settings based on actual usage to control costs
