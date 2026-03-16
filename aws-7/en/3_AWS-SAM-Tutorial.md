# AWS SAM (Serverless Application Model) Tutorial

## Overview
AWS SAM (Serverless Application Model) is a framework for building serverless applications on AWS. It provides a simplified way to define and deploy Lambda functions, APIs, databases, and event source mappings.

## Getting Started with AWS SAM

### 1. Starting AWS Cloud Shell
- Open AWS Console and click on the Cloud Shell icon
- Wait for the environment to prepare your terminal
- Cloud Shell comes with SAM CLI pre-installed

### 2. Verify SAM CLI Installation
```bash
sam --version
```
This command confirms that SAM CLI is installed and shows the version.

## Creating a SAM Application

### Initialize a New SAM Project
```bash
sam init
```

### Configuration Options
When initializing, you'll be prompted with several options:

1. **Template Choice**: Select Quick Start template (option 1)
2. **Template Type**: Choose from 16+ options including:
   - Hello World Example
   - Data Processing
   - Serverless API
   - DynamoDB Example
   - And more...

3. **Runtime Selection**: Choose your preferred Python version (e.g., Python 3.9, 3.13)
4. **Additional Features**:
   - X-ray tracing: Enable/disable distributed tracing
   - CloudWatch Insights: Enable/disable enhanced monitoring
   - JSON log format: Enable/disable structured logging
5. **Project Name**: Enter your application name (default: sam-app)

## Project Structure

After initialization, your SAM application will contain:

### Key Directories
- **hello_world/**: Contains your application code
- **tests/**: Contains test files
- **events/**: Contains sample event payloads for testing

### Important Files

#### 1. `hello_world/app.py`
Your main Lambda function code:
```python
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello world')
    }
```

#### 2. `requirements.txt`
Defines Python packages/dependencies needed for your application:
```
requests
```

#### 3. `samconfig.toml`
Configuration file for your SAM application containing:
- Version information
- Stack name
- Build parameters
- Deployment settings

#### 4. `template.yaml`
The serverless application template - the most important file:
```yaml
Transform: AWS::Serverless
Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.9
      Timeout: 3
```

Key elements:
- **Transform**: Specifies this as a SAM template
- **Type**: AWS::Serverless::Function for Lambda functions
- **CodeUri**: Location of your function code
- **Handler**: Entry point for your function
- **Runtime**: Python version to use

## Building Your SAM Application

### Navigate to Project Directory
```bash
cd sam-app
```

### View Project Files
```bash
find . -print
```

### Build the Application
```bash
sam build
```

This command:
- Packages your application
- Resolves dependencies
- Creates build artifacts in `.aws-sam/` directory

## Troubleshooting

### Python Version Issues
If you encounter a Python version error during build:

1. **Check Available Python Version**:
   ```bash
   python --version
   ```

2. **Update template.yaml**:
   ```bash
   nano template.yaml
   ```
   
3. **Modify the Runtime**:
   Change the runtime to match your available Python version:
   ```yaml
   Runtime: python3.9  # Use the version available in your environment
   ```

4. **Save and Verify**:
   - Press `Ctrl+X`, then `Y`, then `Enter` to save
   - Verify changes: `cat template.yaml`

5. **Rebuild**:
   ```bash
   sam build
   ```

## Next Steps

After successful build:
- Deploy your application using `sam deploy`
- Test locally using `sam local invoke`
- Monitor logs using CloudWatch
- Iterate and improve your serverless application

## Key Benefits of AWS SAM

- **Simplified Syntax**: Easier than raw CloudFormation
- **Local Testing**: Test Lambda functions locally
- **Built-in Best Practices**: Security, monitoring, and logging
- **Quick Start Templates**: Pre-built examples to start quickly
- **Integration**: Works seamlessly with AWS services

## Best Practices

1. Always specify the correct Python runtime version
2. Keep your requirements.txt updated
3. Use environment variables for configuration
4. Enable X-ray tracing for production applications
5. Implement proper error handling in your Lambda functions
6. Use CloudWatch Logs for debugging and monitoring

---

**Note**: This tutorial is based on a hands-on Cloud Shell session demonstrating the basics of AWS SAM framework for serverless application development.
