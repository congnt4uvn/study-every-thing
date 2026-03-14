# AWS Lambda với SQS Event Mapper

## Tổng quan
Hướng dẫn này trình bày cách thiết lập AWS Lambda với SQS (Simple Queue Service) như một event mapper, cho phép các hàm Lambda tự động xử lý các tin nhắn từ hàng đợi SQS.

## Yêu cầu trước
- Tài khoản AWS với quyền phù hợp
- Hiểu biết cơ bản về AWS Lambda
- Quen thuộc với các khái niệm SQS

## Hướng dẫn từng bước

### 1. Tạo Lambda Function
- Truy cập AWS Lambda console
- Nhấp "Create function"
- Tên function: `lambda-SQS`
- Runtime: Python 3.8 (hoặc phiên bản bạn ưa thích)
- Nhấp "Create function"

### 2. Tạo SQS Queue
- Truy cập Amazon SQS console
- Nhấp "Create queue"
- Tên queue: `lambda-demo-SQS`
- Loại queue: Standard queue
- Cuộn xuống và nhấp "Create queue"

### 3. Cấu hình Lambda Trigger
1. Trong Lambda function của bạn, nhấp "Add trigger"
2. Chọn **SQS** từ danh sách các trigger có sẵn
3. Chọn SQS queue: `lambda-demo-SQS`
4. Cấu hình các thiết lập batch:
   - **Batch size**: Số lượng tin nhắn nhận được trong một batch (từ 1 đến số tối đa cho phép)
   - **Batch window**: Thời gian tính bằng giây để thu thập các bản ghi trước khi gọi function
5. Bật trigger
6. Nhấp "Add"

### 4. Vấn đề thường gặp: Quyền IAM
Khi thêm SQS trigger, bạn có thể gặp lỗi:

**Lỗi**: "The execution role does not have permissions to call ReceiveMessage on SQS"

**Giải pháp**: Lambda execution role cần các quyền sau:
- `sqs:ReceiveMessage`
- `sqs:DeleteMessage`
- `sqs:GetQueueAttributes`

Thêm các quyền này vào IAM policy của Lambda execution role.

## Các khái niệm chính

### Xử lý theo Batch
- **Batch Size**: Kiểm soát số lượng tin nhắn Lambda nhận cùng một lúc
- **Batch Window**: Cho phép Lambda chờ và thu thập thêm tin nhắn để xử lý hiệu quả
- Batch lớn hơn giảm số lần gọi Lambda

### Event Mappers
AWS Lambda hỗ trợ nhiều event mapper bao gồm:
- Amazon SQS
- Amazon Kinesis
- Amazon DynamoDB Streams
- Amazon MSK (Managed Streaming for Apache Kafka)
- Các nguồn sự kiện từ đối tác

## Thực hành tốt nhất
1. Cấu hình batch size phù hợp dựa trên nhu cầu xử lý của bạn
2. Đặt batch window hợp lý để cân bằng giữa độ trễ và hiệu quả
3. Đảm bảo quyền IAM phù hợp trước khi bật trigger
4. Theo dõi các chỉ số Lambda và độ sâu hàng đợi SQS
5. Triển khai xử lý lỗi và dead-letter queue

## Tóm tắt
Hướng dẫn này minh họa cách kết nối AWS Lambda với SQS sử dụng event mapper, cho phép xử lý tin nhắn serverless ở quy mô lớn.
