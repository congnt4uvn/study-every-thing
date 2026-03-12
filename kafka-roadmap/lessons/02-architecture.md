# Lesson 02 — Core architecture: brokers, topics, partitions, replication

## Goals
- Understand Kafka cluster building blocks
- Understand replication and fault tolerance at a high level
- Learn how partitions affect scalability and ordering

## Building blocks
- **Broker**: a Kafka server node that stores partitions and serves reads/writes
- **Cluster**: a set of brokers
- **Controller**: coordinates metadata changes (leader election, partition assignments)
- **Topic**: logical stream, split into partitions

## Partitions and parallelism
A topic with N partitions can be processed by up to N consumers in the same consumer group in parallel.

Tradeoffs:
- More partitions → higher parallelism and throughput potential
- More partitions → more overhead (files, memory, metadata, rebalances)

## Replication
Each partition can have a **replication factor (RF)**.

- **Leader replica**: handles reads/writes
- **Follower replicas**: replicate from leader

If the leader broker fails, a follower can become leader (assuming it’s in-sync).

Key term:
- **ISR (in-sync replicas)**: replicas that are caught up enough to be considered “in sync”

## Acks (preview)
Producer `acks` setting affects durability/latency tradeoffs:
- `acks=0`: fastest, least durable
- `acks=1`: leader ack only
- `acks=all`: wait for ISR ack (stronger durability)

You’ll practice this in the Producer lesson.

## Hands-on lab (conceptual)
Draw a topic with 3 partitions and explain:
- What ordering means
- How consumer groups scale
- What happens when a broker fails (leader moves)

## Checklist
- I can define broker, topic, partition, offset
- I can explain why partitions are the unit of ordering
- I can explain at a high level what replication factor and ISR do

## Common pitfalls
- Setting partitions extremely high “just in case” without measuring overhead
- Assuming replication alone replaces backups or disaster recovery planning
