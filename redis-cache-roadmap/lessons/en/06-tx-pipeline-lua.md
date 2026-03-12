# Lesson 06 — Transactions, pipelines, and Lua

## Goal

Use Redis atomic operations correctly, reduce round-trips with pipelining, and understand when Lua scripting is a good idea.

## Key concepts

- Most single Redis commands are atomic.
- `MULTI/EXEC` groups commands; it’s not the same as SQL transactions (no rollback for runtime errors).
- Pipelining reduces network latency by sending multiple commands without waiting.
- Lua scripts run atomically on the Redis server (within the script execution).

## Hands-on

### Transaction (MULTI/EXEC)

- `MULTI`
- `INCR tx:counter`
- `INCR tx:counter`
- `EXEC`

### Optimistic locking with WATCH

- `WATCH user:1`
- `MULTI`
- `HSET user:1 name "Grace"`
- `EXEC` (fails if watched keys changed)

### Pipelining

From a shell (not interactive) you can pipeline like:

- `echo "PING\nPING\nPING\n" | redis-cli --pipe`

### Lua script

Example: get-and-touch TTL (read value and extend TTL in one atomic operation)

- `EVAL "local v = redis.call('GET', KEYS[1]); if v then redis.call('EXPIRE', KEYS[1], ARGV[1]); end; return v" 1 cache:user:1 60`

## Checklist

- You can explain when `WATCH` helps.
- You can pipeline to reduce RTT.
- You can run a small Lua script for an atomic read-modify-write.

## Next

Now that you know primitives, learn caching patterns that avoid production incidents.
