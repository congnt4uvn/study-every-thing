# AWS API Gateway Mapping Templates

## Overview
This guide covers AWS API Gateway mapping templates and how they integrate with Lambda functions to transform request and response data.

## Key Concepts

### 1. API Gateway Integration Types
- **Lambda Proxy Integration**: Lambda function returns status code and body directly
- **Direct Integration**: API Gateway handles the response formatting, Lambda only returns data

### 2. Mapping Templates
Mapping templates allow you to transform the input and output of your API Gateway integrations.

## Practical Example: Creating a Mapping Template

### Step 1: Create API Gateway Resource
1. Create a new resource named `mapping`
2. Add a GET method to this resource
3. Choose Lambda function integration

### Step 2: Create Lambda Function
```python
# Function name: API-gateway-mapping-get
# Runtime: Python 3.11
def lambda_handler(event, context):
    return {
        "example": "hello world"
    }
```

**Important**: Do NOT enable Lambda proxy integration for this example.

### Step 3: Test Initial Setup
- The Lambda function returns: `{"example": "hello world"}`
- API Gateway passes this through with status 200
- No status code or body wrapper needed (non-proxy mode)

### Step 4: Add Mapping Template

#### Location
Go to **Integration Response** → **Mapping Templates**

#### Configuration
- **Content Type**: `application/json`
- **Template Body**:
```json
{
    "myKey": "myValue",
    "renamedKey": $input.json('$.example')
}
```

#### Template Syntax Explanation
- `$input`: Represents the JSON received as input
- `$input.json('$.example')`: Extracts the value of the "example" key
- The template transforms the Lambda output into a new structure

### Step 5: Test the Result
**Before mapping template**:
```json
{
    "example": "hello world"
}
```

**After mapping template**:
```json
{
    "myKey": "myValue",
    "renamedKey": "hello world"
}
```

## Use Cases for Mapping Templates

1. **Data Transformation**: Rename keys, restructure JSON
2. **Adding Static Data**: Include constant values in every response
3. **Integration Request**: Transform incoming API requests before Lambda
4. **Integration Response**: Transform Lambda response before API output
5. **Legacy System Integration**: Adapt between different data formats

## Important Notes

- Mapping templates are available for certain integration types
- Available on both Integration Request and Integration Response
- The syntax can be complex, but for the exam, just know they exist
- Useful for making different systems work together without changing code

## Best Practices

1. Use proxy integration for simple pass-through scenarios
2. Use mapping templates when you need data transformation
3. Test mapping templates thoroughly in the API Gateway console
4. Document your template logic for team members

## Exam Tips

- **Remember**: Mapping templates allow input/output transformation
- You don't need to memorize the exact syntax for AWS exams
- Focus on understanding WHEN to use mapping templates
- Know the difference between proxy and non-proxy integration

## Summary

Mapping templates in API Gateway provide powerful transformation capabilities:
- Transform Lambda responses without changing function code
- Add or remove data fields dynamically
- Integrate with legacy systems requiring specific formats
- Available for Integration Request and Response configurations

---
**Date Created**: March 15, 2026
**Topic**: AWS API Gateway, Lambda Integration, Mapping Templates
