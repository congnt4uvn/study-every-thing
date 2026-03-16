# AWS Study Notes: KMS Key Policies

## 1) What is a KMS Key Policy?
A KMS key policy is the primary resource policy attached to a KMS key. It defines who can use and manage that key.

## 2) Default key policy behavior
When a key is created in the AWS Console, the default key policy usually allows principals in the same AWS account to use the key **if** they also have the required IAM permissions.

Key point:
- In this model, both key policy and IAM permissions matter.

## 3) Explicit allow in key policy
You can explicitly allow a specific principal directly in the key policy, for example:
- IAM user
- IAM role
- Federated user/session
- AWS service principal

You can also scope allowed actions, such as:
- `kms:Encrypt`
- `kms:Decrypt`
- and other KMS actions

If access is explicitly granted in the key policy to that principal, the principal can use the key according to the policy statement (without needing an extra IAM allow in the exact scenario described in the source note).

## 4) Principal types you can reference
Common principal patterns (for KMS and IAM generally):

1. Account root principal
- Example format: `arn:aws:iam::<account-id>:root`
- Meaning: enables delegation to principals in that account, then IAM policies apply.

2. Specific IAM role
- Put the role ARN in `Principal`.

3. IAM role session / assumed role
- Session identities created by `AssumeRole`.
- Also common with federation flows.

4. IAM user
- Put the user ARN in `Principal`.

5. Federated user/session
- Example sources: Cognito Identity, SAML federation, etc.

6. AWS service principal
- Example: allow a service to use your KMS key where needed.

7. Wildcard principal
- `"*"` (or broad account-level patterns)
- Very risky; avoid unless absolutely required and tightly constrained by conditions.

## 5) Security best practices
- Prefer least privilege: grant only required actions.
- Prefer specific principals over broad wildcards.
- Add conditions when possible (context, source account, encryption context constraints, etc.).
- Review CloudTrail logs for KMS usage.
- Regularly audit key policies for over-permissioning.

## 6) Quick self-check questions
1. What is the role of a key policy vs IAM policy in KMS authorization?
2. When would you grant access directly in key policy?
3. Why is `"*"` in `Principal` dangerous?
4. What principal type would you use for SAML-based access?
5. Which actions are required for encrypt-only workloads?

## 7) One-line recap
KMS key policy defines **who** can use a key; IAM often defines **who in your account is allowed by identity policy**, and secure design requires explicit, minimal, and auditable permissions.
