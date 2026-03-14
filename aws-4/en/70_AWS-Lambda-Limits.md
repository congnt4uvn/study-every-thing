# AWS Lambda Limits - Study Guide

## Overview
AWS Lambda has specific limits that vary per region. These limits are important to understand for the AWS certification exam, as they help determine whether Lambda is suitable for a particular workload.

## Execution Limits

### Memory Allocation
- **Range**: 128 MB to 10 GB
- **Increments**: 64 MB
- **Note**: Increasing memory also increases vCPU allocation

### Maximum Execution Time
- **Limit**: 900 seconds (15 minutes)
- **Implication**: Workloads requiring longer execution times are not suitable for Lambda

### Environment Variables
- **Size Limit**: 4 KB
- **Use Case**: Store configuration data and parameters

### Temporary Storage (/tmp)
- **Capacity**: Up to 10 GB
- **Use Case**: Pull in large files during function execution
- **Note**: Use this for files that exceed deployment size limits

### Concurrent Executions
- **Default Limit**: 1,000 concurrent executions across all Lambda functions
- **Scalability**: Can be increased through AWS support request
- **Best Practice**: Use reserved concurrency early on to manage capacity

## Deployment Limits

### Function Package Size
- **Compressed (.zip)**: 50 MB maximum
- **Uncompressed**: 250 MB maximum
- **Workaround**: For larger files, use the /tmp directory instead

### Environment Variables
- **Size Limit**: 4 KB (same as execution limit)

## Exam Tips

When you see exam questions with the following requirements, Lambda is **NOT** the right solution:

❌ Requires 30 GB of RAM (exceeds 10 GB limit)
❌ Needs 30 minutes of execution time (exceeds 15 minutes limit)
❌ Requires a 3 GB deployment file (exceeds 250 MB uncompressed limit)

## Key Takeaways

1. All limits are **per region**
2. Know the difference between **execution** and **deployment** limits
3. Remember the /tmp directory (10 GB) for handling large files during execution
4. Understand when Lambda is NOT suitable for a workload
5. Memory and vCPU are linked - more memory = more vCPU

---
*Study Date: March 14, 2026*
