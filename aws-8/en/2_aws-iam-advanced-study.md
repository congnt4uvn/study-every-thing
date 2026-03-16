# AWS IAM Advanced Study Notes

## 1) IAM Authorization Model (Simplified)

Policy evaluation follows this order:
1. Start with **Deny** (default).
2. Check for **explicit Deny**.
3. If no explicit deny, check for **Allow**.
4. If no allow, final result is **Deny**.

Important rule:
- **Explicit Deny always overrides Allow**.

### Example flow (Create DynamoDB table)
- User requests: `dynamodb:CreateTable`
- IAM evaluates all applicable policies.
- If any statement explicitly denies this action -> **Denied**.
- Otherwise, if at least one statement allows -> **Allowed**.
- Otherwise -> **Denied**.

## 2) IAM Policy + S3 Bucket Policy Interaction

For S3 access, AWS evaluates the **union** of:
- Identity-based policy (IAM user/role/group policy)
- Resource-based policy (S3 bucket policy)

Then normal evaluation applies (explicit deny wins).

### Four key scenarios

1. IAM allows read/write, no bucket policy deny
- Result: **Allowed**

2. IAM allows read/write, bucket policy has explicit deny
- Result: **Denied** (explicit deny wins)

3. IAM has no S3 permission, bucket policy explicitly allows role
- Result: **Allowed** (resource policy can grant access)

4. IAM explicitly denies, bucket policy allows
- Result: **Denied** (explicit deny wins)

## 3) Dynamic IAM Policies

Goal: avoid creating one policy per user for home folders.

### Non-scalable approach
- `Georges` -> allow `/home/georges`
- `Sarah` -> allow `/home/sarah`
- `Matt` -> allow `/home/matt`

### Scalable approach
Use policy variable:
- `${aws:username}`

Example resource pattern:
- `/home/${aws:username}`

At runtime, AWS replaces `${aws:username}` with the current IAM username.

Benefit:
- One reusable policy for all users.
- Per-user access still enforced automatically.

## 4) Policy Types in AWS IAM

### AWS Managed Policies
- Created and maintained by AWS.
- Good for common roles (admin, power user, job functions).
- Updated automatically when AWS adds services/APIs.
- Less granular control.

### Customer Managed Policies
- Created and maintained by your organization.
- Reusable across many principals.
- Support versioning and rollback.
- Better for granular and auditable access control.
- Common best practice for production environments.

### Inline Policies
- Embedded directly in one IAM principal (one-to-one).
- Not reusable.
- Weak version control compared to managed policies.
- Deleted when principal is deleted.
- Size and maintainability limitations.

## 5) Practical Console Notes

- In IAM > Policies:
  - You can filter AWS managed vs customer managed policies.
  - Customer managed policies show versions and usage, improving auditability.
- Inline policies are attached inside a specific user/role/group page, not centralized in the same reusable way.

## 6) Exam and Real-World Focus

Memorize these high-value rules:
- Default decision is **Deny**.
- **Explicit Deny > Allow** in all cases.
- For S3, evaluate IAM + bucket policy **together**.
- Dynamic variables like `${aws:username}` improve scalability.
- Prefer customer managed policies for controlled, reusable access design.

## 7) Quick Self-Check

1. If IAM allows and bucket policy explicitly denies, what is final access?
2. Can an S3 bucket policy grant access even if IAM policy does not mention S3?
3. Why is `${aws:username}` useful for home-folder authorization?
4. Which policy type is usually best for reusable, versioned enterprise access control?

### Answers
1. Denied.
2. Yes, if no explicit deny blocks it.
3. It enables one template policy to map each user to their own folder dynamically.
4. Customer managed policy.
