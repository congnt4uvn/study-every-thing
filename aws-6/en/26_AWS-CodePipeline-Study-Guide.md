# AWS CodePipeline Study Guide

## Overview
This guide covers how to create a pipeline to deploy code from GitHub to Elastic Beanstalk using AWS CodePipeline.

## Creating a Custom Pipeline

### Step 1: Pipeline Configuration
1. **Pipeline Name**: MyFirstPipeline
2. **Execution Mode**: Queued (default setting)
3. **Service Role**: Create a new service role
   - This role allows CodePipeline to perform necessary operations
   - Very important for pipeline functionality

### Step 2: Artifact Store and Encryption
- Leave default settings for:
  - Artifact store
  - Encryption key
  - No variables needed

## Source Provider Configuration

### Available Source Providers
- **CodeCommit** (discontinued)
- **Amazon ECR**
- **Amazon S3**
- **Bitbucket** (Git provider)
- **GitHub** (version 1 and version 2)
- **GitHub Enterprise Server**
- **GitLab** and **GitLab Self-Managed**

### Recommended: GitHub Version 2

#### Setting Up GitHub Connection
1. Create a connection named "MyGitHubConnection"
2. Click "Connect to GitHub"
3. Authorize the AWS connector for GitHub
4. Install GitHub app:
   - Select repositories (can choose all repositories)
   - Enter security codes if required
   - You'll receive a GitHub app ID

5. Wait for connection status to show "Available"

#### Repository Configuration
- **Repository Name**: Select your Node.js app (or your application)
- **Default Branch**: main
- **Output Artifact Format**: CodePipeline default

### Pipeline Triggers
Configure a trigger to start the pipeline:
- **Trigger Type**: Push to branch
- **Branch Name**: main
- Pipeline starts automatically when code is pushed to the main branch

## Build Provider

Available options:
- **CodeBuild**
- **Jenkins**

*Note: Can be skipped initially and added later*

## Deploy Stage

### Deploy Provider: AWS Elastic Beanstalk

Configuration:
1. **Application Name**: Select your created application
2. **Environment**: Choose your environment (e.g., "env")

The pipeline will send code from GitHub directly to your Elastic Beanstalk application.

## Important: Service Role Permissions

### Adding Beanstalk Permissions
1. Go to **Settings** for your pipeline
2. Click on the **Service Role**
3. You'll see two policies already attached
4. Add missing permission for Beanstalk:
   - Click **Attach Policy**
   - Search for "Beanstalk"
   - Add **AdministratorAccess-AWSElasticBeanstalk**
   - *(Note: For demo purposes only; use more restrictive policies in production)*

## Key Takeaways
- CodePipeline automates deployment from source to production
- GitHub Version 2 integration is recommended
- Proper service role permissions are critical
- Pipeline can be customized with build and deploy stages
- Supports multiple source providers and deployment targets

## Best Practices
- Use specific branch triggers to control when deployments occur
- Review and adjust service role permissions for production environments
- Test pipeline with a non-production environment first
- Monitor pipeline executions for failures or issues
