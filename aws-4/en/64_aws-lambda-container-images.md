# AWS Lambda Container Images

## Overview

AWS Lambda now supports **container images** as a deployment method, allowing you to deploy Lambda Functions as container images up to **10 GB** from Amazon ECR (Elastic Container Registry).

## Key Features

### Container Image Support
- Deploy Lambda Functions as container images
- Maximum size: 10 GB from ECR
- Package complex and large dependencies in containers
- Unified workflow for container deployment

### Docker Integration
Docker enables you to package together:
- Application code
- Dependencies
- Data sets
- Base image (that implements the Lambda Runtime API)

## Lambda Runtime API Requirement

**Important**: The base image **must implement the Lambda Runtime API** for Lambda to run the container.

### Supported Base Images

AWS provides base images for multiple languages:
- Python
- Node.js
- Java
- .NET
- Go
- Ruby

### Custom Base Images
You can create your own Lambda base image, but it must implement the Lambda Runtime API. Refer to AWS documentation for the specification.

## Testing

Use the **Lambda Runtime Interface Emulator** to test your containers locally before deployment.

## Unified Workflow

Container images for Lambda allow a unified workflow to publish applications:
- Build containers the same way for ECS or Lambda
- Publish containers to Amazon ECR
- Deploy from ECR to Lambda

## Example: Lambda Container Image

```dockerfile
# Choose a base image that implements Lambda Runtime API
FROM amazon/aws-lambda-nodejs:12

# Copy application code and files
COPY app.js package.json ./

# Install dependencies
RUN npm install

# Specify which function to run
CMD ["app.handler"]
```

## Workflow Steps

1. **Select Base Image**: Choose an image that implements the Lambda Runtime API
2. **Copy Code**: Add your application code and configuration files
3. **Install Dependencies**: Run necessary installation commands (e.g., npm install)
4. **Define Handler**: Specify the function to execute
5. **Build & Push**: Build the image and push to Amazon ECR
6. **Deploy**: Deploy from ECR to Lambda

## Benefits

- ✅ Support for complex dependencies
- ✅ Large dependency packages (up to 10 GB)
- ✅ Consistent deployment workflow across services
- ✅ Local testing capabilities
- ✅ Familiar Docker tooling

## Notes

- Not just any Docker container will work
- Base image must implement Lambda Runtime API
- Containers run in Lambda virtual machines
- ECR integration is required for deployment
