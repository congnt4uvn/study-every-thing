# AWS Study Notes: Cognito User Pools vs Identity Pools

## 1. Big Picture
Amazon Cognito has two different components that solve two different problems:

- **Cognito User Pools** -> Authentication (Who are you?)
- **Cognito Identity Pools** -> Authorization for AWS access (What can you do in AWS?)

A common exam/interview trap is mixing these two.

## 2. Cognito User Pools (Authentication)
Use User Pools when you need a **user directory** for web/mobile apps.

### Main features
- Managed database of application users
- Sign-up / sign-in flows
- Federated login support:
  - Social providers (Google, Facebook, Amazon)
  - OIDC providers
  - SAML (enterprise/corporate login)
- Hosted UI (can be customized with branding/logo)
- Lambda triggers during auth flow (pre-auth, post-auth, etc.)
- Adaptive authentication and MFA support

### Key idea
User Pools verify identity and return user tokens.

## 3. Cognito Identity Pools (Authorization)
Use Identity Pools when users need **temporary AWS credentials** to access AWS services.

### Main features
- Exchanges a valid user identity/token for temporary AWS credentials (via STS)
- Maps users to IAM roles and policies
- Supports fine-grained AWS access control
- Can support unauthenticated users (guest access)

### Key idea
Identity Pools decide what AWS resources users can access.

## 4. What to choose?

### Scenario A
You only need app login and user management.

- Use **Cognito User Pools**

### Scenario B
Users must access AWS resources directly (for example S3 or DynamoDB).

- Use **Cognito Identity Pools**
- Often combined with User Pools

## 5. How they work together (best-practice flow)
1. User signs in through **Cognito User Pool** (or federated IdP).
2. App receives token after user identity is verified.
3. App exchanges token with **Cognito Identity Pool**.
4. Identity Pool uses STS to issue temporary AWS credentials.
5. App calls AWS services (such as S3/DynamoDB) using those credentials.
6. IAM role/policy attached to credentials controls allowed actions.

## 6. Quick comparison table
| Topic | User Pools | Identity Pools |
|---|---|---|
| Primary purpose | Authentication | Authorization to AWS |
| Main output | User identity tokens | Temporary AWS credentials |
| Backed by | Cognito user directory | IAM roles + STS credentials |
| Guest users | Not primary use case | Supported |
| Access to S3/DynamoDB directly | Not by itself | Yes (with IAM policies) |

## 7. Memory shortcut
- **User Pool = "Sign in"**
- **Identity Pool = "Access AWS"**

Or:
- First prove identity (authn)
- Then get permissions (authz)

## 8. Self-check questions
1. Which Cognito component stores app users?
2. Which component provides temporary AWS credentials?
3. Can Identity Pools be used without User Pools?
4. Why combine both for mobile apps accessing S3/DynamoDB?

## 9. One-line summary
Use **User Pools** to authenticate users, and use **Identity Pools** to authorize those users to access AWS resources with temporary IAM-based credentials.
