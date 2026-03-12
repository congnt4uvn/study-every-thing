# Lesson 11 — Observability: metrics, lag, logs, troubleshooting

## Goals
- Know what to monitor for Kafka health
- Understand consumer lag and why it happens
- Build a basic troubleshooting workflow

## What to monitor
Broker health signals:
- Under-replicated partitions (URP)
- Offline partitions
- Controller events
- Disk usage and IO latency

Client health signals:
- Producer error rates and retries
- Consumer lag
- Rebalance frequency and duration

## Consumer lag
Lag = how far behind a consumer is compared to the latest offsets.

Common causes:
- Consumer is too slow (processing bottleneck)
- Not enough partitions for desired parallelism
- Downstream dependency slow (DB, API)
- Large rebalances / restarts

## Logs and diagnostics
Use:
- Broker logs for controller/replication issues
- Client logs for timeouts/retries

## Hands-on lab (local)
1. Create lag intentionally:
   - Start a producer sending messages quickly
   - Run a slow consumer (simulate with sleep in your app later)

2. Inspect group state:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-consumer-groups --bootstrap-server kafka:29092 --describe --group demo-group"
```

## Checklist
- I can define consumer lag and list common causes
- I know a basic step-by-step troubleshooting order
- I can use `kafka-consumer-groups --describe` to inspect lag

## Common pitfalls
- Confusing “Kafka is down” with “my consumer is down/slow”
- Ignoring disk saturation (a frequent root cause)
