# AWS API Gateway - Usage Plans and API Keys

## Overview

Usage Plans and API Keys in AWS API Gateway allow you to monetize and control access to your APIs. These features enable you to manage who can access your API, how much they can use it, and how fast they can make requests.

## Key Concepts

### Usage Plans

A usage plan defines:
- **Who** can access one or more API stages and methods
- **How much** they can access the API (quotas)
- **How fast** they can access the API (throttling)
- **Which API keys** are linked to identify and meter client access

### Throttling Limits

- Controls how fast users can target your API
- Applied at the API key level
- Helps prevent API abuse and manage load

### Quota Limits

- Overall number of requests allowed over a period
- Example: Limit to 10,000 requests per month
- Can be used to implement tiered pricing models

### API Keys

- String values distributed to customers
- Allow customers to securely authenticate their requests
- Used in conjunction with usage plans to control access
- Must be supplied in the `x-api-key` header for API requests

## Implementation Steps

Follow these steps in order to configure usage plans and API keys:

1. **Create APIs**
   - Create one or more APIs in API Gateway

2. **Configure Methods**
   - Configure the methods that will require an API key
   - Mark specific endpoints as requiring authentication

3. **Deploy APIs**
   - Deploy the APIs to your stages (dev, staging, production, etc.)

4. **Generate/Import API Keys**
   - Generate or import API keys to distribute to application developers/customers

5. **Create Usage Plan**
   - Set desired throttle limits
   - Set quota limits
   - Define access policies

6. **Associate Resources** ⚠️ **Critical Step**
   - Associate API stages with the usage plan
   - Associate API keys with the usage plan
   - **If you forget this step, nothing will work!**

## API Request Requirements

Callers must supply the API key in their requests:
```
x-api-key: <your-api-key-value>
```

## Benefits

- **Monetization**: Charge customers for API usage
- **Access Control**: Manage who can use your API
- **Rate Limiting**: Prevent abuse and manage server load
- **Usage Monitoring**: Track customer API consumption
- **Flexible Pricing**: Implement tiered pricing models

## Important Notes

- Throttling limits are applied at the API key level
- Quota limits represent the overall number of requests
- The association step (step 6) is critical - forgetting it will cause the system to fail
- API keys must be securely distributed to customers
