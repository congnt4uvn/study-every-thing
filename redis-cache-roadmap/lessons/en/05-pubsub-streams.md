# Lesson 05 — Pub/Sub and Streams

## Goal

Understand Redis Pub/Sub for ephemeral notifications and Redis Streams for durable event processing.

## Key concepts

- Pub/Sub messages are not stored; if a subscriber is offline, it misses messages.
- Streams store events and support consumer groups (more reliable for processing).
- For caching systems, these can help with:
  - cache invalidation broadcasts
  - async refresh pipelines

## Hands-on

### Pub/Sub

Open two terminals.

Terminal A:

- `redis-cli`
- `SUBSCRIBE cache:invalidate`

Terminal B:

- `redis-cli`
- `PUBLISH cache:invalidate "user:1"`

### Streams

- `XADD cache-events * type invalidate key user:1`
- `XRANGE cache-events - + COUNT 10`

Consumer group example:

- `XGROUP CREATE cache-events cache-workers $ MKSTREAM`
- `XREADGROUP GROUP cache-workers worker-1 COUNT 10 STREAMS cache-events >`

## Checklist

- You can explain why Pub/Sub is not durable.
- You can add/read Stream entries.
- You understand the high-level purpose of consumer groups.

## Next

Learn atomicity tools: transactions, pipelining, and Lua.
