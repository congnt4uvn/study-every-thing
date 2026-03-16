# AWS SSM Parameter Store - Study Guide

## Overview

AWS Systems Manager (SSM) Parameter Store is a secure storage solution for managing configuration and secrets across your AWS applications and infrastructure.

## Key Features

### 1. **Secure Storage**
- Stores configuration and secrets securely
- Optional encryption using AWS KMS (Key Management Service)
- Encrypted data is protected both at rest and during transmission

### 2. **Serverless & Scalable**
- Fully managed service (no infrastructure to manage)
- Automatically scales with your needs
- Durable storage with built-in redundancy

### 3. **Easy Integration**
- Simple SDK for developers to use
- Full integration with AWS CloudFormation
- CloudFormation can use parameters as input for stacks

### 4. **Version Tracking**
- Automatic versioning when parameters are updated
- Easy rollback to previous versions
- Track parameter change history

### 5. **Security & Monitoring**
- Access control through IAM (Identity and Access Management)
- Notifications via Amazon EventBridge
- Audit trail of all parameter access and modifications

## Parameter Hierarchy & Organization

Parameters can be organized in a hierarchical structure using paths:

```
/my-department/
  ├── my-app/
  │   ├── /dev/
  │   │   ├── DB-URL
  │   │   └── DB-password
  │   └── /prod/
  │       ├── DB-URL
  │       └── DB-password
  └── another-app/
      ...
```

This structured approach:
- Organizes parameters logically
- Simplifies IAM policy management
- Allows applications to access entire departments or specific paths

## Types of Parameters

### 1. **Plain Text Configuration**
- Unencrypted parameters
- Suitable for non-sensitive configuration
- Faster retrieval

### 2. **Encrypted Configuration (Secrets)**
- Encrypted using KMS
- Requires KMS key permissions for applications
- Suitable for sensitive data like passwords, API keys

## How It Works

1. **Application requests parameter** from Parameter Store
2. **IAM permissions checked** to verify access
3. **If encrypted:** KMS service handles decryption
4. **Parameter retrieved** and returned to application

### Access Requirements
- Application must have IAM permissions to Parameter Store
- For encrypted parameters, application needs access to the KMS key
- Common scenarios: EC2 instance roles, Lambda execution roles, ECS task roles

## Use Cases

- Database credentials
- API keys and tokens
- Application configuration
- Feature flags
- License keys
- Environment-specific settings

## Best Practices

1. Use hierarchical naming for organization
2. Encrypt sensitive data with KMS
3. Use IAM policies to restrict access by path
4. Enable version tracking for audit purposes
5. Use EventBridge for notifications on parameter changes
6. Regularly audit parameter access
7. Implement principle of least privilege in IAM policies

## Retrieval with IAM

By organizing parameters in a hierarchy, you can grant permissions at different levels:
- Grant access to entire `/my-department/` path
- Or restrict to specific `/my-department/my-app/dev/` path
- This greatly simplifies permission management
