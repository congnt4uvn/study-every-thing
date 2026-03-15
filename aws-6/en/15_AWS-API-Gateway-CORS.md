# AWS API Gateway - CORS (Cross-Origin Resource Sharing)

## Overview
API Gateway supports browser security features for cross-origin resource sharing (CORS). CORS must be enabled if you want to receive API calls from another domain.

## Key Concepts

### What is CORS?
CORS (Cross-Origin Resource Sharing) is a security feature implemented by web browsers to control how web pages from one domain can request resources from another domain.

### Why CORS is Needed in API Gateway
When your web application hosted on one domain (e.g., `www.example.com`) needs to make API calls to API Gateway hosted on a different domain (e.g., `api.example.com`), CORS must be enabled to allow these cross-origin requests.

## How CORS Works with API Gateway

### Pre-flight Request
1. **OPTIONS Method**: API Gateway creates an OPTIONS pre-flight request
2. **Security Check**: The web browser sends this request before the actual API call as a security measure
3. **Response**: API Gateway responds with allowed origins and methods

### Required CORS Headers
The OPTIONS pre-flight response must contain the following headers:
- `Access-Control-Allow-Methods` - Specifies which HTTP methods are allowed
- `Access-Control-Allow-Headers` - Specifies which headers can be used
- `Access-Control-Allow-Origins` - Specifies which origins are allowed to make requests

### Configuration
These CORS settings can be configured directly from the AWS Console.

## Practical Example

### Scenario
```
1. Web Browser → S3 Bucket (www.example.com)
   - Browser retrieves static website content
   
2. JavaScript (from S3) → API Gateway (api.example.com)
   - JavaScript needs to make API calls to different domain
   
3. Web Browser → API Gateway
   - Sends OPTIONS pre-flight request (security check)
   
4. API Gateway → Web Browser
   - Returns pre-flight response (if origin is allowed)
   
5. Web Browser ↔ API Gateway
   - If approved, browser and API Gateway can communicate
```

## Exam Tips

For AWS certification exams, remember:
- **CORS must be enabled** on API Gateway for cross-origin requests
- Pre-flight requests use the **OPTIONS** method
- CORS can be configured from the **AWS Console**
- Look for scenarios involving web applications making API calls to different domains

## Summary
- CORS is a browser security feature
- Required when API Gateway receives calls from different domains
- Uses OPTIONS pre-flight requests to verify permissions
- Configuration includes Allow-Methods, Allow-Headers, and Allow-Origins
- Essential for modern web applications with separated frontend and backend domains
