# Lesson 13 — Capstone: build an event-driven workflow end-to-end

## Goal
Build a small but realistic event-driven workflow using Kafka.

## Suggested capstone project
### Scenario: Order processing
Events:
- `orders.events` (CREATED, PAID, SHIPPED)

Services (can be simple scripts at first):
1. **Order API** (producer)
2. **Payment service** (consumer + producer)
3. **Shipping service** (consumer)

## Deliverables
- Topic design document:
  - Topics, partitions, retention, compaction decisions
  - Keys and ordering requirements
- Producer configuration choices:
  - `acks`, retries, idempotence
- Consumer configuration choices:
  - group strategy, commit strategy
- A short runbook:
  - How to start local stack
  - How to inspect lag and troubleshoot

## Hands-on steps (local)
1. Start your Docker Compose Kafka lab (Lesson 03).
2. Create topics:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --create --topic orders.events --partitions 3 --replication-factor 1"
```

3. Produce some `CREATED` events (CLI is fine initially).
4. Consume with a group and simulate processing.
5. Add a second consumer instance in the same group and observe partition assignment.

## Quality bar
You “pass” when:
- You can explain why you chose keys and partitions
- You can demonstrate at-least-once processing and handle duplicates conceptually
- You can create and diagnose lag intentionally

## Stretch goals
- Add a compacted topic `orders.state` keyed by `orderId`
- Add a schema contract and a compatibility policy
- Add basic metrics and dashboards in your environment

## Checklist
- I can design topics and keys for ordering and scalability
- I can reason about producer/consumer semantics
- I can troubleshoot lag and rebalances
