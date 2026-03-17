# AWS Study Notes: ACM Private Certificates and AWS Private CA

## 1. Core Idea
AWS Certificate Manager (ACM) can issue:
- Public certificates
- Private certificates

To issue private certificates, you must use **AWS Private Certificate Authority (AWS Private CA)**.

## 2. What Is AWS Private CA?
AWS Private CA is a managed service that lets you build a private PKI (Public Key Infrastructure) inside an organization.

You can create:
- A root CA
- Subordinate CAs (which depend on a root CA)

## 3. End-Entity X.509 Certificates
From your private CA, you can issue end-entity X.509 certificates for apps, users, and devices.

Important:
- End-entity certificates are for identity and encryption use.
- They **cannot** be used to issue new certificates.

## 4. Trust Model
Private certificates are trusted only by systems that trust your private CA.

This usually means:
- Internal applications
- Internal users/devices/services in your organization

These private certificates are **not** for public internet trust by default.

## 5. AWS Service Integration
If an AWS service integrates with ACM, you can often attach private certificates to it.

Examples mentioned:
- CloudFront
- API Gateway
- Load Balancers
- Kubernetes-related services

## 6. Typical Subjects for Certificates
Private CA certificates can be issued to:
- Users
- Computers
- APIs / HTTP endpoints
- IoT devices

## 7. Main Use Cases
- Internal TLS encryption for secure communication
- Code signing and authentication use cases
- Authenticating users, computers, APIs, and IoT devices
- Building enterprise private PKI

## 8. Exam/Interview Quick Review
- ACM supports both public and private certs.
- Private cert issuance requires AWS Private CA.
- Root CA can sign subordinate CAs.
- End-entity certs cannot sign other certs.
- Private certs are for internal trust, not public internet trust.

## 9. Memory Aids
- "Public certs = internet trust"
- "Private certs = organization trust"
- "Private CA = your internal certificate factory"
