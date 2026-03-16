# AWS STS Study Notes

## What Is AWS STS?
AWS Security Token Service (STS) provides temporary security credentials to access AWS resources.

- Credential duration: typically 15 minutes to 1 hour
- Common use cases: role assumption, federation, MFA-protected API access, cross-account access

## Important STS APIs

### 1. AssumeRole
Used to assume an IAM role:
- Within the same account
- Across different AWS accounts (cross-account)

Why it matters:
- Fundamental for least-privilege access
- Core topic for AWS exams

### 2. AssumeRoleWithSAML
Used when users authenticate with SAML-based identity providers.

### 3. AssumeRoleWithWebIdentity
Used for users authenticated by web identity providers (for example Google, Facebook, OIDC).

Note:
- In many modern architectures, Cognito Identity Pools are preferred instead of direct `AssumeRoleWithWebIdentity` usage.

### 4. GetSessionToken
Used to get temporary credentials for IAM users (or root user) especially when MFA is required.

Returns:
- Access key ID
- Secret access key
- Session token
- Expiration time

### 5. GetFederationToken
Used to get temporary credentials for federated users.

### 6. GetCallerIdentity
Returns identity information for the caller:
- Account ID
- ARN
- Principal details

Useful when:
- You are unsure which credentials/profile are currently being used.

### 7. DecodeAuthorizationMessage
Decodes encoded authorization failure messages from AWS API responses.

Useful for:
- Troubleshooting `AccessDenied`-style issues.

## High-Priority APIs for Exam Prep
Focus heavily on:
- `AssumeRole`
- `GetSessionToken`
- `GetCallerIdentity`
- `DecodeAuthorizationMessage`

## How AssumeRole Works
1. Create or identify a target IAM role.
2. Configure trust policy (who can assume the role).
3. Attach permission policies (what the role can do).
4. Call STS `AssumeRole`.
5. Use returned temporary credentials to call AWS services as that role.

## Cross-Account Access Flow
1. Create role in target account.
2. Set trust relationship to allow source account principal.
3. Ensure both sides have correct IAM permissions.
4. Call `AssumeRole` from source account.
5. Use temporary credentials to access target account resources (for example S3).

## STS with MFA (Key Concept)
Use `GetSessionToken` after MFA authentication, then enforce MFA in IAM policy conditions.

Example IAM condition:
- `"aws:MultiFactorAuthPresent": true`

Practical effect:
- Sensitive actions (for example EC2 stop/terminate) are allowed only when MFA is present.

## Quick Revision Checklist
- Know when to use `AssumeRole` vs `GetSessionToken`.
- Understand trust policy + permission policy in role assumption.
- Remember temporary credentials always expire.
- Use `GetCallerIdentity` to confirm active identity.
- Use `DecodeAuthorizationMessage` for denied API diagnostics.
