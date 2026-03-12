# Lesson 05 — Consumers: groups, offsets, delivery semantics

## Goals
- Understand consumer groups and parallelism
- Understand offsets and commits
- Understand at-most-once vs at-least-once vs effectively-once processing

## Consumer groups
A **consumer group** is a set of consumers sharing work for a topic.

Rules of thumb:
- Max parallelism per topic = number of partitions
- One partition is consumed by at most one consumer in the same group at a time

## Offsets
An **offset** is the position of a record within a partition.

Consumers track progress by committing offsets.

Two common commit styles:
- Auto-commit (simpler, riskier for correctness)
- Manual commit after processing (more control)

## Delivery semantics (practical)
### At-most-once
Commit before processing.
- Fast
- Can lose messages on failure

### At-least-once
Process then commit.
- No loss (assuming retries)
- Can produce duplicates (you must handle idempotency downstream)

### Effectively-once (application-level)
With idempotent writes / dedupe keys / transactional patterns, you can get “effectively once” results.

## Rebalancing
When group membership changes (consumer joins/leaves), Kafka reassigns partitions.

Symptoms:
- Temporary pauses
- Duplicate processing if you don’t handle commits correctly

## Hands-on lab
1. Consume from beginning:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-consumer --bootstrap-server kafka:29092 --topic demo.orders --from-beginning --group demo-group"
```

2. In another terminal, produce a few more messages.

3. Stop the consumer and start it again with the same group.
   - Observe: it continues from the committed offsets.

## Checklist
- I can explain consumer groups and partition assignment
- I understand offsets and commits
- I can choose at-most-once vs at-least-once intentionally

## Common pitfalls
- Treating duplicates as “impossible” (they happen)
- Assuming rebalances are rare (in dynamic environments they’re common)
