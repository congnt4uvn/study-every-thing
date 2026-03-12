# Bài 06 — Transaction, pipeline và Lua

## Mục tiêu

Dùng đúng thao tác atomic, giảm round-trip bằng pipelining, và biết khi nào nên dùng Lua script.

## Khái niệm chính

- Phần lớn lệnh Redis đơn lẻ là atomic.
- `MULTI/EXEC` nhóm lệnh; không giống transaction SQL (không rollback khi lỗi runtime).
- Pipelining giảm latency mạng bằng cách gửi nhiều lệnh liên tiếp.
- Lua chạy atomic trên Redis (trong phạm vi script).

## Thực hành

### Transaction (MULTI/EXEC)

- `MULTI`
- `INCR tx:counter`
- `INCR tx:counter`
- `EXEC`

### Optimistic locking với WATCH

- `WATCH user:1`
- `MULTI`
- `HSET user:1 name "Grace"`
- `EXEC` (fail nếu key bị đổi)

### Pipelining

Từ shell (không interactive):

- `echo "PING\nPING\nPING\n" | redis-cli --pipe`

### Lua script

Ví dụ: get + gia hạn TTL atomic

- `EVAL "local v = redis.call('GET', KEYS[1]); if v then redis.call('EXPIRE', KEYS[1], ARGV[1]); end; return v" 1 cache:user:1 60`

## Checklist

- Giải thích được khi nào `WATCH` hữu ích.
- Pipeline để giảm RTT được.
- Chạy được Lua script nhỏ cho read-modify-write.

## Tiếp theo

Học các pattern caching để tránh sự cố production.
