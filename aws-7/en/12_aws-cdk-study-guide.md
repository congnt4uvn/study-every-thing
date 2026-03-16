# AWS CDK Study Guide

## What Is AWS CDK?
AWS CDK (Cloud Development Kit) lets you define cloud infrastructure using programming languages, then convert it into AWS CloudFormation templates.

## Core CDK Commands

### 1. Install CDK CLI and Libraries
Install the AWS CDK CLI and language libraries first so you can create and manage CDK apps.

### 2. `cdk init`
Initializes a new CDK application from a template.
You can choose template languages such as Python, JavaScript, and others.

### 3. `cdk synth`
Synthesizes your CDK code into a CloudFormation template and prints it.
This is the transformation from infrastructure-as-code to CloudFormation JSON/YAML.

### 4. `cdk bootstrap`
Prepares an AWS environment before deployment by creating required resources.
(Details in the bootstrapping section below.)

### 5. `cdk deploy`
Deploys your synthesized CloudFormation stack to AWS.

### 6. `cdk diff`
Shows differences between your local CDK code and the currently deployed CloudFormation stack.
Useful for reviewing changes before deployment.

### 7. `cdk destroy`
Deletes deployed CDK stacks and their resources.

## CDK Bootstrapping Explained
Bootstrapping is the process of provisioning prerequisite resources in AWS before you deploy CDK apps.

For CDK, an **environment** means:
- AWS account
- AWS region

So each unique account+region combination must be bootstrapped.

When you run:

```bash
cdk bootstrap aws://<aws_account>/<aws_region>
```

CDK creates a CloudFormation stack named **CDKToolkit** containing required resources such as:
- An S3 bucket
- An IAM role

These are required for CDK deployments in that environment.

## What Happens If You Skip Bootstrap?
If the target environment is not bootstrapped, deployment may fail with errors related to invalid IAM principal/policy statements.

## Suggested Learning Flow
1. Install CDK tools.
2. Create an app with `cdk init`.
3. Run `cdk synth` to inspect the generated template.
4. Run `cdk bootstrap` for the target account/region.
5. Deploy with `cdk deploy`.
6. Validate changes with `cdk diff` in future updates.
7. Clean up with `cdk destroy` when done.

## Quick Summary
- CDK code -> `cdk synth` -> CloudFormation template
- Environment setup -> `cdk bootstrap`
- Deployment -> `cdk deploy`
- Change review -> `cdk diff`
- Cleanup -> `cdk destroy`
