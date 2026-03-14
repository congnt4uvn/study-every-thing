# AWS Lambda and Application Load Balancer Integration

## Overview
This guide demonstrates how to integrate AWS Lambda functions with an Application Load Balancer (ALB) to create a serverless HTTP endpoint.

## Objectives
- Create a Lambda function
- Configure an Application Load Balancer
- Set up a target group for Lambda integration
- Establish secure communication between ALB and Lambda

## Prerequisites
- AWS Account with appropriate permissions
- Basic understanding of AWS services
- Familiarity with Python (for Lambda function)

## Step-by-Step Implementation

### 1. Create Lambda Function

**Function Configuration:**
- **Name:** Lambda-alb
- **Runtime:** Python 3.x
- **Purpose:** Backend compute for ALB requests

**Steps:**
1. Navigate to AWS Lambda console
2. Click "Create function"
3. Enter function name: `Lambda-alb`
4. Select runtime: Python version 3
5. Click "Create function"

### 2. Create Application Load Balancer

**ALB Configuration:**
- **Name:** demo-Lambda-alb
- **Type:** Application Load Balancer
- **Scheme:** Internet-facing
- **IP Address Type:** IPv4
- **Availability Zones:** Deploy across 3 AZs for high availability

**Steps:**
1. Navigate to EC2 > Load Balancers
2. Click "Create Load Balancer"
3. Choose "Application Load Balancer"
4. Configure basic settings with name and scheme
5. Select 3 availability zones for redundancy

### 3. Configure Security Group

**Security Group Settings:**
- **Name:** DemoLambdaALBSG
- **Inbound Rules:**
  - Protocol: HTTP
  - Port: 80
  - Source: 0.0.0.0/0 (anywhere IPv4)

**Steps:**
1. Create new security group
2. Set name: `DemoLambdaALBSG`
3. Add inbound rule for HTTP (port 80) from anywhere
4. Create security group
5. Assign to the load balancer

### 4. Create Target Group

**Target Group Configuration:**
- **Name:** demo-tg-lambda
- **Target Type:** Lambda function
- **Associated Service:** Application Load Balancer only

**Steps:**
1. Navigate to Target Groups
2. Click "Create target group"
3. Select target type: "Lambda function"
4. Enter name: `demo-tg-lambda`
5. Click "Next"
6. Select the Lambda function: `Lambda-alb`
7. Click "Create target group"

### 5. Configure Listener

**Listener Settings:**
- **Protocol:** HTTP
- **Port:** 80
- **Default Action:** Forward to target group `demo-tg-lambda`

**Steps:**
1. In ALB configuration, set up listener
2. Configure to listen on port 80 (HTTP)
3. Set default action to forward requests to `demo-tg-lambda`
4. Complete ALB creation
5. Wait for provisioning to complete

## Architecture Flow

```
Internet Request (HTTP:80)
    ↓
Application Load Balancer (demo-Lambda-alb)
    ↓
Security Group (DemoLambdaALBSG)
    ↓
Target Group (demo-tg-lambda)
    ↓
Lambda Function (Lambda-alb)
```

## Key Concepts

### Application Load Balancer (ALB)
- Layer 7 load balancer
- Routes HTTP/HTTPS traffic
- Can invoke Lambda functions directly
- Provides automatic scaling and high availability

### Lambda Target Groups
- Special target group type for serverless integration
- Automatically handles Lambda invocation
- No need to manage EC2 instances
- Pay only for actual Lambda execution time

### Benefits of ALB + Lambda Integration
1. **Serverless:** No infrastructure to manage
2. **Cost-effective:** Pay per request
3. **Scalable:** Automatic scaling based on traffic
4. **Highly Available:** Multi-AZ deployment
5. **Simple:** Direct integration without API Gateway

## Best Practices

1. **Multi-AZ Deployment:** Always deploy ALB across multiple availability zones
2. **Security Groups:** Restrict inbound traffic to necessary sources only
3. **Lambda Configuration:** Set appropriate timeout and memory settings
4. **Monitoring:** Enable CloudWatch logs for both ALB and Lambda
5. **Testing:** Verify target group health before production use

## Next Steps

After setup:
1. Configure Lambda function code to handle ALB events
2. Test the integration using the ALB DNS name
3. Monitor CloudWatch logs for requests and responses
4. Optimize Lambda function performance
5. Consider adding custom domains and SSL certificates

## Troubleshooting

**Common Issues:**
- Target group showing unhealthy status
- Lambda function timeout errors
- Security group blocking traffic
- IAM permission issues

**Solutions:**
- Verify Lambda function is registered in target group
- Increase Lambda timeout if needed
- Check security group rules
- Ensure proper IAM roles and policies

## Conclusion

Integrating Lambda with Application Load Balancer provides a powerful serverless solution for handling HTTP requests without managing servers. This setup is ideal for microservices, APIs, and web applications that need to scale automatically.
