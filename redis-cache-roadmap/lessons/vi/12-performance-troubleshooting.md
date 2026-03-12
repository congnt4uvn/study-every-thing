# Bài 12 — Tối ưu & xử lý sự cố hiệu năng

## Mục tiêu

Có quy trình chẩn đoán Redis chậm và vấn đề bộ nhớ.

## Khái niệm chính

Nguyên nhân phổ biến khiến Redis “chậm”:

- Big key hoặc command nặng (`KEYS`, `SORT` lớn, `ZRANGE` quá rộng)
- CPU bão hoà (quá nhiều công việc trong mỗi command)
- Áp lực bộ nhớ dẫn đến eviction hoặc swap (đừng để Redis swap)
- Latency mạng hoặc bùng nổ kết nối client

## Checklist xử lý nhanh (theo thứ tự)

1) Redis còn sống?

- `PING`
- `INFO server`

2) Latency có cao?

- `LATENCY DOCTOR`
- `SLOWLOG GET 20`

3) Memory có áp lực?

- `INFO memory`
- Xem eviction: `INFO stats` (`evicted_keys`)

4) Có big key?

- Dùng `SCAN` + `MEMORY USAGE` theo kiểu sampling (viết script trong ngôn ngữ của bạn).

## Thực hành

- `SLOWLOG RESET` (chỉ làm trong môi trường không-prod)
- Tạo load, sau đó `SLOWLOG GET 10`

## Checklist

- Nêu được 3 command/pattern nên tránh trong production.
- Dùng được `SLOWLOG` và `LATENCY DOCTOR`.

## Tiếp theo

Làm capstone để ghép tất cả lại thành một lớp cache hoàn chỉnh.
