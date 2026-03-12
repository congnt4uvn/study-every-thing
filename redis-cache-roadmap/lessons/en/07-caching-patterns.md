# Lesson 07 — Core caching patterns

## Goal

Learn the main caching patterns and how to avoid cache stampedes and invalidation bugs.

## Key concepts

### Cache-aside (lazy loading)

Flow:

1. Read from cache.
2. If miss: read from DB/source.
3. Write to cache with TTL.
4. Return.

Pros: simple, widely used.
Cons: stampede risk on hot keys; stale reads around invalidation.

### Write-through / write-behind

- Write-through: app writes cache and DB together.
- Write-behind: app writes cache, async flush to DB (riskier).

### Invalidation

Common strategies:

- TTL-only (accept eventual consistency)
- Explicit delete on write (`DEL cache:key`)
- Versioned keys (`cache:user:1:v42`), where version increments on update

### Stampede (dogpile) prevention techniques

- Add random TTL jitter: e.g., `ttl = base + rand(0..jitter)`
- Single-flight (mutex): only one request recomputes a missing key
- Soft TTL: serve stale while refreshing

## Hands-on exercises (Redis-only building blocks)

1) TTL jitter:

- `SET cache:demo "x" EX 60`
- Repeat with random TTLs and observe expiration distribution.

2) Simple mutex lock idea (see next lesson for safer lock patterns):

- `SET lock:cache:demo 1 NX EX 10`

## Checklist

- You can diagram cache-aside.
- You can list at least 3 stampede mitigations.
- You can explain at least 2 invalidation strategies.

## Next

Locks and rate limiting are common “cache-adjacent” problems.
