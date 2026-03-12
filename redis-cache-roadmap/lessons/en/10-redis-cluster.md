# Lesson 10 — Redis Cluster (sharding)

## Goal

Understand what Redis Cluster is, when you need it, and what changes for clients and key design.

## Key concepts

- Cluster shards data across nodes using hash slots.
- Some multi-key operations require keys to be in the same hash slot.
- Hash tags `{...}` in keys can force related keys into the same slot.

## Practical cache guidance

- Prefer single-key operations for cluster-friendly designs.
- If you must use multi-key ops (e.g., `MGET`), design keys with hash tags.

Example:

- `cache:user:{1}:profile`
- `cache:user:{1}:settings`

Both share the same hash tag `{1}`.

## Checklist

- You know why multi-key commands can fail in cluster.
- You can explain what hash tags are used for.

## Next

Security and operations fundamentals.
