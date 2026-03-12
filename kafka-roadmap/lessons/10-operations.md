# Lesson 10 — Operations: sizing, configs, rebalancing, upgrades

## Goals
- Understand the operational surface area of Kafka
- Learn the most important configuration categories
- Understand rebalancing and upgrade planning at a high level

## Sizing (high level)
Capacity planning depends on:
- Throughput (MB/s in and out)
- Number of partitions and replication factor
- Retention (time/size)
- Consumer lag expectations

A practical approach:
- Start with realistic peak throughput estimates
- Choose a partition count that supports parallelism
- Validate disk and network budgets

## Critical configuration areas
Broker-side (examples):
- Log retention and segment settings
- Replication and ISR settings
- Network threads and IO threads

Topic-side:
- Partitions and replication factor
- Retention and cleanup policy

Client-side:
- Producer acks/idempotence, batching
- Consumer max poll settings, commit strategy

## Rebalancing
Rebalances happen when:
- Consumers join/leave
- Partitions change
- Group coordinator events occur

Operational guidance:
- Keep consumers stable (avoid unnecessary restarts)
- Use cooperative rebalancing where supported by clients

## Upgrades
Plan upgrades like a production system:
- Read version compatibility notes
- Upgrade in stages
- Monitor controller and replication health

## Hands-on lab (local)
In your local lab, practice safe restarts:
1. Start consumer group `demo-group`.
2. Restart the consumer and observe continuity.
3. Restart Kafka container and observe recovery.

## Checklist
- I can list the main levers that drive Kafka sizing
- I understand why rebalances happen and why they matter
- I can describe a cautious upgrade mindset

## Common pitfalls
- Treating Kafka as “just run it” without monitoring, backups, and upgrade plans
- Over-partitioning without measuring impact
