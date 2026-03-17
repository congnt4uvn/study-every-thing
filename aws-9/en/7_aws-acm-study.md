# AWS Study Notes: AWS Certificate Manager (ACM)

## What is ACM?
AWS Certificate Manager (ACM) is a service that helps you easily provision, manage, and deploy SSL/TLS certificates.

## Why certificates matter
SSL/TLS certificates are used to provide in-flight encryption for websites and APIs through HTTPS endpoints.

## Example architecture
- Users connect to an Application Load Balancer (ALB) over HTTPS.
- The ALB forwards traffic to EC2 instances (for example, over HTTP in a private backend).
- ACM provisions and manages the TLS certificate for your domain.
- The certificate is attached to the ALB so clients can use HTTPS securely.

## Key ACM features
- Supports both public and private TLS certificates.
- Public TLS certificates are free.
- Automatic certificate renewal.
- Integrates with AWS services, including:
  - Elastic Load Balancing (ELB/ALB)
  - CloudFront
  - API Gateway

## Quick reminder
If you need in-flight encryption and managed certificates on AWS, think of ACM.
