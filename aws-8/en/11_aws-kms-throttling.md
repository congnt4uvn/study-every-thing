# AWS KMS – Request Quotas & Throttling

## Overview

AWS KMS (Key Management Service) is an **internal AWS service** and, like all AWS services, it enforces **request quotas**. Exceeding these quotas results in a `ThrottlingException`.

---

## ThrottlingException

When you exceed the KMS request quota, you receive an error like:

```
Status Code: 400
Error Code: ThrottlingException
```

This means you are calling KMS too fast — more requests per second than your quota allows.

---

## How KMS Quotas Work

- Every **cryptographic operation** (encrypt, decrypt, GenerateDataKey, GenerateRandom, etc.) shares **the same quota**.
- This is a **per-account, per-region** shared quota.
- Third-party AWS services acting **on your behalf** also consume this quota.
  - Example: **Amazon S3 with SSE-KMS** — every time S3 uses your KMS key to encrypt/decrypt an object, it counts against your quota.

### Default Quota Values (Symmetric CMK)

| Region | Requests per second |
|--------|-------------------|
| Most regions | 5,500 |
| Some regions | 10,000 |
| Select regions | 30,000 |

> All cryptographic operations **share** the above quota value.

---

## Solutions for KMS Throttling

There are **3 ways** to handle KMS throttling:

### 1. Exponential Backoff *(for transient throttling)*
- Retry the failed request with an exponentially increasing wait time between retries.
- Suitable when throttling is temporary or infrequent.

### 2. DEK Caching with Envelope Encryption *(reduce API calls)*
- If you are using the `GenerateDataKey` API, enable **Data Encryption Key (DEK) caching**.
- Cache the DEK **locally** to reuse it for multiple encrypt/decrypt operations.
- This dramatically reduces the number of calls made to KMS.
- DEK caching is a feature of the **AWS Encryption SDK**.

### 3. Request a Quota Increase *(for persistent high-volume usage)*
- If you consistently hit the quota limit, request an increase through:
  - An **AWS API call**, or
  - Opening a **support ticket** with AWS Support.

---

## Key Takeaways

| # | Solution | When to Use |
|---|----------|-------------|
| 1 | Exponential Backoff | Transient / occasional throttling |
| 2 | DEK Caching (Envelope Encryption SDK) | High frequency of encrypt/decrypt calls |
| 3 | Request Quota Increase | Consistently exceeding the quota |

---

## Related KMS API Operations (Shared Quota)

- `Encrypt`
- `Decrypt`
- `GenerateDataKey`
- `GenerateDataKeyWithoutPlaintext`
- `GenerateRandom`
- `ReEncrypt`
- `Sign` / `Verify`

> All operations above **share** the same cryptographic operations quota.

---

## Quick Reference

```
ThrottlingException
    → Use Exponential Backoff (transient)
    → Enable DEK Caching via Encryption SDK (reduce calls)
    → Request Quota Increase via API / AWS Support (permanent fix)
```
