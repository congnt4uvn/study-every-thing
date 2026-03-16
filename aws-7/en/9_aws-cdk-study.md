# AWS Cloud Development Kit (CDK) - Study Guide

## Overview

The **AWS Cloud Development Kit (CDK)** is a framework that allows you to define your cloud infrastructure using familiar programming languages instead of declarative configuration files.

### Supported Languages
- JavaScript/TypeScript
- Python
- Java
- .NET

## Key Concepts

### What is CDK?

CDK enables you to define cloud infrastructure using programming languages, which offers several advantages over traditional CloudFormation YAML templates:

- **Type Safety**: Code must compile before generating templates
- **Error Detection**: Catch errors during development, not deployment
- **Flexibility**: Use full programming language features
- **Reusability**: Create and share reusable components

### Relationship with CloudFormation

CDK **supersedes** CloudFormation by:
- Compiling into CloudFormation templates (JSON or YAML)
- Providing higher-level abstractions (constructs)
- Maintaining CloudFormation compatibility in the backend

## Constructs

**Constructs** are high-level components in CDK that encapsulate AWS resources with pre-made configurations.

### Example: TypeScript Infrastructure Definition

```typescript
// 1. Create a VPC with 3 Availability Zones
const vpc = new VPC(this, 'MyVPC', {
  maxAzs: 3
});

// 2. Create an ECS Cluster
const cluster = new ECS.Cluster(this, 'MyCluster', {
  vpc: vpc
});

// 3. Create an Application Load-Balanced Fargate Service
const fargateService = new ApplicationLoadBalancedFargateService(this, 'MyService', {
  cluster: cluster,
  cpu: 512,
  desiredCount: 6,
  taskImageOptions: { /* config */ },
  memoryLimitMiB: 2048,
  publicLoadBalancer: true
});
```

## CDK Workflow

1. **Write Code**: Define infrastructure using programming language
2. **Compile**: Ensure code is typesafe and error-free
3. **Synthesize**: Use CDK CLI to generate CloudFormation template
4. **Deploy**: Apply template through CloudFormation

```
Application Constructs (Lambda, DynamoDB, S3, ECS, Step Functions)
         ↓
Programming Language (Python, TypeScript, Java, .NET)
         ↓
CDK CLI (cdk synth)
         ↓
CloudFormation Template
         ↓
Infrastructure Deployment
```

## Use Cases

CDK is particularly great for:
- **Lambda Functions**: Deploy infrastructure and code together
- **Docker Containers**: ECS and EKS deployments
- **Complex Infrastructure**: Multi-service architectures
- **Application Runtime**: Infrastructure and application code combined

## CDK vs SAM

### SAM (Serverless Application Model)
- **Focus**: Serverless and Lambda functions
- **Format**: Declarative JSON/YAML templates
- **Best For**: Quickly getting started with Lambda
- **Backend**: Leverages CloudFormation

### CDK (Cloud Development Kit)
- **Focus**: All AWS services (superset of CloudFormation)
- **Format**: Programming languages (TypeScript, Python, Java, .NET)
- **Best For**: Complex infrastructure with type safety
- **Backend**: Generates CloudFormation templates

## CDK + SAM Integration

You can combine CDK and SAM for local testing:

1. Run `cdk synth` to generate CloudFormation template from CDK app
2. Use SAM CLI to locally test the CDK application
3. Leverage SAM's local testing capabilities with CDK's infrastructure definition

## Key Benefits

✅ **Type Safety**: Compile-time error checking  
✅ **IDE Support**: Auto-completion and inline documentation  
✅ **Reusable Components**: Create and share constructs  
✅ **Familiar Languages**: Use tools and patterns you already know  
✅ **CloudFormation Power**: Full AWS service support  
✅ **Flexible**: Combine infrastructure and application code  

## Commands

- `cdk synth`: Synthesize CDK app into CloudFormation template
- `cdk deploy`: Deploy infrastructure to AWS
- `cdk diff`: Compare deployed stack with current state
- `cdk destroy`: Remove deployed resources

---

**Study Tip**: Practice by converting simple CloudFormation templates into CDK code to understand the differences and benefits of using a programming language approach.
