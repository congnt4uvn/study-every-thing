# Bài 13 — Capstone: xây workflow event-driven end-to-end

## Mục tiêu
Xây một workflow event-driven nhỏ nhưng “thật” với Kafka.

## Gợi ý dự án capstone
### Kịch bản: xử lý đơn hàng
Events:
- `orders.events` (CREATED, PAID, SHIPPED)

Services (ban đầu có thể chỉ là script):
1. **Order API** (producer)
2. **Payment service** (consumer + producer)
3. **Shipping service** (consumer)

## Deliverables
- Tài liệu thiết kế topic:
  - Topics, partitions, retention, compaction
  - Keys và yêu cầu ordering
- Lựa chọn cấu hình producer:
  - `acks`, retries, idempotence
- Lựa chọn cấu hình consumer:
  - group strategy, commit strategy
- Runbook ngắn:
  - Cách start stack local
  - Cách xem lag và troubleshooting

## Các bước thực hành (local)
1. Start Docker Compose Kafka lab (Bài 03).
2. Tạo topics:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --create --topic orders.events --partitions 3 --replication-factor 1"
```

3. Produce vài event `CREATED` (CLI cũng được lúc đầu).
4. Consume bằng group và mô phỏng xử lý.
5. Chạy thêm một consumer nữa trong cùng group và quan sát partition assignment.

## Tiêu chí đạt
Bạn “đạt” khi:
- Giải thích được vì sao chọn keys và partitions
- Demo được at-least-once và hiểu cách xử lý duplicate
- Tạo và chẩn đoán lag có chủ đích

## Stretch goals
- Thêm compacted topic `orders.state` key theo `orderId`
- Thêm schema contract và compatibility policy
- Bổ sung metrics/dashboard theo môi trường của bạn

## Checklist
- Tôi thiết kế topic và key cho ordering và scale
- Tôi suy luận được producer/consumer semantics
- Tôi troubleshoot lag và rebalances được
