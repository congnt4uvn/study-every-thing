# Bài 10 — Redis Cluster (sharding)

## Mục tiêu

Hiểu Redis Cluster là gì, khi nào cần, và điều gì thay đổi ở client và thiết kế key.

## Khái niệm chính

- Cluster shard dữ liệu qua nhiều node theo hash slot.
- Một số lệnh multi-key yêu cầu các key cùng slot.
- Hash tag `{...}` giúp ép các key liên quan vào cùng slot.

## Gợi ý thiết kế cache

- Ưu tiên thao tác single-key để “cluster-friendly”.
- Nếu bắt buộc multi-key (vd `MGET`), thiết kế key dùng hash tag.

Ví dụ:

- `cache:user:{1}:profile`
- `cache:user:{1}:settings`

Cả hai dùng cùng tag `{1}`.

## Checklist

- Hiểu vì sao multi-key có thể fail trong cluster.
- Giải thích được hash tag dùng để làm gì.

## Tiếp theo

Học security và vận hành.
