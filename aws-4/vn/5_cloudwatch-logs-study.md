# Ghi chú học AWS — CloudWatch Logs

## 1) CloudWatch Logs dùng để làm gì?
- **CloudWatch Logs** là dịch vụ quản lý tập trung để **lưu trữ log ứng dụng/dịch vụ trên AWS**.
- Đây là nơi phù hợp để gom log từ nhiều dịch vụ AWS và cả workload của bạn.

## 2) Khái niệm cốt lõi
### Log group
- **Log group** là “nhóm” logic chứa log.
- Tên log group **tự đặt** (thường dùng theo tên ứng dụng).

### Log stream
- Bên trong một log group sẽ có nhiều **log stream**.
- Log stream thường đại diện cho **một nguồn log cụ thể**, ví dụ:
  - một instance của ứng dụng,
  - một file log cụ thể,
  - một container cụ thể (trong một cluster).

### Retention (chính sách hết hạn)
- Bạn cấu hình thời gian giữ log:
  - **Giữ vĩnh viễn** (không hết hạn), hoặc
  - hết hạn từ **1 ngày đến 10 năm**.

### Mã hóa
- Log được **mã hóa mặc định**.
- Có thể cấu hình mã hóa bằng **KMS (khóa do bạn quản lý)** nếu cần.

## 3) Đưa log đi đâu được? (destinations)
CloudWatch Logs có thể xuất/stream log tới:
- **Amazon S3** (xuất theo lô/batch)
- **Kinesis Data Streams** (stream real-time)
- **Kinesis Data Firehose** (đẩy dữ liệu gần real-time)
- **AWS Lambda**
- **Amazon OpenSearch Service**

## 4) Log vào CloudWatch Logs bằng cách nào? (nguồn log)
Các cách gửi log:
- Dùng **SDK**
- **CloudWatch Logs Agent** (cũ / đang bị thay thế dần)
- **CloudWatch Unified Agent** (khuyến nghị hơn so với Logs Agent)

Một số dịch vụ AWS thường đẩy log vào CloudWatch Logs:
- **Elastic Beanstalk** (log ứng dụng)
- **ECS** (log container)
- **AWS Lambda** (log function)
- **VPC Flow Logs** (metadata lưu lượng mạng VPC)
- **API Gateway** (request vào API)
- **CloudTrail** (có thể gửi log dựa trên filter)
- **Route 53** (log truy vấn DNS)

## 5) Truy vấn log: CloudWatch Logs Insights
**CloudWatch Logs Insights** là tính năng truy vấn trong CloudWatch Logs.

Cách dùng:
- Viết query bằng **ngôn ngữ truy vấn của Logs Insights**
- Chọn **khoảng thời gian** cần truy vấn
- Nhận kết quả dạng **biểu đồ/visualization** và xem **các dòng log** tạo ra kết quả đó

Tính năng hữu ích:
- Có nhiều **mẫu query** sẵn trên console (event gần nhất, lỗi/exception, lọc theo IP, ...)
- Field được **tự động nhận diện** từ log
- Có thể:
  - lọc theo điều kiện,
  - tính toán thống kê tổng hợp,
  - sắp xếp,
  - giới hạn số lượng kết quả.
- Lưu query và thêm vào **CloudWatch Dashboards**.
- Truy vấn **nhiều log group cùng lúc**, kể cả ở **nhiều account** khác nhau.

Lưu ý quan trọng:
- Logs Insights là **query engine, không phải real-time engine** — chỉ truy vấn **dữ liệu lịch sử** tại thời điểm bạn chạy query.

## 6) Export vs subscription (batch vs real-time)
### Batch export sang S3
- Xuất log sang **Amazon S3** theo dạng batch.
- Có thể mất **tối đa 12 giờ** để hoàn tất.
- API để bắt đầu export: **`CreateExportTask`**.
- Không phải real-time / near real-time.

### Stream real-time: subscription filters
- Dùng **CloudWatch Logs subscription filters** để stream log **real-time**.
- Đích nhận có thể là:
  - **Kinesis Data Streams**
  - **Kinesis Data Firehose**
  - **AWS Lambda**
- Có thể cấu hình **subscription filter** để chọn loại log event cần gửi.

## 7) Gom log nhiều account/region (tổng quan)
Bạn có thể gom log từ **nhiều account và region** về một đích chung.

Luồng tham khảo trong nội dung:
- CloudWatch Logs (nhiều account/region)
  → **Subscription filter**
  → **Destination** (đại diện cho Kinesis Data Stream ở account nhận)
  → (tuỳ chọn) **Kinesis Data Firehose**
  → **Amazon S3** (near real-time)

Các thành phần chính:
- **Destination**: đối tượng “ảo” đại diện cho Kinesis Data Stream ở account nhận.
- **Destination access policy**: cho phép account gửi đẩy dữ liệu vào destination.
- **IAM role (account nhận)**: có quyền ghi record vào Kinesis Data Stream.
- Cấu hình trust/assume-role để account gửi có thể sử dụng role này.

## 8) Tự kiểm tra (câu hỏi ôn tập)
- Phân biệt **log group** và **log stream**.
- Khi nào dùng **S3 export** và khi nào dùng **subscription filter**?
- Vì sao Logs Insights **không phải real-time**?
- Kể ít nhất **4 dịch vụ AWS** có thể đẩy log vào CloudWatch Logs.
- Mô tả các phần khi stream cross-account: destination, policy, role.

## 9) Flashcards nhanh
- **Retention** → 1 ngày đến 10 năm (hoặc không hết hạn)
- **API batch export** → `CreateExportTask`
- **Cơ chế real-time** → Subscription filter
- **Mã hóa mặc định** → Có (có thể dùng KMS key riêng)
