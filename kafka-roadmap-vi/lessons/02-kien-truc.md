# Bài 02 — Kiến trúc lõi: broker, topic, partition, replication

## Mục tiêu
- Hiểu các thành phần chính của Kafka cluster
- Hiểu replication và chịu lỗi ở mức tổng quan
- Hiểu partition ảnh hưởng scale và ordering

## Các khối xây dựng
- **Broker**: máy chủ Kafka lưu partitions và phục vụ đọc/ghi
- **Cluster**: tập các broker
- **Controller**: điều phối thay đổi metadata (leader election, phân bổ partition)
- **Topic**: luồng logic, được chia thành partitions

## Partition và song song
Topic có N partitions => có thể xử lý song song tối đa N consumer (trong cùng consumer group).

Đánh đổi:
- Nhiều partitions → tăng song song và throughput tiềm năng
- Nhiều partitions → tăng overhead (file, memory, metadata, rebalances)

## Replication
Mỗi partition có thể có **replication factor (RF)**.

- **Leader replica**: xử lý đọc/ghi
- **Follower replicas**: replicate từ leader

Nếu broker chứa leader fail, một follower có thể lên leader (nếu còn “in-sync”).

Thuật ngữ:
- **ISR (in-sync replicas)**: replicas bắt kịp đủ mức để được coi là “đồng bộ”

## Acks (xem trước)
Cấu hình producer `acks` quyết định đánh đổi độ bền vs độ trễ:
- `acks=0`: nhanh nhất, kém bền
- `acks=1`: leader ack
- `acks=all`: chờ ISR ack (bền hơn)

Bạn sẽ thực hành ở bài Producer.

## Lab (mang tính khái niệm)
Vẽ topic có 3 partitions và giải thích:
- Ordering nghĩa là gì
- Consumer group scale ra sao
- Broker fail thì chuyện gì xảy ra (leader chuyển)

## Checklist
- Tôi định nghĩa được broker, topic, partition, offset
- Tôi giải thích được vì sao partition là đơn vị của ordering
- Tôi hiểu RF và ISR ở mức tổng quan

## Lỗi hay gặp
- Đặt số partition cực cao “cho chắc” mà không đo overhead
- Nghĩ replication thay thế backup/DR (không phải)
