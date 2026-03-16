# AWS Study Notes: Cognito Identity Pool

## Overview
A Cognito Identity Pool lets users obtain temporary AWS credentials. These credentials are mapped to IAM roles and permissions.

This note is based on a practical setup flow with:
- Authenticated access
- Guest (unauthenticated) access
- IAM role assignment for both access types

## What You Configure First
When creating an Identity Pool, choose access types:
- Authenticated access
- Guest access (optional)

For authenticated access, define identity providers (IdPs), such as:
- Amazon Cognito User Pool
- Facebook
- Google
- Apple
- Amazon
- Twitter
- OIDC
- SAML
- Custom developer provider

In this practice flow, the IdP is an Amazon Cognito User Pool.

## IAM Roles in Identity Pool
You must configure two IAM roles:
- Authenticated role: assumed by signed-in users
- Unauthenticated role: assumed by guest users

Each role should contain only the permissions required (least privilege).

Example role names used in the walkthrough:
- Cognito Identity Pool Authenticated Role Demo
- Unauthenticated Role Demo

## Link User Pool to Identity Pool
Because Cognito User Pool is selected as login source, you provide:
- User Pool ID
- App Client ID

## Role Resolution Options
For authenticated users, role mapping can be:
- Default authenticated role
- Rule-based role mapping (based on token claims)

Advanced option:
- Use token attributes (for example username, client) in IAM policy conditions for fine-grained access control.

## Final Creation Steps
- Name the Identity Pool (example: Demo Identity Pool)
- Keep default authentication mode if unsure
- Create the Identity Pool

After creation, both authenticated and guest access paths are available.

## After Creating the Pool
Typical app integration flow:
1. Configure AWS SDK in your application.
2. Authenticate user through the chosen IdP.
3. Exchange identity for temporary AWS credentials.
4. Use those credentials to call AWS services.

## Where to Manage Permissions
Go to IAM Roles and find roles created for the Identity Pool (often containing "Cognito").

Then:
- Attach managed policies, or
- Add inline policies

Example permission setup:
- Service: Amazon S3
- Permission: read/get access

## Key Exam / Interview Points
- Identity Pool provides AWS credentials, not user authentication UI.
- User Pool handles user sign-up/sign-in; Identity Pool handles AWS access delegation.
- Separate roles for authenticated and guest users is a core security design.
- Claims-based role mapping enables granular authorization.

## Best Practices
- Start with minimal permissions.
- Separate guest and authenticated capabilities clearly.
- Review IAM policy conditions when using token attributes.
- Test credentials and access paths in real application code.

## Quick Summary
Cognito Identity Pool is the bridge between user identity and AWS resource access. You decide who can access (auth vs guest), which role they assume, and exactly what AWS actions they can perform through IAM policies.
