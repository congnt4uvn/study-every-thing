# Lesson 09 — Replication and Sentinel

## Goal

Understand Redis replication for read scaling and how Sentinel provides failover coordination.

## Key concepts

- Replication creates replicas of a primary node.
- Reads can be served from replicas (with consistency caveats).
- Sentinel monitors nodes and can promote a replica to primary on failure.

## What to learn (conceptual)

- Replication is asynchronous → you can read stale data from replicas.
- For caches, stale reads may be acceptable; for locks/coordination, be careful.
- Failover changes which node is primary; clients must handle reconnect/redirect.

## Hands-on (optional)

If you can run multiple Redis instances locally:

- Configure one as primary and one as replica.
- Run `INFO replication` on both.

## Checklist

- You can describe primary/replica roles.
- You can state the consistency risk of reading from replicas.

## Next

Move from HA to horizontal scaling: Redis Cluster.
