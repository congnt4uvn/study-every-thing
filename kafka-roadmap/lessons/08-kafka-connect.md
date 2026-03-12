# Lesson 08 — Kafka Connect: connectors, CDC concepts, ops basics

## Goals
- Understand what Kafka Connect is and when to use it
- Understand source vs sink connectors
- Learn operational concerns: offsets, tasks, scaling, error handling

## What Kafka Connect is
Kafka Connect is a framework for:
- Ingesting data into Kafka (source connectors)
- Delivering data out of Kafka (sink connectors)

Why it’s useful:
- Standardizes integration patterns
- Manages offsets/checkpointing for connector tasks
- Provides scaling and restart behavior

## Connector concepts
- **Connector**: high-level configuration of an integration
- **Task**: a unit of parallel work under a connector
- **Worker**: a Connect runtime process

## CDC (Change Data Capture) overview
CDC captures database changes (inserts/updates/deletes) as events.

Common CDC approach:
- Debezium source connector reads DB transaction log
- Events go to Kafka topics
- Downstream services react or materialize views

## Error handling (important)
Plan for:
- Poison pill messages
- Bad schemas
- Destination outages

Typical strategies:
- Dead letter topics
- Retry with backoff
- Alerting and dashboards

## Hands-on lab (conceptual)
This roadmap keeps labs vendor-neutral.

Exercise:
- List 3 integrations you’d build with Connect:
  - A DB → Kafka source
  - Kafka → data warehouse sink
  - Kafka → search index sink

For a full hands-on lab, you can add Connect + a demo connector later.

## Checklist
- I can explain source vs sink connectors
- I understand tasks/workers and how Connect scales
- I know why CDC is a common Kafka use case

## Common pitfalls
- Running Connect without thinking about schema governance
- Treating connectors as “set and forget” (they need monitoring)
