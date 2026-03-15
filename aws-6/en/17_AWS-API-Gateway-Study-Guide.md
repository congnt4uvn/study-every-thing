# AWS API Gateway - Study Guide

## Overview
This document covers the different types of APIs available in AWS API Gateway and their key differences.

## Types of APIs in API Gateway

### 1. REST API
The REST API is the most feature-rich option in API Gateway with comprehensive capabilities:

**Key Features:**
- Full data mapping capabilities
- Resource policies support
- Usage plans and API keys
- Multiple authorization methods
- Stage variables
- Request/response transformations
- Caching support
- Comprehensive monitoring and logging

**Authorization Options:**
- IAM roles and policies
- Amazon Cognito User Pools
- Lambda Authorizers (Custom Authorizers)
- Resource policies

**Use Cases:**
- Enterprise applications requiring advanced features
- Applications needing fine-grained access control
- Systems requiring usage plans and API quotas

### 2. HTTP API
HTTP API is a newer, simpler, and more cost-effective alternative to REST API:

**Key Features:**
- Low latency
- Cost-effective (much cheaper than REST API)
- AWS Lambda proxy
- HTTP proxy API
- Private integration
- Built-in CORS support
- Proxy-only (no data mapping)

**Authorization Options:**
- OIDC (OpenID Connect)
- OAuth 2.0

**Limitations:**
- No usage plans or API keys
- No resource policies
- Limited data transformation capabilities

**Use Cases:**
- Simple proxy APIs
- Cost-sensitive applications
- Modern authentication requirements (OAuth 2.0, OIDC)

### 3. WebSocket API
WebSocket API enables bidirectional communication between clients and servers:

**Key Features:**
- Real-time two-way communication
- Persistent connections
- Event-driven architecture

**Use Cases:**
- Chat applications
- Real-time dashboards
- Live notifications
- Gaming applications

## Key Differences: HTTP API vs REST API

| Feature | HTTP API | REST API |
|---------|----------|----------|
| **Cost** | Much cheaper | More expensive |
| **Data Mapping** | Not supported (proxy only) | Full support |
| **Authorization** | OIDC, OAuth 2.0 | IAM, Cognito, Lambda Auth, Resource Policies |
| **Usage Plans/API Keys** | Not supported | Supported |
| **CORS** | Built-in support | Manual configuration |
| **Resource Policies** | Not supported | Supported |
| **Latency** | Lower | Standard |

## Exam Tips

1. **HTTP API is cheaper** than REST API - remember this key distinction
2. **REST API supports resource policies**, HTTP API does not
3. HTTP API is best for **simple proxy use cases** with modern authentication
4. REST API is best for **complex enterprise scenarios** requiring advanced features
5. WebSocket API is for **real-time, bidirectional communication**

## When to Choose Which API?

### Choose REST API when you need:
- Resource policies
- Usage plans and API keys
- Advanced data transformation
- Request/response validation
- Caching
- Full IAM integration

### Choose HTTP API when you need:
- Lower cost solution
- Simple proxy functionality
- OAuth 2.0 or OIDC authentication
- Built-in CORS
- Low latency requirements

### Choose WebSocket API when you need:
- Real-time bidirectional communication
- Persistent connections
- Event-driven interactions

---

**Note:** This study guide is based on AWS API Gateway features. Always refer to the latest AWS documentation for the most up-to-date information.
