# AWS Lambda in VPC - Study Guide

## Overview
This guide covers how to deploy AWS Lambda functions within a Virtual Private Cloud (VPC) and understand the networking implications.

## Step-by-Step Practice: Lambda in VPC

### 1. Create a Lambda Function
- Navigate to AWS Lambda console
- Create a new function from scratch
- Function name: `Lambda VPC`
- Runtime: Python 3.8
- Create the function

### 2. Create a Security Group for Lambda
- Go to EC2 console
- Navigate to Security Groups
- Create a new security group:
  - Name: `Lambda SG`
  - Attach to your VPC
  - No inbound rules needed
  - Default outbound rules
- Purpose: To attach to your Lambda function for VPC deployment

### 3. Configure Lambda VPC Settings
- Go to Lambda function Configuration tab
- Select VPC from the left-hand menu
- Click Edit to attach the Lambda function to a VPC

## Important Networking Concepts

### Internet Access Limitations
⚠️ **Warning**: When you connect a Lambda function to a VPC in your account:
- **The function does NOT have internet access** by default
- Even if deployed in public subnets, Lambda cannot access the internet directly

### Requirements for Internet Access
To provide internet access to a VPC-connected Lambda function:
1. Deploy Lambda in **private subnets**
2. Set up a **NAT Gateway** or **NAT Instance** in a public subnet
3. Route outbound traffic through the NAT Gateway/Instance

### Common Use Case
Lambda functions are typically deployed within a VPC to:
- Perform local operations within the VPC
- Access private resources (RDS, ElastiCache, etc.)
- Maintain secure, isolated networking

## Key Takeaways
- Lambda functions in VPC need proper networking configuration
- Public subnets alone don't provide internet access to Lambda
- Use private subnets + NAT Gateway for internet-enabled Lambda in VPC
- Security groups control access to Lambda functions in VPC
