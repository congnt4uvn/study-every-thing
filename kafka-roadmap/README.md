# Apache Kafka Zero → Hero Roadmap

A practical, hands-on study plan to learn Kafka from fundamentals to production-minded usage.

## Who this is for
- Backend developers integrating event streaming into services
- Data engineers building pipelines and CDC workflows
- DevOps/SREs operating Kafka clusters

## How to use this roadmap
- Follow lessons in order.
- Each lesson contains:
  - **Goals** (what you’ll be able to do)
  - **Concepts** (what you should understand)
  - **Hands-on labs** (commands + expected outcomes)
  - **Checklist** (quick self-test)

## Prerequisites
- Basic terminal usage (PowerShell/Bash)
- Comfort with at least one programming language
- Docker Desktop installed (recommended for labs)

## Lab stack (recommended)
For consistent hands-on practice, lessons use a small Docker Compose stack:
- ZooKeeper + Kafka (single broker) for simplicity
- Kafdrop (web UI) to inspect topics/messages

You will create this stack in Lesson 03.

## Suggested schedule
- **Fast (1 week):** 1–2 lessons/day + capstone
- **Steady (2–3 weeks):** 3–5 lessons/week + repeat labs

## Lessons
1. [Lesson 01 — What Kafka is + use cases + core guarantees](lessons/01-what-is-kafka.md)
2. [Lesson 02 — Core architecture: brokers, topics, partitions, replication](lessons/02-architecture.md)
3. [Lesson 03 — Local lab: Docker Compose + Kafka CLI + first topic](lessons/03-local-lab.md)
4. [Lesson 04 — Producers: acks, idempotence, ordering, batching](lessons/04-producers.md)
5. [Lesson 05 — Consumers: groups, offsets, delivery semantics](lessons/05-consumers.md)
6. [Lesson 06 — Schema & serialization: JSON vs Avro/Protobuf, compatibility](lessons/06-schemas.md)
7. [Lesson 07 — Topic design: keys, partitioning, retention, compaction](lessons/07-topic-design.md)
8. [Lesson 08 — Kafka Connect: connectors, CDC concepts, ops basics](lessons/08-kafka-connect.md)
9. [Lesson 09 — Stream processing: Kafka Streams fundamentals](lessons/09-kafka-streams.md)
10. [Lesson 10 — Operations: sizing, configs, rebalancing, upgrades](lessons/10-operations.md)
11. [Lesson 11 — Observability: metrics, lag, logs, troubleshooting](lessons/11-observability.md)
12. [Lesson 12 — Security: TLS, SASL, ACLs, secrets hygiene](lessons/12-security.md)
13. [Lesson 13 — Capstone: build an event-driven workflow end-to-end](lessons/13-capstone.md)

## What “hero” looks like
You’re Kafka-proficient when you can:
- Design topics and keys to support ordering, scaling, and evolution
- Configure producers/consumers for your required semantics
- Diagnose consumer lag, rebalances, and throughput bottlenecks
- Operate a cluster safely (configs, upgrades, monitoring, security)

## Optional next steps
- KRaft mode (ZooKeeper-less Kafka) operations
- Exactly-once patterns and transactional messaging
- Advanced Connect + schema registry + governance
