# AWS API Gateway Caching

## Overview

Caching in API Gateway reduces the number of calls made to the backend by storing responses and serving them directly from the cache when available.

## How It Works

1. **Client Request Flow:**
   - Client sends request to API Gateway
   - API Gateway checks the cache first
   - If **cache hit**: Returns cached result immediately
   - If **cache miss**: Forwards request to backend and caches the response

2. **Purpose:**
   - Reduce pressure on backend systems
   - Improve response times
   - Lower costs by reducing backend invocations

## Cache Configuration

### Time to Live (TTL)
- **Default:** 300 seconds (5 minutes)
- **Minimum:** 0 seconds (no caching)
- **Maximum:** 3,600 seconds (1 hour)

### Cache Size
- **Range:** 0.5 GB to 237 GB
- **Note:** Cache is expensive - recommended for production environments only

### Stage Level Configuration
- Cache is defined per stage
- Each stage has its own cache settings
- Cache settings can be overridden at the method level

### Security
- Cache can be encrypted
- IAM authorization can be required for cache invalidation

## Cache Invalidation

### Manual Invalidation
- Can invalidate entire cache immediately from AWS Console UI

### Client-Side Invalidation
- Clients can invalidate cache using header: `Cache-Control: max-age=0`
- **Requires:** Proper IAM authorization
- **Without IAM policy:** Any client can invalidate the cache (security risk!)

### Per-Key Invalidation
- Specific cache entries can be invalidated based on keys
- Authorization options:
  - **Require authorization:** Recommended for security
  - **Ignore unauthorized requests:** Ignores cache control headers
  - **Fail with 403:** Returns forbidden error
  - **Add warning:** Allows request but adds warning response

## IAM Policy Example

To allow a client to invalidate cache on a specific resource:

```json
{
  "Effect": "Allow",
  "Action": "execute-api:InvalidateCache",
  "Resource": "arn:aws:execute-api:region:account-id:api-id/stage-name/*/resource-path"
}
```

## Best Practices

1. **Use in Production:** Cache is expensive, only enable for production or pre-production environments
2. **Require Authorization:** Always require IAM authorization for cache invalidation to prevent abuse
3. **Set Appropriate TTL:** Balance between freshness and performance based on your data update frequency
4. **Method-Level Customization:** Override cache settings for specific methods that need different behavior
5. **Monitor Cache Performance:** Track cache hit rates to ensure effective caching strategy

## Key Takeaways

- Caching significantly reduces backend load
- Configuration is flexible at both stage and method levels
- Security considerations are critical for cache invalidation
- Cost-effective only in high-traffic production environments
- Proper IAM policies prevent unauthorized cache manipulation
