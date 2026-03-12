# Bài 11 — Quan sát hệ thống: metrics, lag, logs, troubleshooting

## Mục tiêu
- Biết cần monitor gì để đánh giá Kafka “khoẻ”
- Hiểu consumer lag và nguyên nhân
- Có workflow troubleshooting cơ bản

## Monitor gì
Tín hiệu broker:
- Under-replicated partitions (URP)
- Offline partitions
- Controller events
- Disk usage và IO latency

Tín hiệu client:
- Producer error rate và retries
- Consumer lag
- Tần suất và thời lượng rebalance

## Consumer lag
Lag = consumer đang chậm so với latest offsets bao nhiêu.

Nguyên nhân hay gặp:
- Consumer xử lý chậm (bottleneck xử lý)
- Không đủ partition cho mức song song mong muốn
- Dependency downstream chậm (DB, API)
- Rebalance lớn / restart

## Logs và chẩn đoán
Dùng:
- Broker logs cho controller/replication
- Client logs cho timeout/retry

## Lab (local)
1. Tạo lag có chủ đích:
   - Start producer gửi nhanh
   - Chạy consumer chậm (mô phỏng bằng sleep trong app sau)

2. Xem trạng thái group:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-consumer-groups --bootstrap-server kafka:29092 --describe --group demo-group"
```

## Checklist
- Tôi định nghĩa được consumer lag và liệt kê nguyên nhân
- Tôi có thứ tự troubleshooting cơ bản
- Tôi dùng `kafka-consumer-groups --describe` để xem lag được

## Lỗi hay gặp
- Nhầm “Kafka down” với “consumer down/chậm”
- Bỏ qua disk saturation (nguyên nhân gốc hay gặp)
