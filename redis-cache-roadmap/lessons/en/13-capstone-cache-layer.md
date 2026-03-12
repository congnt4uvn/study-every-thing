# Lesson 13 — Capstone: build a cache layer

## Goal

Design and implement a cache layer (in your preferred language) that is safe under load and operationally observable.

## Requirements (keep it small)

Build a cache wrapper for reading “user profiles” from a slow source.

Your cache layer must:

- Use cache-aside
- Use TTL with jitter
- Prevent stampede on hot keys (single-flight/mutex)
- Emit basic metrics/logs (hit/miss, latency)
- Support manual invalidation

## Suggested key design

- `cache:user:<id>:profile`

## Recommended algorithm (pseudo)

1) `GET key`
2) If hit → return
3) If miss:
   - Try acquire lock `SET lock:key token NX EX lockTTL`
   - If lock acquired:
     - Read from source
     - `SET key value EX ttl`
     - Release lock safely (token check)
     - Return value
   - If lock not acquired:
     - Wait briefly + retry cache a few times
     - If still miss → optionally fall back to source (depends on SLO)

## What to measure

- Cache hit ratio over time
- P95/P99 latency of `GET` and your overall endpoint
- Error rate (timeouts, command errors)
- `evicted_keys` and memory usage

## Stretch goals (optional)

- Use soft TTL with background refresh
- Add versioned keys to simplify invalidation
- Add a Stream to record invalidation events

## Done definition

- You can load test your endpoint and the cache layer stays stable.
- You can explain how you avoided stampede.
- You can handle Redis down (degrade gracefully).
