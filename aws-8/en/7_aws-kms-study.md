# AWS KMS Study Notes

## 1. What is AWS KMS?
- AWS KMS (Key Management Service) helps you create and manage encryption keys.
- It is deeply integrated with many AWS services.
- In most AWS encryption features, KMS is used behind the scenes.

## 2. Why use KMS?
- AWS manages key infrastructure, reducing operational work.
- Integrated with IAM for access control.
- Every key usage API call can be audited via CloudTrail.
- Easy encryption at rest integration for services like EBS, S3, RDS, SSM, and more.

## 3. Using KMS for secrets
- Never store secrets in plain text (especially in source code).
- Use KMS APIs (CLI or SDK) to encrypt sensitive values.
- Store only encrypted data (for example in code or environment variables).

## 4. KMS key types

### Symmetric keys
- One key is used for both encryption and decryption.
- Common for AWS service integrations.
- You do not get raw key material; you use KMS APIs.

### Asymmetric keys
- Public key encrypts (or verifies), private key decrypts (or signs).
- Public key can be downloaded.
- Private key stays in KMS and is accessed only via API.
- Useful when external users need to encrypt data outside AWS using the public key.

## 5. Key ownership and management models

### AWS owned keys
- Free.
- Fully managed by AWS service teams.
- Typically not directly visible or manageable by customers.

### AWS managed keys
- Free.
- Named like `aws/<service>` (for example `aws/rds`, `aws/ebs`, `aws/dynamodb`).
- Usable only with the associated AWS service.

### Customer managed keys (CMK)
- Created and managed by you.
- Cost: about $1/month per key (plus API usage cost).
- Can be imported key material (also charged similarly).
- Best for custom permissions, auditing requirements, and cross-account use cases.

## 6. Pricing basics
- Key cost: around $1/month for each customer managed key.
- API requests: about $0.03 per 10,000 requests.

## 7. Key rotation
- AWS managed keys: automatic yearly rotation.
- Customer managed keys: configurable automatic rotation period, plus on-demand rotation support.
- Imported keys: manual rotation only (often managed via aliases).

## 8. Regional scope of KMS keys
- KMS keys are regional.
- The same key cannot exist across multiple regions.
- For encrypted EBS migration across regions:
  1. Create snapshot from encrypted volume.
  2. Copy snapshot to target region.
  3. Re-encrypt using a target-region KMS key.
  4. Restore volume from copied snapshot.

## 9. KMS key policies
- Key policies control who can use/administer KMS keys.
- Without an appropriate key policy, access fails.

### Default key policy
- Usually enables account-level usage with IAM permissions.

### Custom key policy
- Lets you define specific users/roles for usage/admin tasks.
- Required for fine-grained and cross-account scenarios.

## 10. Cross-account encrypted snapshot flow
1. Create snapshot encrypted with a customer managed key in source account.
2. Add key policy permissions for target account.
3. Share encrypted snapshot with target account.
4. In target account, copy snapshot and re-encrypt with target account CMK.
5. Create EBS volume from copied snapshot.

## 11. Exam and practice tips
- Remember: KMS + IAM + key policy + CloudTrail are strongly related.
- Distinguish clearly: AWS owned vs AWS managed vs customer managed keys.
- Know when asymmetric keys are required.
- Know regional limitation and re-encryption behavior.
- Practice cross-account encryption workflows.
