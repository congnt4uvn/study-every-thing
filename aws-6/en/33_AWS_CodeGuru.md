# Amazon CodeGuru

## Overview

Amazon CodeGuru is a machine learning-powered service that provides two main capabilities:

1. **Automated code reviews**
2. **Application performance recommendations**

## Components

### CodeGuru Reviewer

**Purpose:** Automated code reviews with static code analysis

**Key Features:**
- Analyzes code in repositories (CodeCommit, GitHub, Bitbucket)
- Provides actionable recommendations for bugs and memory leaks
- Detects issues before human reviewers using machine learning
- Identifies critical issues, security vulnerabilities, and hard-to-find bugs

**Capabilities:**
- Implement coding best practices
- Find resource leaks
- Security detection and vulnerability identification
- Input validation

**Supported Languages:**
- Java
- Python

**How It Works:**
- Uses machine learning and automated reasoning
- Trained on thousands of open source repositories
- Trained on all amazon.com repositories

### CodeGuru Profiler

**Purpose:** Application performance monitoring and optimization

**When to Use:**
- During build and test phases (pre-production)
- In production runtime

**Key Features:**
- Provides visibility into application performance during runtime
- Detects and optimizes expensive lines of code pre-production
- Measures application performance in real-time
- Identifies performance and cost improvements in production

**Capabilities:**
- Understand runtime behavior of applications
- Identify code that consumes excessive CPU capacity
- Remove code inefficiencies
- Improve application performance
- Reduce CPU utilization and decrease compute costs
- Provide heap summaries to identify memory-intensive objects
- Anomaly detection for unusual application behavior

**Deployment:**
- Supports applications running on AWS Cloud
- Supports on-premises applications
- Minimal overhead on monitored applications

## Summary

CodeGuru combines automated code review and performance profiling to help developers:
- Catch bugs early in development
- Improve code quality
- Optimize application performance
- Reduce costs
- Enhance security
