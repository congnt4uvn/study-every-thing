# AWS Lambda - Ghi Log, Giám Sát và Theo Dõi

## Tổng Quan
Tài liệu này giới thiệu cách AWS Lambda xử lý các khả năng ghi log, giám sát và theo dõi.

## Tích Hợp CloudWatch Logs

Lambda có tích hợp sẵn với **CloudWatch Logs**, nơi tất cả các log thực thi của Lambda được tự động lưu trữ.

### Yêu Cầu
- Lambda function phải có **execution role** với IAM policy phù hợp
- Policy phải cho phép Lambda function ghi vào CloudWatch Logs
- Điều này đã được bao gồm trong **Lambda basic execution role** theo mặc định

## CloudWatch Metrics

CloudWatch metrics có thể được xem trong:
- CloudWatch Metrics UI
- Lambda UI

### Các Metrics Có Sẵn
Các metrics sau đây có sẵn cho Lambda functions:
- **Invocations** - Số lần function được gọi
- **Duration** - Thời gian function thực thi
- **Concurrent Executions** - Số lượng thực thi đồng thời
- **Error Counts** - Số lượng lỗi
- **Success Rate** - Tỷ lệ thành công
- **Throttles** - Số lần bị giới hạn (throttled)
- **Async Delivery Failures** - Lỗi trong các lần gọi bất đồng bộ
- **Iterator Age** - (Đối với Kinesis/DynamoDB streams) Mức độ chậm trễ trong việc đọc stream

## X-Ray Tracing

AWS X-Ray cung cấp distributed tracing cho Lambda functions.

### Các Bước Thiết Lập
1. **Bật Active Tracing** trong cấu hình Lambda
2. **Sử dụng X-Ray SDK** trong code của bạn
3. **Cấu hình IAM Role** với managed policy: `AWS X-Ray daemon write access`

### Biến Môi Trường
Các biến môi trường sau được sử dụng để giao tiếp với X-Ray:
- `_X_AMZN_TRACE_ID`
- `AWS_XRAY_CONTEXT_MISSING`
- `AWS_XRAY_DAEMON_ADDRESS` - Chỉ định IP và port nơi X-Ray daemon đang chạy

Các biến môi trường này có thể được truy cập giống như các biến môi trường khác trong Lambda.

### Lưu Ý Quan Trọng
- X-Ray daemon chạy tự động khi active tracing được bật
- Biến `AWS_XRAY_DAEMON_ADDRESS` là quan trọng nhất cho mục đích thi
- Nó chứa địa chỉ IP và port của X-Ray daemon

## Điểm Chính Cần Nhớ
- Lambda tự động ghi log vào CloudWatch Logs (với quyền IAM phù hợp)
- CloudWatch Metrics cung cấp khả năng hiển thị hiệu suất Lambda
- X-Ray tracing dễ dàng được bật thông qua cấu hình Lambda
- IAM roles phù hợp là bắt buộc cho cả tích hợp CloudWatch và X-Ray
