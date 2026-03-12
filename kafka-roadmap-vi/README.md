# Lộ trình Apache Kafka Từ Số 0 → Thành Thạo

Một kế hoạch học thực hành để nắm Kafka từ nền tảng đến mức dùng được theo hướng production.

## Dành cho ai
- Backend developer tích hợp event streaming vào hệ thống
- Data engineer xây pipeline/CDC
- DevOps/SRE vận hành Kafka cluster

## Cách học theo lộ trình
- Học theo thứ tự bài.
- Mỗi bài có:
  - **Mục tiêu** (làm được gì)
  - **Khái niệm** (hiểu được gì)
  - **Lab thực hành** (lệnh + kết quả mong đợi)
  - **Checklist** (tự kiểm tra nhanh)

## Điều kiện trước
- Biết dùng terminal cơ bản (PowerShell/Bash)
- Biết ít nhất một ngôn ngữ lập trình
- Có Docker Desktop (khuyến nghị để làm lab)

## Lab stack (khuyến nghị)
Để thực hành nhất quán, các bài dùng Docker Compose stack nhỏ:
- ZooKeeper + Kafka (1 broker) để đơn giản
- Kafdrop (web UI) để xem topics/messages

Bạn sẽ tạo stack này ở Bài 03.

## Lịch học gợi ý
- **Nhanh (1 tuần):** 1–2 bài/ngày + capstone
- **Đều (2–3 tuần):** 3–5 bài/tuần + lặp lại lab

## Danh sách bài học
1. [Bài 01 — Kafka là gì + use case + các đảm bảo cốt lõi](lessons/01-kafka-la-gi.md)
2. [Bài 02 — Kiến trúc lõi: broker, topic, partition, replication](lessons/02-kien-truc.md)
3. [Bài 03 — Lab local: Docker Compose + Kafka CLI + topic đầu tiên](lessons/03-lab-local.md)
4. [Bài 04 — Producer: acks, idempotence, ordering, batching](lessons/04-producer.md)
5. [Bài 05 — Consumer: group, offset, delivery semantics](lessons/05-consumer.md)
6. [Bài 06 — Schema & serialization: JSON vs Avro/Protobuf, compatibility](lessons/06-schema.md)
7. [Bài 07 — Thiết kế topic: key, partitioning, retention, compaction](lessons/07-thiet-ke-topic.md)
8. [Bài 08 — Kafka Connect: connector, CDC, vận hành cơ bản](lessons/08-kafka-connect.md)
9. [Bài 09 — Stream processing: Kafka Streams nền tảng](lessons/09-kafka-streams.md)
10. [Bài 10 — Vận hành: sizing, cấu hình, rebalancing, upgrade](lessons/10-van-hanh.md)
11. [Bài 11 — Quan sát hệ thống: metrics, lag, logs, troubleshooting](lessons/11-quan-sat.md)
12. [Bài 12 — Bảo mật: TLS, SASL, ACLs, quản lý secrets](lessons/12-bao-mat.md)
13. [Bài 13 — Capstone: xây workflow event-driven end-to-end](lessons/13-capstone.md)

## “Thành thạo” nghĩa là gì
Bạn được xem là dùng Kafka tốt khi có thể:
- Thiết kế topic và key để đảm bảo ordering, scale, và tiến hoá schema
- Cấu hình producer/consumer đúng theo yêu cầu semantics
- Chẩn đoán consumer lag, rebalances, và bottleneck throughput
- Vận hành cluster an toàn (config, upgrade, monitoring, security)

## Bước tiếp theo (tuỳ chọn)
- KRaft mode (Kafka không cần ZooKeeper)
- Mẫu exactly-once và transactional messaging
- Connect nâng cao + schema registry + governance
