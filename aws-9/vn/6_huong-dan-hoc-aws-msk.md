# Tài Liệu Học AWS: Amazon MSK (Managed Streaming for Apache Kafka)

## 1. Amazon MSK là gì?
Amazon MSK là dịch vụ Apache Kafka được quản lý hoàn toàn trên AWS.

Với Amazon MSK, bạn có thể:
- Tạo, cập nhật và xóa cụm Kafka.
- Triển khai cụm trong VPC của bạn.
- Chạy đa AZ (tối đa 3 Availability Zones) để tăng tính sẵn sàng cao.
- Tự động khôi phục khi có lỗi Kafka phổ biến.
- Lưu dữ liệu trên EBS trong thời gian rất dài (trả phí theo dung lượng lưu trữ).

## 2. MSK Serverless
MSK Serverless cho phép chạy Kafka mà không cần tự quản lý server hay dung lượng.

AWS tự động xử lý:
- Cấp phát hạ tầng
- Tự động mở rộng tài nguyên tính toán
- Tự động mở rộng lưu trữ

Phù hợp khi bạn muốn giảm công việc vận hành.

## 3. Kiến thức cơ bản về Apache Kafka
Một hệ thống Kafka gồm:
- **Brokers**: Các máy chủ Kafka trong cụm.
- **Producers**: Ứng dụng gửi dữ liệu vào topic.
- **Topics**: Luồng dữ liệu (có thể chia partition và nhân bản).
- **Consumers**: Ứng dụng đọc và xử lý dữ liệu từ topic.

Nguồn dữ liệu producer (theo nội dung gốc):
- Kinesis
- IoT
- RDS

Đích dữ liệu consumer (theo nội dung gốc):
- EMR
- S3
- SageMaker
- Kinesis
- RDS

## 4. So sánh MSK và Kinesis Data Streams (trọng tâm thi)

### Điểm giống
Cả hai đều hỗ trợ streaming dữ liệu thời gian thực.

### Điểm khác chính
- **Kích thước message**:
  - Kinesis Data Streams: giới hạn 1 MB/message.
  - MSK (Kafka): mặc định khoảng 1 MB, có thể cấu hình lớn hơn (ví dụ 10 MB).

- **Đơn vị scale**:
  - Kinesis: Shards.
  - MSK: Topics và partitions.

- **Cách scale**:
  - Kinesis: tăng/giảm bằng split/merge shard.
  - MSK: có thể thêm partition, không thể xóa partition.

- **Mã hóa khi truyền (in-flight)**:
  - Kinesis: hỗ trợ in-flight encryption.
  - MSK: plaintext hoặc TLS.

- **Mã hóa khi lưu (at-rest)**:
  - Cả hai đều hỗ trợ.

- **Data retention**:
  - Kinesis có thời gian retention cấu hình.
  - MSK có thể giữ dữ liệu rất lâu (kể cả trên 1 năm) miễn là trả phí EBS.

## 5. Cách đọc dữ liệu từ MSK
Các cách phổ biến:
- Kinesis Data Analytics for Apache Flink
- AWS Glue streaming ETL (Spark Streaming)
- AWS Lambda làm consumer qua event source
- Tự viết Kafka consumer chạy trên EC2, ECS hoặc EKS

## 6. Ghi nhớ nhanh cho kỳ thi
- Amazon MSK = Kafka được quản lý trên AWS.
- MSK Serverless = không cần quản lý server/dung lượng.
- Triển khai đa AZ để tăng độ sẵn sàng.
- Scale trong MSK chủ yếu bằng cách thêm partitions.
- Lưu dữ liệu dài hạn trong MSK phụ thuộc chi phí EBS.
