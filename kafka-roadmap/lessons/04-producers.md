# Lesson 04 — Producers: acks, idempotence, ordering, batching

## Goals
- Understand producer durability/latency tradeoffs
- Know how idempotent producers reduce duplicates
- Understand ordering guarantees and when you lose them

## Producer responsibilities
A Kafka producer chooses:
- Which topic to write to
- Which partition (via key + partitioner)
- How durable the write should be (`acks`)
- How to batch/compress for throughput

## `acks` (durability vs latency)
- `acks=0`: fire-and-forget (can lose data)
- `acks=1`: leader ack only
- `acks=all`: wait for ISR ack (stronger durability)

Stronger durability often needs:
- Replication factor > 1
- `min.insync.replicas` configured appropriately

## Idempotent producer
Idempotence reduces duplicates due to retries.

Conceptually:
- If the producer must retry, Kafka can deduplicate based on producer ID and sequence numbers

In many clients, idempotence is enabled with something like:
- `enable.idempotence=true`

## Ordering
Kafka ordering is:
- Guaranteed **within a single partition**
- Typically preserved when a single producer writes with a consistent key

You can lose ordering if:
- You write the same “entity” to different partitions (wrong key)
- You enable certain retry/out-of-order settings in some clients

## Throughput knobs
Common levers:
- `batch.size`
- `linger.ms`
- Compression (snappy, lz4, zstd)

## Hands-on lab (CLI-level intuition)
The console producer is not a full-featured client configuration lab, but you can still practice:
- Using keys (so you control partitioning)

Produce messages with keys:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-producer --bootstrap-server kafka:29092 --topic demo.orders --property parse.key=true --property key.separator=:"
```

Type:
```text
order-1:{"orderId":1,"status":"CREATED"}
order-1:{"orderId":1,"status":"PAID"}
order-2:{"orderId":2,"status":"CREATED"}
```

Observe in Kafdrop how keys show up and how partitioning works (especially if you increase partitions later).

## Checklist
- I can explain `acks` choices and the tradeoff
- I understand idempotence at a conceptual level
- I understand ordering is per-partition and tied to keys

## Common pitfalls
- Using random keys (destroys ordering per entity)
- Assuming `acks=all` automatically means “no loss” without correct replication and ISR settings
