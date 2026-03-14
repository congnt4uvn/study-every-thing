# AWS Lambda Destinations

## Tổng Quan
Lambda Destinations là tính năng cho phép bạn định tuyến kết quả của các lần gọi Lambda function bất đồng bộ đến các dịch vụ AWS khác nhau dựa trên điều kiện thành công hoặc thất bại.

## Các Khái Niệm Chính

### Lambda Destinations là gì?
- **Destinations** là các dịch vụ AWS nhận kết quả thực thi của Lambda function
- Có thể cấu hình cho cả trường hợp thực thi **thành công** và **thất bại**
- Hỗ trợ cho các lần gọi bất đồng bộ và các lần gọi dựa trên stream

### Các Loại Destination Được Hỗ Trợ
- **SQS Queue** - Simple Queue Service (Hàng đợi)
- **SNS Topic** - Simple Notification Service (Thông báo)
- **Lambda Function** - Lambda function khác
- **EventBridge** - Event bus cho kiến trúc hướng sự kiện

## Ví Dụ Thực Hành: Cấu Hình SQS Destinations

### Bước 1: Tạo SQS Queues
Tạo hai hàng đợi để xử lý các kết quả khác nhau:

1. **Hàng đợi Thành công**: `S3-success`
   - Nhận tin nhắn khi Lambda thực thi thành công
   
2. **Hàng đợi Thất bại**: `S3-failure`
   - Nhận tin nhắn khi Lambda thực thi thất bại

### Bước 2: Cấu Hình Lambda Function
1. Điều hướng đến Lambda function của bạn (ví dụ: `lambda-S3-function`)
2. Vào tab **Configuration** (Cấu hình)
3. Chọn **Destinations**
4. Nhấp **Add destination** (Thêm destination)

### Bước 3: Thêm Failure Destination
- **Source type**: Asynchronous invocation (Gọi bất đồng bộ)
- **Condition**: On failure (Khi thất bại)
- **Destination type**: SQS queue
- **Destination**: Chọn hàng đợi `S3-failure`

### Bước 4: Thêm Success Destination
- **Source type**: Asynchronous invocation (Gọi bất đồng bộ)
- **Condition**: On success (Khi thành công)
- **Destination type**: SQS queue
- **Destination**: Chọn hàng đợi `S3-success`

## Quyền IAM

### Tự Động Thêm Quyền
Khi bạn cấu hình destination thông qua Lambda console, nó sẽ tự động thêm các quyền IAM cần thiết vào execution role của Lambda.

### Quyền Bắt Buộc
Execution role cần quyền để gửi tin nhắn đến dịch vụ destination. Đối với SQS, bao gồm:
- Quyền `sqs:SendMessage`
- Resource ARN của hàng đợi destination

### Xác Minh
Bạn có thể xác minh quyền bằng cách:
1. Mở cấu hình Lambda function
2. Vào tab **Permissions** (Quyền)
3. Nhấp vào **Execution role**
4. Xem lại các IAM policies đã được gắn

Tên policy ví dụ: `AmazonLambdaSQSQueueDestinationExecutionRole`

## Các Trường Hợp Sử Dụng

### Khi Nào Nên Dùng Destinations
- **Xử Lý Lỗi**: Định tuyến các lần thực thi thất bại đến dead-letter queue để phân tích
- **Theo Dõi Thành Công**: Gửi chi tiết thực thi thành công đến hệ thống giám sát
- **Điều Phối Workflow**: Kết nối các Lambda functions với nhau
- **Ghi Log Kiểm Toán**: Lưu trữ bản ghi của tất cả các lần gọi

### Các Loại Invocation Khác
- **Asynchronous Invocation**: Lambda đưa sự kiện vào hàng đợi và trả về thành công ngay lập tức
- **Stream Invocation**: Cho Kinesis hoặc DynamoDB streams được ánh xạ với Lambda functions

## Các Phương Pháp Tốt Nhất
1. Luôn cấu hình cả success và failure destinations cho các workflow quan trọng
2. Giám sát các destination queues thường xuyên
3. Sử dụng cấu hình retry phù hợp cho các lần gọi thất bại
4. Kiểm tra quyền IAM trước khi triển khai lên production
5. Cân nhắc sử dụng EventBridge cho các kịch bản định tuyến phức tạp

## Tài Nguyên Bổ Sung
- Tài liệu AWS Lambda Destinations
- Phương Pháp Tốt Nhất Cấu Hình SQS Queue
- Các Mẫu Xử Lý Lỗi Lambda
