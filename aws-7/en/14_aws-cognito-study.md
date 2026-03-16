# AWS Study Note: Amazon Cognito

## What is Amazon Cognito?
Amazon Cognito gives users an identity so they can interact with web and mobile applications.

- These users are usually outside your AWS account.
- Cognito helps authenticate and manage those external app users.

## Core Components
Amazon Cognito has two main sub-services:

### 1. Cognito User Pool
Purpose: Sign-in and user authentication for app users.

Key points:
- Provides sign-up/sign-in functionality.
- Integrates well with API Gateway.
- Integrates well with Application Load Balancer (ALB).

### 2. Cognito Identity Pool (Federated Identities)
Purpose: Provide temporary AWS credentials to authenticated users.

Key points:
- Formerly called Federated Identity.
- Lets app users access AWS resources directly (with controlled permissions).
- Integrates with Cognito User Pools.

## Cognito vs IAM Users
- IAM users are typically for people/resources inside your AWS account.
- Cognito users are usually web/mobile app users outside your AWS account.

## Exam and Interview Keywords
Look for these clues:
- Large number of users (hundreds or more)
- Mobile or web application users
- Authentication/federation use cases (for example, SAML)
- Need temporary AWS credentials for end users

## Quick Summary
- Use User Pools for authentication (who the user is).
- Use Identity Pools for authorization to AWS resources (what the user can access).
