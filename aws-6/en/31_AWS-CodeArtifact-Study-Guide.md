# AWS CodeArtifact - Study Guide

## Overview

**AWS CodeArtifact** is a fully managed artifact repository service that makes it easy for organizations to securely store, publish, and share software packages used in their software development process.

## What is Artifact Management?

- When building software, your code depends on other software libraries and packages (called **code dependencies**)
- These dependencies are typically stored in repositories
- The entire web of dependencies is called **artifact management**
- Traditionally, setting up and maintaining your own artifact management system can be complicated

## Key Benefits

1. **Secure** - Artifacts live within your VPC in AWS
2. **Scalable** - Managed by AWS, scales automatically
3. **Cost-effective** - Pay for what you use
4. **Integrated** - Works seamlessly with common dependency management tools

## Supported Package Managers

CodeArtifact integrates with popular dependency management tools:

- **Maven** (Java)
- **Gradle** (Java/Kotlin)
- **npm** (JavaScript/Node.js)
- **yarn** (JavaScript/Node.js)
- **pip** (Python)
- **twine** (Python)
- **NuGet** (.NET)

## Architecture

### Domains and Repositories

- CodeArtifact organizes artifacts using **domains**
- Each domain contains a set of **repositories**
- All artifacts live within your VPC in AWS

### How It Works

#### 1. Proxy for Public Repositories

Instead of developers directly accessing public artifact repositories, CodeArtifact acts as a **proxy**:

```
Developer → CodeArtifact → Public Artifact Repository
```

**Benefits:**
- **Network Security**: Developers only interact with CodeArtifact
- **Caching**: Dependencies are cached in CodeArtifact
- **Availability**: Even if a dependency disappears from the public repo, you retain your cached copy

**Supported Languages:**
- JavaScript (npm/yarn)
- Python (pip)
- .NET (NuGet)
- Java (Maven/Gradle)

#### 2. Private Artifact Publishing

- Developers and teams can publish their own packages to CodeArtifact
- Internal artifacts are approved and shared across teams
- All artifacts centralized in one place within your VPC

#### 3. Integration with AWS CodeBuild

- CodeBuild can fetch dependencies directly from CodeArtifact
- No need to reach out to public repositories during builds
- Faster, more secure, and more reliable builds

## Event-Driven Integration

### EventBridge Integration

CodeArtifact events trigger downstream AWS services:

**Event Types:**
- Package created
- Package modified
- Package deleted

**Triggered Services:**
- AWS Lambda functions
- AWS Step Functions
- Amazon SNS (Simple Notification Service)
- Amazon SQS (Simple Queue Service)
- AWS CodePipeline

### Example Use Case

When a package version is updated in CodeArtifact:
1. Event is emitted to EventBridge
2. EventBridge triggers CodePipeline
3. CodePipeline automatically starts a build/deployment process

## Key Concepts Summary

| Concept | Description |
|---------|-------------|
| **Artifact** | A software package or library |
| **Domain** | A logical grouping of repositories |
| **Repository** | Storage location for artifacts |
| **Proxy** | CodeArtifact fetches from public repos on your behalf |
| **Caching** | Dependencies are stored locally for reliability |
| **EventBridge** | AWS service for event-driven integrations |

## Study Tips

1. Understand the difference between public and private repositories
2. Know how CodeArtifact improves security through proxying
3. Remember the supported package managers
4. Understand how CodeArtifact integrates with CodeBuild and CodePipeline
5. Be familiar with EventBridge integration patterns

## Exam Preparation

**Key Points to Remember:**
- ✅ CodeArtifact is a **managed artifact repository service**
- ✅ Supports common package managers (Maven, Gradle, npm, yarn, pip, NuGet)
- ✅ Acts as a **proxy** for public repositories with caching
- ✅ Integrates with **CodeBuild** for CI/CD pipelines
- ✅ Emits events to **EventBridge** for automation
- ✅ All artifacts stored securely within your **VPC**
