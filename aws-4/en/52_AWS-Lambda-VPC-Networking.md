# AWS Lambda and VPC Networking

## Overview
This document covers how AWS Lambda functions interact with Virtual Private Clouds (VPCs) and how to configure them for private resource access.

## Default Lambda Deployment

By default, Lambda functions are launched **outside of your own VPC** - they operate in an AWS-owned VPC.

### What Lambda Can Access by Default:
- ✅ Public websites
- ✅ External APIs
- ✅ AWS services like DynamoDB

### What Lambda Cannot Access by Default:
- ❌ EC2 instances in your VPC
- ❌ RDS databases in private subnets
- ❌ ElastiCache clusters
- ❌ Internal Elastic Load Balancers

## Deploying Lambda in Your VPC

To access private resources in your VPC, you must configure Lambda to run within your VPC.

### Configuration Requirements:
1. **VPC ID** - Specify your VPC
2. **Subnets** - Define which subnets to use
3. **Security Group** - Assign a security group to Lambda

### How It Works:

When you configure Lambda for VPC access, AWS automatically creates an **Elastic Network Interface (ENI)** in your selected subnets.

#### Required IAM Role:
- **Lambda VPC Access Execution Role** - Lambda needs this role to create the ENI

### Network Flow:

```
Lambda Function → ENI (with Lambda Security Group) → Private Resource (e.g., RDS)
```

### Security Group Configuration:

For Lambda to access resources like RDS:
- The **RDS security group** must allow inbound traffic from the **Lambda security group**
- Similar to how you would configure access for EC2 instances

## Key Points to Remember:

1. Lambda functions run outside your VPC by default
2. VPC configuration is required for accessing private resources
3. Lambda creates an ENI in your subnets (invisible to you)
4. Proper security group rules are essential for connectivity
5. Lambda needs appropriate IAM permissions to create ENIs

## Use Cases:

- Accessing private RDS databases
- Connecting to ElastiCache clusters
- Communicating with internal load balancers
- Interacting with EC2 instances in private subnets
