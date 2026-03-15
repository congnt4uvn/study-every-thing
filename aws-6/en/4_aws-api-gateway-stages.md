# AWS API Gateway - Deployment Stages and Stage Variables

## Overview
This document covers API Gateway deployment stages and stage variables, essential concepts for managing different versions of your API.

## Deployment Stages

### Key Concepts
- **Changes are not effective until deployed**: When you modify API Gateway configuration, you must deploy the changes for them to take effect
- **Common mistake**: Forgetting to deploy changes after making configuration updates
- **Multiple stages**: You can create as many stages as you want with custom naming conventions
  - Examples: `dev`, `test`, `prod`
  - Examples: `v1`, `v2`, `v3`

### Stage Features
- Each stage has its own configuration parameters
- Seamless rollback capability
- Complete deployment history is maintained
- Each stage gets a unique URL

### Use Case: Managing Breaking API Changes

**Scenario**: You need to deploy a new version of Lambda that breaks compatibility with v1

**Solution**: Create separate stages
```
v1 Stage → v1 Lambda Function → api.example.com/v1
v2 Stage → v2 Lambda Function → api.example.com/v2
```

**Benefits**:
- v1 and v2 can coexist simultaneously
- Gradual client migration from v1 to v2
- No downtime during transition
- Shutdown v1 when no longer needed

## Stage Variables

### Definition
Stage variables are like environment variables but specifically for API Gateway stages.

### Purpose
- Change configuration values without redeploying your API
- Dynamic configuration management

### Common Use Cases
1. **Lambda function ARN configuration**
2. **HTTP endpoint configuration**
3. **Parameter mapping templates**
4. **Environment-specific endpoints** (dev, test, prod)
5. **Pass configuration to Lambda functions**
6. **Point to different Lambda function versions**

### Accessing Stage Variables

**In API Gateway**: 
```
$stageVariables.variableName
```

**In Lambda Function**: Stage variables are passed in the context object

## Advanced Pattern: Lambda Aliases with Stage Variables

### Architecture Example

```
dev Stage → stageVariable: lambdaAlias=dev
  ↓
dev Alias → 100% traffic to Lambda latest version

test Stage → stageVariable: lambdaAlias=test
  ↓
test Alias → 100% traffic to Lambda v2

prod Stage → stageVariable: lambdaAlias=prod
  ↓
prod Alias → 95% traffic to v1, 5% traffic to v2
```

### Benefits
- Stage variable indicates which Lambda alias to invoke
- API Gateway automatically invokes the correct Lambda function
- Update Lambda alias percentages without modifying API Gateway
- Enables canary deployments and gradual rollouts
- Each stage maintains its own routing logic

## Best Practices

1. ✅ **Always deploy** after making API Gateway changes
2. ✅ **Use meaningful stage names** (dev, test, prod or v1, v2, v3)
3. ✅ **Leverage stage variables** for environment-specific configuration
4. ✅ **Use Lambda aliases** with stage variables for version management
5. ✅ **Keep deployment history** for easy rollback
6. ✅ **Test in lower stages** before promoting to production

## Important Reminders

⚠️ **Critical**: Changes to API Gateway are NOT live until you deploy them to a stage

⚠️ **Common Pattern**: Use stage variables to point to Lambda aliases for flexible version management without API Gateway redeployment

---

**Study Tip**: This pattern (API Gateway Stages → Stage Variables → Lambda Aliases → Lambda Versions) is very common in AWS and frequently appears in certification exams.
