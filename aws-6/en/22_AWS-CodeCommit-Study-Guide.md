# AWS CodeCommit Study Guide

## Overview
AWS CodeCommit is a fully managed source control service that hosts secure Git-based repositories. It is part of the AWS Developer Tools suite, which includes CodeBuild, CodeDeploy, and CodePipeline.

## Key Concepts

### What is CodeCommit?
- Fully managed source control service
- Git-based repositories
- Integrated with other AWS DevOps services
- Secure and scalable

## Getting Started with CodeCommit

### Creating a Repository
1. Open the CodeCommit console
2. Navigate to the left-hand side menu to access:
   - CodeCommit
   - CodeBuild
   - CodeDeploy
   - CodePipeline
3. Click "Create repository"
4. Enter repository name (e.g., `my-nodejs-app`)
5. Add description and tags (optional)
6. Click "Create"

### Connection Methods
CodeCommit supports three connection methods:
- **HTTPS** - Standard HTTP-based authentication
- **SSH** - Secure Shell authentication
- **HTTPS GRC** - Git Remote CodeCommit

**Important Note**: SSH option is only available when using IAM Users. If connected with the root account, SSH will not appear.

## Working with Files

### Uploading Files
1. Navigate to the repository
2. Click "Add file" → "Upload file"
3. Select file to upload (one file at a time)
4. Enter commit details:
   - Author name
   - Email address
   - Commit message
5. Click "Commit changes"

### Example Upload
- File: `index.html`
- Author: Stephane
- Email: stephane@example.com
- Commit message: "first commit"

## Repository Features

### Code View
- Browse repository files
- View file contents
- Create and upload files
- View commit history

### Branches
- **Master Branch**: Default branch created automatically
- **Multiple Branches**: Support for collaborative development
- **Branch Creation**: Can create additional branches (dev, test, etc.)
- **Branch From**: Specify source branch for new branches

### Pull Requests
- Allow developers to merge changes from different branches
- Merge into master or other target branches
- Required for DevOps exam knowledge
- Enable code review and collaboration

### Commits
- **View Commits**: See all repository commits
- **Commit Visualizer**: Visual representation of commit history
- **Compare Commits**: Compare changes between branches or commits
- **Browse Repository**: View repository state at specific commit

### Git Tags
- Used for marking specific points in repository history
- Typically used for release versions

### Settings
Repository information includes:
- Repository name
- Repository ID
- ARN (Amazon Resource Name)
- Description

## Best Practices
1. Use IAM Users instead of root account
2. Provide meaningful commit messages
3. Use branches for development work
4. Use pull requests for code review
5. Tag releases appropriately

## Integration with Other Services
CodeCommit integrates seamlessly with:
- **AWS CodeBuild**: Automated build service
- **AWS CodeDeploy**: Automated deployment service
- **AWS CodePipeline**: Continuous integration and delivery
- **AWS Elastic Beanstalk**: Application deployment

## Exam Tips
- Understand difference between HTTPS and SSH authentication
- Know when SSH is available (IAM Users only)
- Understand pull requests in DevOps context
- Be familiar with branching strategies
- Know how CodeCommit integrates with other AWS services

## Summary
AWS CodeCommit provides a secure, scalable Git-based repository hosting service that integrates with AWS DevOps tools. It supports standard Git operations, multiple authentication methods, and collaborative development features like branches and pull requests.
