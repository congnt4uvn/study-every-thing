# AWS API Gateway Security

## Overview
This document covers the security options available for AWS API Gateway, including authentication and authorization mechanisms.

## Key Security Options

### 1. IAM Authorization
- **Location**: Method Request → Authorization section
- **Purpose**: Use IAM policies to control access to your APIs
- **Use Case**: Control which IAM users/roles can invoke API methods
- **Implementation**: Enable IAM authorization at the method level

### 2. Resource Policies
- **Purpose**: Define policies to control access to your API as a whole
- **Key Features**:
  - Cross-account access
  - IP-based access control
  - VPC-based access control

#### Common Resource Policy Templates

##### AWS Account Allow List
- Allow other accounts, users, or roles from other accounts to invoke your API
- Enables cross-account access to API Gateway

##### IP Range Deny List
- Allow or deny specific IP addresses/ranges
- Useful for restricting access based on network location

##### Source VPC Allow List
- Create a private API Gateway
- API accessible only from within a specific VPC
- Enhanced security for internal APIs

### 3. Authorizers
Alternative to IAM authorization with two main types:

#### Lambda Authorizer
- **Maximum Control**: Provides the most flexibility
- **Configuration Requirements**:
  - Lambda function implementation
  - IAM role (possibly)
  - Event payload configuration
  - Caching settings for authorization results
- **Benefit**: Caching improves performance by avoiding repeated authorizer calls

#### Cognito User Pool Authorizer
- **Simpler Setup**: Less configuration required
- **Purpose**: Authenticate requests using Amazon Cognito
- **Configuration**: Specify which Cognito User Pool to use
- **Benefit**: Built-in user authentication and management

## Best Practices
1. Choose the appropriate authorization method based on your use case
2. Enable caching for Lambda authorizers to improve performance
3. Use resource policies for cross-account access scenarios
4. Implement IP restrictions when applicable
5. Use VPC allow lists for internal/private APIs

## When to Use Each Method

| Method | Best For |
|--------|----------|
| IAM Authorization | AWS service-to-service communication |
| Lambda Authorizer | Custom authorization logic, third-party tokens |
| Cognito User Pool | User-facing applications with standard authentication |
| Resource Policies | Cross-account access, IP restrictions, VPC isolation |

## Summary
AWS API Gateway provides multiple security layers that can be combined to create a robust authorization strategy. Understanding each option helps you implement the right security posture for your API.
