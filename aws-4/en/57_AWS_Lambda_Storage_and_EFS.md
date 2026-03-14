# AWS Lambda Storage and EFS Integration

## File System Mounting with Lambda

### Overview
Lambda functions can access Amazon EFS (Elastic File System) file systems when running in a VPC. This provides persistent, shared storage for serverless applications.

### Configuration Requirements
To mount an EFS file system to a Lambda function:
- Configure Lambda to mount the EFS file system to a local directory during initialization
- Use **EFS Access Points** feature
- Deploy Lambda functions in a **Private Subnet** with connectivity to the VPC

### Architecture
```
EFS File System
    ↓
EFS Access Point
    ↓
Lambda Function (Private Subnet) → VPC
```

### Limitations
- **Connection Limits**: Each Lambda instance creates one connection to the EFS file system
  - Monitor to avoid hitting EFS connection limits
- **Burst Limits**: Multiple Lambda functions starting simultaneously may hit connection burst limits

---

## Lambda Storage Options Comparison

### 1. Ephemeral Storage (/tmp)

| Property | Details |
|----------|---------|
| **Max Size** | 10 GB |
| **Persistence** | Ephemeral (lost when function instance is destroyed) |
| **Content** | Dynamic (can be modified) |
| **Type** | File system with full file system operations |
| **Cost** | Included up to 512 MB, pay for additional storage |
| **Access** | Single function only (not shared) |
| **Performance** | Fastest level of data retrieval |
| **Sharing** | Not shared across function invocations |

**Use Case**: Temporary storage for function execution, downloads, or processing temporary files.

### 2. Lambda Layers

| Property | Details |
|----------|---------|
| **Max Size** | 5 layers per function, 250 MB total (within package size limit) |
| **Persistence** | Durable (immutable) |

**Use Case**: Share common code, libraries, or dependencies across multiple Lambda functions.

---

## Key Takeaways

1. **EFS Integration** provides persistent, shared storage for Lambda functions
2. **Access Points** are required for Lambda-EFS integration
3. **VPC Configuration** is mandatory for EFS access
4. **Connection Management** is critical to avoid hitting limits
5. **/tmp Storage** is fast but ephemeral
6. **Lambda Layers** are immutable and reusable across functions

---

## Best Practices

- Use EFS for persistent, shared data across multiple Lambda invocations
- Use /tmp for temporary processing within a single invocation
- Use Lambda Layers for shared code and dependencies
- Monitor EFS connection counts when scaling
- Consider burst patterns when designing architecture
