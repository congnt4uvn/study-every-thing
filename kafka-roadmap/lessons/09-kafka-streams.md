# Lesson 09 — Stream processing: Kafka Streams fundamentals

## Goals
- Understand Kafka Streams at a high level
- Understand stream vs table concepts
- Recognize when Streams is a good fit

## What Kafka Streams is
Kafka Streams is a Java library for building stream processing applications.

It provides:
- Stateful processing (aggregations, joins)
- Exactly-once capable processing patterns (with correct config)
- Local state stores with changelog topics

## Stream vs Table (mental model)
- **Stream**: a sequence of immutable events over time
- **Table**: the latest value per key (a materialized view)

Streams often turn streams into tables via aggregation, and tables back into streams via change events.

## Common patterns
- Filtering/enrichment
- Windowed aggregation (e.g., events per minute)
- Joins (stream-stream, stream-table)

## Operational considerations
- Scaling depends on partitions (again)
- Stateful operations create local state that must be managed
- Rebalancing and restoration can take time

## Hands-on lab (design exercise)
Using `demo.orders`:
1. Define a stream processing task: “count PAID orders per 1-minute window”.
2. Define keying strategy.
3. Define output topic schema.

## Checklist
- I can explain stream vs table
- I know why partitions drive scaling for stream apps
- I can name 2–3 processing patterns Streams supports

## Common pitfalls
- Under-partitioning input topics for future scale
- Ignoring state store restoration time during deploys
