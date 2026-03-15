# AWS CodeBuild and CodePipeline Study Guide

## Overview
This guide covers AWS CodeBuild integration with GitHub and the fundamentals of CI/CD pipelines using AWS services.

## Key Concepts

### 1. AWS CodeBuild
- **Purpose**: Fully managed build service that compiles source code, runs tests, and produces software packages
- **Key Feature**: Continuous integration service that scales automatically

### 2. buildspec.yaml File
The `buildspec.yaml` file is the configuration file that tells CodeBuild how to run a build.

#### Structure of buildspec.yaml
```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      nodejs: latest
    commands:
      - echo "installing something"
  
  pre_build:
    commands:
      - echo "we are in the pre_build phase"
  
  build:
    commands:
      - echo "we are in the build block"
      - echo "we will run some test"
      - grep -Fq "Congratulations" index.html
  
  post_build:
    commands:
      - echo "we are in the post_build phase"
```

### 3. Build Phases

#### Phase Sequence:
1. **Submitted** - Build job submitted
2. **Queued** - Build waiting in queue
3. **Provisioning** - Setting up build environment
4. **Download_source** - Downloading source code from repository
5. **Install** - Installing dependencies and runtimes
6. **Pre_build** - Commands before build (e.g., logging in to registries)
7. **Build** - Main build commands and tests
8. **Post_build** - Commands after build (e.g., packaging)
9. **Upload_artifacts** - Uploading build outputs
10. **Finalizing** - Cleanup operations
11. **Completed** - Build finished

### 4. GitHub Integration

#### Webhook Configuration
- CodeBuild can be automatically triggered when code is pushed to GitHub
- GitHub Hook sends notifications to CodeBuild on push events
- Automatic builds start when commits are made to the repository

#### Setting Up:
1. Create `buildspec.yaml` file in GitHub repository root
2. Configure CodeBuild project to connect to GitHub
3. Set up webhook for automatic triggers
4. Commit changes directly to main branch

### 5. Testing in Build Phase

#### Example Test Command:
```bash
grep -Fq "Congratulations" index.html
```

**Explanation**:
- `grep`: Search for patterns in files
- `-F`: Fixed string search (not regex)
- `-q`: Quiet mode (only return exit status)
- Returns success if "Congratulations" is found in index.html
- Build fails if the text is not found

### 6. Monitoring and Logs

#### CloudWatch Integration
- All build logs are automatically sent to CloudWatch Logs
- You can view logs in two ways:
  1. **CodeBuild Console**: Inline log viewer
  2. **CloudWatch Console**: Full log console with search capabilities

#### Viewing Logs:
- Click on build ID to see build details
- Navigate to "Phase details" to see status of each phase
- Click "View entire Log" to open CloudWatch console

### 7. CodePipeline Integration
- CodePipeline orchestrates the entire CI/CD workflow
- Can include multiple stages: Source → Build → Test → Deploy
- CodeBuild is typically used as the Build stage

## Best Practices

1. **Echo Statements**: Use echo commands to track progress through build phases
2. **Runtime Versions**: Specify runtime versions explicitly or use "latest"
3. **Testing**: Include automated tests in the build phase
4. **Error Handling**: Monitor phase details to identify failures
5. **Log Analysis**: Use CloudWatch for detailed debugging

## Common Workflow

1. Developer pushes code to GitHub
2. GitHub webhook triggers CodeBuild
3. CodeBuild downloads source from GitHub
4. Installs required runtimes (e.g., Node.js 20)
5. Executes commands in each phase
6. Runs tests to validate build
7. Generates artifacts
8. Uploads to specified location
9. Reports build status

## Troubleshooting

### Build Failures
- Check phase details to identify which phase failed
- Review CloudWatch logs for error messages
- Verify buildspec.yaml syntax
- Ensure test commands are correct

### Source Download Issues
- Verify GitHub repository access
- Check webhook configuration
- Confirm branch name is correct

## Key Takeaways

- `buildspec.yaml` is essential for CodeBuild configuration
- Build process has multiple distinct phases
- GitHub integration enables automatic CI/CD
- CloudWatch provides comprehensive logging
- Testing should be integrated into build phase
- CodePipeline orchestrates the complete workflow

## Next Steps

- Learn about CodePipeline stages
- Explore artifact management
- Study deployment strategies
- Practice creating custom buildspec files
- Implement automated testing strategies
