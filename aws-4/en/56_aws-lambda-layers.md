# AWS Lambda Layers - Study Guide

## Overview
This guide demonstrates how to use AWS Lambda layers to add external libraries to your Lambda functions without packaging them directly in your deployment package.

## What are Lambda Layers?
Lambda layers are a distribution mechanism for libraries, custom runtimes, and other function dependencies. They help you:
- Manage dependencies separately from function code
- Share common components across multiple functions
- Keep deployment packages small

## Practical Example: Using Pandas Library with Lambda Layers

### Step 1: Create a Lambda Function
1. Go to AWS Lambda console
2. Click "Create function"
3. **Function name**: `Lambda-layer-demo`
4. **Runtime**: Python 3.13 (or latest available version)
5. Click "Create function"

### Step 2: Add Code with External Dependency
The function code imports and uses the Pandas library for data manipulation:

```python
import pandas as pd

# Generate sample data
# Filter data using Pandas library
```

**Important**: At this point, the function will fail because Pandas is not included by default.

### Step 3: Deploy and Test (Expected Failure)
1. Click "Deploy" to save the code
2. Go to the "Test" tab
3. Click "Test" to execute the function
4. **Expected result**: Failure with error message "Unable to find the module pandas"

### Step 4: Add a Lambda Layer
1. Scroll down to the "Layers" section in your function configuration
2. Click "Add a layer" at the bottom
3. Select "AWS layers" (pre-built layers provided by AWS)
4. Choose: **AWSSDK Pandas-Python313 Version 1**
5. Confirm the layer addition

### Step 5: Test Again (Success)
After adding the layer, test your function again. It should now execute successfully with access to the Pandas library.

## Key Concepts

### Benefits of Lambda Layers
- **Separation of concerns**: Keep libraries separate from application code
- **Reusability**: Share layers across multiple functions
- **Easier updates**: Update dependencies without modifying function code
- **Size optimization**: Keep function deployment packages smaller

### Types of Layers
- **AWS layers**: Pre-built layers provided by AWS (e.g., AWS SDK, Pandas)
- **Custom layers**: Layers you create yourself with specific dependencies
- **Public layers**: Community-shared layers

## Best Practices
1. Use AWS-provided layers when available (maintained and optimized)
2. Keep layers version-specific for consistency
3. Layer size limit: 50 MB (zipped) per layer
4. Maximum 5 layers per function
5. Layers are extracted to `/opt` directory in the Lambda execution environment

## Troubleshooting
- If module is not found after adding layer, verify:
  - Runtime version matches (e.g., Python 3.13)
  - Layer is compatible with your function's runtime
  - Layer is properly attached to the function

## Study Questions
1. What problem do Lambda layers solve?
2. What is the maximum number of layers you can attach to a single Lambda function?
3. Why might you choose an AWS-provided layer over a custom layer?
4. What happens when you test a Lambda function with external dependencies before adding the required layer?

## Further Learning
- Explore creating custom Lambda layers
- Learn about layer versioning and management
- Study Lambda layer sharing across AWS accounts
- Investigate layer deployment with IaC tools (CloudFormation, Terraform)
