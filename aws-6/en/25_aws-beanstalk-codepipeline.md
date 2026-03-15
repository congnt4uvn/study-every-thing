# AWS Elastic Beanstalk and Code Pipeline Study Guide

## Overview
This guide covers the setup and configuration of AWS Elastic Beanstalk environments for use with AWS Code Pipeline, enabling automated deployment workflows.

## Prerequisites
Before working with Code Pipeline, you need to set up AWS Elastic Beanstalk environments that will serve as deployment targets.

## AWS Elastic Beanstalk Setup

### Creating the First Environment

**Step 1: Application Configuration**
- Application Name: `my first web app Beanstalk`
- Environment Type: Web server environment
- Environment Name: `My first web app Beanstalk`

**Step 2: Platform Selection**
- Platform: Managed platform
- Runtime: Node.js (latest version)
- Application Code: Sample application
- Instance Type: Single instance

**Step 3: Configuration**
- Key Pair: Not defined (optional)
- Review and submit the configuration

**Step 4: Deployment**
- Wait for the environment to be created and successfully deployed
- You should see a "Congratulations" message upon successful deployment

### Creating the Second Environment (Production)

**Step 1: Navigate to Application**
- Go to your application dashboard
- Select "Create new environment"

**Step 2: Environment Configuration**
- Environment Type: Web server environment
- Environment Name: `prod`
- Platform: Node.js
- Application Code: Sample application

**Step 3: Deployment**
- Skip to review
- Submit the configuration
- Wait for deployment to complete

## AWS Code Pipeline Integration

### Purpose
Code Pipeline will be used to deploy updates to both Beanstalk environments:
1. Development environment
2. Production environment

### Deployment Workflow
Code Pipeline enables automated deployment of application updates to multiple environments, streamlining the CI/CD process.

## Important Notes

### Cost Management
⚠️ **IMPORTANT**: Remember to delete your environments after completing the labs:
- Running EC2 instances will incur charges
- Always clean up resources when not in use
- Delete both environments to avoid unnecessary costs

### Key Concepts
- **Elastic Beanstalk**: AWS service for deploying and scaling web applications
- **Code Pipeline**: Continuous integration and continuous delivery service
- **Environment**: A version of your application running on AWS resources
- **Single Instance**: Deployment configuration using one EC2 instance

## Best Practices
1. Always use sample applications for learning and testing
2. Clean up resources after completing tutorials
3. Use multiple environments for proper deployment workflows (dev, staging, prod)
4. Monitor your AWS billing dashboard regularly

## Next Steps
- Complete hands-on Code Pipeline configuration
- Practice deploying updates through the pipeline
- Explore multi-environment deployment strategies
