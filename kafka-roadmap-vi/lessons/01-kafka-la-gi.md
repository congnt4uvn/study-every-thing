# Bài 01 — Kafka là gì + use case + các đảm bảo cốt lõi

## Mục tiêu
- Giải thích Kafka là gì theo cách thực tế
- Nhận biết khi nào Kafka phù hợp (và khi nào không)
- Hiểu các đảm bảo cơ bản bạn có thể (và không thể) dựa vào

## Kafka là gì
Apache Kafka là một **nền tảng event streaming phân tán**.

Nói đơn giản:
- Producer ghi **record (event/message)** vào **topic**
- Kafka lưu các record bền vững (trong thời gian cấu hình)
- Consumer đọc record từ topic để xây pipeline thời gian thực hoặc hệ event-driven

Kafka thường dùng cho:
- Microservices event-driven
- Audit log và event sourcing
- Data pipeline và CDC (change data capture)
- Stream processing (fraud detection, monitoring, enrichment)

## Kafka không phải là
- Thứ thay thế mọi loại message queue kiểu request/response
- Database (Kafka lưu dạng log; khả năng truy vấn bị giới hạn)
- “Đúng một lần” mặc định (semantics phụ thuộc cấu hình và cách bạn xử lý)

## Các đảm bảo cốt lõi (thực tế)
Những thứ thường có thể tin tưởng:
- **Lưu trữ bền vững** (nếu cấu hình và replication đúng)
- **Ordering trong phạm vi một partition**
- **Khả năng scale** nhờ partitioning

Những thứ phụ thuộc cấu hình:
- Delivery semantics (at-most-once / at-least-once / effectively-once)
- Cách xử lý duplicate
- Failure ảnh hưởng offset và reprocessing thế nào

## Từ vựng quan trọng
- **Record**: key + value + headers + timestamp
- **Topic**: luồng record có tên
- **Partition**: log append-only có thứ tự trong topic
- **Offset**: vị trí trong partition

## Thực hành nhẹ
Nếu bạn đã có Docker, kiểm tra nhanh (bạn sẽ dựng Kafka ở Bài 03):

```powershell
docker version
docker compose version
```

## Checklist
- Tôi mô tả Kafka như một log bền vững, được chia partition
- Tôi biết ordering chỉ đảm bảo theo partition (không phải toàn topic)
- Tôi kể được 3 use case Kafka làm rất tốt

## Lỗi hay gặp
- Dùng Kafka như database và kỳ vọng truy vấn tuỳ ý
- Tự tin “exactly once” mà không hiểu idempotence và transactional processing
