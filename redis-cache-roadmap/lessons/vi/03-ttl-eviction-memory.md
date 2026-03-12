# Bài 03 — TTL, eviction và bộ nhớ

## Mục tiêu

Kiểm soát vòng đời cache bằng TTL, hiểu semantics của expiration, và biết Redis xử lý ra sao khi thiếu bộ nhớ.

## Khái niệm chính

- TTL là thời gian sống theo từng key; đây là nền tảng để cache đúng.
- Expiration không nhất thiết xảy ra “đúng từng mili-giây”; Redis dùng kết hợp passive + active expiration.
- Khi bộ nhớ đầy và có cấu hình `maxmemory`, Redis sẽ **evict** theo policy.

## Thực hành

### Set key có TTL

- `SET cache:page:home "..." EX 60`
- `TTL cache:page:home`
- `PTTL cache:page:home`

### Cập nhật TTL

- `EXPIRE cache:page:home 120`
- `PERSIST cache:page:home` (bỏ TTL)

### Ý tưởng “soft TTL” (do ứng dụng tự quản)

TTL Redis là “hết hạn cứng”. Nhiều hệ thống production thêm *soft expiry* trong value (ví dụ field `staleAt`) để có thể trả dữ liệu hơi cũ trong lúc refresh nền.

### Xem thông tin bộ nhớ

- `INFO memory`
- `MEMORY STATS`
- `MEMORY USAGE cache:page:home`

## Tổng quan eviction

Một số policy thường gặp:

- `noeviction`: hết bộ nhớ thì lệnh ghi fail (nguy hiểm nếu app không handle).
- `allkeys-lru`: evict key ít được truy cập gần đây nhất.
- `allkeys-lfu`: evict key ít được truy cập thường xuyên nhất.
- `volatile-*`: chỉ evict key có TTL.

Với cache, `allkeys-lfu` thường là điểm bắt đầu tốt, nhưng còn tuỳ workload.

## Checklist

- Set/đọc TTL được.
- Hiểu expiration là xấp xỉ.
- Giải thích được eviction và vì sao policy quan trọng.

## Tiếp theo

Học persistence để biết Redis “giữ được gì” khi restart.
