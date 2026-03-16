# AWS Study Notes: CloudFormation Dynamic References

## Overview
Dynamic references let AWS CloudFormation retrieve external values during stack create, update, or delete operations.

These values usually come from:
- AWS Systems Manager Parameter Store
- AWS Secrets Manager

This is useful when you do not want to hardcode passwords, usernames, or configuration values directly inside a CloudFormation template.

## Supported Dynamic Reference Types
CloudFormation supports three main dynamic reference types:

1. `ssm`
   - For plain text values stored in Systems Manager Parameter Store.
2. `ssm-secure`
   - For encrypted secure string values stored in Systems Manager Parameter Store.
3. `secretsmanager`
   - For secret values stored in AWS Secrets Manager.

## General Syntax
The general format is:

```text
{{resolve:service-name:reference-key}}
```

Examples:

```text
{{resolve:ssm:parameter-name:version}}
{{resolve:ssm-secure:parameter-name:version}}
{{resolve:secretsmanager:secret-id:SecretString:json-key}}
```

## Example 1: Use Parameter Store Plain Text Value
This example resolves an SSM parameter and uses it in an S3 bucket property.

```yaml
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      AccessControl: '{{resolve:ssm:my-s3-access-control:1}}'
```

Use this when the value is not sensitive.

## Example 2: Use Parameter Store Secure String
This example retrieves an encrypted value from Parameter Store.

```yaml
Resources:
  MyUser:
    Type: AWS::IAM::User
    Properties:
      LoginProfile:
        Password: '{{resolve:ssm-secure:iam-user-password:1}}'
```

Use `ssm-secure` when the parameter is stored as a secure string.

## Example 3: Use Secrets Manager for RDS Credentials
This example shows how an RDS database can read credentials from Secrets Manager.

```yaml
Resources:
  MyDatabase:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: mysql
      MasterUsername: '{{resolve:secretsmanager:my-db-secret:SecretString:username}}'
      MasterUserPassword: '{{resolve:secretsmanager:my-db-secret:SecretString:password}}'
```

This is a common approach for database credentials.

## CloudFormation + RDS + Secrets Manager Patterns
There are two important patterns to know.

### Pattern 1: RDS Creates the Secret Automatically
If you configure an RDS cluster with:

```yaml
ManageMasterUserPassword: true
```

RDS automatically creates and manages the master user secret in Secrets Manager.

To output the secret ARN, use `GetAtt`:

```yaml
Outputs:
  MasterUserSecretArn:
    Value: !GetAtt MyDBCluster.MasterUserSecret.SecretArn
```

In this pattern:
- CloudFormation creates the RDS resource.
- RDS creates and manages the secret.
- Secrets Manager stores the password and can rotate it.

### Pattern 2: CloudFormation Creates the Secret
In this pattern, CloudFormation creates the secret first, often with an auto-generated password, then the database uses a dynamic reference to read it.

Typical flow:
- Create a secret in Secrets Manager.
- Generate the password automatically.
- Reference the secret in the RDS resource.
- Attach the secret to the RDS database for rotation.

Example structure:

```yaml
Resources:
  MySecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      GenerateSecretString:
        SecretStringTemplate: '{"username":"admin"}'
        GenerateStringKey: password

  MyDatabase:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: mysql
      MasterUsername: '{{resolve:secretsmanager:MySecret:SecretString:username}}'
      MasterUserPassword: '{{resolve:secretsmanager:MySecret:SecretString:password}}'

  SecretAttachment:
    Type: AWS::SecretsManager::SecretTargetAttachment
    Properties:
      SecretId: !Ref MySecret
      TargetId: !Ref MyDatabase
      TargetType: AWS::RDS::DBInstance
```

In this pattern:
- CloudFormation creates the secret.
- The database reads credentials through dynamic references.
- The secret can be attached for rotation support.

## Why Dynamic References Matter
Dynamic references are important because they:
- Avoid hardcoding sensitive values in templates.
- Improve security and maintainability.
- Support secret rotation workflows.
- Make CloudFormation templates cleaner and safer.

## Quick Review
Remember these key points:
- `ssm` is for plain text parameters.
- `ssm-secure` is for encrypted parameters in Parameter Store.
- `secretsmanager` is for secrets stored in Secrets Manager.
- Dynamic references are resolved during stack operations.
- RDS can either create its own secret or use a secret created by CloudFormation.

## Practice Questions
1. When should you use `ssm` instead of `ssm-secure`?
2. Why is Secrets Manager a better choice for database passwords?
3. What does `ManageMasterUserPassword: true` do in RDS?
4. Why would you use `SecretTargetAttachment`?
5. At what time does CloudFormation resolve dynamic references?
