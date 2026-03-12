# Bài 11 — Security và vận hành

## Mục tiêu

Vận hành Redis như một thành phần production: bảo mật truy cập, theo dõi health, tránh “bẫy” phổ biến.

## Khái niệm chính

- Không bao giờ expose Redis trực tiếp ra internet public.
- Dùng authentication và ACL.
- Dùng TLS khi cần.
- Theo dõi latency, memory, eviction, persistence.

## Thực hành

### Xem client và truy vấn chậm

- `CLIENT LIST`
- `SLOWLOG GET 10`
- `LATENCY DOCTOR`

### Thống kê keyspace

- `INFO stats`
- `INFO keyspace`

### ACL cơ bản (khái niệm)

- Tạo user chỉ được phép chạy một số command và key pattern.
- Nguyên tắc: least privilege.

## Checklist

- Liệt kê được 3 metric phải monitor (latency, memory, evictions).
- Hiểu vì sao public exposure cực nguy hiểm.

## Tiếp theo

Học cách debug hiệu năng: slow command, big key, hot key.
