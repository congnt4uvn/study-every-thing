# AWS Study Notes: Cognito Identity Pools (Federated Identities)

## 1. What It Is

Amazon Cognito Identity Pools (also called Federated Identities) let external users get temporary AWS credentials.

These users are usually:
- Web app users
- Mobile app users

They can then access AWS services directly, such as:
- Amazon S3
- Amazon DynamoDB

## 2. Why Identity Pools Exist

You should not create a normal IAM user for every end user because:
- The number of users is too large
- It does not scale
- End users are not fully trusted

Instead, Identity Pools issue temporary credentials through AWS STS.

## 3. Supported Identity Providers

Identity Pools can trust login tokens from:
- Amazon Cognito User Pools
- Public providers (Amazon, Google, Facebook, Apple)
- OpenID Connect (OIDC) providers
- SAML providers
- Developer authenticated identities (custom login system)

Identity Pools can also support unauthenticated (guest) users.

## 4. High-Level Authentication Flow

1. User signs in with a configured identity provider.
2. User receives a token.
3. App sends token to Cognito Identity Pool.
4. Identity Pool validates token with the provider.
5. Identity Pool calls AWS STS (AssumeRoleForWebIdentity).
6. STS returns temporary AWS credentials.
7. App uses credentials to call AWS services directly.

## 5. Identity Pools + User Pools Together

A common architecture:
- User authentication and user directory are handled in Cognito User Pools.
- User Pools provide JWT tokens.
- Identity Pools exchange those JWTs for temporary AWS credentials.

This pattern gives:
- Centralized user management in User Pools
- Fine-grained AWS access control through IAM roles/policies

## 6. Role Mapping and Authorization

Identity Pools decide access by IAM roles and IAM policies.

You can configure:
- Default role for authenticated users
- Default role for unauthenticated (guest) users
- Rules to map users to roles (for example based on user attributes or IDs)

Important requirement:
- IAM roles used by Identity Pools must trust Cognito Identity Pools in their trust policy.

## 7. Fine-Grained Access Control Examples

### Example A: Guest Access to a Single S3 Object

Guest role policy can allow only:
- `s3:GetObject` on one object (example: `my_picture.jpg`)

This keeps guest permissions very limited.

### Example B: Authenticated User Access to Own S3 Prefix

Use policy variables (like identity ID) so each user can access only objects under their own prefix.

Result:
- User A cannot access User B's objects.

### Example C: Row-Level Security in DynamoDB

Use IAM condition keys (for example, `dynamodb:LeadingKeys`) tied to the user identity.

Result:
- Each user can access only rows that belong to their own key.

## 8. Key API and Security Detail

Identity Pools obtain credentials from STS using:
- `AssumeRoleForWebIdentity`

Security model:
- Credentials are temporary
- Access scope is controlled by role policy
- Least privilege should be applied

## 9. Exam and Interview Focus

Remember these distinctions:
- User Pool = authentication and user directory
- Identity Pool = authorization to AWS resources using temporary credentials

Quick summary:
- Sign in -> token -> Identity Pool -> STS credentials -> direct AWS access

## 10. Practice Checklist

- Create an Identity Pool
- Add at least one identity provider
- Configure auth and guest roles
- Attach least-privilege IAM policies
- Test S3 access with both guest and authenticated users
- Test DynamoDB fine-grained access rules
