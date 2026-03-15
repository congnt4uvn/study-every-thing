# AWS Session State Storage Options

## Overview

This document covers different AWS services that can be used for storing session states in web applications, along with their use cases and differences.

## Storage Options for Session States

### 1. **DynamoDB**

- **Type**: Serverless NoSQL database
- **Storage Type**: Key/value store
- **Characteristics**:
  - Serverless architecture
  - Automatic scaling
  - Persistent storage (not entirely in-memory)
  - Can share user login across backend web applications
  
**Best for**: Scenarios requiring automatic scaling and serverless solutions

### 2. **ElastiCache**

- **Type**: In-memory caching service
- **Storage Type**: Key/value store
- **Characteristics**:
  - Fully in-memory
  - Very fast access
  - Can share session states across instances
  
**Best for**: Scenarios requiring in-memory session storage for maximum performance

### 3. **Amazon EFS (Elastic File System)**

- **Type**: Network file system
- **Storage Type**: File system
- **Characteristics**:
  - Must be attached to EC2 instances as a network drive
  - Can be shared across many EC2 instances
  - Disk-based storage
  
**Best for**: When you need to share data on disk across many EC2 instances

### 4. **EBS Volumes & EC2 Instance Store** ❌

- **Type**: Local storage
- **Limitation**: Attached to only one EC2 instance
- **Use Case**: Local caching only, NOT for shared caching
  
**Not suitable for**: Sharing session states across multiple instances

### 5. **Amazon S3** ❌

- **Type**: Object storage
- **Limitation**: Higher latency
- **Designed for**: Big files, not small objects
  
**Not suitable for**: Session state storage (not optimal for this use case)

## Comparison Table

| Service | Type | Memory/Disk | Shared Across Instances | Best Use Case |
|---------|------|-------------|-------------------------|---------------|
| **DynamoDB** | Database | Serverless | ✅ Yes | Automatic scaling, serverless |
| **ElastiCache** | Cache | In-memory | ✅ Yes | In-memory, high performance |
| **EFS** | File System | Disk | ✅ Yes | Shared file system storage |
| **EBS/Instance Store** | Local Storage | Disk | ❌ No | Local caching only |
| **S3** | Object Storage | Disk | ✅ Yes | Large files (not session states) |

## Key Exam Tips

### DynamoDB vs ElastiCache

- **ElastiCache**: Choose when exam mentions "in-memory" requirement
- **DynamoDB**: Choose when exam mentions "automatic scaling" or "serverless"
- Both are key/value stores and suitable for session states

### Best Options for Session States

**Top 3 choices**:
1. DynamoDB
2. ElastiCache  
3. EFS

**Preferred**: DynamoDB and ElastiCache are the best two options

## Summary

When storing session states in AWS:
- ✅ **Use DynamoDB** for serverless, auto-scaling solutions
- ✅ **Use ElastiCache** for fully in-memory, high-performance needs
- ✅ **Use EFS** when you need a shared file system
- ❌ **Avoid EBS/Instance Store** for shared session states
- ❌ **Avoid S3** for session state storage (high latency for small objects)
