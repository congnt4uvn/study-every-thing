# AWS KMS (Key Management Service) Study Guide

## Introduction to AWS KMS

AWS Key Management Service (KMS) is a managed service that helps you create and manage encryption keys used to encrypt your data across AWS services.

---

## Types of KMS Keys

### 1. AWS Managed Keys
- **Definition**: Keys created and managed by AWS for specific AWS services
- **Cost**: No additional charge
- **Usage**: Automatically appears in KMS when you use KMS encryption with AWS services
- **Example**: AWS EBS managed key for EBS encryption

#### Key Characteristics:
- Service-specific (e.g., EBS, SQS, RDS)
- Defined with key policies that restrict usage to specific services
- Read-only (you cannot modify the key policy)

#### Key Policy Example:
```
{
  "Principal": "Service",
  "Service": "ec2.amazonaws.com",
  "Action": "kms:*",
  "Condition": {
    "StringEquals": {
      "kms:ViaService": "ec2.region.amazonaws.com"
    }
  }
}
```

**Condition Requirements**:
- Caller account must be yours
- Via Service must be the appropriate AWS service (EC2 for EBS, SQS for SQS queue, etc.)

---

### 2. Customer Managed Keys
- **Definition**: Keys created and managed by you within KMS
- **Cost**: $1 per month per key
- **Flexibility**: Full control over key policies and usage
- **Best for**: Custom encryption requirements

#### When to Use:
- Need more control over encryption
- Want to restrict key access to specific users/roles
- Building custom encryption solutions

---

### 3. Custom Key Store
- **Definition**: Uses AWS CloudHSM for key storage
- **Scope**: Out of scope for this study (advanced topic)

---

## Creating a Customer Managed Key

### Step 1: Choose Key Type
- **Symmetric Key**: Single key for both encryption and decryption
  - Most common
  - More efficient
  - Used for general encryption/decryption

- **Asymmetric Key**: Separate public and private keys
  - Used for encryption/decryption OR sign/verify operations
  - Out of scope for this lecture

### Step 2: Advanced Options
- **Key Origin**: Where the key material is created
  - **KMS**: AWS KMS creates the key material (recommended)
  - **External**: Import key material from external sources
  - **Custom Key Store**: Use CloudHSM (out of scope)

### Step 3: Regional Configuration
- **Single Region Key**: Key exists in one region only (most common)
- **Multi-Region Key**: Key replicated across multiple regions

### Step 4: Add Key Alias
- Friendly name for the key (e.g., "tutorial")
- Makes key easier to identify

### Step 5: Define Key Administrators
- Specify who can administer the key
- Skip if using default key policy

### Step 6: Define Key Users
- Specify who can use the key
- **Default Policy**: Allows anyone with IAM permissions to use the key
- **Custom Policy**: Restrict to specific users/roles

---

## Key Policies

### Default Key Policy
- Enables IAM user permissions
- Allows any resource to use KMS with proper IAM permissions
- Most common configuration

### Key Policy Structure
The key policy defines:
- Who can use the key
- What actions they can perform
- Under what conditions

### Use Cases

#### Sharing Encrypted Snapshots
- Add another AWS account to key policy
- Allow cross-account access to encrypted EBS snapshots

#### Inter-Account Access
- Add external AWS account ID to principal
- Define specific permissions for that account

---

## Cryptographic Configuration

### Symmetric Key Configuration
- **Type**: Symmetric
- **Origin**: KMS
- **Operations**: Encrypt and Decrypt
- **Characteristics**:
  - Single key for both operations
  - Highly efficient
  - Most secure when key is properly protected

---

## Key Takeaways

1. **AWS Managed Keys**: Free, service-specific, AWS-maintained
2. **Customer Managed Keys**: $1/month, full control, custom policies
3. **Key Types**: Symmetric (most common) vs Asymmetric
4. **Key Policy**: Defines access and usage permissions
5. **Regional Scope**: Choose between single and multi-region keys
6. **Best Practice**: Use AWS managed keys unless you need custom control

---

## Summary Comparison Table

| Feature | AWS Managed | Customer Managed |
|---------|-----------|------------------|
| Cost | Free | $1/month |
| Control | Limited | Full |
| Policy | Read-only | Customizable |
| Use Case | Service-specific | Custom needs |
| Administration | AWS | You |

