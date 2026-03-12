# Amazon S3 Event Notifications - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách thiết lập và kiểm tra Amazon S3 Event Notifications, cho phép bạn tự động kích hoạt các hành động khi có sự kiện cụ thể xảy ra trong S3 bucket của bạn.

## Yêu Cầu Trước

- Quyền truy cập vào AWS Console
- Quyền tạo S3 bucket và SQS queue
- Hiểu biết cơ bản về các dịch vụ S3 và SQS

## Bước 1: Tạo S3 Bucket

1. Truy cập Amazon S3 trong AWS Console
2. Tạo bucket mới với tên `stephane-v3-events-notifications`
3. Chọn region Ireland
4. Nhấn "Create bucket"

## Bước 2: Cấu Hình Event Notifications

### Hai Tùy Chọn Có Sẵn

Khi thiết lập S3 event notifications, bạn có hai tùy chọn chính:

1. **Tạo Event Notification** - Tích hợp trực tiếp với các dịch vụ AWS cụ thể (Lambda, SNS, SQS)
2. **Bật Amazon EventBridge Integration** - Gửi tất cả sự kiện đến EventBridge để định tuyến và xử lý nâng cao

Trong hướng dẫn này, chúng ta sẽ sử dụng tùy chọn đầu tiên đơn giản hơn.

### Thiết Lập Event Notification

1. Vào bucket vừa tạo
2. Chuyển đến tab **Properties**
3. Cuộn xuống phần **Event notifications**
4. Nhấn **Create event notification**

#### Chi Tiết Cấu Hình

- **Name**: `DemoEventNotification`
- **Prefix**: (để trống)
- **Suffix**: (để trống)

#### Loại Sự Kiện (Event Types)

Chọn **All object create events** - điều này sẽ kích hoạt thông báo mỗi khi có đối tượng được tạo trong bucket.

Các loại sự kiện có sẵn bao gồm:
- Sự kiện tạo đối tượng
- Sự kiện xóa đối tượng
- Sự kiện khôi phục đối tượng
- Và nhiều loại sự kiện cụ thể khác

#### Đích Đến (Destination)

Chọn **SQS queue** làm đích đến (các tùy chọn khác bao gồm Lambda function và SNS topic).

## Bước 3: Tạo SQS Queue

Trước khi cấu hình đích đến, bạn cần tạo một SQS queue:

1. Truy cập Amazon SQS
2. Nhấn **Create queue**
3. Đặt tên: `DemoS3Notification`
4. Nhấn **Create queue**

## Bước 4: Cấu Hình Access Policy

### Vấn Đề

Nếu bạn thử lưu cấu hình event notification ngay lập tức, bạn sẽ nhận được lỗi cho biết không thể xác thực cấu hình đích đến. Đây là vì SQS queue chưa có quyền chấp nhận tin nhắn từ S3.

### Giải Pháp

Bạn cần cập nhật access policy của SQS queue:

1. Vào SQS queue của bạn (`DemoS3Notification`)
2. Nhấn **Edit**
3. Cuộn xuống **Access policy**
4. Nhấn **Policy Generator**

#### Tạo Policy

- **Type**: SQS Queue Policy
- **Effect**: Allow
- **Principal**: * (bất kỳ ai - cho mục đích demo)
- **Actions**: SendMessage
- **ARN**: Sao chép và dán ARN của queue

5. Nhấn **Add Statement**
6. Nhấn **Generate Policy**
7. Sao chép policy đã tạo
8. Dán vào access policy của queue
9. Nhấn **Save**

> **Lưu ý**: Policy sử dụng trong demo này rất dễ dãi (cho phép bất kỳ ai gửi tin nhắn). Trong môi trường production, bạn nên hạn chế quyền này chỉ cho S3 bucket của bạn.

## Bước 5: Hoàn Thành Thiết Lập Event Notification

1. Quay lại cấu hình event notification của S3 bucket
2. Làm mới dropdown SQS queue
3. Chọn `DemoS3Notification`
4. Nhấn **Save changes**

### Sự Kiện Kiểm Tra (Test Event)

Sau khi lưu, Amazon S3 sẽ tự động gửi một sự kiện kiểm tra đến SQS queue để xác minh kết nối.

Bạn có thể xác minh bằng cách:
1. Vào SQS queue của bạn
2. Nhấn **Send and receive messages**
3. Nhấn **Poll for messages**
4. Bạn sẽ thấy một tin nhắn kiểm tra từ S3

## Bước 6: Kiểm Tra Event Notification

Bây giờ hãy kiểm tra event notification với một file thực tế:

1. Truy cập S3 bucket của bạn
2. Nhấn **Upload**
3. Nhấn **Add files**
4. Chọn một file (ví dụ: `coffee.jpeg`)
5. Nhấn **Upload**

### Xác Minh Thông Báo

1. Quay lại SQS queue
2. Nhấn **Send and receive messages**
3. Nhấn **Poll for messages**
4. Bạn sẽ thấy một tin nhắn mới

### Kiểm Tra Tin Nhắn

Tin nhắn sẽ chứa thông tin chi tiết về sự kiện S3:

```json
{
  "eventName": "ObjectCreated:Put",
  "s3": {
    "object": {
      "key": "coffee.jpeg"
    }
  }
}
```

Tin nhắn bao gồm:
- **eventName**: Loại sự kiện (ví dụ: `ObjectCreated:Put`)
- **key**: Tên của file đã được upload (ví dụ: `coffee.jpeg`)
- Metadata bổ sung về sự kiện

## Các Trường Hợp Sử Dụng

S3 Event Notifications rất mạnh mẽ cho việc tự động hóa quy trình làm việc, chẳng hạn như:

- **Xử Lý Hình Ảnh**: Tự động tạo thumbnail khi có ảnh được upload
- **Xử Lý Dữ Liệu**: Kích hoạt Lambda function để xử lý các file đã upload
- **Sao Lưu và Lưu Trữ**: Tự động sao chép file sang vị trí khác
- **Thông Báo**: Cảnh báo nhóm khi có file cụ thể được upload hoặc xóa

## Dọn Dẹp

Sau khi hoàn thành hướng dẫn:
1. Xóa tin nhắn kiểm tra khỏi SQS
2. Tùy chọn xóa file đã upload khỏi S3
3. Nếu không cần, xóa S3 bucket và SQS queue

## Những Điểm Chính Cần Nhớ

- S3 Event Notifications có thể được gửi đến **SQS**, **SNS**, và **Lambda**
- Bạn cũng có thể gửi tất cả sự kiện đến **Amazon EventBridge** để định tuyến và lọc nâng cao
- Cần có access policy phù hợp để S3 có thể gửi tin nhắn đến đích đến của bạn
- Event notification bao gồm thông tin chi tiết về những gì đã xảy ra trong bucket
- Điều này cho phép tự động hóa mạnh mẽ và kiến trúc hướng sự kiện (event-driven)

## Các Bước Tiếp Theo

- Khám phá việc sử dụng Lambda function làm đích đến cho xử lý phức tạp hơn
- Tìm hiểu về Amazon EventBridge để định tuyến sự kiện nâng cao
- Triển khai các trường hợp sử dụng thực tế như tạo thumbnail hình ảnh
- Nghiên cứu các loại sự kiện và tùy chọn lọc khác nhau

---

*Hướng dẫn này trình bày một triển khai cơ bản. Luôn tuân theo các best practice bảo mật của AWS và nguyên tắc quyền tối thiểu (principle of least privilege) khi cấu hình access policy trong môi trường production.*