# Lesson 07 — Topic design: keys, partitioning, retention, compaction

## Goals
- Design topics and keys for ordering and scalability
- Understand retention policies and log compaction
- Know how partitions affect performance and consumer parallelism

## Naming and domain boundaries
Good topic naming helps you avoid chaos:
- Prefer domain-oriented names like `orders.events`, `payments.events`
- Avoid dumping unrelated events into a single “events” topic

## Keys and partitioning
Keys matter because they determine partitioning and ordering.

Guidance:
- If you need ordering per entity (e.g., per order), use a stable key (e.g., `orderId`).
- If you use random keys, you trade ordering for even load distribution.

## Retention
Kafka deletes old data based on retention configuration.

Common retention types:
- Time-based (e.g., keep 7 days)
- Size-based (keep until disk threshold)

Retention is not a backup strategy.

## Log compaction
Compaction keeps the latest value per key (roughly speaking).

Use cases:
- “Current state” topics (e.g., user profile latest state)
- CDC-like streams where you want last known value

Compaction is not:
- A guarantee every intermediate state remains

## Hands-on lab (create a compacted topic)
Create a compacted topic:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --create --topic demo.users.compacted --partitions 1 --replication-factor 1 --config cleanup.policy=compact"
```

Produce keyed messages:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-producer --bootstrap-server kafka:29092 --topic demo.users.compacted --property parse.key=true --property key.separator=:"
```

Type:
```text
u1:{"name":"Alice","tier":"free"}
u1:{"name":"Alice","tier":"pro"}
u2:{"name":"Bob","tier":"free"}
```

Consume and observe:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-consumer --bootstrap-server kafka:29092 --topic demo.users.compacted --from-beginning --property print.key=true --property key.separator= : "
```

Note: compaction happens asynchronously; you may not immediately see old values removed.

## Checklist
- I can choose a key strategy aligned with ordering needs
- I understand retention vs compaction and when to use each
- I can create topics with configs

## Common pitfalls
- Using too many topics/partitions without a governance strategy
- Misusing compaction as if it were a database
