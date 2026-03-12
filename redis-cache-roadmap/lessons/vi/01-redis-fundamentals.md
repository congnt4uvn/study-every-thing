# Bài 01 — Nền tảng Redis

## Mục tiêu

Hiểu Redis là gì, khi nào Redis phù hợp làm **cache**, và cách tương tác bằng `redis-cli`.

## Khái niệm chính

- Redis là kho dữ liệu chạy chủ yếu trong RAM. Khi dùng làm cache, bạn tận dụng:
  - đọc/ghi rất nhanh
  - TTL (time-to-live) và cơ chế hết hạn
  - thao tác atomic đơn giản
- Redis xử lý đa số command theo kiểu single-thread (ngoài ra có I/O threads và tác vụ nền). Nhanh vì command thường ngắn và thao tác trên bộ nhớ.
- “Cache” nghĩa là dữ liệu có thể dựng lại từ nguồn chuẩn (DB, API, kết quả tính toán).

## Cách cài (chọn 1)

1. Docker: chạy Redis container (dễ học).
2. Cài native.
3. WSL trên Windows.

Lộ trình này tập trung vào CLI nên bạn dùng cách nào cũng được.

## Thực hành

1) Kết nối:

- `redis-cli -h 127.0.0.1 -p 6379`

2) Kiểm tra health:

- `PING` → trả về `PONG`
- `INFO server` → xem version, run-id

3) Ghi / đọc / xoá:

- `SET hello "world"`
- `GET hello`
- `DEL hello`

4) Quan sát keyspace:

- `SET user:1:name "Ada"`
- `KEYS user:*` (chỉ để học; tránh dùng production)
- `SCAN 0 MATCH user:* COUNT 100` (pattern nên dùng)

## Checklist

- Kết nối được bằng `redis-cli` và chạy `PING`.
- Hiểu vì sao `KEYS` nguy hiểm khi dữ liệu lớn.
- Dùng được `SCAN` để duyệt key theo từng đợt.

## Lỗi hay gặp

- Dùng Redis như DB chính mà chưa hiểu persistence/HA.
- Nghĩ “in-memory” là “không bao giờ mất dữ liệu”. Nếu cần giữ dữ liệu, phải có backup/replication.

## Tiếp theo

Học cấu trúc dữ liệu; caching không chỉ có `SET/GET`.
