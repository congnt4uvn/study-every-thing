# AWS Encryption CLI - Study Guide

## Overview
This guide covers the installation and usage of the AWS Encryption CLI for encrypting and decrypting data using AWS Key Management Service (KMS).

## Installation

### Prerequisites
- Python installed on your system
- Access to AWS services

### Installation Steps

1. **Check Python Version**
   - Verify your Python installation
   - Windows instructions are available if needed

2. **Install AWS Encryption CLI**
   ```bash
   pip install aws-encryption-cli
   ```

3. **Verify Installation**
   ```bash
   aws-encryption-cli --version
   ```
   - Example output: Encryption CLI version 1.3.7

## Key Concepts

### Data Key Encryption
- This section covers how encryption works in practice
- **Note**: Execution knowledge is not required for exams, but useful for practical understanding

### Master Key Setup
- Export a CMK (Customer Master Key) ARN
- Cannot use just the key alias
- Must use the full ARN of the key

## Encryption Process

### Step 1: Prepare the File
Create a text file to encrypt:
```bash
vi hello.txt
```
- Example: Create a file with sensitive data
- File size can vary (1MB+)

### Step 2: Set Up the Key
```bash
key=<your-cmk-arn>
```

### Step 3: Encrypt the File
```bash
aws-encryption-cli encrypt \
  --plaintext-input hello.txt \
  --master-key factory=aws-kms key=$key \
  --metadata-output metadata \
  --output output/
```

**PowerShell equivalent available if needed**

#### Important Considerations:
- **Metadata Output**: Cannot be in the output directory
- Create a separate output directory if needed
- Encryption context is optional (can be removed for simplicity)

### Output Files
After encryption, you'll have:
1. **metadata** - JSON document containing:
   - Algorithm used
   - Data key information
   - Key provider details
   - Encryption context
   - Other encryption parameters

2. **output/hello.txt.encrypted** - The encrypted file
   - Appears as gibberish when displayed
   - Contains the KMS key reference and generated data key
   - Required for future decryption

## Decryption Process

### Step 1: Run Decryption Command
```bash
aws-encryption-cli decrypt \
  --ciphertext-input output/hello.txt.encrypted \
  --metadata-output metadata \
  --output decrypted/
```

### Step 2: Create Output Directory
```bash
mkdir decrypted
```

### Results
- The encrypted data is decrypted
- Original file content is restored
- Metadata about the decryption process is saved

## Key Points to Remember

1. **File Encryption**: Ensures sensitive data is protected using AWS KMS
2. **Metadata**: Provides information about the encryption process
3. **Decryption**: Requires the same AWS permissions as encryption
4. **Master Keys**: Must use full ARN, not just the alias
5. **Output Management**: Plan directory structure carefully

## Practical Tips

- Always ensure you have proper AWS IAM permissions
- Keep track of your CMK ARN for reference
- Use metadata files for auditing and documentation
- The Encryption SDK automatically handles key management
- Test encryption/decryption workflows before production use

## Exam Preparation Notes

- Focus on understanding the concepts, not memorizing exact commands
- Know when to use AWS Encryption CLI
- Understand KMS key management principles
- Be familiar with encryption context and metadata concepts
