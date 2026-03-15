# AWS API Gateway - OpenAPI Integration

## Overview
This document covers how to work with OpenAPI definitions in AWS API Gateway, including importing and exporting API configurations.

## Importing an OpenAPI Definition

### Steps to Import:
1. **Create a new API**
   - Choose REST API type
   - Click on "Import" option

2. **Provide API Definition File**
   - You need an API definition file in OpenAPI format
   - Example: Click on "Example API" to see a sample OpenAPI definition
   - This defines how an API should be built on API Gateway

3. **Import and Create**
   - Import the example API file
   - Click "Create API"
   - Result: A new API (e.g., "Pet Store") is created with proper resources

### Benefits:
- All resources are automatically created from the OpenAPI definition file
- Very handy for quick API setup
- Ensures consistency across API deployments

## Exporting an API as OpenAPI

### Steps to Export:
1. **Navigate to API**
   - Go to your API in API Gateway
   - Select a stage (e.g., "prod" stage)

2. **Export Options**
   - Click on "Stage Actions"
   - Select "Export"
   
3. **Configure Export Settings**
   - **Format**: Choose between Swagger or OpenAPI 3
   - **File Type**: JSON or YAML
   - **Extensions**: Include API Gateway and Postman extensions (optional)

4. **Generate File**
   - Export generates the file
   - This file can be imported elsewhere if needed

## SDK Generation

### Automatic SDK Creation:
Once you're using the OpenAPI format, you can automatically generate SDKs for various programming languages:

- **Android**
- **JavaScript**
- **iOS**
- **Java**
- **Ruby**

### Benefits:
- Applications can easily interact with your API through the generated SDK
- Reduces development time
- Ensures type safety and proper API usage

## Key Takeaways

The power of OpenAPI definitions in API Gateway includes:
- Easy import/export of API configurations
- Automatic SDK generation for multiple platforms
- Standardized API documentation
- Simplified API management and deployment

---

**AWS Service**: API Gateway  
**Topic**: OpenAPI Integration  
**Date**: 2026
