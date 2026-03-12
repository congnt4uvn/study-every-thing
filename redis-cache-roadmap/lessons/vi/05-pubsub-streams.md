# Bài 05 — Pub/Sub và Streams

## Mục tiêu

Hiểu Pub/Sub (thông báo tức thời, không lưu) và Streams (lưu sự kiện, xử lý bền vững).

## Khái niệm chính

- Pub/Sub không lưu message; subscriber offline sẽ miss.
- Streams lưu event và hỗ trợ consumer group.
- Với hệ thống cache, chúng hữu ích cho:
  - broadcast invalidation
  - pipeline refresh async

## Thực hành

### Pub/Sub

Mở 2 terminal.

Terminal A:

- `redis-cli`
- `SUBSCRIBE cache:invalidate`

Terminal B:

- `redis-cli`
- `PUBLISH cache:invalidate "user:1"`

### Streams

- `XADD cache-events * type invalidate key user:1`
- `XRANGE cache-events - + COUNT 10`

Ví dụ consumer group:

- `XGROUP CREATE cache-events cache-workers $ MKSTREAM`
- `XREADGROUP GROUP cache-workers worker-1 COUNT 10 STREAMS cache-events >`

## Checklist

- Giải thích được vì sao Pub/Sub không bền.
- Thêm/đọc được Stream entry.
- Hiểu mục đích consumer group ở mức tổng quan.

## Tiếp theo

Học công cụ atomicity: transaction, pipeline, Lua.
