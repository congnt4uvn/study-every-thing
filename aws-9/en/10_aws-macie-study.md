# AWS Macie Study Notes

## What is AWS Macie?
AWS Macie is a fully managed data security and data privacy service.
It uses machine learning and pattern matching to discover and protect sensitive data stored in AWS.

## Main Purpose
Macie helps identify sensitive data, especially:
- PII (Personally Identifiable Information)

## How It Works (Basic Flow)
1. Your data is stored in Amazon S3 buckets.
2. AWS Macie scans and classifies the data.
3. Macie detects sensitive content such as PII.
4. Findings are sent through Amazon EventBridge.
5. You can integrate actions with services like:
- Amazon SNS
- AWS Lambda

## Key Exam/Study Points
- Macie is focused on sensitive data discovery in S3.
- It is a managed service (no infrastructure to manage).
- It supports automated detection using ML and pattern matching.
- EventBridge can route findings for alerts and automation.

## Quick Summary
Use AWS Macie when you want to discover and monitor sensitive data (like PII) in Amazon S3 and trigger alerts or automation based on findings.
