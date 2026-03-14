# AWS Lambda - Gọi Bất Đồng Bộ (Asynchronous Invocation)

## Tổng Quan

AWS Lambda hỗ trợ nhiều kiểu gọi hàm khác nhau. Tài liệu này tập trung vào **gọi bất đồng bộ** (asynchronous invocations), khác với gọi đồng bộ ở cách xử lý và quản lý các sự kiện.

## Gọi Bất Đồng Bộ Là Gì?

Gọi bất đồng bộ được sử dụng khi các dịch vụ AWS gọi Lambda function ở phía sau mà không cần chờ phản hồi ngay lập tức.

### Các Dịch Vụ Sử Dụng Gọi Bất Đồng Bộ

- **Amazon S3** - Thông báo sự kiện S3 cho các file mới
- **Amazon SNS** - Chủ đề SNS
- **Amazon CloudWatch Events** - Kích hoạt theo sự kiện
- Và nhiều dịch vụ khác...

## Cách Hoạt Động

### Ví Dụ: Luồng Sự Kiện S3 Bucket

1. **Kích Hoạt Sự Kiện**: Một file mới được tải lên S3 bucket
2. **Thông Báo Sự Kiện S3**: S3 tạo thông báo sự kiện
3. **Dịch Vụ Lambda**: Sự kiện được gửi đến dịch vụ Lambda
4. **Hàng Đợi Sự Kiện Nội Bộ**: Các sự kiện được đặt vào hàng đợi nội bộ
5. **Xử Lý**: Lambda function đọc và xử lý sự kiện từ hàng đợi

```
S3 Bucket → Thông Báo S3 → Dịch Vụ Lambda → Hàng Đợi → Lambda Function
```

## Cơ Chế Thử Lại (Retry)

Khi có lỗi xảy ra, Lambda tự động thử lại các lần gọi thất bại:

- **Tổng Số Lần Thử**: 3 lần
- **Lần Thử Thứ Nhất**: Ngay lập tức
- **Lần Thử Thứ Hai**: 1 phút sau lần đầu
- **Lần Thử Thứ Ba**: 2 phút sau lần thứ hai

### Lưu Ý Quan Trọng

⚠️ **Lambda function có thể xử lý cùng một sự kiện nhiều lần** do cơ chế thử lại.

## Tính Idempotent (Bất Biến)

### Idempotent Là Gì?

**Idempotency** (tính bất biến) có nghĩa là xử lý cùng một sự kiện nhiều lần vẫn cho ra kết quả giống nhau.

### Tại Sao Quan Trọng

- Việc thử lại có thể gây ra xử lý trùng lặp
- Các function không idempotent có thể gây vấn đề (ví dụ: tạo bản ghi trùng trong database, tính phí nhiều lần)
- Lambda function của bạn **nên được thiết kế idempotent** để xử lý an toàn khi thử lại

### Khả Năng Quan Sát

Khi có thử lại, bạn sẽ thấy:
- **Các bản ghi log trùng lặp** trong CloudWatch Logs
- Nhiều bản ghi thực thi cho cùng một sự kiện

## Dead Letter Queue (DLQ) - Hàng Đợi Thư Chết

### Mục Đích

Sau khi tất cả các lần thử đều thất bại, các sự kiện lỗi có thể được gửi đến Dead Letter Queue để xử lý sau.

### Các Dịch Vụ DLQ Được Hỗ Trợ

- **Amazon SQS** - Simple Queue Service (Dịch vụ Hàng Đợi Đơn Giản)
- **Amazon SNS** - Simple Notification Service (Dịch vụ Thông Báo Đơn Giản)

### Cách Sử Dụng DLQ

1. Định nghĩa một DLQ (SQS queue hoặc SNS topic)
2. Cấu hình Lambda function để sử dụng DLQ
3. Các sự kiện thất bại sẽ được gửi đến DLQ sau khi thử lại hết
4. Xử lý hoặc điều tra các sự kiện thất bại sau

## Các Điểm Chính Cần Nhớ

✅ Gọi bất đồng bộ sử dụng hàng đợi sự kiện nội bộ
✅ Lambda tự động thử lại 3 lần khi có lỗi
✅ Luôn thiết kế Lambda function có tính idempotent
✅ Cấu hình DLQ để xử lý các sự kiện thất bại vĩnh viễn
✅ Theo dõi CloudWatch Logs để phát hiện log trùng lặp (dấu hiệu thử lại)

## Thực Hành Tốt Nhất

1. **Thiết Kế Idempotent**: Đảm bảo function có thể xử lý an toàn cùng một sự kiện nhiều lần
2. **Triển Khai DLQ**: Luôn cấu hình Dead Letter Queue để bắt các sự kiện thất bại
3. **Giám Sát Thử Lại**: Theo dõi CloudWatch Logs để phát hiện các mẫu lỗi liên tục
4. **Xử Lý Lỗi Tốt**: Triển khai xử lý lỗi đúng cách để giảm thiểu thử lại
5. **Đặt Timeout Phù Hợp**: Cấu hình thời gian timeout cho function để tránh thử lại không cần thiết

---

*Tài Liệu Học Tập - AWS Lambda Gọi Bất Đồng Bộ*
