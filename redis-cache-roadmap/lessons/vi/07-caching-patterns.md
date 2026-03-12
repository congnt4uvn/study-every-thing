# Bài 07 — Các pattern caching cốt lõi

## Mục tiêu

Nắm các pattern caching phổ biến và cách tránh cache stampede / lỗi invalidation.

## Khái niệm chính

### Cache-aside (lazy loading)

Luồng:

1. Đọc cache.
2. Miss → đọc DB/nguồn.
3. Ghi vào cache kèm TTL.
4. Trả kết quả.

Ưu: đơn giản, dùng rộng rãi.
Nhược: dễ stampede ở hot key; stale quanh thời điểm invalidation.

### Write-through / write-behind

- Write-through: ghi cache + DB cùng lúc.
- Write-behind: ghi cache, flush DB async (rủi ro hơn).

### Invalidation

Chiến lược phổ biến:

- Chỉ TTL (chấp nhận eventual consistency)
- Xoá khi write (`DEL cache:key`)
- Key có version (`cache:user:1:v42`) và tăng version khi cập nhật

### Chống stampede (dogpile)

- Thêm jitter vào TTL: `ttl = base + rand(0..jitter)`
- Single-flight (mutex): chỉ 1 request recompute
- Soft TTL: trả dữ liệu hơi cũ trong lúc refresh nền

## Bài tập (building block Redis)

1) TTL jitter:

- `SET cache:demo "x" EX 60`
- Thử nhiều TTL ngẫu nhiên và quan sát phân bố hết hạn.

2) Ý tưởng mutex cơ bản (bài sau sẽ làm lock an toàn hơn):

- `SET lock:cache:demo 1 NX EX 10`

## Checklist

- Vẽ/giải thích được cache-aside.
- Liệt kê được ≥ 3 cách chống stampede.
- Giải thích được ≥ 2 cách invalidation.

## Tiếp theo

Lock và rate limiting là bài toán “sát cạnh” caching.
