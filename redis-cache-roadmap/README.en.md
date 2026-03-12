# Redis Cache Roadmap (Zero → Hero)

This roadmap is a practical, hands-on path to learn Redis specifically as a **cache** (and the Redis features you’ll need to run caches reliably in production).

## How to use this roadmap

- Do lessons in order.
- For each lesson: read the concepts, run the commands, then complete the checklist.
- Keep a simple notes file with: what you tried, what broke, and what you fixed.

## Prerequisites

- Basic CLI comfort
- Basic networking concepts (IP/port)
- Optional: a language/runtime you use (Node.js / Python / Java / Go). The roadmap stays language-neutral.

## Environment setup (recommended)

- Redis 7.x locally (native install, Docker, or WSL)
- `redis-cli`

## Lessons

1. [Lesson 01 — Redis fundamentals](lessons/en/01-redis-fundamentals.md)
2. [Lesson 02 — Data structures for caching](lessons/en/02-data-structures.md)
3. [Lesson 03 — TTL, eviction, and memory](lessons/en/03-ttl-eviction-memory.md)
4. [Lesson 04 — Persistence basics (RDB/AOF)](lessons/en/04-persistence.md)
5. [Lesson 05 — Pub/Sub and Streams](lessons/en/05-pubsub-streams.md)
6. [Lesson 06 — Transactions, pipelines, and Lua](lessons/en/06-tx-pipeline-lua.md)
7. [Lesson 07 — Core caching patterns](lessons/en/07-caching-patterns.md)
8. [Lesson 08 — Locks and rate limiting](lessons/en/08-locks-rate-limiting.md)
9. [Lesson 09 — Replication and Sentinel](lessons/en/09-replication-sentinel.md)
10. [Lesson 10 — Redis Cluster (sharding)](lessons/en/10-redis-cluster.md)
11. [Lesson 11 — Security and operations](lessons/en/11-security-ops.md)
12. [Lesson 12 — Performance troubleshooting](lessons/en/12-performance-troubleshooting.md)
13. [Lesson 13 — Capstone: build a cache layer](lessons/en/13-capstone-cache-layer.md)

## Suggested weekly pacing (adjust as needed)

- Week 1: Lessons 01–03
- Week 2: Lessons 04–06
- Week 3: Lessons 07–10
- Week 4: Lessons 11–13 (capstone)

## Success criteria (what “hero” looks like)

- You can choose the right Redis structure for a use case and explain tradeoffs.
- You can set TTLs intentionally, avoid stampedes, and handle cache invalidation.
- You can operate Redis safely (monitoring, backups, failover basics).
- You can troubleshoot slow commands, memory pressure, and hot keys.
