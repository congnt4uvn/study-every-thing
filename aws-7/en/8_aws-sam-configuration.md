# AWS SAM - Managing Multiple Environments with samconfig.toml

## Overview
AWS SAM (Serverless Application Model) provides an efficient way to manage multiple deployment environments (dev, prod, staging, etc.) within your development stack using configuration files.

## SAMconfig.toml File

### Purpose
The `samconfig.toml` file allows you to define environment-specific parameters for your SAM deployments, eliminating the need to specify parameters manually each time you deploy.

### File Format
The configuration file uses TOML (Tom's Obvious, Minimal Language) format and organizes parameters by environment and command type.

## Configuration Structure

### Development Environment Example
```toml
[dev.deploy.parameters]
stack_name = "my-app-dev"
s3_bucket = "my-deployment-bucket-dev"
s3_prefix = "dev"
region = "us-east-1"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Environment=development"

[dev.sync.parameters]
# Sync parameters for dev environment
```

### Production Environment Example
```toml
[prod.deploy.parameters]
stack_name = "my-app-prod"
s3_bucket = "my-deployment-bucket-prod"
s3_prefix = "prod"
region = "us-east-1"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Environment=production"

[prod.sync.parameters]
# Sync parameters for prod environment
```

## Deployment Commands

### Deploy to Development Environment
```bash
sam deploy --config-env dev
```

### Deploy to Production Environment
```bash
sam deploy --config-env prod
```

## How It Works

1. **Initial Setup**: Create a `samconfig.toml` file in your SAM project root
2. **Define Environments**: Configure parameters for each environment (dev, prod, staging, etc.)
3. **Automatic Parameter Selection**: SAM CLI reads the TOML file and applies the correct parameters based on the `--config-env` flag
4. **Simplified Deployment**: Deploy to any environment with a single command

## Key Parameters

- **stack_name**: CloudFormation stack name for the environment
- **s3_bucket**: S3 bucket for deployment artifacts
- **s3_prefix**: Prefix for organizing files in S3
- **region**: AWS region for deployment
- **capabilities**: IAM capabilities required (e.g., CAPABILITY_IAM)
- **parameter_overrides**: Custom parameters passed to your SAM template

## Benefits

✅ **Environment Isolation**: Separate configurations for different environments  
✅ **Reduced Errors**: No manual parameter entry reduces deployment mistakes  
✅ **Version Control**: Configuration as code - track changes in Git  
✅ **Scalability**: Add unlimited environments as needed  
✅ **Team Collaboration**: Standardized deployment process across team members

## Exam Tips

⚠️ **Important for AWS Certification Exams**:
- Understanding how to configure multiple environments using `samconfig.toml`
- Knowing the command structure: `sam deploy --config-env <environment>`
- Recognizing the TOML file format and structure
- Understanding parameter overrides and environment-specific settings

## Best Practices

1. Store `samconfig.toml` in version control
2. Use meaningful environment names (dev, staging, prod)
3. Keep sensitive data out of configuration files (use parameter overrides or secrets manager)
4. Document required parameters for team members
5. Test configuration changes in dev before applying to prod

---

**Related AWS Services**: CloudFormation, Lambda, API Gateway, S3  
**Certification Relevance**: AWS Certified Developer Associate, AWS Certified Solutions Architect
