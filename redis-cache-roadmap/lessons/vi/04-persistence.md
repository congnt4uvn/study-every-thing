# Bài 04 — Persistence cơ bản (RDB/AOF)

## Mục tiêu

Hiểu Redis lưu dữ liệu xuống disk bằng cách nào và vì sao cache đôi khi vẫn cần persistence (warm restart, giảm tải DB, phục hồi nhanh).

## Khái niệm chính

- RDB: snapshot theo thời điểm.
- AOF: log ghi các lệnh write.
- Nhiều hệ thống dùng AOF hoặc hybrid; default cụ thể phụ thuộc config.
- Persistence giúp hành vi khi restart, không thay thế cho HA.

## Thực hành

### Xem config

- `CONFIG GET save`
- `CONFIG GET appendonly`
- `CONFIG GET appendfsync`

### Trigger snapshot

- `SAVE` (blocking; chỉ để học)
- `BGSAVE` (chạy nền)

### AOF

Nếu môi trường của bạn bật AOF:

- `INFO persistence`
- `BGREWRITEAOF` (nén/compact)

## Gợi ý thực tế khi cache

- Nếu cache dựng lại rẻ, persistence là tuỳ chọn.
- Nếu dựng lại đắt (nhiều key derived), persistence giúp phục hồi nhanh.
- Nếu persist dữ liệu cache, hãy cẩn thận về freshness/invalidation khi deploy.

## Checklist

- Mô tả được tradeoff RDB vs AOF.
- Biết xem trạng thái qua `INFO persistence`.

## Tiếp theo

Học Pub/Sub và Streams.
