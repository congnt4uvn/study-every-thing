# Bài 04 — Producer: acks, idempotence, ordering, batching

## Mục tiêu
- Hiểu đánh đổi độ bền vs độ trễ của producer
- Biết idempotent producer giúp giảm duplicate thế nào
- Hiểu đảm bảo ordering và khi nào bạn làm mất nó

## Producer chịu trách nhiệm gì
Producer quyết định:
- Ghi vào topic nào
- Ghi vào partition nào (qua key + partitioner)
- Độ bền của ghi (`acks`)
- Cách batch/compress để tăng throughput

## `acks` (độ bền vs độ trễ)
- `acks=0`: gửi xong là thôi (có thể mất dữ liệu)
- `acks=1`: leader ack
- `acks=all`: chờ ISR ack (bền hơn)

Độ bền mạnh thường cần:
- Replication factor > 1
- `min.insync.replicas` cấu hình phù hợp

## Idempotent producer
Idempotence giảm duplicate do retry.

Về mặt ý tưởng:
- Nếu producer phải retry, Kafka có thể deduplicate dựa trên producer ID và sequence number

Ở nhiều client, idempotence bật bằng kiểu:
- `enable.idempotence=true`

## Ordering
Ordering của Kafka:
- Đảm bảo **trong một partition**
- Thường được giữ nếu một producer ghi với key nhất quán

Bạn mất ordering nếu:
- Cùng một “entity” bị ghi sang các partition khác nhau (key sai)
- Một số client bật các chế độ khiến retry/out-of-order

## Các núm throughput
Các lever phổ biến:
- `batch.size`
- `linger.ms`
- Compression (snappy, lz4, zstd)

## Lab thực hành (trực giác qua CLI)
Console producer không phải lab cấu hình đầy đủ, nhưng bạn vẫn luyện:
- Dùng key để kiểm soát partitioning

Produce message có key:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-producer --bootstrap-server kafka:29092 --topic demo.orders --property parse.key=true --property key.separator=:"
```

Gõ:
```text
order-1:{"orderId":1,"status":"CREATED"}
order-1:{"orderId":1,"status":"PAID"}
order-2:{"orderId":2,"status":"CREATED"}
```

Quan sát trong Kafdrop để thấy key và partitioning (đặc biệt khi bạn tăng partitions).

## Checklist
- Tôi giải thích được lựa chọn `acks` và đánh đổi
- Tôi hiểu idempotence ở mức khái niệm
- Tôi hiểu ordering theo partition và gắn với key

## Lỗi hay gặp
- Dùng key ngẫu nhiên (phá ordering theo entity)
- Nghĩ `acks=all` tự động “không mất dữ liệu” dù replication/ISR chưa đúng
