# AWS API Gateway - Logging and Monitoring

## Overview
This document covers API Gateway logging, tracing, monitoring metrics, and throttling mechanisms.

---

## 1. CloudWatch Logs Integration

### Features
- **Purpose**: Captures request and response body information passing through API Gateway
- **Configuration Level**: Enabled at the Stage Level
- **Log Levels**: 
  - ERROR (minimal information)
  - INFO (moderate information)
  - DEBUG (most detailed information)
- **Flexibility**: Can override settings on a per-API basis

### Request Flow
```
User → API Gateway → CloudWatch Logs
              ↓
          Backend
              ↓
     API Gateway → CloudWatch Logs
              ↓
           User
```

### ⚠️ Security Warning
Enabling CloudWatch Logs may capture sensitive information. Use with caution in production environments.

---

## 2. X-Ray Tracing

### Purpose
- Provides distributed tracing information for requests through API Gateway
- **Best Practice**: Enable X-Ray for both API Gateway and Lambda to get the complete picture

### Benefits
- End-to-end visibility
- Performance bottleneck identification
- Request flow analysis

---

## 3. CloudWatch Metrics

### Configuration
- Monitored per stage
- Can enable detailed metrics

### Key Metrics

#### Cache Metrics
- **CacheHitCount**: Number of successful cache retrievals
  - High count = Efficient cache
- **CacheMissCount**: Number of times cache didn't have the data
  - High count = Inefficient cache

#### Request Metrics
- **Count**: Total number of API requests in a given period

#### Performance Metrics
- **IntegrationLatency**: Time taken for API Gateway to:
  - Relay request to backend
  - Receive response from backend
  - Indicates backend processing time

- **Latency**: Total time from when API Gateway:
  - Receives request from client
  - Returns response to client
  - Includes: IntegrationLatency + API Gateway processing time
  
**Latency Components**:
- Authorization and authentication checks
- Cache lookups
- Mapping templates
- Other API Gateway operations

**Important**: Latency ≥ IntegrationLatency

#### ⏱️ Timeout Limit
**Maximum request time: 29 seconds**
- If Latency or IntegrationLatency exceeds 29 seconds → Timeout occurs

#### Error Metrics
- **4XXError**: Client-side errors (invalid requests from clients)
- **5XXError**: Server-side errors (backend failures)

---

## 4. API Gateway Throttling

### Account Limits
- **Default Throttle Rate**: 10,000 requests per second (across all APIs)
- **Limit Type**: Soft limit (can be increased upon request to AWS)

### ⚠️ Cross-API Impact
If one API experiences heavy traffic, other APIs in the same account can also be throttled.

### Throttling Error Response
- **Error Code**: `429 Too Many Requests`
- **Error Type**: Client-side error
- **Retry Strategy**: Use exponential backoff

### Throttling Optimization Strategies

#### 1. Stage Limits
Set throttle limits at the stage level to prevent a single stage from consuming all quota.

#### 2. Method Limits
Configure limits per API method to protect against targeted attacks.

#### 3. Usage Plans
Define plans to throttle per customer, ensuring fair resource distribution.

### Comparison with Lambda
Similar to Lambda Concurrency limits:
- Overloaded API without limits can throttle other APIs
- Proper limits prevent cascading failures

---

## Best Practices Summary

1. ✅ Enable CloudWatch Logs for debugging (be mindful of sensitive data)
2. ✅ Use X-Ray for distributed tracing across services
3. ✅ Monitor Latency vs IntegrationLatency to identify bottlenecks
4. ✅ Set appropriate stage and method limits
5. ✅ Implement usage plans for customer-based throttling
6. ✅ Use exponential backoff for 429 errors
7. ✅ Keep requests under 29 seconds to avoid timeouts

---

## Exam Key Points

- **CloudWatch Logs**: Stage level, with ERROR/INFO/DEBUG levels
- **X-Ray**: Full tracing with Lambda integration
- **Latency** > **IntegrationLatency** (always)
- **29-second timeout** limit
- **10,000 req/s** default throttle (soft limit)
- **429 error** = Too Many Requests (retriable with exponential backoff)
- **4XX** = Client errors, **5XX** = Server errors
- **CacheHitCount** vs **CacheMissCount** indicates cache efficiency
