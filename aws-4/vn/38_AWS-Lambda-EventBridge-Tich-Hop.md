# Tích Hợp AWS Lambda và EventBridge

## Tổng Quan
Hướng dẫn này trình bày cách tích hợp AWS Lambda với Amazon EventBridge để tự động gọi các hàm Lambda theo lịch trình hoặc dựa trên các sự kiện.

## Tạo Lambda Function

1. **Tạo Lambda function mới**
   - Tên function: `lambda-demo-eventbridge`
   - Runtime: Python 3.9
   - Function sẽ được gọi bởi EventBridge

## Cấu Hình EventBridge

### Tạo EventBridge Rule

1. **Truy cập EventBridge Console**
   - Vào mục **Rules** (Quy tắc)
   - Tạo rule mới

2. **Cấu Hình Rule**
   - Tên rule: `InvokeLambdaEveryMinute`
   - Event bus: Default Event bus

3. **Các Loại Rule**
   
   **Tùy chọn 1: Event Pattern** (Mẫu Sự kiện)
   - Sử dụng để khớp các sự kiện xảy ra trong AWS
   - Ví dụ:
     - Code được commit vào CodeCommit
     - EC2 instance bị terminate
     - Các sự kiện AWS service khác
   
   **Tùy chọn 2: Schedule** (Lịch trình - Dùng trong demo này)
   - Kích hoạt function theo lịch trình định kỳ
   - Có thể sử dụng biểu thức Cron hoặc khoảng thời gian cố định

### Thiết Lập Lịch Trình

1. **Tùy Chọn Schedule Pattern**
   - **Biểu thức Cron**: Cho các mẫu lịch trình phức tạp
   - **Fixed-rate schedule**: Cho các khoảng thời gian đều đặn (ví dụ: mỗi 1 phút)

2. **Cấu Hình**
   - Đặt lịch chạy mỗi 1 phút
   - Click **Next**

### Cấu Hình Target (Mục Tiêu)

1. **Chọn Loại Target**
   - Chọn **Lambda function**

2. **Chọn Lambda Function**
   - Function: `lambda-demo-eventbridge`

3. **Cài Đặt Bổ Sung** (Tùy chọn)
   - Version hoặc alias cụ thể
   - Cấu hình dead-letter queue
   - Số lần thử lại tối đa
   - Các cài đặt nâng cao khác

## Các Khái Niệm Chính

### EventBridge vs EventBridge Scheduler
- **EventBridge Rules**: Cách gọi truyền thống dựa trên quy tắc
- **EventBridge Scheduler**: Dịch vụ mới với khả năng lập lịch nâng cao
- Cả hai cung cấp chức năng tương tự với giao diện khác nhau

### Resource Policies (Chính Sách Tài Nguyên)
EventBridge tự động quản lý các quyền cần thiết để gọi Lambda function thông qua resource policies.

## Các Trường Hợp Sử Dụng

- **Scheduled Tasks**: Chạy Lambda functions theo khoảng thời gian đều đặn
- **Event-Driven Architecture**: Phản hồi các sự kiện từ AWS services
- **Automation**: Kích hoạt workflows dựa trên các thay đổi hạ tầng AWS
- **Monitoring và Alerts**: Xử lý sự kiện và gửi thông báo

## Thực Hành Tốt Nhất

1. **Xử Lý Lỗi**: Cấu hình dead-letter queues cho các lần gọi thất bại
2. **Retry Logic**: Đặt số lần thử lại tối đa phù hợp
3. **Monitoring**: Sử dụng CloudWatch để giám sát các lần gọi function
4. **Version Control**: Sử dụng Lambda versions và aliases cho triển khai production
5. **Testing**: Kiểm tra kỹ các EventBridge rules trước khi đưa vào production

## Tài Liệu Tham Khảo

- Tài liệu AWS Lambda
- Tài liệu Amazon EventBridge
- Tài liệu EventBridge Scheduler
