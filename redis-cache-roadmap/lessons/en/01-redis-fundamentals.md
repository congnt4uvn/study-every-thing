# Lesson 01 — Redis fundamentals

## Goal

Understand what Redis is, when it’s a good cache, and how to interact with it using `redis-cli`.

## Key concepts

- Redis is an in-memory data store. For caching, you’re mainly using:
  - very fast reads/writes
  - TTL (time-to-live) and expiration
  - simple atomic operations
- Redis is single-threaded for most command execution (with I/O threads and background work). It’s fast because commands are short and memory-local.
- “Cache” means the data can be rebuilt from a source of truth (DB, API, computed results).

## Install options (pick one)

1. Docker: run a Redis container (good for learning).
2. Native install: fine for learning.
3. WSL on Windows: also fine.

This roadmap stays CLI-focused so you can use any method.

## Hands-on

Open a shell and run:

1) Connect:

- `redis-cli -h 127.0.0.1 -p 6379`

2) Check health:

- `PING` → should return `PONG`
- `INFO server` → learn version and run-id

3) Write / read / delete:

- `SET hello "world"`
- `GET hello`
- `DEL hello`

4) Observe keyspace basics:

- `SET user:1:name "Ada"`
- `KEYS user:*` (learning only; avoid in production)
- `SCAN 0 MATCH user:* COUNT 100` (preferred pattern)

## Checklist

- You can connect with `redis-cli` and run `PING`.
- You understand why `KEYS` is dangerous at scale.
- You can use `SCAN` for iterative key discovery.

## Common pitfalls

- Using Redis as a primary database without understanding persistence/HA.
- Assuming “in-memory” means “no data loss”. You still need backups/replication if you care.

## Next

Move to data structures; caching isn’t only `SET/GET`.
