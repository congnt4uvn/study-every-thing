# Bài 07 — Thiết kế topic: key, partitioning, retention, compaction

## Mục tiêu
- Thiết kế topic và key để đảm bảo ordering và scale
- Hiểu retention và log compaction
- Biết partition ảnh hưởng performance và song song của consumer

## Naming và ranh giới domain
Tên topic tốt giúp bạn tránh hỗn loạn:
- Ưu tiên tên theo domain như `orders.events`, `payments.events`
- Tránh nhét mọi thứ vào một topic “events” chung

## Keys và partitioning
Key quan trọng vì nó quyết định partitioning và ordering.

Gợi ý:
- Nếu cần ordering theo entity (vd theo order), dùng key ổn định (vd `orderId`).
- Nếu dùng key ngẫu nhiên, bạn đánh đổi ordering để lấy phân phối tải đều.

## Retention
Kafka xoá dữ liệu cũ theo cấu hình retention.

Kiểu phổ biến:
- Theo thời gian (vd giữ 7 ngày)
- Theo dung lượng (giữ tới khi chạm ngưỡng)

Retention không phải chiến lược backup.

## Log compaction
Compaction giữ “giá trị mới nhất theo key” (gần đúng).

Use cases:
- Topic “trạng thái hiện tại” (vd profile người dùng)
- Luồng kiểu CDC nơi bạn muốn last known value

Compaction không phải:
- Đảm bảo giữ mọi trạng thái trung gian

## Lab thực hành (tạo topic compacted)
Tạo topic compacted:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-topics --bootstrap-server kafka:29092 --create --topic demo.users.compacted --partitions 1 --replication-factor 1 --config cleanup.policy=compact"
```

Produce message có key:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-producer --bootstrap-server kafka:29092 --topic demo.users.compacted --property parse.key=true --property key.separator=:"
```

Gõ:
```text
u1:{"name":"Alice","tier":"free"}
u1:{"name":"Alice","tier":"pro"}
u2:{"name":"Bob","tier":"free"}
```

Consume và quan sát:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-consumer --bootstrap-server kafka:29092 --topic demo.users.compacted --from-beginning --property print.key=true --property key.separator= : "
```

Lưu ý: compaction chạy bất đồng bộ; bạn có thể không thấy việc loại bỏ giá trị cũ ngay lập tức.

## Checklist
- Tôi chọn được key strategy phù hợp yêu cầu ordering
- Tôi hiểu retention vs compaction và khi nào dùng
- Tôi tạo topic kèm config được

## Lỗi hay gặp
- Tạo quá nhiều topic/partition mà không có governance
- Dùng compaction như thể đó là database
