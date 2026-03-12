# Bài 09 — Stream processing: Kafka Streams nền tảng

## Mục tiêu
- Hiểu Kafka Streams ở mức tổng quan
- Hiểu khái niệm stream vs table
- Nhận biết khi nào Streams phù hợp

## Kafka Streams là gì
Kafka Streams là thư viện Java để xây ứng dụng stream processing.

Nó cung cấp:
- Xử lý có state (aggregation, joins)
- Pattern xử lý có thể đạt exactly-once (với cấu hình đúng)
- Local state stores kèm changelog topics

## Stream vs Table (mô hình tư duy)
- **Stream**: chuỗi event bất biến theo thời gian
- **Table**: giá trị mới nhất theo key (materialized view)

Streams thường biến stream → table qua aggregation, rồi table → stream qua change events.

## Pattern phổ biến
- Filter/enrichment
- Windowed aggregation (vd số event mỗi phút)
- Joins (stream-stream, stream-table)

## Vận hành
- Scale phụ thuộc partitions (lại là partitions)
- Stateful operations tạo local state cần quản lý
- Rebalancing/restore có thể tốn thời gian

## Lab (bài tập thiết kế)
Với `demo.orders`:
1. Định nghĩa tác vụ: “đếm số order PAID theo cửa sổ 1 phút”.
2. Chọn keying strategy.
3. Định nghĩa schema cho output topic.

## Checklist
- Tôi giải thích được stream vs table
- Tôi biết partitions quyết định scale cho stream app
- Tôi kể được 2–3 pattern Streams hỗ trợ

## Lỗi hay gặp
- Under-partition input topic khiến khó scale về sau
- Bỏ qua thời gian restore state store khi deploy
