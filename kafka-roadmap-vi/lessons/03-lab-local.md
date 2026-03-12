# Bài 03 — Lab local: Docker Compose + Kafka CLI + topic đầu tiên

## Mục tiêu
- Dựng Kafka local bằng Docker Compose
- Tạo topic và produce/consume bằng CLI
- Hiểu advertised listeners (cái bẫy số 1 khi dựng local)

## Tạo local stack
Tạo một folder (vd `kafka-lab/`) và thêm `compose.yaml`:

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

Start:
```powershell
docker compose up -d
```

Mở Kafdrop:
- http://localhost:9000

## Tạo topic
Chạy Kafka CLI trong container:

```powershell
# Tạo topic 1 partition, RF=1
# (Trong kafka container, dùng listener nội bộ kafka:29092)
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --create --topic demo.orders --partitions 1 --replication-factor 1"

# Liệt kê topics
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --list"
```

## Produce và consume
Terminal 1: chạy consumer:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-consumer --bootstrap-server kafka:29092 --topic demo.orders --from-beginning"
```

Terminal 2: chạy producer:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-producer --bootstrap-server kafka:29092 --topic demo.orders"
```

Gõ:
```text
{"orderId":1,"status":"CREATED"}
{"orderId":2,"status":"PAID"}
```

Bạn sẽ thấy message xuất hiện ở terminal consumer.

## Bẫy “advertised listeners”
- Container nói chuyện với Kafka qua `kafka:29092`
- Máy host nói chuyện với Kafka qua `localhost:9092`

Nếu `KAFKA_ADVERTISED_LISTENERS` sai, client có thể connect được lúc đầu rồi fail khi Kafka redirect sang host không truy cập được.

## Cleanup
```powershell
docker compose down -v
```

## Checklist
- Tôi start stack và mở Kafdrop được
- Tôi tạo topic và produce/consume message được
- Tôi hiểu vì sao phải cấu hình 2 listeners

## Lỗi hay gặp
- Dùng `localhost:9092` từ trong container (phải dùng `kafka:29092`)
- Quên expose port hoặc cấu hình sai `KAFKA_ADVERTISED_LISTENERS`
