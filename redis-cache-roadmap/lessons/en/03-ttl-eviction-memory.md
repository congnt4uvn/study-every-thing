# Lesson 03 — TTL, eviction, and memory

## Goal

Control cache lifetime (TTL), understand expiration semantics, and learn how Redis behaves under memory pressure.

## Key concepts

- TTL is per-key expiration; it’s the foundation of cache correctness.
- Expiration is not always immediate at the exact millisecond; Redis uses a mix of passive and active expiration.
- When memory is full and `maxmemory` is set, Redis uses an **eviction policy**.

## Hands-on

### Set keys with TTL

- `SET cache:page:home "..." EX 60` (seconds)
- `TTL cache:page:home`
- `PTTL cache:page:home` (milliseconds)

### Update TTL

- `EXPIRE cache:page:home 120`
- `PERSIST cache:page:home` (remove TTL)

### Cache “soft TTL” idea (application-level)

Redis TTL is “hard expiry”. Many production caches add a *soft expiry* inside the value (e.g., JSON field `staleAt`) so the app can serve slightly stale data while refreshing in background.

### Explore memory info

- `INFO memory`
- `MEMORY STATS`
- `MEMORY USAGE cache:page:home`

## Eviction overview

Common policies you’ll see:

- `noeviction`: writes fail when memory is full (dangerous for caches unless handled).
- `allkeys-lru`: evict least-recently-used keys across all keys.
- `allkeys-lfu`: evict least-frequently-used keys across all keys.
- `volatile-*`: only evict keys with TTL set.

For caches, `allkeys-lfu` is often a solid starting point, but it depends on your workload.

## Checklist

- You can set and inspect TTL.
- You understand that expiration is approximate.
- You can explain what eviction is and why policy matters.

## Next

Learn persistence (so you know what you are and aren’t getting from Redis).
