# AWS SAM with DynamoDB - Study Guide

## Overview
This guide covers AWS SAM (Serverless Application Model) integration with DynamoDB, including how to create, deploy, and test serverless APIs backed by DynamoDB tables.

---

## What is AWS SAM?

**AWS SAM (Serverless Application Model)** is a framework that simplifies the development and deployment of serverless applications on AWS. It provides:
- A simplified syntax compared to raw CloudFormation
- Easy definition of serverless functions, APIs, and databases
- Local testing capabilities without deploying to AWS
- Quick deployment and cleanup commands

---

## Key Components

### 1. SAM CLI Commands

#### Initialize a New Project
```bash
sam init
```
- Use quick start templates
- Select template type (e.g., Serverless API)
- Choose runtime (e.g., nodejs22)
- Configure options (X-Ray, etc.)

#### Deploy Application
```bash
sam deploy
```

#### Delete Application
```bash
sam delete
```
**Important**: Always delete deployed resources after testing to avoid unnecessary charges.

#### Local Testing Commands
```bash
# Invoke a function locally
sam local invoke <FunctionName> -e <event-file>

# Start local API Gateway
sam local start-api
```

---

## Template Structure (template.yaml)

### Essential Elements

#### 1. Transform Declaration
```yaml
Transform: AWS::Serverless-2016-10-31
```
This line is **crucial** for SAM - it enables SAM-specific resource types and simplified syntax.

#### 2. Resources Section

**Serverless Function Example:**
```yaml
Resources:
  GetAllItemsFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./src
      Handler: get-all-items.handler
      Runtime: nodejs22.x
      MemorySize: 128
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref SampleTable
      Events:
        GetAllItems:
          Type: Api
          Properties:
            Path: /
            Method: GET
```

**DynamoDB Table Example:**
```yaml
  SampleTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      PrimaryKey:
        Name: id
        Type: String
      ProvisionedThroughput:
        ReadCapacityUnits: 2
        WriteCapacityUnits: 2
```

---

## Simplified IAM Policies with SAM

### DynamoDBCrudPolicy
SAM provides simplified policy templates that automatically generate proper IAM policies:

```yaml
Policies:
  - DynamoDBCrudPolicy:
      TableName: !Ref SampleTable
```

This single line replaces complex CloudFormation IAM policy definitions with full CRUD access to the specified DynamoDB table.

---

## API Gateway Integration

SAM makes API definition extremely simple:

### GET Endpoint
```yaml
Events:
  GetItems:
    Type: Api
    Properties:
      Path: /
      Method: GET
```

### POST Endpoint
```yaml
Events:
  CreateItem:
    Type: Api
    Properties:
      Path: /
      Method: POST
```

---

## Local Development Workflow

### 1. Sample Events
SAM projects typically include sample event files in the `events/` directory. These JSON files simulate API Gateway or other AWS service events.

### 2. Local Invocation
```bash
sam local invoke PutItemFunction -e events/put-item-event.json
sam local invoke GetAllItemsFunction -e events/get-all-items-event.json
```

**Requirements for Local Testing:**
- Docker must be installed
- Necessary runtime environments
- Not available on AWS CloudShell

### 3. Local API Gateway
```bash
sam local start-api
```
This starts a local API Gateway on your computer, allowing you to:
- Test your entire API locally
- Iterate quickly without AWS deployment
- Make changes and test immediately
- Deploy to AWS only when ready

---

## Complete Serverless API Example

A typical serverless API with DynamoDB includes:

1. **Multiple Lambda Functions** - for different operations (GET, POST, PUT, DELETE)
2. **API Gateway Events** - defining HTTP paths and methods
3. **DynamoDB Table** - for data persistence
4. **IAM Policies** - simplified through SAM policy templates
5. **Configuration** - runtime, memory, timeout settings

---

## Best Practices

1. **Use SAM Templates** - Leverage pre-built templates with `sam init`
2. **Test Locally First** - Use `sam local` commands to test before deployment
3. **Clean Up Resources** - Always run `sam delete` after testing
4. **Use Simple Policies** - Leverage SAM policy templates instead of raw IAM
5. **Version Control** - Keep your template.yaml in version control
6. **Read Documentation** - Check README.md files in sam projects for specific instructions

---

## Project Structure

A typical SAM project looks like:
```
sam-app-dynamodb/
├── template.yaml          # SAM template definition
├── README.md              # Project documentation
├── events/                # Sample event files
│   ├── put-item-event.json
│   └── get-all-items-event.json
└── src/                   # Lambda function source code
    ├── get-all-items.js
    ├── put-item.js
    └── package.json
```

---

## Key Takeaways

✅ **SAM simplifies serverless development** compared to raw CloudFormation
✅ **Local testing saves time and money** by avoiding constant AWS deployments
✅ **Policy templates reduce complexity** of IAM configuration
✅ **API definition is straightforward** with SAM's simplified syntax
✅ **Full-stack serverless APIs** can be deployed with a single command

---

## Additional Resources

- Official AWS SAM Documentation
- AWS Lambda Documentation
- Amazon DynamoDB Documentation
- CloudFormation Documentation
- Docker Installation Guide

---

*Study this guide thoroughly to understand AWS SAM's power in simplifying serverless application development and deployment.*
