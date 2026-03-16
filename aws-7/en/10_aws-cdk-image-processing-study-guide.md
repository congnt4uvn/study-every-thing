# AWS CDK Image Processing Study Guide

## Overview

This study note is based on a walkthrough that uses AWS CDK to deploy an image-processing pipeline on AWS. The solution creates:

- An Amazon S3 bucket to store uploaded images
- An AWS Lambda function to process uploaded images
- Amazon Rekognition to detect labels in images
- An Amazon DynamoDB table to store detection results

The main goal is to show how Infrastructure as Code works with AWS CDK and how AWS services can be connected into an event-driven workflow.

## Architecture

The application flow is:

1. A user uploads an image to an S3 bucket.
2. S3 triggers a Lambda function.
3. The Lambda function sends the image to Amazon Rekognition.
4. Rekognition returns detected labels.
5. The Lambda function stores the image name and labels in DynamoDB.

## Why Use AWS CDK

AWS CDK lets you define cloud infrastructure with programming languages such as JavaScript or Python instead of writing raw CloudFormation templates.

Benefits mentioned in the walkthrough:

- Faster development with familiar languages
- Reusable constructs and abstractions
- Easier integration between infrastructure resources
- CDK automatically generates the CloudFormation template

## Main AWS Services Used

### Amazon S3

- Stores uploaded image files
- Sends event notifications when new objects are created

### AWS Lambda

- Runs serverless code when triggered by S3
- Calls Rekognition and writes results to DynamoDB

### Amazon Rekognition

- Detects labels in uploaded images
- Example labels include `penguin`, `bird`, `person`, and `shoe`

### Amazon DynamoDB

- Stores processed results
- Each item contains the image name and detected labels

### AWS IAM

- Grants the Lambda function permission to access other AWS services
- Policies can be attached in CDK code

### AWS CloudFormation

- CDK synthesizes the infrastructure into a CloudFormation template
- CloudFormation handles the actual deployment

## Setup Steps From the Walkthrough

### 1. Install CDK libraries

The walkthrough installs CDK dependencies with `npm`.

Example idea:

```bash
sudo npm install aws-cdk-lib
```

After installation, the `cdk` command becomes available.

### 2. Create a CDK project

Create a project directory and initialize the CDK app.

Example:

```bash
mkdir cdk-app
cd cdk-app
cdk init app --language javascript
```

To verify initialization:

```bash
cdk ls
```

Expected result: one stack, such as `CdkAppStack`.

### 3. Replace the generated stack file

The generated file in the `lib` directory is replaced with custom CDK code that defines:

- S3 bucket
- IAM role and permissions
- DynamoDB table
- Lambda function
- S3 event source for Lambda
- Outputs such as bucket name

## Important CDK Concepts Shown

### Removal Policy

Resources can be configured with a removal policy like `DESTROY`, meaning they are deleted when the stack is deleted.

### Outputs

CDK can create CloudFormation outputs, for example:

- Bucket name
- Table name

These are useful after deployment.

### Permissions Shortcuts

CDK provides helper methods such as granting read or write permissions directly to Lambda without manually writing full IAM policies.

### Service References

Resources can reference one another in code. For example:

- Lambda receives environment variables based on the DynamoDB table
- Lambda is attached to S3 events

This is a key advantage of programming infrastructure.

## Lambda Function Purpose

The Lambda function does the following:

1. Receives an event from S3 when an image is uploaded.
2. Reads the image information.
3. Calls Amazon Rekognition to detect labels.
4. Writes the result into DynamoDB.

The walkthrough mentions that the Lambda source file is written in Python as `index.py`.

## Bootstrap, Synthesize, Deploy

### CDK Bootstrap

Before deploying CDK apps in an account and region, you must run bootstrap once.

```bash
cdk bootstrap
```

This creates support resources such as:

- S3 bucket
- IAM roles
- ECR repository
- SSM parameters

These resources are typically created in a CloudFormation stack called `CDKToolkit`.

### CDK Synthesize

Generate the CloudFormation template locally:

```bash
cdk synth
```

This helps you preview what AWS resources will be deployed.

### CDK Deploy

Deploy the stack to AWS:

```bash
cdk deploy
```

This creates the actual resources in your account.

## End-to-End Test

After deployment:

1. Open the created S3 bucket.
2. Upload test images.
3. Wait for the Lambda function to run.
4. Check the DynamoDB table.

Expected result:

- A new DynamoDB item appears for each image.
- The item includes the file name and detected labels.

Examples from the walkthrough include images such as:

- `penguins.jpeg`
- `kid_and_pigeons`
- `swans`

## Cleanup

To remove everything:

1. Empty the S3 bucket first.
2. Destroy the CDK stack.

```bash
cdk destroy
```

This prevents deletion from failing because S3 buckets must usually be empty before stack removal.

## Key Exam and Study Points

- AWS CDK is an Infrastructure as Code tool that generates CloudFormation.
- S3 can trigger Lambda through object-created events.
- Lambda can call Amazon Rekognition for image analysis.
- DynamoDB is a good fit for storing fast key-value style results.
- IAM permissions are required for service-to-service access.
- `cdk bootstrap`, `cdk synth`, `cdk deploy`, and `cdk destroy` are core CDK commands.
- CDK makes cross-service integration easier than writing raw templates manually.

## Suggested Review Questions

1. Why would you use AWS CDK instead of writing CloudFormation directly?
2. What event causes the Lambda function to run in this architecture?
3. What type of data does Rekognition return in this example?
4. Why is DynamoDB suitable for storing detection results?
5. Why must the S3 bucket be emptied before `cdk destroy`?

## Short Summary

This example demonstrates an event-driven AWS application built with CDK. Images are uploaded to S3, processed by Lambda with Rekognition, and stored in DynamoDB. The walkthrough highlights how CDK simplifies infrastructure creation, permissions, deployment, and cleanup.