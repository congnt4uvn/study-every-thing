# AWS DynamoDB - Security and Features Study Guide

## Overview
This document covers essential security features and capabilities of Amazon DynamoDB, a fully managed NoSQL database service in AWS.

## Security Features

### 1. VPC Endpoints
- **Purpose**: Access DynamoDB without using the public internet
- **Benefit**: All traffic remains within your VPC for enhanced security
- **Use Case**: Secure, private connection to DynamoDB from your VPC

### 2. Access Control via IAM
- **Full IAM Integration**: DynamoDB access is completely controlled by IAM
- **Granular Permissions**: Define specific permissions for users and roles
- **Best Practice**: Makes it a great database choice in AWS environments

### 3. Encryption
- **At Rest**: Uses AWS KMS (Key Management Service)
- **In Transit**: Secured using SSL/TLS protocols
- **Compliance**: Meets security and compliance requirements

## Backup and Restore

### Point-in-Time Recovery (PITR)
- Similar to RDS PITR functionality
- **No performance impact** during backup operations
- Enable continuous backups for disaster recovery

### Standard Backup and Restore
- Create on-demand backups
- Restore tables to any point in time

## Global Tables

### Multi-Region Replication
- **Multi-region**: Deploy across multiple AWS regions
- **Multi-active**: Active-active replication
- **Fully replicated**: Data synchronized across all regions
- **High-performance**: Low-latency access globally

### Prerequisites
- Must enable **DynamoDB Streams** first
- Streams capture item-level changes for replication

## DynamoDB Local

### Development Tool
- **Purpose**: Local simulation of DynamoDB
- **Benefits**:
  - Develop and test applications locally
  - No need to connect to AWS service
  - Cost-effective for development
  - Offline development capability

## Data Migration

### AWS Database Migration Service (DMS)
- Migrate data **to** and **from** DynamoDB
- **Supported Sources/Targets**:
  - MongoDB ↔ DynamoDB
  - DynamoDB ↔ Oracle
  - DynamoDB ↔ MySQL
  - DynamoDB ↔ S3
  - And more...

## Fine-Grained Access Control

### Use Case
- Web and mobile applications need direct access to DynamoDB
- **Problem**: Don't want to create individual IAM users for each client
- **Solution**: Use federated identity with temporary credentials

### Identity Providers
- Amazon Cognito User Pools
- Google Login
- Facebook Login
- OpenID Connect
- SAML
- Other identity providers

### Authentication Flow
1. Users login through identity provider
2. Exchange credentials for **temporary AWS credentials**
3. Temporary credentials are more secure
4. Credentials associated with restricted IAM role

### Row-Level Access Control

#### Using LeadingKeys Condition
```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:BatchGetItem",
    "dynamodb:Query",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:BatchWriteItem"
  ],
  "Resource": "arn:aws:dynamodb:region:account:table/TableName",
  "Condition": {
    "ForAllValues:StringEquals": {
      "dynamodb:LeadingKeys": [
        "${cognito-identity.amazonaws.com:sub}"
      ]
    }
  }
}
```

**Key Points**:
- LeadingKeys restricts access at the **row level**
- Users can only access/modify data where primary key matches their identity
- `${cognito-identity.amazonaws.com:sub}` is replaced at runtime with actual user ID

### Column-Level Access Control

#### Using Attribute Conditions
- Specify conditions on **attributes**
- Limits which columns (attributes) a user can see
- Provides attribute-level security

## Summary

### Fine-Grained Access Control Implementation
1. **Federated Login**: Use identity providers for authentication
2. **Temporary Credentials**: Exchange for AWS temporary credentials
3. **Restricted IAM Role**: Apply conditions to limit access
4. **LeadingKeys Condition**: For row-level access control
5. **Attribute Conditions**: For column-level access control

### Security Best Practices
- ✅ Use VPC endpoints for private connectivity
- ✅ Implement IAM policies with least privilege
- ✅ Enable encryption at rest and in transit
- ✅ Use fine-grained access control for client applications
- ✅ Enable PITR for disaster recovery
- ✅ Use DynamoDB Local for development/testing

## Key Takeaways
- DynamoDB provides enterprise-grade security features
- Fine-grained access control enables secure direct client access
- Global tables offer multi-region high availability
- Multiple backup options ensure data durability
- DMS facilitates easy data migration

---
*Last Updated: March 15, 2026*
