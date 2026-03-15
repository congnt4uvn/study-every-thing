# AWS CodeBuild Study Guide

## Overview
AWS CodeBuild is a fully managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy.

## Key Concepts

### What is CodeBuild?
- A managed build service in the cloud
- Compiles source code and runs tests
- No need to provision, manage, or scale build servers
- Integrates with other AWS services and popular source control systems

## Creating a CodeBuild Project

### 1. Project Configuration
- **Project Name**: Choose a descriptive name (e.g., "MyFirstBuild")
- **Description**: Optional project description
- **Build Badge**: Optional status badge
- **Tags**: Optional metadata tags

### 2. Source Configuration

#### Supported Source Providers:
- Amazon S3
- AWS CodeCommit
- GitHub
- Bitbucket
- GitHub Enterprise
- GitLab
- GitLab Self-Managed

#### GitHub Integration:
1. Select GitHub as source provider
2. Connect using OAuth
3. Authorize AWS CodeSuite to access your repositories
4. Select the repository (e.g., nodejs-app)
5. Choose branch (default: main)

#### Build Triggers:
- **Rebuild on code change**: Automatically trigger builds when code is pushed
- **Single Build**: Execute one build per trigger
- **Event Types**:
  - PUSH: Build when code is pushed
  - Pull Request: Build when PR is created
  - Release: Build when release is created

### 3. Environment Configuration

#### Compute Options:
- **Managed Image**: Amazon Linux or Ubuntu
- **Runtime**: Standard
- **Image Version**: Latest (e.g., standard 7.0)

#### Service Role:
- Create a new service role (e.g., "CodeBuildDemoServiceRole")
- Grants necessary permissions for CodeBuild operations

#### Additional Configuration:
- **Timeout**: Maximum build duration (default: 1 hour, adjustable to shorter durations like 10 minutes)
- **VPC**: Optional - select VPC to access private resources (databases, internal services)
- **Compute Size**: 
  - 3 GB memory
  - 2 vCPUs
  - (Can be adjusted based on needs)
- **Environment Variables**: Define variables for build process

### 4. Buildspec Configuration

#### What is Buildspec?
- A YAML file that defines build commands and settings
- Must be named `buildspec.yaml` (or `buildspec.yml`)
- Located in the source code root directory

#### Buildspec Options:
1. **Use a buildspec file**: Reference buildspec.yaml in repository
2. **Insert build commands**: Define commands directly in console

**Important**: If using a buildspec file, ensure it exists in your repository root. Build will fail if the file is missing.

### 5. Artifacts (Optional)
- Store build outputs in Amazon S3
- Useful for compiled binaries, packages, or deployment artifacts
- Not required for testing-only builds

### 6. Logs
- **CloudWatch Logs**: Stream logs to CloudWatch
- **Amazon S3**: Store logs in S3 bucket

## Running a Build

### Build Process:
1. CodeBuild pulls source code from repository
2. Sets up build environment
3. Executes commands defined in buildspec.yaml
4. Runs tests or compiles code
5. Produces artifacts (if configured)
6. Reports success or failure

### Common Failure Reasons:
- Missing buildspec.yaml file
- Incorrect buildspec syntax
- Build command failures
- Test failures
- Insufficient permissions

## Best Practices

1. **Version Control**: Always store buildspec.yaml in your repository
2. **Timeouts**: Set appropriate timeouts to avoid unnecessary costs
3. **VPC Configuration**: Use VPC for accessing private resources
4. **Environment Variables**: Store secrets in AWS Systems Manager Parameter Store or Secrets Manager
5. **Build Triggers**: Configure appropriate triggers (PUSH, PR, Release) based on workflow
6. **Compute Size**: Choose appropriate compute resources based on build complexity
7. **Logs**: Enable CloudWatch Logs for debugging and monitoring

## Use Cases

- **Continuous Integration**: Automatically build and test code on every commit
- **Continuous Testing**: Run test suites on pull requests
- **Package Creation**: Compile and package applications for deployment
- **Multi-Environment Builds**: Build for different environments (dev, staging, prod)

## Integration with AWS Services

- **CodePipeline**: Orchestrate build, test, and deployment workflows
- **CodeCommit**: Use AWS-native Git repositories
- **S3**: Store artifacts and logs
- **CloudWatch**: Monitor builds and view logs
- **IAM**: Manage permissions and access control

## Summary

AWS CodeBuild eliminates the need to manage build servers while providing a scalable, secure, and integrated solution for building and testing code. By properly configuring source integration, environment settings, and buildspec files, you can create automated CI/CD workflows that improve code quality and deployment speed.
