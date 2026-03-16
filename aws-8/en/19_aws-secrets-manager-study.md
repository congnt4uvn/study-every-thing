# AWS Secrets Manager Study Notes

## Overview

AWS Secrets Manager is a managed AWS service for storing, retrieving, rotating, and managing secrets securely. It is commonly used for database credentials, API keys, and other sensitive configuration values that applications need at runtime.

## Core Purpose

- Store secrets securely instead of hardcoding them in applications.
- Retrieve secrets through API calls when applications need them.
- Manage the lifecycle of secrets from creation to deletion.
- Rotate credentials automatically to improve security.

## How It Differs from Parameter Store

Compared with Systems Manager Parameter Store using `SecureString`, Secrets Manager is more focused on secret lifecycle management.

Key difference:

- Secrets Manager supports automatic rotation.
- Rotation can be connected to an AWS Lambda function.
- It has strong integration with databases such as Amazon RDS, PostgreSQL-compatible systems, Redshift, and DocumentDB.

In short, both services can store encrypted values, but Secrets Manager is designed to make secret rotation easier and more secure.

## What You Can Store

Secrets Manager supports several kinds of secrets, including:

- Database credentials
- API keys
- Custom key-value secrets
- Plaintext JSON secrets

For a database secret, you typically store:

- Username
- Password

For a custom secret, you can store one or more key-value pairs, such as:

```json
{
  "apiKey": "your-secret-value",
  "secretKey": "your-second-secret-value"
}
```

This is a practical difference from simpler parameter storage because one secret can contain multiple related values.

## Encryption

When creating a secret, you choose the encryption key:

- Use the default AWS managed key
- Use a customer-managed KMS key

This determines how the secret is encrypted at rest.

## Creating a Secret

Typical steps:

1. Choose the secret type.
2. Enter the values manually or paste JSON.
3. Choose the encryption key.
4. Give the secret a name.
5. Optionally add a description and tags.
6. Configure rotation if needed.

Example secret name:

- `prod/my-secret-api`

## Automatic Rotation

One of the most important features of Secrets Manager is automatic rotation.

How it works:

- You define a rotation interval, such as every 60 days.
- Secrets Manager triggers a Lambda function.
- That Lambda function performs the rotation logic.
- The function must have the required IAM permissions.

The Lambda function could:

- Generate a new password
- Update credentials in a third-party service
- Refresh or replace an API key

Maximum rotation interval mentioned in the lecture:

- Up to 1 year

## Database Integrations

Secrets Manager can integrate directly with supported databases.

With these integrations:

- The secret stores the username and password.
- Secrets Manager can also update the linked database credentials.
- Rotation can be enabled so both the secret and the database credentials stay synchronized.

This makes it more powerful than simple secret storage alone.

## Access Control

Access to secrets is controlled with IAM.

That means you can define:

- Which users can read secrets
- Which roles can rotate them
- Which applications can retrieve them

## Pricing Mentioned in the Source

The transcript mentions:

- `$0.40` per secret per month
- `$0.05` per 10,000 API calls
- A 30-day free trial for secret storage

Pricing can change over time, so verify on the official AWS pricing page.

## Retrieving a Secret in Code

The source explains that retrieving a secret is straightforward through the AWS SDK:

- Create a Secrets Manager client
- Call `GetSecretValue`
- Pass the secret name or identifier
- Read the returned secret string

Typical use case in Python:

- Create the client
- Call `get_secret_value`
- Read the `SecretString` field
- Parse the returned JSON if needed

## Deletion Behavior

When deleting a secret, you can configure a waiting period before final deletion. This helps avoid accidental removal.

## Exam and Practical Takeaways

- Secrets Manager is for sensitive values such as credentials and API keys.
- Its biggest advantage is automatic rotation.
- Rotation is usually implemented with Lambda.
- It integrates well with AWS databases.
- IAM controls access.
- KMS handles encryption.

## Quick Review Questions

1. What is the main advantage of Secrets Manager over Parameter Store for secrets?
2. Why is Lambda important for rotation?
3. What kinds of values can be stored in one secret?
4. How does IAM help secure Secrets Manager?
5. Why is database integration useful?

## Short Summary

AWS Secrets Manager is a secure service for storing and managing secrets. Its standout feature is automatic rotation, often powered by Lambda, and it provides strong integration with AWS database services. It is a good choice when applications need secure, centrally managed, and frequently rotated credentials.