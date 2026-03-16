# AWS CodeBuild Security - Study Notes

## 1. CodeBuild and VPC
- By default, AWS CodeBuild runs outside your VPC.
- You can configure CodeBuild to run inside your VPC when your build needs private resources.
- Typical use case: accessing private RDS, ElastiCache, or internal services.

## 2. Secret Management in CodeBuild
Do not store sensitive values as plaintext environment variables in CodeBuild.

### Bad practice
- `DB_PASSWORD = supersecret` (plaintext)
- Risk: secret exposure in logs, configuration views, or accidental leaks.

### Recommended options
Use environment variables that reference:
- AWS Systems Manager Parameter Store parameters
- AWS Secrets Manager secrets

At build runtime, CodeBuild fetches the real secret value and injects it into the container.

## 3. Using SSM Parameter Store (Example)
Example flow:
1. Create a parameter in Parameter Store.
2. Example name: `/CodeBuild/DBPassword`
3. Parameter type: `SecureString`
4. Encrypt with a KMS key (CMK).
5. Store value (for example: `SuperSecret`).
6. In CodeBuild environment variables:
   - Name: `DB_PASSWORD`
   - Type: `Parameter Store`
   - Value: `/CodeBuild/DBPassword`

Result: CodeBuild resolves `/CodeBuild/DBPassword` at runtime and injects the decrypted value.

## 4. Using AWS Secrets Manager (Alternative)
- You can do the same using Secrets Manager.
- In CodeBuild env vars, choose secret reference type and provide the secret name.

## 5. IAM Permissions Required
The IAM role used by the CodeBuild project must allow access to:
- SSM Parameter Store (for example: `ssm:GetParameters`)
- Secrets Manager (for example: `secretsmanager:GetSecretValue`)
- KMS decrypt permissions if customer-managed KMS key is used

Without these permissions, secret retrieval fails during build.

## 6. Exam Tips
- Remember: plaintext env vars are insecure for secrets.
- Prefer Parameter Store or Secrets Manager references.
- If private resources are needed, configure CodeBuild VPC settings (subnets + security groups).
- Always verify IAM permissions for secret retrieval.

## Quick Review Checklist
- Is CodeBuild in the right network (default or VPC)?
- Are all secrets stored outside plaintext env vars?
- Are secret references configured correctly?
- Does the CodeBuild IAM role have SSM/Secrets Manager/KMS permissions?
