# AWS CDK Constructs Study Guide

## Overview

AWS CDK uses **Constructs** as the main building blocks for defining cloud infrastructure. A construct packages the configuration CDK needs to generate a final CloudFormation stack.

A construct can represent:

- A single AWS resource, such as an S3 bucket
- A group of related resources, such as a worker system using SQS and compute services

CDK provides constructs through:

- The **Construct Library**, which includes constructs for AWS resources
- The **Construct Hub**, which includes constructs from AWS, third parties, and the open-source community

## The 3 Construct Levels

### Level 1: L1 Constructs

L1 constructs are the most basic form of constructs.

- Also called **CFN Resources**
- Directly map to CloudFormation resources
- Usually begin with `Cfn`, for example `s3.CfnBucket`
- Require you to define properties close to raw CloudFormation syntax

#### When to use L1

- When you want full control over CloudFormation properties
- When migrating from existing CloudFormation templates to CDK
- When a higher-level construct does not expose a specific low-level property you need

#### Example

```ts
new s3.CfnBucket(this, 'MyBucket', {
  bucketName: 'my-bucket'
});
```

#### Key idea

L1 is powerful but low-level. It is close to infrastructure definition in raw CloudFormation.

### Level 2: L2 Constructs

L2 constructs are higher-level AWS resource abstractions.

- Represent AWS resources with better developer experience
- Do **not** start with `Cfn`, for example `s3.Bucket`
- Provide sensible defaults and helper methods
- Let you express intent more clearly

#### Benefits of L2

- Less boilerplate
- Easier configuration
- Additional helper methods
- Better readability

#### Example

```ts
const bucket = new s3.Bucket(this, 'MyBucket', {
  versioned: true,
  encryption: s3.BucketEncryption.KMS
});
```

With L2 constructs, you can also use helper methods such as lifecycle configuration methods instead of manually writing every CloudFormation detail.

#### Key idea

L2 gives you the same infrastructure outcome as L1 in many cases, but in a more convenient and maintainable way.

### Level 3: L3 Constructs

L3 constructs are also called **Patterns**.

- Combine multiple related resources into one reusable solution
- Focus on common AWS architectures
- Reduce the complexity of assembling multiple services manually

#### Examples

- Lambda REST API pattern
- ECS with Application Load Balancer and Fargate Service

#### Why L3 is useful

Some AWS architectures are complex in raw CloudFormation because they require many connected resources, such as:

- Load balancers
- Compute services
- Security groups
- Listeners
- Integrations between services

L3 constructs hide much of that setup and let you focus on the architecture you want.

#### Key idea

L3 is best for quickly building common AWS solutions with less manual wiring.

## Quick Comparison

| Level | Name | Scope | Main Benefit | Example |
| --- | --- | --- | --- | --- |
| L1 | CFN Resource | Single CloudFormation resource | Maximum control | `s3.CfnBucket` |
| L2 | AWS Resource Construct | Single AWS resource | Defaults and helper methods | `s3.Bucket` |
| L3 | Pattern | Multiple related resources | Faster architecture setup | Lambda REST API pattern |

## How to Recognize Each Level

- If the construct name starts with `Cfn`, it is usually **L1**
- If it models a single AWS resource in a friendly way, it is usually **L2**
- If it creates a complete architecture or solution pattern, it is usually **L3**

## Study Notes

- **Construct** is the core abstraction in AWS CDK
- CDK converts constructs into CloudFormation
- **L1** is closest to raw CloudFormation
- **L2** is the most commonly used level for daily development
- **L3** helps you build common architectures quickly
- Construct Hub extends what you can use beyond the built-in AWS library

## Exam and Interview Focus

Be ready to explain:

1. What a construct is in AWS CDK
2. The difference between L1, L2, and L3 constructs
3. Why L2 and L3 are often preferred over L1 for productivity
4. When L1 is still necessary
5. The difference between the Construct Library and Construct Hub

## Short Summary

AWS CDK constructs are reusable building blocks for defining infrastructure as code. L1 constructs map directly to CloudFormation, L2 constructs provide higher-level resource abstractions, and L3 constructs package common architectural patterns. The higher the level, the more convenience and abstraction you get.