# Bài 13 — Capstone: xây lớp cache

## Mục tiêu

Thiết kế và implement một lớp cache (bằng ngôn ngữ bạn chọn) đủ an toàn khi tải cao và có thể quan sát vận hành.

## Yêu cầu (giữ nhỏ gọn)

Xây một wrapper cache để đọc “user profile” từ một nguồn chậm.

Lớp cache phải có:

- Cache-aside
- TTL có jitter
- Chống stampede cho hot key (single-flight/mutex)
- Có metrics/log cơ bản (hit/miss, latency)
- Hỗ trợ invalidation thủ công

## Gợi ý thiết kế key

- `cache:user:<id>:profile`

## Thuật toán khuyến nghị (pseudo)

1) `GET key`
2) Hit → trả
3) Miss:
   - Thử acquire lock `SET lock:key token NX EX lockTTL`
   - Nếu acquire được:
     - Đọc từ source
     - `SET key value EX ttl`
     - Release lock an toàn (check token)
     - Trả value
   - Nếu chưa acquire được:
     - Chờ ngắn + retry cache vài lần
     - Nếu vẫn miss → tuỳ SLO có thể fallback sang source

## Nên đo gì

- Tỉ lệ hit theo thời gian
- P95/P99 latency của `GET` và latency endpoint tổng
- Error rate (timeout, lỗi command)
- `evicted_keys` và memory usage

## Mở rộng (tuỳ chọn)

- Soft TTL + background refresh
- Versioned keys để đơn giản hoá invalidation
- Dùng Stream để ghi nhận sự kiện invalidation

## Tiêu chí hoàn thành

- Load test ổn định.
- Giải thích rõ cách bạn tránh stampede.
- Redis down vẫn degrade hợp lý.
