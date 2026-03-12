# Bài 08 — Kafka Connect: connector, CDC, vận hành cơ bản

## Mục tiêu
- Hiểu Kafka Connect là gì và khi nào nên dùng
- Hiểu source vs sink connector
- Biết các vấn đề vận hành: offsets, tasks, scaling, error handling

## Kafka Connect là gì
Kafka Connect là framework để:
- Đưa dữ liệu vào Kafka (source connectors)
- Đưa dữ liệu ra khỏi Kafka (sink connectors)

Vì sao hữu ích:
- Chuẩn hoá pattern tích hợp
- Quản lý offsets/checkpointing cho connector tasks
- Hỗ trợ scale và restart

## Khái niệm connector
- **Connector**: cấu hình mức cao của một tích hợp
- **Task**: đơn vị công việc song song dưới một connector
- **Worker**: tiến trình runtime của Connect

## CDC (Change Data Capture) tổng quan
CDC ghi nhận thay đổi DB (insert/update/delete) thành events.

Cách làm thường gặp:
- Debezium source connector đọc transaction log
- Events được đưa vào Kafka topics
- Downstream service phản ứng hoặc materialize views

## Error handling (rất quan trọng)
Cần chuẩn bị cho:
- Poison pill messages
- Schema sai
- Đích (sink) bị down

Chiến lược thường dùng:
- Dead letter topics
- Retry + backoff
- Alerting + dashboard

## Lab (mang tính khái niệm)
Lộ trình này giữ lab theo hướng vendor-neutral.

Bài tập:
- Kể 3 tích hợp bạn sẽ làm với Connect:
  - DB → Kafka source
  - Kafka → data warehouse sink
  - Kafka → search index sink

Nếu muốn lab thật, có thể bổ sung Connect + demo connector sau.

## Checklist
- Tôi giải thích được source vs sink
- Tôi hiểu tasks/workers và Connect scale thế nào
- Tôi biết CDC là use case phổ biến của Kafka

## Lỗi hay gặp
- Chạy Connect mà không nghĩ về schema governance
- Coi connector là “set and forget” (thực tế phải monitor)
