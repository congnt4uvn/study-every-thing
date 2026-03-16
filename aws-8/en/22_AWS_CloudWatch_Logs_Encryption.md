# AWS CloudWatch Logs Encryption with KMS

## Overview
CloudWatch Logs encryption allows you to encrypt your logs using AWS Key Management Service (KMS) keys to enhance security and compliance.

## Key Concepts

### Encryption Level
- **Encryption Scope**: Encryption happens at the **log group level**, not at the log stream level
- **KMS Key Association**: You can associate a Customer Master Key (CMK) with a log group to encrypt all logs within that group

### Methods to Associate KMS Keys

#### 1. Associate KMS Key with Existing Log Group
Use the `associate-kms-key` command to associate a KMS key with an existing log group.

**Limitation**: You cannot perform this operation through the CloudWatch console. You must use:
- CloudWatch Logs API
- AWS CLI
- AWS SDK

#### 2. Create New Log Group with KMS Key
Use the `create-log-group` command to create a new log group that doesn't exist yet and directly associate it with a KMS key at creation time.

## CLI Commands

### Associate KMS Key with Existing Log Group
```bash
aws logs associate-kms-key \
  --log-group-name <log-group-name> \
  --kms-key-id <kms-key-id> \
  --region <region>
```

### Create Log Group with KMS Key
```bash
aws logs create-log-group \
  --log-group-name <log-group-name> \
  --kms-key-id <kms-key-id> \
  --region <region>
```

## Practical Example

### Troubleshooting: Access Denied Exception

When attempting to associate a KMS key with a log group, you might encounter:
```
AccessDeniedException: Associate KMS key operation failed
```

**Possible Causes**:
1. The KMS key does not exist
2. The KMS key is not authorized to be used with the log group
3. Insufficient IAM permissions

**Resolution**:
- Verify the KMS key exists in your AWS account
- Ensure the key policy allows CloudWatch Logs service to use the key
- Check IAM permissions for your user/role

## Important Notes

1. **Console Limitation**: The AWS Management Console UI does not provide an option to associate KMS keys with log groups after creation
2. **Log Group Level**: All log streams within a log group share the same encryption key
3. **Access Control**: Proper KMS key policies and IAM permissions are required for successful encryption setup

## Best Practices

- Use KMS encryption for log groups containing sensitive information
- Ensure KMS key policies are properly configured to allow CloudWatch Logs service access
- Test key association in a non-production environment first
- Monitor KMS key usage for compliance and audit purposes
