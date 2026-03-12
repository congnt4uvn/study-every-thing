# Lesson 02 — Data structures for caching

## Goal

Use Redis structures to model cached data efficiently and avoid anti-patterns like huge JSON blobs when you need partial updates.

## Key concepts

- Redis supports multiple data types; choosing the right one often reduces latency and memory.
- The “right” structure depends on:
  - access pattern (whole object vs partial fields)
  - update pattern (single field updates vs rewrite)
  - ordering needs (ranking, recent items)

## Hands-on (core structures)

### Strings

- Use for simple values and whole-object cache entries.
- Commands:
  - `SET cache:user:1 "{...json...}"`
  - `GET cache:user:1`
  - `MSET k1 v1 k2 v2`
  - `MGET k1 k2`

### Hashes

- Great for objects with many fields.
- Commands:
  - `HSET user:1 name "Ada" age "37"`
  - `HGET user:1 name`
  - `HGETALL user:1`
  - `HINCRBY user:1 visits 1`

### Lists

- Simple ordered list (often used for queues, but Streams is better for durable messaging).
- Commands:
  - `LPUSH recent:log "a" "b" "c"`
  - `LRANGE recent:log 0 10`
  - `LTRIM recent:log 0 99` (keep last 100)

### Sets

- Unordered unique items.
- Commands:
  - `SADD user:1:tags "pro" "beta"`
  - `SISMEMBER user:1:tags "beta"`
  - `SMEMBERS user:1:tags`

### Sorted Sets (ZSET)

- Ranking, leaderboards, time-based ordering.
- Commands:
  - `ZADD leaderboard 100 "alice" 200 "bob"`
  - `ZREVRANGE leaderboard 0 9 WITHSCORES`
  - `ZINCRBY leaderboard 5 "alice"`

## For caching, remember

- Small keys, predictable patterns: `cache:<domain>:<id>`.
- Avoid “big keys”: very large values or very large collections.
- Consider splitting large entities (hash fields) if partial invalidation is common.

## Checklist

- You can explain when to use String vs Hash for a cached object.
- You can model “top N” with a ZSET.
- You can keep a bounded “recent items” list with `LTRIM`.

## Next

Learn TTL, expiration, and memory eviction (core cache mechanics).
