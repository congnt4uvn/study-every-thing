# Amazon Managed Service cho Apache Flink

## Tổng Quan

Amazon Managed Service cho Apache Flink (trước đây gọi là Kinesis Data Analytics for Apache Flink) là một dịch vụ được quản lý hoàn toàn, cho phép bạn xử lý và phân tích dữ liệu streaming theo thời gian thực bằng cách sử dụng các ứng dụng Apache Flink.

## Apache Flink là gì?

Apache Flink là một framework mạnh mẽ để xử lý luồng dữ liệu theo thời gian thực. Nó hỗ trợ nhiều ngôn ngữ lập trình:
- Java
- SQL
- Scala

## Tính Năng Chính

### Nguồn Dữ Liệu
Amazon Managed Service cho Apache Flink có thể đọc dữ liệu từ:
- **Amazon Kinesis Data Streams** - Cho streaming dữ liệu thời gian thực
- **Amazon MSK (Managed Streaming for Apache Kafka)** - Dịch vụ quản lý cho Apache Kafka

> **Lưu ý Quan Trọng**: Flink có thể đọc từ Kinesis Data Streams nhưng **không thể** đọc từ Amazon Data Firehose. Đây là câu hỏi thường gặp trong kỳ thi.

### Hạ Tầng Được Quản Lý
AWS xử lý việc quản lý hạ tầng cho bạn:
- **Cung Cấp Tài Nguyên Tính Toán** - AWS tự động cung cấp các tài nguyên tính toán cần thiết
- **Tính Toán Song Song** - Hỗ trợ xử lý song song tích hợp sẵn
- **Tự Động Mở Rộng** - Tự động mở rộng quy mô dựa trên khối lượng công việc

### Quản Lý Ứng Dụng
- **Sao Lưu Tự Động** - Được thực hiện thông qua checkpoints và snapshots
- **Cluster Được Quản Lý** - Chạy trên cluster được quản lý hoàn toàn trên AWS

### Chuyển Đổi Dữ Liệu
- Truy cập đầy đủ vào các tính năng lập trình của Apache Flink
- Linh hoạt hoàn toàn trong các loại chuyển đổi bạn có thể áp dụng cho luồng dữ liệu
- Khả năng xử lý dữ liệu theo thời gian thực

## Trường Hợp Sử Dụng

Amazon Managed Service cho Apache Flink được thiết kế đặc biệt cho:
- Xử lý luồng dữ liệu theo thời gian thực
- Phân tích thời gian thực
- Chuyển đổi luồng dữ liệu
- Xử lý sự kiện phức tạp

## Điểm Chính Cần Nhớ

1. Trước đây có tên là "Kinesis Data Analytics for Apache Flink"
2. Dịch vụ Apache Flink được quản lý hoàn toàn trên AWS
3. Hỗ trợ Java, SQL và Scala
4. Có thể đọc từ Kinesis Data Streams và Amazon MSK
5. **Không thể** đọc từ Amazon Data Firehose
6. Cung cấp tự động mở rộng và tính toán song song
7. Bao gồm sao lưu tự động thông qua checkpoints và snapshots
8. Chỉ dành riêng cho xử lý luồng dữ liệu

## Mẹo Thi

- Hãy nhớ rằng Flink **không thể** đọc từ Amazon Data Firehose - đây là một câu hỏi lừa phổ biến trong kỳ thi
- Tập trung vào khả năng xử lý luồng thời gian thực của nó
- Hiểu rõ sự khác biệt giữa Kinesis Data Streams (được hỗ trợ) và Data Firehose (không được hỗ trợ)