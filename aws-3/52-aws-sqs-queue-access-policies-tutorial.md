# Hướng Dẫn AWS SQS Queue Access Policies

## Giới Thiệu

SQS Queue Access Policies là các chính sách tài nguyên tương tự như S3 Bucket policies. Chúng là các chính sách IAM dạng JSON mà bạn gắn trực tiếp vào SQS Queue để kiểm soát quyền truy cập. Hướng dẫn này đề cập đến hai trường hợp sử dụng quan trọng cho SQS Queue Access Policies.

## Trường Hợp 1: Truy Cập Xuyên Tài Khoản (Cross-Account Access)

### Kịch Bản
Bạn có một SQS queue trong một tài khoản AWS, và một tài khoản khác cần truy cập queue đó (ví dụ: một EC2 instance cần lấy tin nhắn).

### Triển Khai
Để cho phép truy cập xuyên tài khoản, hãy tạo Queue Access Policy và gắn nó vào SQS Queue trong tài khoản đầu tiên.

**Ví Dụ Policy:**
```json
{
  "Principal": {
    "AWS": "111122223333"
  },
  "Action": "sqs:ReceiveMessage",
  "Resource": "<queue-arn>"
}
```

Policy này cho phép tài khoản AWS `111122223333` nhận tin nhắn từ SQS Queue.

## Trường Hợp 2: S3 Event Notifications Đến SQS

### Kịch Bản
Một S3 bucket xuất bản thông báo sự kiện đến SQS Queue. Khi một object được tải lên S3 bucket, một tin nhắn sẽ tự động được gửi đến SQS Queue.

### Triển Khai
SQS Queue phải cấp quyền cho S3 Bucket để ghi tin nhắn vào nó.

**Ví Dụ Policy:**
```json
{
  "Action": "sqs:SendMessage",
  "Principal": {
    "AWS": "*"
  },
  "Condition": {
    "ArnLike": {
      "aws:SourceArn": "arn:aws:s3:::bucket1"
    },
    "StringEquals": {
      "aws:SourceAccount": "<account-id>"
    }
  }
}
```

Policy này cho phép S3 bucket có tên `bucket1` gửi tin nhắn đến SQS Queue, miễn là tài khoản nguồn khớp với chủ sở hữu S3 bucket.

## Hướng Dẫn Thực Hành: S3 Event Notifications Đến SQS

### Bước 1: Tạo SQS Queue

1. Điều hướng đến Amazon SQS
2. Tạo queue mới với tên `events-from-s3`
3. Giữ cài đặt mặc định
4. Đối với Access Policy, ban đầu chọn phương thức "Basic"
5. Chọn "Only the queue owner" cho người có thể gửi tin nhắn
6. Tạo queue

### Bước 2: Tạo S3 Bucket

1. Điều hướng đến Amazon S3
2. Tạo bucket mới: `demo-sqs-queue-access-policy`
3. Nhấp "Create bucket"

### Bước 3: Cấu Hình S3 Event Notification (Lần Thử Đầu Tiên)

1. Vào Properties của S3 bucket
2. Cuộn xuống Event notifications
3. Tạo event notification:
   - **Tên:** NewObjects
   - **Event types:** All object create events
   - **Destination:** SQS Queue
   - **Queue:** EventFrom S3
4. Nhấp "Save changes"

**Kết Quả:** Bạn sẽ gặp lỗi - "Unable to validate the following destination configurations"

Lỗi này xảy ra vì SQS Queue chưa có access policy phù hợp để cho phép S3 bucket ghi vào nó.

### Bước 4: Cập Nhật SQS Queue Access Policy

1. Điều hướng đến SQS Queue
2. Vào phần Access Policy
3. Chỉnh sửa policy
4. Thay thế bằng policy sau:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "<queue-arn>",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:::demo-sqs-queue-access-policy"
        },
        "StringEquals": {
          "aws:SourceAccount": "<your-account-id>"
        }
      }
    }
  ]
}
```

**Quan Trọng:** Thay thế các giá trị sau:
- `<queue-arn>`: ARN của SQS Queue của bạn
- `<your-account-id>`: ID tài khoản AWS của bạn
- Cập nhật tên bucket trong `aws:SourceArn` nếu khác

5. Lưu policy (đảm bảo cú pháp JSON hợp lệ)

### Bước 5: Thử Lại Cấu Hình S3 Event Notification

1. Quay lại event notifications của S3 bucket
2. Tạo lại event notification với cùng cài đặt
3. Lần này nó sẽ lưu thành công

### Bước 6: Kiểm Tra Tích Hợp

1. Điều hướng đến Amazon SQS
2. Chọn queue của bạn và nhấp "Send and receive messages"
3. Nhấp "Poll for messages"
4. Bạn sẽ thấy một tin nhắn sự kiện test được gửi bởi Amazon S3
5. Tùy chọn, tải một file lên S3 bucket và xác minh tin nhắn mới xuất hiện trong SQS Queue

## Những Điểm Chính Cần Nhớ

- **SQS Queue Access Policies** là các chính sách IAM JSON được gắn trực tiếp vào SQS Queues
- **Truy cập xuyên tài khoản** yêu cầu policy chỉ định principal AWS account
- **S3 event notifications** yêu cầu SQS Queue cấp quyền SendMessage cho dịch vụ S3
- Luôn sử dụng **conditions** để hạn chế quyền truy cập đến các S3 buckets và tài khoản cụ thể
- Kỳ thi có thể kiểm tra kiến thức của bạn về các policy cần thiết cho truy cập xuyên tài khoản hoặc S3 event notifications

## Câu Hỏi Thường Gặp Trong Kỳ Thi

1. Điều gì cần thiết để có quyền truy cập xuyên tài khoản vào SQS Queue?
2. Policy nào cần thiết để S3 xuất bản event notifications đến SQS?
3. Những actions và conditions nào nên có trong Queue Access Policy?

## Kết Luận

Bằng cách sửa đổi SQS Queue Access Policy, bạn có thể cho phép truy cập an toàn từ các dịch vụ AWS khác và các tài khoản khác. Đây là một khái niệm cơ bản để tích hợp các dịch vụ AWS và thường xuyên được kiểm tra trong các kỳ thi chứng chỉ AWS.