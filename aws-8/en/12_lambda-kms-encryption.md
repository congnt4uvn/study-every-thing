# AWS Lambda & KMS — Encrypting Environment Variables

## Overview

This guide covers how to **encrypt Lambda environment variables** using **AWS KMS (Key Management Service)**, preventing sensitive data (like database passwords) from being exposed in plain text.

---

## The Problem

When building Lambda functions that connect to databases or external services, you need to store credentials. There are three approaches — each with different security levels:

| Approach | Risk |
|---|---|
| Hardcode credentials in source code | **High** — visible to anyone with code access |
| Store as plain-text environment variables | **Medium** — visible in Lambda configuration console |
| Encrypt environment variables with KMS | **Low** — only users with KMS key access can decrypt |

---

## Step-by-Step: Lambda + KMS Encryption

### 1. Create the Lambda Function

- Runtime: **Python**
- Start with a simple function that reads a `DB_PASSWORD` environment variable

```python
import os

def lambda_handler(event, context):
    db_password = os.environ['DB_PASSWORD']
    return "great"
```

---

### 2. Add an Environment Variable (Plain Text — Insecure)

1. Go to **Configuration → Environment Variables**
2. Add key: `DB_PASSWORD`, value: `super_secret`

> **Problem:** Anyone with access to the Lambda configuration can read this value directly.

---

### 3. Enable KMS Encryption on the Environment Variable

1. Go to **Configuration → Environment Variables → Encryption Configuration**
2. Enable **Encryption Helpers**
3. Select your KMS key (e.g., `tutorial-key`)
4. Click **Encrypt** next to the environment variable

The variable is now stored encrypted at rest.

---

### 4. Update the Code to Decrypt at Runtime

AWS provides a **decrypt snippet** in the console. Use the `boto3` KMS client to decrypt:

```python
import os
import boto3
from base64 import b64decode

ENCRYPTED = os.environ['DB_PASSWORD']

# Decrypt at cold start (outside handler for efficiency)
DECRYPTED = boto3.client('kms').decrypt(
    CiphertextBlob=b64decode(ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

def lambda_handler(event, context):
    print("Encrypted value:", ENCRYPTED)
    print("Decrypted value:", DECRYPTED)
    return "great"
```

---

### 5. Increase the Function Timeout

- Default timeout is **3 seconds** — KMS decryption may exceed this.
- Go to **Configuration → General Configuration → Edit**
- Set timeout to **10 seconds** (or appropriate value)

---

### 6. Grant the Lambda IAM Role Permission to Decrypt

The Lambda execution role must be allowed to call `kms:Decrypt` on the specific key.

**Steps:**

1. Go to **Configuration → Permissions**
2. Click the **IAM Role** link
3. Add an **Inline Policy**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:<region>:<account-id>:key/<key-id>"
    }
  ]
}
```

4. Name the policy: `allow-decrypt-kms`
5. Save the policy

---

### 7. Test the Function

- Deploy and run a test event
- **Expected output in logs:**
  - Line 1: the encrypted (Base64) value of `DB_PASSWORD`
  - Line 2: the decrypted plain-text value (`super_secret`)
  - Result: `"great"`

---

## Key Concepts

| Concept | Description |
|---|---|
| **KMS** | AWS Key Management Service — manages cryptographic keys |
| **Encryption at rest** | Data is encrypted when stored, not just in transit |
| **EncryptionContext** | Metadata used to bind encryption to a specific resource (e.g., Lambda function name) |
| **IAM Inline Policy** | A policy attached directly to a role, not reusable |
| **boto3** | AWS SDK for Python |
| **kms:Decrypt** | The specific IAM permission needed to decrypt KMS-encrypted data |

---

## Security Best Practices

- **Never hardcode credentials** in source code.
- **Use KMS-encrypted environment variables** for secrets in Lambda.
- **Apply least-privilege IAM policies** — only grant `kms:Decrypt` on the specific key ARN.
- Consider **AWS Secrets Manager** or **SSM Parameter Store** for more complex secret management.

---

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `Task timed out` | Default 3s timeout too short for KMS call | Increase timeout to 10s+ |
| `AccessDeniedException` | Lambda role lacks `kms:Decrypt` permission | Add inline policy with `kms:Decrypt` on the key ARN |

---

## Summary

1. Store sensitive values as **encrypted environment variables** using KMS.
2. Use the **KMS SDK decrypt call** in your Lambda code to read the value at runtime.
3. Ensure the Lambda **IAM role** has `kms:Decrypt` permission on the correct key.
4. This ensures credentials are **never visible** in plain text in your code or console.
