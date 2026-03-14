# AWS Lambda Function Configuration and Performance

## Lambda RAM Configuration

### Memory Allocation
- **Default**: 128 megabytes of RAM
- **Maximum**: 10 gigabytes of RAM
- **Increments**: 1 megabyte increments

### vCPU Credits and RAM Relationship
- More RAM = More vCPU credits
- **Important**: You cannot set vCPUs directly
- You must increase RAM to implicitly get more vCPU

### vCPU Threshold
- **At 1,792 MB of RAM**: Function gets equivalent of **one full vCPU**
- **Above 1,792 MB**: You get more than one vCPU
- **Multi-threading required** to benefit from additional vCPUs

### CPU-Bound Applications
- If your application is **CPU-bound** (heavy computations):
  - Increase RAM to improve performance
  - This decreases execution time
  - **Common exam question** ⚠️

## Lambda Timeout Configuration

### Default Settings
- **Default timeout**: 3 seconds
- If function runs > 3 seconds → Timeout error

### Maximum Timeout
- **Maximum**: 900 seconds (15 minutes)
- Valid execution range: 0 seconds to 15 minutes

### Use Case Guidelines
- **0-15 minutes**: Good use case for Lambda ✅
- **Above 15 minutes**: Consider alternatives ❌
  - AWS Fargate
  - Amazon ECS
  - Amazon EC2
- **Exam topic** ⚠️

## Lambda Performance and Execution Context

### What is Execution Context?
The execution context is a **temporary runtime environment** that:
- Initializes external dependencies of your Lambda code
- Establishes database connections
- Creates HTTP clients and SDK clients

### Context Persistence
- The execution context is **maintained for some time**
- Anticipates another Lambda function invocation
- Improves performance for subsequent invocations

### Best Practices
- Initialize connections and clients outside the handler function
- Reuse execution context when possible
- Reduces cold start overhead

## Key Exam Points 📝

1. **RAM → vCPU relationship**: Increase RAM to get more vCPU
2. **1,792 MB threshold**: One full vCPU at this memory level
3. **CPU-bound apps**: Increase RAM to improve performance
4. **15-minute limit**: Maximum Lambda execution time
5. **Long-running tasks**: Use Fargate/ECS/EC2 instead of Lambda
6. **Execution context**: Reused across invocations for performance
