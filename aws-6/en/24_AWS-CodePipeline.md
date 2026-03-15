# AWS CodePipeline - Study Guide

## Overview
CodePipeline is a visual workflow tool that orchestrates CI/CD (Continuous Integration/Continuous Deployment) within AWS.

## Pipeline Stages

### 1. Source Stage
CodePipeline can integrate with various source repositories:
- **AWS Services:**
  - CodeCommit (AWS managed Git repository)
  - Amazon ECR (Docker images)
  - Amazon S3 (code stored in S3 buckets)
- **External Tools:**
  - Bitbucket
  - GitHub

### 2. Build Stage
Once the code is retrieved, the build phase can use:
- CodeBuild (AWS native service)
- Jenkins
- CloudBees
- TeamCity

### 3. Test Stage
After building, you can test your code using:
- CodeBuild (for general testing)
- AWS Device Farm (for iOS and Android apps)
- Third-party testing tools

### 4. Deploy Stage
Final deployment options include:
- CodeDeploy
- Elastic Beanstalk
- CloudFormation
- Amazon ECS
- Amazon S3
- Lambda functions
- Step Functions

## Pipeline Structure

### Sequential and Parallel Actions
- Each stage can contain **sequential actions** (executed one after another)
- Each stage can also have **parallel actions** (executed simultaneously)

### Example Pipeline Flow
```
Source → Build → Test → Deploy to Staging → Load Testing → Deploy to Production
```

### Manual Approval
- You can define **manual approval steps** at any stage
- Common use case: Requiring human review before deploying to production
- Example: Review load testing results before production deployment

## How CodePipeline Works Internally

### Artifact Management
1. **Artifacts** are outputs created by each pipeline stage
2. All artifacts are stored in **Amazon S3 buckets**
3. Artifacts are passed from one stage to the next through S3

### Example Workflow
```
Developer → Push code to CodeCommit
         ↓
CodePipeline extracts code → Creates artifact → Stores in S3
         ↓
CodeBuild receives artifact from S3 → Builds code → Creates deployment artifact
         ↓
Artifact stored in S3 → Passed to CodeDeploy
         ↓
CodeDeploy deploys the artifact
```

**Key Point:** Stages interact with each other through Amazon S3, not directly. CodePipeline orchestrates the data flow between stages.

## Troubleshooting

### Monitoring with CloudWatch Events / EventBridge
You can monitor pipeline execution using CloudWatch Events to track:
- Pipeline action state changes
- Stage execution state changes
- Failed pipelines
- Cancelled stages

**Common Actions:**
- Create event rules for failed pipelines
- Set up email notifications for pipeline failures

### Console Visibility
- Pipeline failures are visible in the AWS Console
- You can view detailed information about stage failures
- Each failed stage shows error information

### IAM Permissions
If CodePipeline cannot perform specific actions (e.g., invoking CodeBuild, pulling from CodeCommit), check:
- The **IAM service role** attached to CodePipeline
- Verify the role has proper permissions for all integrated services

## Key Takeaways
✓ CodePipeline orchestrates the entire CI/CD process
✓ Highly flexible with multiple integration options
✓ Uses S3 as the central artifact storage mechanism
✓ Supports both automated and manual approval workflows
✓ Provides comprehensive monitoring and troubleshooting capabilities
