# Lesson 08 — Locks and rate limiting

## Goal

Implement basic distributed coordination patterns using Redis primitives: locks and rate limiting.

## Key concepts

### Distributed locks

- A basic Redis lock often uses `SET key value NX EX seconds`.
- The lock value should be unique (random token) so you can safely release only your own lock.
- Releasing requires a check-and-delete, typically via Lua.

### Rate limiting

Common approaches:

- Fixed window counter (simple, bursty)
- Sliding window (more accurate)
- Token bucket / leaky bucket (good smoothing)

## Hands-on

### Lock acquire

- `SET lock:job:1 "token-123" NX EX 10`

### Safe lock release (Lua)

- `EVAL "if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end" 1 lock:job:1 token-123`

### Fixed-window rate limit

For user `u1` and 60-second window:

- `INCR rl:u1`
- `EXPIRE rl:u1 60` (set on first request; app logic needed)

## Checklist

- You understand why lock release must verify the token.
- You can explain pros/cons of fixed window limiting.

## Next

High availability basics: replication and Sentinel.
