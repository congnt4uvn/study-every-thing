# Lesson 12 — Security: TLS, SASL, ACLs, secrets hygiene

## Goals
- Understand Kafka security layers at a high level
- Know the purpose of TLS, SASL, and ACLs
- Avoid common secret-handling mistakes

## Security layers
Kafka security is typically made of:
- **Encryption in transit** (TLS)
- **Authentication** (SASL mechanisms like SCRAM, OAUTHBEARER)
- **Authorization** (ACLs)

## TLS (encryption)
TLS protects data in transit and helps prevent MITM attacks.

Practical notes:
- TLS adds operational complexity (cert lifecycle)
- Standardize cert provisioning and rotation

## SASL (authentication)
SASL confirms clients are who they claim to be.

Common patterns:
- SCRAM usernames/passwords
- OAuth/JWT integration in some environments

## ACLs (authorization)
ACLs define which principals can:
- Read from topics
- Write to topics
- Create/alter topics
- Use consumer groups

## Secrets hygiene
- Don’t commit credentials to git
- Avoid embedding secrets in container images
- Prefer secret managers and runtime injection

## Hands-on (conceptual)
In a real cluster, you’d:
- Turn on TLS
- Require SASL
- Create least-privilege ACLs per app

For local learning, focus on understanding the model before adding complexity.

## Checklist
- I can explain TLS vs SASL vs ACLs
- I know why least privilege matters in Kafka
- I have a plan for handling secrets safely

## Common pitfalls
- Running production Kafka in PLAINTEXT
- Giving broad topic permissions to every app
