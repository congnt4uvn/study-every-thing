# AWS Lambda Versions and Aliases

## Overview
This document covers the key concepts of Lambda Versions and Aliases in AWS.

## Lambda Versions

### The $LATEST Version
- When working with Lambda functions, you use the **$LATEST** version by default
- This version is **mutable** - you can edit your code, environment variables, and configuration

### Publishing Versions
- When you're satisfied with your code, you can **publish** the Lambda function to create a new version
- Once published, it becomes **V1**, **V2**, **V3**, etc.
- Published versions are **immutable**

### What Does Immutable Mean?
- You **cannot change** the code
- You **cannot change** environment variables
- You **cannot change** any configuration afterwards
- The version is fixed permanently

### Version Characteristics
- Versions have **increasing version numbers** (V1 → V2 → V3)
- Each version is **independent**
- Each version gets its **own ARN** (Amazon Resource Name)
- Each version contains both your code and configuration locked in

### Use Cases
- Great for **iterating** and development
- Mark your **advancement** and progress
- Control **releases** of your Lambda function

## Lambda Aliases

### Purpose
- Provide a **standard endpoint** for end users
- Avoid exposing changing version numbers to users

### What Are Aliases?
- **Pointers** that point to Lambda function versions
- Are **mutable** (can be updated to point to different versions)
- Can be used to create different environments

### Common Alias Examples
- **DEV** - points to development version
- **TEST** - points to testing version  
- **PROD** - points to production version

### How Aliases Work
```
$LATEST (mutable version)
   ↓
  V1 (immutable version)
   ↓
  V2 (immutable version)
   ↑
DEV Alias → points to V2
TEST Alias → points to V1
PROD Alias → points to V1
```

### Key Difference
- **Versions**: Immutable (cannot change)
- **Aliases**: Mutable (can be updated to point to different versions)

## Benefits
1. **Version Control**: Track different versions of your Lambda function
2. **Environment Management**: Separate DEV, TEST, and PROD environments
3. **Safe Deployments**: Test new versions before promoting to production
4. **Stable Endpoints**: Users access stable alias names instead of changing version numbers
