# Bài 02 — Cấu trúc dữ liệu cho caching

## Mục tiêu

Biết chọn cấu trúc dữ liệu Redis để cache hiệu quả, tránh anti-pattern kiểu nhét tất cả vào 1 JSON khổng lồ khi bạn cần update từng phần.

## Khái niệm chính

- Redis có nhiều kiểu dữ liệu; chọn đúng thường giúp giảm latency và tiết kiệm bộ nhớ.
- Chọn “đúng” phụ thuộc:
  - cách truy cập (đọc cả object hay từng field)
  - cách cập nhật (update 1 field hay ghi đè toàn bộ)
  - có cần sắp xếp/ranking hay không

## Thực hành (các cấu trúc cốt lõi)

### String

- Dùng cho giá trị đơn hoặc cache cả object.
- Lệnh:
  - `SET cache:user:1 "{...json...}"`
  - `GET cache:user:1`
  - `MSET k1 v1 k2 v2`
  - `MGET k1 k2`

### Hash

- Rất hợp cho object có nhiều field.
- Lệnh:
  - `HSET user:1 name "Ada" age "37"`
  - `HGET user:1 name`
  - `HGETALL user:1`
  - `HINCRBY user:1 visits 1`

### List

- Danh sách có thứ tự (queue bền vững thì Streams thường tốt hơn).
- Lệnh:
  - `LPUSH recent:log "a" "b" "c"`
  - `LRANGE recent:log 0 10`
  - `LTRIM recent:log 0 99` (giữ 100 phần tử mới nhất)

### Set

- Tập hợp không thứ tự, phần tử duy nhất.
- Lệnh:
  - `SADD user:1:tags "pro" "beta"`
  - `SISMEMBER user:1:tags "beta"`
  - `SMEMBERS user:1:tags`

### Sorted Set (ZSET)

- Ranking/leaderboard, sắp xếp theo điểm hoặc timestamp.
- Lệnh:
  - `ZADD leaderboard 100 "alice" 200 "bob"`
  - `ZREVRANGE leaderboard 0 9 WITHSCORES`
  - `ZINCRBY leaderboard 5 "alice"`

## Ghi nhớ khi làm cache

- Key nhỏ, có quy tắc: `cache:<domain>:<id>`.
- Tránh “big key”: value quá lớn hoặc collection quá lớn.
- Nếu thường xuyên invalidate một phần, cân nhắc tách field (hash) thay vì 1 blob.

## Checklist

- Giải thích được khi nào dùng String vs Hash.
- Mô hình hoá “top N” bằng ZSET.
- Giữ danh sách “gần đây” có giới hạn bằng `LTRIM`.

## Tiếp theo

Học TTL, expiration và eviction (cơ chế sống còn của cache).
