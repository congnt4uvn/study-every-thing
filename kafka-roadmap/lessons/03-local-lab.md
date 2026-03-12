# Lesson 03 — Local lab: Docker Compose + Kafka CLI + first topic

## Goals
- Start a local Kafka environment with Docker Compose
- Create topics and publish/consume messages using the CLI
- Understand advertised listeners (the #1 local setup gotcha)

## Create a local stack
Create a folder (e.g., `kafka-lab/`) and add `compose.yaml`:

```yaml
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.1
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:7.6.1
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: "zookeeper:2181"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT"
      KAFKA_LISTENERS: "PLAINTEXT://0.0.0.0:29092,PLAINTEXT_HOST://0.0.0.0:9092"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092"
      KAFKA_INTER_BROKER_LISTENER_NAME: "PLAINTEXT"

  kafdrop:
    image: obsidiandynamics/kafdrop:latest
    depends_on:
      - kafka
    ports:
      - "9000:9000"
    environment:
      KAFKA_BROKERCONNECT: "kafka:29092"
      SERVER_PORT: 9000
```

Start it:
```powershell
docker compose up -d
```

Open Kafdrop:
- http://localhost:9000

## Create a topic
Run Kafka CLI inside the container:

```powershell
# Create a topic with 1 partition, RF=1
# (Inside the kafka container, use the internal listener kafka:29092)
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --create --topic demo.orders --partitions 1 --replication-factor 1"

# List topics
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --list"
```

## Produce and consume
In one terminal, start a consumer:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-consumer --bootstrap-server kafka:29092 --topic demo.orders --from-beginning"
```

In another terminal, produce a few lines:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-producer --bootstrap-server kafka:29092 --topic demo.orders"
```

Type:
```text
{"orderId":1,"status":"CREATED"}
{"orderId":2,"status":"PAID"}
```

You should see the messages appear in the consumer terminal.

## The “advertised listeners” gotcha
- Containers talk to Kafka using `kafka:29092`
- Your host machine talks to Kafka using `localhost:9092`

If `KAFKA_ADVERTISED_LISTENERS` is wrong, clients will connect once and then fail when Kafka redirects them to an unreachable host.

## Cleanup
```powershell
docker compose down -v
```

## Checklist
- I can start the stack and open Kafdrop
- I can create a topic and publish/consume messages
- I understand why two listeners are configured

## Common pitfalls
- Using `localhost:9092` from inside a container (use `kafka:29092` instead)
- Forgetting to expose ports or misconfiguring `KAFKA_ADVERTISED_LISTENERS`
