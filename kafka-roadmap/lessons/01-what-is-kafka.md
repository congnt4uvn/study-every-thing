# Lesson 01 — What Kafka is + use cases + core guarantees

## Goals
- Explain what Kafka is in practical terms
- Recognize when Kafka is a good fit (and when it isn’t)
- Understand the basic guarantees you can (and can’t) rely on

## What Kafka is
Apache Kafka is a **distributed event streaming platform**.

In plain words:
- Producers write **records (events/messages)** into **topics**
- Kafka stores those records durably (for a configurable time)
- Consumers read records from topics, often as part of real-time pipelines

Kafka is commonly used for:
- Event-driven microservices
- Audit logs and event sourcing
- Data pipelines and CDC (change data capture)
- Stream processing (fraud detection, monitoring, enrichment)

## Kafka is not
- A traditional request/response message queue replacement for every job
- A database (it stores logs, but query capabilities are limited)
- A guarantee of “exactly once” by default (semantics depend on configuration and your processing)

## Core guarantees (practical)
What you can typically rely on:
- **Durable storage** (if configured and replicated)
- **Ordering within a partition**
- **Scalability** via partitioning

What depends on your configuration:
- Delivery semantics (at-most-once / at-least-once / effectively-once)
- How duplicates are handled
- How failures affect offsets and reprocessing

## Key vocabulary
- **Record**: key + value + headers + timestamp
- **Topic**: named stream of records
- **Partition**: ordered append-only log inside a topic
- **Offset**: position within a partition

## Hands-on (light)
If you already have Docker installed, confirm it works (you’ll set up Kafka in Lesson 03):

```powershell
docker version
docker compose version
```

## Checklist
- I can describe Kafka as a durable, partitioned log
- I know ordering is per-partition (not per-topic)
- I can name 3 real use cases where Kafka shines

## Common pitfalls
- Treating Kafka like a database table with arbitrary queries
- Assuming “exactly once” without understanding producer idempotence and transactional processing
