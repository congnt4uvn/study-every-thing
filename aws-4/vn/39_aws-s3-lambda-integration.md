# Tích Hợp AWS S3 Event Notifications với Lambda

## Tổng Quan
S3 event notifications cung cấp cách thức để nhận thông báo bất cứ khi nào có hành động cụ thể xảy ra trên các đối tượng trong S3 bucket của bạn. Sự tích hợp này với Lambda cho phép xây dựng kiến trúc hướng sự kiện (event-driven) mạnh mẽ.

## S3 Event Notifications

### S3 Event Notifications Là Gì?
S3 event notifications cho phép bạn nhận cảnh báo khi:
- Một đối tượng được **tạo mới**
- Một đối tượng bị **xóa**
- Một đối tượng được **khôi phục**
- Quá trình **sao chép (replication)** đang diễn ra

### Tùy Chọn Lọc
- **Lọc theo prefix**: Lọc theo đường dẫn tiền tố của đối tượng
- **Lọc theo suffix**: Lọc theo phần mở rộng hoặc hậu tố của file

### Use Case Kinh Điển
**Tạo Ảnh Thumbnail**: Tự động tạo ảnh thumbnail cho mỗi hình ảnh được tải lên Amazon S3.

## Các Mô Hình Tích Hợp

### 1. S3 → SNS → SQS (Mô hình Fan-out)
- S3 gửi sự kiện đến SNS topic
- SNS phân phối (fan out) đến nhiều SQS queue
- Nhiều consumer có thể xử lý cùng một sự kiện

### 2. S3 → SQS → Lambda
- S3 gửi sự kiện đến SQS queue
- Lambda function đọc trực tiếp từ SQS queue
- Cung cấp khả năng đệm (buffering) và thử lại (retry)

### 3. S3 → Lambda (Gọi Trực Tiếp)
- S3 event notification gọi trực tiếp Lambda function
- **Gọi bất đồng bộ (asynchronous invocation)**
- Mô hình tích hợp đơn giản nhất

## Xử Lý Lỗi
- Cấu hình **Dead-Letter Queue (DLQ)** sử dụng SQS
- Lưu trữ các lần gọi thất bại để phân tích sau
- Ngăn chặn mất mát sự kiện

## Những Điểm Quan Trọng Cần Lưu Ý

### Thời Gian Gửi Sự Kiện
- Thông thường gửi sự kiện trong vòng vài **giây**
- Đôi khi có thể mất **một phút hoặc lâu hơn**
- Cần lập kế hoạch cho tính nhất quán cuối cùng (eventual consistency)

### Versioning Để Đảm Bảo Độ Tin Cậy
⚠️ **Quan Trọng**: Bật versioning trên S3 bucket của bạn để ngăn chặn mất mát sự kiện.

**Tại sao?** Nếu hai thao tác ghi xảy ra trên cùng một đối tượng vào cùng một thời điểm:
- **Không có versioning**: Bạn có thể chỉ nhận được MỘT thông báo thay vì HAI
- **Có versioning**: Mỗi lần ghi tạo ra một phiên bản duy nhất, đảm bảo tất cả thông báo được gửi

## Mô Hình Kiến Trúc Đơn Giản

```
S3 Bucket (Sự kiện file mới)
    ↓
Lambda Function (Xử lý file)
    ↓
Lưu trữ dữ liệu
    ├── DynamoDB Table
    └── RDS Database
```

### Quy Trình Hoạt Động
1. File mới được tải lên S3 bucket
2. S3 kích hoạt thông báo sự kiện
3. Lambda function tự động được gọi
4. Lambda xử lý file
5. Dữ liệu được chèn vào DynamoDB hoặc RDS database

## Best Practices (Thực Hành Tốt Nhất)
- ✅ Luôn bật versioning cho S3 bucket
- ✅ Cấu hình DLQ cho các lần xử lý thất bại
- ✅ Sử dụng lọc phù hợp để giảm số lần gọi không cần thiết
- ✅ Giám sát các chỉ số thực thi Lambda
- ✅ Triển khai Lambda function có tính idempotent (xử lý sự kiện trùng lặp một cách khéo léo)

## Điểm Chính Cần Nhớ
- S3 event notifications cho phép xử lý theo thời gian thực, hướng sự kiện
- Có nhiều mô hình tích hợp khác nhau (trực tiếp Lambda, qua SNS, qua SQS)
- Versioning rất quan trọng cho độ tin cậy của sự kiện
- Gọi bất đồng bộ cung cấp khả năng mở rộng nhưng cần xử lý lỗi đúng cách
