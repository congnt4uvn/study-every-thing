# AWS S3 Bucket Key with SSE-KMS Encryption

## Overview

AWS S3 Bucket Key is a feature that significantly optimizes the use of **SSE-KMS** (Server-Side Encryption with AWS Key Management Service) for Amazon S3.

---

## The Problem It Solves

When you enable SSE-KMS on S3, **every object encryption/decryption** requires an API call to AWS KMS to generate a data key. At scale, this leads to:

- **High number of KMS API calls**
- **High costs** from KMS usage
- Risk of hitting **KMS request rate limits**

---

## How S3 Bucket Key Works

Instead of calling KMS for every single object, S3 Bucket Key introduces an intermediate key layer:

```
AWS KMS (Customer Master Key - CMK)
        │
        ▼  (used once in a while)
  S3 Bucket Key  ◄─── generated and rotated periodically
        │
        ▼  (used for many objects)
  Data Keys  ──► Encrypt individual S3 objects
```

1. AWS KMS uses the **Customer Master Key (CMK)** to generate an **S3 Bucket Key** once in a while.
2. The S3 Bucket Key is **rotated periodically** (not per-object).
3. The S3 Bucket Key then generates **data keys** locally using **envelope encryption** to encrypt your S3 objects.
4. This dramatically reduces the number of direct calls to KMS.

---

## Key Benefits

| Benefit | Detail |
|---|---|
| **99% fewer KMS API calls** | S3 handles encryption locally using the Bucket Key |
| **Up to 99% cost reduction** | KMS pricing is based on API call volume |
| **No security compromise** | Encryption strength remains the same |
| **Fewer CloudTrail events** | Less KMS activity means fewer KMS-related logs in CloudTrail |

---

## Important Notes

- S3 Bucket Key uses **envelope encryption** to generate many data keys locally.
- You will notice **fewer KMS-related events in AWS CloudTrail** — this is expected behavior, not a loss of visibility.
- This setting is especially recommended when using **SSE-KMS at scale** with high object throughput.
- The feature can be enabled at the **bucket level** in the S3 Console.

---

## How to Enable (S3 Console)

1. Go to the **AWS S3 Console**.
2. Create a new bucket or open an existing one.
3. Under **Default encryption**, select **SSE-KMS**.
4. Enable the **Bucket Key** option.
5. Save changes.

---

## Concepts to Remember

| Term | Description |
|---|---|
| **SSE-KMS** | Server-Side Encryption using AWS KMS keys |
| **CMK** | Customer Master Key — the root key managed in KMS |
| **S3 Bucket Key** | An intermediate key generated from the CMK, used to derive data keys locally |
| **Data Key** | The actual key used to encrypt individual S3 objects |
| **Envelope Encryption** | A technique where a data key is encrypted by another key (the Bucket Key) |
| **CloudTrail** | AWS service that logs API activity, including KMS calls |

---

## Summary

> **S3 Bucket Key** is an optimization for SSE-KMS that reduces KMS API calls by up to **99%**, significantly lowering costs and reducing the risk of hitting rate limits — all without compromising security.

---

*Topic: AWS S3 | Encryption | KMS | Cost Optimization*
