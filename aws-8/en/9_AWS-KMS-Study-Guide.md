# AWS KMS (Key Management Service) - Study Guide

## Overview
AWS Key Management Service (KMS) is used for encrypting and decrypting data. It provides two main approaches:
1. Direct encryption/decryption (for data under 4KB)
2. Envelope encryption (for data over 4KB)

## 1. KMS Encrypt and Decrypt APIs

### Encryption Process
- **Input**: Secret/data less than 4 kilobytes
- **Step 1**: Use the Encrypt API via SDK or CLI
- **Step 2**: Specify the Customer Master Key (CMK) to use in KMS
- **Step 3**: KMS checks with IAM for proper permissions
- **Output**: Encrypted data

### Decryption Process
- **Step 1**: Use the Decrypt API via SDK or CLI
- **Step 2**: KMS automatically identifies which CMK was used for encryption
- **Step 3**: KMS checks with IAM for decryption permissions
- **Output**: Decrypted secret in plain-text

### Key Limitation
- **Size Limit**: Maximum 4 kilobytes per encryption

---

## 2. Envelope Encryption (For Data > 4KB)

### What is Envelope Encryption?
Envelope encryption is a technique for encrypting large amounts of data (over 4KB, up to multiple megabytes or more) by wrapping it with an encrypted data key.

### Main API: GenerateDataKey
**Important Concept**: Any data over 4 kilobytes MUST be encrypted using envelope encryption with the `GenerateDataKey` API.

### Envelope Encryption Process

#### Encryption Steps:
1. **Call GenerateDataKey API**
   - Specify the CMK to use
   - KMS checks IAM permissions
   - KMS generates a Data Encryption Key (DEK)

2. **Receive Two Keys from KMS**
   - Plain-text version of DEK (for client-side use)
   - Encrypted version of DEK (for storage)

3. **Client-Side Encryption**
   - Use the plain-text DEK to encrypt the large file on client side
   - This uses the client's CPU for the actual encryption work

4. **Build the Envelope**
   - Combine the encrypted file with the encrypted DEK
   - Store both in a single envelope file
   - This creates the final encrypted package

#### Decryption Steps:
1. **Extract from Envelope**
   - Retrieve the encrypted DEK from the envelope file
   - Retrieve the encrypted file from the envelope file

2. **Call Decrypt API**
   - Pass the encrypted DEK (max 4KB) to KMS Decrypt API
   - KMS checks IAM permissions
   - KMS returns the plain-text DEK

3. **Client-Side Decryption**
   - Use the plain-text DEK to decrypt the large file on client side

### Architecture Summary
```
ENCRYPTION:
Large File + GenerateDataKey API → Plain-text DEK (client-side)
           → Encrypted DEK (from KMS) + Encrypted File → ENVELOPE

DECRYPTION:
ENVELOPE → Extract Encrypted DEK → Decrypt API → Plain-text DEK
        → Decrypt Large File (client-side) → Original File
```

---

## 3. Key Exam Points

✓ **Encrypt/Decrypt APIs**: For data ≤ 4KB  
✓ **GenerateDataKey API**: For data > 4KB (Envelope Encryption)  
✓ **Always Check IAM**: KMS always verifies IAM permissions before encryption/decryption  
✓ **Client-Side Processing**: Most encryption work for large files happens on the client side  
✓ **Envelope Contains**: Both encrypted DEK and encrypted file together  

---

## 4. Benefits of Envelope Encryption

- ✓ Supports encryption of data larger than 4KB
- ✓ Reduces load on KMS service (client-side encryption/decryption)
- ✓ Maintains security through encrypted envelope
- ✓ Scalable for large files (several megabytes or more)
