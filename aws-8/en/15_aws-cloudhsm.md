# AWS CloudHSM – Study Guide

## Overview

| Service | Who Manages Keys | Who Manages Hardware |
|---------|-----------------|---------------------|
| **KMS** | AWS manages software & keys | AWS |
| **CloudHSM** | **You** manage keys entirely | AWS provisions hardware |

---

## What Is CloudHSM?

- **HSM** = Hardware Security Module — a **dedicated physical device** provisioned by AWS inside the cloud.
- You have **full control** over your encryption keys; AWS cannot access them.
- Compliant with **FIPS 140-2 Level 3** (tamper-resistant — any physical tampering attempt is blocked).
- Supports both **symmetric** and **asymmetric** encryption keys (e.g., SSL/TLS keys).
- **No free tier** available.
- Requires the **CloudHSM client software** to establish a connection.

---

## Key Concepts

### Encryption Key Types Supported
| Type | Supported |
|------|-----------|
| Symmetric | ✅ |
| Asymmetric | ✅ |
| Digital Signing | ✅ |
| Hashing | ✅ |

### IAM vs CloudHSM Software
- **IAM permissions** → used to **create, read, update, delete** an HSM *cluster* (high-level management).
- **CloudHSM software** → used to **manage keys, users, and their permissions** (fine-grained, inside the cluster).
- This is different from KMS where **everything is managed via IAM**.

---

## High Availability (HA)

- CloudHSM clusters can be spread across **multiple Availability Zones (AZs)**.
- HSM devices are **replicated** across AZs.
- The CloudHSM client can connect to **any** HSM device in the cluster transparently.

---

## Integration with AWS Services

### CloudHSM + KMS (Custom Key Store)
1. Create a **CloudHSM cluster**.
2. Define a **KMS Custom Key Store** backed by that CloudHSM cluster.
3. Now KMS encryption for **EBS, S3, RDS**, etc. will use keys stored in **your** CloudHSM.
4. All API calls through KMS are **logged in CloudTrail**.

### CloudHSM + Redshift
- Native integration for **database encryption and key management**.

### CloudHSM + S3 (SSE-C)
- Ideal for **Server-Side Encryption with Customer-Provided Keys (SSE-C)** on S3.
- You manage and store your own keys inside CloudHSM.

---

## CloudHSM vs KMS — Comparison Table

| Feature | KMS | CloudHSM |
|---------|-----|----------|
| Tenancy | Multi-tenant | **Single-tenant** |
| Key Management | AWS owned / AWS managed / Customer managed | Customer managed **only** |
| Key Types | Symmetric, Asymmetric, Digital Signing | Symmetric, Asymmetric, Digital Signing, **Hashing** |
| Key Accessibility | Multiple regions (natively) | VPC-based; share via **VPC Peering** across regions |
| Cryptographic Acceleration | None | **SSL/TLS** acceleration; **Oracle TDE** acceleration |
| Access & Auth | **IAM** | CloudHSM's **own user/permission system** |
| High Availability | Managed service (always available) | Multiple HSM devices across **multiple AZs** |
| Monitoring | CloudTrail + CloudWatch | CloudTrail + CloudWatch + **MFA support** |
| Free Tier | ✅ Yes | ❌ No |

---

## Key Takeaways

- Use **KMS** when you want a simple, fully-managed encryption service integrated with IAM.
- Use **CloudHSM** when you need:
  - **Dedicated hardware** with single-tenant isolation.
  - **Full ownership** of encryption keys (AWS never touches them).
  - **FIPS 140-2 Level 3** compliance.
  - Hardware-level **SSL/TLS or Oracle TDE** acceleration.
- You can combine both: use **CloudHSM as a KMS custom key store** to get CloudTrail logging with your own hardware keys.

---

## Quick Quiz

1. Who manages the encryption keys in CloudHSM?
2. What compliance standard does CloudHSM meet?
3. What is the difference between managing a CloudHSM cluster with IAM vs the CloudHSM software?
4. How can CloudHSM be used with S3 encryption?
5. Is CloudHSM part of the AWS free tier?

<details>
<summary>Answers</summary>

1. **The customer** — AWS has no access to CloudHSM keys.
2. **FIPS 140-2 Level 3**.
3. IAM = cluster-level operations (create/delete cluster). CloudHSM software = key and user management inside the cluster.
4. Via **SSE-C** (Server-Side Encryption with Customer-Provided Keys) — keys are stored in CloudHSM.
5. **No**, CloudHSM has no free tier.

</details>
