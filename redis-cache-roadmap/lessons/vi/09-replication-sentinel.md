# Bài 09 — Replication và Sentinel

## Mục tiêu

Hiểu replication để scale đọc và Sentinel để điều phối failover.

## Khái niệm chính

- Replication tạo node replica từ primary.
- Có thể đọc từ replica (có rủi ro consistency).
- Sentinel giám sát và có thể promote replica làm primary khi lỗi.

## Nội dung cần nắm (khái niệm)

- Replication thường async → đọc replica có thể stale.
- Với cache, stale đôi khi chấp nhận được; với lock/coordination phải cẩn thận.
- Failover đổi primary; client cần xử lý reconnect/redirect.

## Thực hành (tuỳ chọn)

Nếu chạy được nhiều instance local:

- Cấu hình 1 primary, 1 replica.
- Chạy `INFO replication` ở cả hai.

## Checklist

- Mô tả được vai trò primary/replica.
- Nêu được rủi ro stale read từ replica.

## Tiếp theo

Học scale ngang: Redis Cluster.
