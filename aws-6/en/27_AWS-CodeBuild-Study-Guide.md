# AWS CodeBuild - Study Guide

## Overview
AWS CodeBuild is a fully managed continuous integration service that compiles source code, runs tests, and produces software packages ready to deploy.

## Key Concepts

### Source Code Support
CodeBuild can fetch source code from:
- **AWS CodeCommit**
- **Amazon S3**
- **Bitbucket**
- **GitHub**

### buildspec.yml File ⭐ EXAM IMPORTANT
- **Name**: `buildspec.yml`
- **Location**: Must be at the **root of your code directory**
- **Alternative**: Build instructions can be manually inserted in the console, but best practice is to use buildspec.yml
- **Exam Focus**: Know the file name and location requirement

## Output & Monitoring

### Logs
- Output logs stored in:
  - **Amazon S3**
  - **CloudWatch Logs**

### Monitoring & Alerts
- **CloudWatch Metrics**: View build statistics
- **EventBridge**: Detect failed builds and trigger notifications
- **CloudWatch Alarms**: Alert on excessive failures

## Build Projects
Build Projects can be defined in:
- **CodeBuild** directly
- **CodePipeline** (can also invoke existing CodeBuild projects)

## Supported Environments

### Pre-built Images Available For:
- Java
- Ruby
- Python
- Go
- Node.js
- Android
- .NET Core
- PHP

### Custom Environments
- Extend a Docker image to support any other language/environment
- You maintain and support your own custom environment

## How CodeBuild Works

### Workflow
1. **Fetch Code**: CodeBuild retrieves source code (e.g., from CodeCommit) including buildspec.yml
2. **Container Creation**: CodeBuild pulls a Docker image (AWS prepackaged or custom)
3. **Build Environment**: Container is created with selected environment (Java, Go, etc.)
4. **Load Code**: Container loads source code and buildspec.yml
5. **Execute Instructions**: Runs all commands from buildspec.yml
6. **Caching (Optional)**: Files can be cached in S3 bucket for reuse between builds
7. **Logging**: All logs sent to CloudWatch Logs and S3 (if enabled)
8. **Artifacts**: Final output artifacts extracted and stored in S3 bucket

## buildspec.yml Structure

### Key Sections

#### **Environment**
Define environmental variables:
- **Plain text variables**
- **SSM Parameter Store** values
- **Secrets Manager** secrets (for passwords, credentials, etc.)

#### **Phases**
- **install**: Commands to install pre-requisite packages
- **pre_build**: Commands to execute before the build
- **build**: Actual build commands ⭐ IMPORTANT
- **post_build**: Finishing touches and cleanup

### Important Notes
- Never store passwords in plaintext in buildspec.yml
- Use SSM Parameter Store or Secrets Manager for sensitive data
- File must be at the root of code directory

## Exam Tips
✅ Remember: `buildspec.yml` file name
✅ Location: Root of code directory
✅ Best practice: Use buildspec.yml file (not manual console entry)
✅ Understand the complete build workflow
✅ Know where logs are stored (S3, CloudWatch)
✅ Recognize supported programming languages

---
*Study Date: March 2026*
