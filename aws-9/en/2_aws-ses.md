# AWS SES – Simple Email Service

## Overview

**Amazon SES (Simple Email Service)** is one of the simplest services in AWS. It is designed specifically for sending and receiving emails.

---

## Key Features

- **Send emails** using:
  - SMTP interface
  - AWS SDK

- **Receive emails** and integrate with other AWS services:
  - Amazon S3
  - Amazon SNS
  - AWS Lambda

- Uses **IAM permissions** for access control, fully integrated with SES.

---

## When to Use SES?

| Scenario | Use SES? |
|---|---|
| Need to send transactional/marketing emails | ✅ Yes |
| Need to receive and process incoming emails | ✅ Yes |
| Non-email related notifications | ❌ No |

---

## Exam Tips

> **SES = Email**

- If an exam question mentions **email**, SES is likely the correct answer.
- Be careful — exam questions may try to trick you into using SES for non-email use cases.
- Remember: SES is **only** for email sending and receiving.

---

## Quick Summary

| Property | Detail |
|---|---|
| Full Name | Simple Email Service |
| Use Case | Send & receive emails |
| Interface | SMTP or AWS SDK |
| Integrations | S3, SNS, Lambda |
| Access Control | IAM permissions |

---

## Related Services

- **SNS** – Simple Notification Service (for push notifications, SMS, etc.)
- **S3** – Can store received email content
- **Lambda** – Can trigger functions on received emails
