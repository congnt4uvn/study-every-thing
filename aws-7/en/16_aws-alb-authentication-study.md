# AWS Study Notes: Authenticate Users with Application Load Balancer (ALB)

## 1) Big Idea
An Application Load Balancer (ALB) can authenticate users **before** traffic reaches your application.
This removes authentication work from app code, so your app can focus on business logic.

## 2) Authentication Options for ALB
ALB supports two main options:

1. **`authenticate-cognito`**
- Uses Amazon Cognito User Pools.
- Good for social login (Amazon, Google, Facebook) and enterprise federation (SAML/LDAP/Microsoft AD through Cognito setup).

2. **`authenticate-oidc`**
- Uses any OpenID Connect (OIDC)-compliant Identity Provider directly.
- More flexible, but usually requires more manual endpoint configuration.

## 3) Required Listener Setup
To use ALB authentication, configure:
- An **HTTPS listener** (secure listener is required)
- A listener rule action:
  - `authenticate-cognito`, or
  - `authenticate-oidc`
- Then forward traffic to target group/backend.

Typical flow in listener rules:
1. Authenticate user
2. Forward request to backend

## 4) Behavior for Unauthenticated Users
ALB can be configured with one of three behaviors:

1. **Authenticate** (default): redirect user to login
2. **Deny**: reject request
3. **Allow**: pass request without authentication

`Allow` can be useful for public endpoints such as a login page.

## 5) Example: ALB + Amazon ECS + Cognito
High-level sequence:
1. User calls API (for example: `GET /api/data`)
2. ALB enforces `authenticate-cognito`
3. Cognito authenticates user
4. ALB forwards request to ECS, including user identity context/claims
5. Application can return user-specific responses

## 6) Setup Steps (Cognito)
1. Create Cognito User Pool
2. Create App Client
3. Create/Configure Cognito Domain
4. Ensure ID token (JWT) is returned (default behavior)
5. Optionally connect social/corporate IdPs
6. Configure callback and redirect URLs
7. Attach Cognito configuration to ALB listener rule

## 7) OIDC Direct Integration Flow
When using `authenticate-oidc`, ALB interacts directly with the IdP:

1. ALB redirects user to IdP authorization endpoint
2. User authenticates and IdP returns authorization code
3. ALB exchanges code at token endpoint for ID/access tokens
4. ALB calls user info endpoint using access token to retrieve user claims
5. ALB forwards original request + claims to backend

## 8) OIDC Configuration Items
You usually need to provide:
- Authorization endpoint
- Token endpoint
- User info endpoint
- Client ID
- Client secret
- Correct redirect/callback URLs

## 9) Cognito vs OIDC (Quick Compare)
- **Cognito**: easier AWS-native integration, faster setup in many AWS workloads
- **Direct OIDC**: more provider flexibility, but more manual configuration

## 10) Exam/Interview Focus Points
- ALB authentication requires **HTTPS listener**.
- Rule actions are `authenticate-cognito` and `authenticate-oidc`.
- ALB can offload authentication from application code.
- Unauthenticated behavior can be authenticate/deny/allow.
- Backend receives user-related context after successful auth.

## 11) Quick Review Questions
1. Why is ALB authentication useful for application architecture?
2. What is the difference between `authenticate-cognito` and `authenticate-oidc`?
3. Why must ALB authentication use HTTPS?
4. When would you choose `allow` for unauthenticated requests?
5. Which OIDC endpoints must be configured?
