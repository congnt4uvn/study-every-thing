# Lộ trình học Redis Cache (Từ số 0 → Thành thạo)

Đây là lộ trình **thực hành** để học Redis tập trung vào vai trò **cache** (và các tính năng cần thiết để vận hành cache ổn định trong môi trường production).

## Cách dùng lộ trình

- Học theo thứ tự.
- Mỗi bài: đọc khái niệm, chạy lệnh, rồi hoàn thành checklist.
- Ghi chú lại: bạn đã thử gì, lỗi gì xảy ra, và bạn đã sửa thế nào.

## Điều kiện đầu vào

- Biết dùng terminal/CLI cơ bản
- Biết khái niệm mạng cơ bản (IP/port)
- Tuỳ chọn: 1 ngôn ngữ bạn hay dùng (Node.js / Python / Java / Go). Lộ trình này không phụ thuộc ngôn ngữ.

## Chuẩn bị môi trường (khuyến nghị)

- Redis 7.x chạy local (cài native, Docker, hoặc WSL)
- `redis-cli`

## Danh sách bài học

1. [Bài 01 — Nền tảng Redis](lessons/vi/01-redis-fundamentals.md)
2. [Bài 02 — Cấu trúc dữ liệu cho caching](lessons/vi/02-data-structures.md)
3. [Bài 03 — TTL, eviction và bộ nhớ](lessons/vi/03-ttl-eviction-memory.md)
4. [Bài 04 — Persistence cơ bản (RDB/AOF)](lessons/vi/04-persistence.md)
5. [Bài 05 — Pub/Sub và Streams](lessons/vi/05-pubsub-streams.md)
6. [Bài 06 — Transaction, pipeline và Lua](lessons/vi/06-tx-pipeline-lua.md)
7. [Bài 07 — Các pattern caching cốt lõi](lessons/vi/07-caching-patterns.md)
8. [Bài 08 — Lock và rate limiting](lessons/vi/08-locks-rate-limiting.md)
9. [Bài 09 — Replication và Sentinel](lessons/vi/09-replication-sentinel.md)
10. [Bài 10 — Redis Cluster (sharding)](lessons/vi/10-redis-cluster.md)
11. [Bài 11 — Security và vận hành](lessons/vi/11-security-ops.md)
12. [Bài 12 — Tối ưu & xử lý sự cố hiệu năng](lessons/vi/12-performance-troubleshooting.md)
13. [Bài 13 — Capstone: xây lớp cache](lessons/vi/13-capstone-cache-layer.md)

## Gợi ý lịch học theo tuần

- Tuần 1: Bài 01–03
- Tuần 2: Bài 04–06
- Tuần 3: Bài 07–10
- Tuần 4: Bài 11–13 (capstone)

## Tiêu chí “thành thạo”

- Chọn đúng cấu trúc dữ liệu Redis cho từng use case và giải thích tradeoff.
- Đặt TTL có chủ đích, tránh cache stampede, và xử lý invalidation.
- Vận hành Redis an toàn (monitoring, backup/restore, failover cơ bản).
- Debug được slow command, áp lực bộ nhớ, và hot key.
