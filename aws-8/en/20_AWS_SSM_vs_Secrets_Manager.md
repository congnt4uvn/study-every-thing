# AWS: SSM Parameter Store vs Secrets Manager

## Overview
This guide covers the differences between AWS Systems Manager (SSM) Parameter Store and Secrets Manager, including their features, use cases, and secret rotation capabilities.

## Key Differences

### Secrets Manager
**Cost:** More expensive compared to Parameter Store

**Features:**
- Automated secret rotation using Lambda functions
- Many Lambda functions provided out-of-the-box integrations
- Strong integration with AWS services:
  - Amazon RDS
  - Amazon Redshift
  - Document DB
- Mandatory KMS encryption for all secrets
- CloudFormation integration available

**Use Case:** Best for managing sensitive credentials that require automated rotation

---

### SSM Parameter Store
**Cost:** Less expensive than Secrets Manager

**Features:**
- Wider range of use cases (parameters and secrets)
- Simple API
- No native secret rotation (but can be implemented manually)
- Optional KMS encryption
- CloudFormation integration available
- Can reference Secrets from Secrets Manager using Parameter Store API

**Use Case:** Best for storing configuration parameters and simple secrets with lower cost requirements

---

## Secret Rotation

### Secrets Manager Rotation
When rotating a secret (e.g., Amazon RDS database password):

1. Set up Secrets Manager to automatically invoke a Lambda function
2. Default rotation interval: Every 30 days
3. AWS provides pre-built Lambda functions for common services (RDS, Redshift, etc.)
4. These Lambda functions automatically change passwords in integrated services
5. No custom code required for native integrations

---

### Parameter Store Rotation
Unlike Secrets Manager, Parameter Store has no native rotation feature.

**Manual Implementation:**
1. Create an Amazon EventBridge rule
2. Trigger on a defined schedule (similar to 30-day interval)
3. Use a custom Lambda function to rotate the secret manually
4. AWS documentation provided for custom implementation

**Note:** If using RDS password in Parameter Store, EventBridge + Lambda approach is needed

---

## Summary

| Feature | Secrets Manager | Parameter Store |
|---------|-----------------|-----------------|
| Cost | Higher | Lower |
| Native Rotation | Yes (30 days) | No |
| KMS Encryption | Mandatory | Optional |
| Use Cases | Sensitive credentials | Wide range |
| Pre-built Integrations | Yes | No |
| Custom Rotation | Manual Lambda | Manual Lambda + EventBridge |

Choose **Secrets Manager** for automated secret management with strong AWS integrations.
Choose **Parameter Store** for general configuration and cost-optimized scenarios.
