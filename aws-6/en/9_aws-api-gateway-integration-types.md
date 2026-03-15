# AWS API Gateway Integration Types

## Overview
This document covers the different ways to integrate API Gateway with backend services. Understanding these integration types is crucial for designing and implementing AWS API solutions.

## 1. MOCK Integration

**Purpose:** Returns a response without sending a request to the backend.

**Use Cases:**
- Development and testing
- API Gateway configuration without backend setup
- Not suitable for production environments

**Key Features:**
- No backend required
- Useful for prototyping and development
- Returns predefined responses

---

## 2. HTTP/AWS Lambda Integration (Non-Proxy)

**Purpose:** Forward requests to Lambda or other AWS services with the ability to modify requests and responses.

**Configuration Requirements:**
- Integration request setup
- Integration response setup
- Data mapping using mapping templates

**Capabilities:**
- Modify request before sending to backend
- Transform response before returning to client
- Use mapping templates for data transformation

**Example Use Case:**
Create a REST API that maps to an SQS Queue by:
- Changing request format
- Renaming parameters
- Reordering data structures
- Ensuring SQS can understand the API call

**Key Point:** API Gateway has full control to modify both request and response.

---

## 3. AWS Proxy (Lambda Proxy)

**Purpose:** Direct integration where requests pass through to Lambda without modification.

**Characteristics:**
- Request from client becomes direct input to Lambda
- No request/response modification possible
- No mapping templates allowed
- Cannot modify headers or query string parameters
- Function handles all logic for request and response

**Request Structure:**
Lambda receives a JSON document containing:
- Resource information
- Path
- HTTP method
- Headers
- Query string parameters
- Stage variables
- Body
- Other metadata

**Response Structure:**
Lambda must return:
```json
{
  "statusCode": 200,
  "headers": {...},
  "body": "..."
}
```

**Key Point:** All work is on the backend; API Gateway only proxies requests through.

---

## 4. HTTP Proxy

**Purpose:** Proxy requests directly to HTTP endpoints without modification.

**Characteristics:**
- No mapping templates
- Request passed directly to backend
- Response passed directly back to client
- Can add HTTP headers (e.g., API keys)

**Example Scenario:**
1. Client makes HTTP request to API Gateway
2. API Gateway proxies request to backend (e.g., Application Load Balancer)
3. Optional: Add HTTP headers like API key
4. Backend receives request with added headers
5. Response proxied back to client

**Security Benefit:** Can add authentication headers that clients don't need to know about.

---

## Mapping Templates

**Availability:** Only for HTTP/AWS Lambda integration (non-proxy methods)

**Functions:**
- Rename or modify query string parameters
- Modify body content
- Add or modify headers
- Transform request and response data

**Technology:** Uses Velocity Template Language (VTL)

---

## Comparison Summary

| Integration Type | Modify Request | Modify Response | Mapping Templates | Use Case |
|-----------------|----------------|-----------------|-------------------|----------|
| MOCK | N/A | ✓ | ✓ | Development/Testing |
| HTTP/AWS Lambda | ✓ | ✓ | ✓ | Full control over transformation |
| AWS Proxy | ✗ | ✗ | ✗ | Simple pass-through to Lambda |
| HTTP Proxy | ✗ | ✗ | ✗ | Direct HTTP backend integration |

---

## Study Tips

1. **MOCK** is for testing only
2. **Proxy integrations** (AWS Proxy & HTTP Proxy) don't allow transformations
3. **Non-proxy integrations** (HTTP/AWS Lambda) allow full control via mapping templates
4. **VTL** is the language used for mapping templates
5. Choose integration type based on whether you need request/response transformation

---

## Key Takeaways

- Proxy methods provide simplicity and direct pass-through
- Non-proxy methods provide flexibility with transformations
- Mapping templates enable powerful data transformations
- Security features like API keys can be added transparently
- Lambda Proxy puts all logic in the Lambda function
