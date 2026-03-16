# AWS Encryption Fundamentals

## Overview
This note summarizes three common encryption models used in cloud systems and AWS services:
- Encryption in flight
- Server-side encryption at rest
- Client-side encryption

---

## 1) Encryption In Flight (TLS/SSL)

### What it is
Data is encrypted before it is sent over the network and decrypted after it is received.

### Key ideas
- TLS is the modern version of SSL.
- HTTPS means communication is protected with TLS certificates.
- This protects data moving between client and server.

### Why it matters
- Prevents man-in-the-middle interception on public or shared networks.
- Intermediate network devices can forward packets, but cannot read encrypted content.

### Example
1. A user enters username and password on a client.
2. The client encrypts data using TLS.
3. Encrypted data travels through the network.
4. Only the destination server decrypts it.

---

## 2) Server-Side Encryption At Rest

### What it is
Data is encrypted by the server after receiving it, then decrypted by the server before returning it to clients.

### Key ideas
- Stored data remains encrypted at rest.
- Encryption and decryption are handled by the service.
- The service must manage and access encryption keys (often data keys).

### AWS example (Amazon S3)
1. Client uploads an object (often over HTTPS).
2. S3 receives data, then encrypts it for storage.
3. Stored object is encrypted at rest.
4. On download, S3 decrypts and returns plaintext to the client (typically over HTTPS).

---

## 3) Client-Side Encryption

### What it is
The client encrypts data before upload and decrypts after download. The server never sees plaintext.

### Key ideas
- Client controls encryption keys.
- Storage services store only ciphertext.
- Useful when you do not fully trust the storage/server environment.

### Example flow
1. Client has plaintext object and encryption key.
2. Client encrypts object locally.
3. Encrypted object is uploaded to storage (S3, FTP server, EBS-backed system, etc.).
4. Client downloads encrypted object.
5. Client decrypts it locally using its key.

---

## Quick Comparison

| Model | Where encryption happens | Who can decrypt plaintext | Main benefit |
|---|---|---|---|
| In flight (TLS) | During network transfer | Destination endpoint | Protects data over network |
| Server-side at rest | On server/storage service | Service (with keys) | Protects stored data |
| Client-side | On client | Client only | Maximum data confidentiality from server |

---

## Exam/Interview Tips
- Distinguish in-flight vs at-rest clearly.
- Remember: HTTPS implies TLS for transport encryption.
- In server-side encryption, key management is on the service side.
- In client-side encryption, the server cannot decrypt without client keys.

## One-Sentence Summary
Use TLS for transport protection, server-side encryption for managed secure storage, and client-side encryption when only the client should ever access plaintext.
