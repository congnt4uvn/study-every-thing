# Lesson 04 — Persistence basics (RDB/AOF)

## Goal

Understand how Redis can persist data and why caches often still care about persistence (warm restart, lower DB load, faster recovery).

## Key concepts

- RDB: point-in-time snapshots.
- AOF: append-only log of write commands.
- Many deployments use AOF or a hybrid approach; exact defaults vary by distro and config.
- Persistence is about restart behavior, not a replacement for HA.

## Hands-on

### Inspect config

- `CONFIG GET save`
- `CONFIG GET appendonly`
- `CONFIG GET appendfsync`

### Trigger an RDB snapshot

- `SAVE` (blocking; learning only)
- `BGSAVE` (background)

### AOF basics

If AOF is enabled in your environment:

- `INFO persistence`
- `BGREWRITEAOF` (compaction)

## Practical caching guidance

- If your cache can be rebuilt cheaply, persistence is optional.
- If rebuilding is expensive (e.g., many derived keys), persistence can speed recovery.
- If you persist cache data, be extra careful about data freshness and invalidation on deploys.

## Checklist

- You can describe RDB vs AOF tradeoffs.
- You know how to find persistence status using `INFO persistence`.

## Next

Messaging primitives: Pub/Sub and Streams.
