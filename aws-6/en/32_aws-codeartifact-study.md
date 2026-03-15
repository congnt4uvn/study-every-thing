# AWS CodeArtifact Study Guide

## Overview
AWS CodeArtifact is a fully managed artifact repository service that makes it easy for organizations to securely store, publish, and share software packages used in their software development process.

## Key Concepts

### 1. Repository
- A repository contains packages and can have connections to external repositories
- Example: Demo Repository connected to PyPI store

### 2. Upstream Repository
- Repositories can have upstream repositories to pull packages from
- Allows fetching packages from external sources like public PyPI
- Can configure multiple upstream repositories if needed

### 3. Domain
- Represents the organizational boundary for storing artifact data
- All repositories and packages are stored within a domain
- Naming convention: typically company name (e.g., `my-company`)
- **Security**: Requires a KMS key for encryption
  - Can use AWS managed key
  - Or custom KMS key for enhanced control

### 4. External Connection
- Enables upstream repositories to connect to public package repositories
- Example: PyPI store with external connection to public python.org PyPI

## Practical Setup Walkthrough

### Step 1: Create a Repository
1. Navigate to AWS CodeArtifact console
2. Click "Create repository"
3. Name: `Demo Repository`
4. Optionally select an upstream (e.g., Python store)

### Step 2: Define Domain
1. Choose your AWS account
2. Create a new domain if none exists
3. Name the domain (e.g., `my-company`)
4. Select KMS key for encryption (AWS managed or custom)

### Step 3: Review Configuration
- Main repository: `demo-repository`
- Upstream repository: `pypi-store`
- External connection: Public PyPI store

## Connecting pip to CodeArtifact

### Method 1: Automated CLI Setup (May have issues)
```bash
# May not work in CloudShell due to pip vs pip3 compatibility
aws codeartifact login --tool pip --domain my-company --repository demo-repository
```

### Method 2: Manual Setup (Recommended)

#### Step 1: Get Authorization Token
```bash
export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
    --domain my-company \
    --domain-owner <account-id> \
    --region <region> \
    --query authorizationToken \
    --output text)
```

**Important Notes:**
- Token is valid for **12 hours**
- After expiration, you must regenerate the token
- Verify token: `echo $CODEARTIFACT_AUTH_TOKEN`

#### Step 2: Configure pip
```bash
pip3 config set global.index-url https://aws:$CODEARTIFACT_AUTH_TOKEN@<domain>-<account-id>.d.codeartifact.<region>.amazonaws.com/pypi/<repository>/simple/
```

**Note:** Use `pip3` instead of `pip` if you encounter "pip not found" errors in CloudShell.

#### Step 3: Install Packages
```bash
pip3 install response
```

This will:
- Connect to CodeArtifact repository
- Pull the specified package (`response`)
- Automatically download all dependencies
- Cache packages in CodeArtifact for future use

## Common Issues & Solutions

### Problem: "pip: command not found" in CloudShell
**Solution:** Use `pip3` instead of `pip`
- CloudShell has `pip3` installed by default
- CodeArtifact CLI may not detect this correctly

### Problem: Token expired
**Symptom:** Unable to connect or install packages
**Solution:** Regenerate authorization token (valid 12 hours)

## Benefits of AWS CodeArtifact

1. **Centralized Package Management**: Single source of truth for all dependencies
2. **Security**: Encrypted storage with KMS, IAM-based access control
3. **Caching**: Reduces external network calls, improves build speed
4. **Version Control**: Track and manage package versions
5. **Integration**: Works with npm, pip, Maven, NuGet, and more

## Best Practices

- Regularly rotate authorization tokens
- Use custom KMS keys for sensitive environments
- Configure upstream repositories to cache frequently used packages
- Implement IAM policies for fine-grained access control
- Monitor repository usage through CloudWatch

## Exam Tips

- Remember token validity: **12 hours**
- Domain is required for repository creation
- KMS encryption is mandatory for domains
- CodeArtifact supports multiple package formats (PyPI, npm, Maven, NuGet)
- Upstream repositories enable package caching from external sources
