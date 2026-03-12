# Bài 08 — Lock và rate limiting

## Mục tiêu

Áp dụng các pattern điều phối phân tán cơ bản bằng Redis: lock và rate limiting.

## Khái niệm chính

### Distributed lock

- Lock cơ bản thường dùng `SET key value NX EX seconds`.
- Value phải là token unique để chỉ owner mới được unlock.
- Unlock cần check-and-delete, thường dùng Lua.

### Rate limiting

Một số cách phổ biến:

- Fixed window counter (đơn giản, dễ burst)
- Sliding window (chính xác hơn)
- Token bucket / leaky bucket (làm mượt tốt)

## Thực hành

### Acquire lock

- `SET lock:job:1 "token-123" NX EX 10`

### Release lock an toàn (Lua)

- `EVAL "if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end" 1 lock:job:1 token-123`

### Fixed-window rate limit

Với user `u1`, window 60 giây:

- `INCR rl:u1`
- `EXPIRE rl:u1 60` (set ở lần đầu; cần logic ở app)

## Checklist

- Hiểu vì sao unlock phải kiểm tra token.
- Nêu được ưu/nhược của fixed window.

## Tiếp theo

Học HA: replication và Sentinel.
