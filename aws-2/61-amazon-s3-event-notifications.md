# Amazon S3 Event Notifications (Thông báo Sự kiện S3)

## Tổng quan

Amazon S3 Event Notifications cho phép bạn tự động phản ứng với các sự kiện xảy ra trong S3 bucket của bạn. Tính năng này giúp bạn xây dựng kiến trúc hướng sự kiện và tự động hóa quy trình làm việc dựa trên các thao tác với đối tượng S3.

## S3 Events là gì?

S3 events là các hành động xảy ra trong Amazon S3 bucket của bạn, bao gồm:

- **Object Created (Tạo đối tượng)** - Khi một đối tượng mới được tải lên S3
- **Object Removed (Xóa đối tượng)** - Khi một đối tượng bị xóa khỏi S3
- **Object Restored (Khôi phục đối tượng)** - Khi một đối tượng được khôi phục từ lưu trữ lưu trữ
- **Replication Events (Sự kiện sao chép)** - Khi các hoạt động sao chép xảy ra

## Lọc Sự kiện

Bạn có thể lọc các sự kiện dựa trên thuộc tính của đối tượng. Ví dụ:
- Lọc theo phần mở rộng tệp (ví dụ: chỉ các tệp `.jpeg`)
- Lọc theo tiền tố hoặc hậu tố của object key
- Áp dụng các quy tắc lọc tùy chỉnh

## Trường hợp Sử dụng

Một trường hợp sử dụng phổ biến là tự động tạo ảnh thu nhỏ (thumbnail) cho các hình ảnh được tải lên S3:
1. Người dùng tải hình ảnh lên S3
2. Event Notification được kích hoạt
3. Quy trình tự động tạo ảnh thu nhỏ
4. Ảnh thu nhỏ được lưu trữ lại trong S3

## Đích của Event Notification

S3 Event Notifications có thể được gửi đến ba đích chính:

### 1. SNS (Simple Notification Service) Topic
- Xuất bản thông báo đến các subscriber
- Yêu cầu SNS resource access policy

### 2. SQS (Simple Queue Service) Queue
- Xếp hàng các thông điệp để xử lý
- Yêu cầu SQS resource access policy

### 3. Lambda Function
- Thực thi các hàm serverless
- Yêu cầu Lambda resource policy

## Đặc điểm Phân phối

- Các sự kiện thường được phân phối **trong vòng vài giây**
- Trong một số trường hợp, việc phân phối có thể mất một phút hoặc lâu hơn
- Bạn có thể tạo bao nhiêu event notification tùy ý

## Quyền IAM Cần thiết

S3 Event Notifications yêu cầu **resource-based policies** (không phải IAM roles):

### Đối với SNS Topics
Đính kèm **SNS resource access policy** để cho phép S3 bucket gửi thông điệp đến SNS topic.

### Đối với SQS Queues
Đính kèm **SQS resource access policy** để ủy quyền cho dịch vụ S3 gửi dữ liệu vào queue.

### Đối với Lambda Functions
Đính kèm **Lambda resource policy** để đảm bảo Amazon S3 có quyền gọi hàm.

> **Lưu ý:** Các resource access policies này hoạt động tương tự như S3 bucket policies.

## Tích hợp Nâng cao: Amazon EventBridge

Amazon EventBridge cung cấp khả năng nâng cao cho S3 Event Notifications:

### Tính năng Chính

- **Tất cả S3 events** tự động chuyển đến EventBridge
- **Tùy chọn lọc nâng cao** - Lọc theo metadata, kích thước đối tượng và tên
- **Nhiều đích** - Gửi đến hơn 18 dịch vụ AWS đồng thời
- **Các đích bổ sung** bao gồm:
  - AWS Step Functions
  - Amazon Kinesis Data Streams
  - Amazon Kinesis Data Firehose
  - Và nhiều hơn nữa

### Ưu điểm của EventBridge

- **Archive events (Lưu trữ sự kiện)** - Lưu trữ các sự kiện để phân tích lịch sử
- **Replay events (Phát lại sự kiện)** - Xử lý lại các sự kiện khi cần
- **Reliable delivery (Phân phối đáng tin cậy)** - Đảm bảo phân phối nâng cao
- **Rules-based routing (Định tuyến dựa trên quy tắc)** - Thiết lập các quy tắc định tuyến phức tạp

## Tóm tắt

Amazon S3 Event Notifications cho phép bạn phản ứng với các sự kiện trong S3 bucket bằng cách gửi thông báo đến:
- SNS Topics
- SQS Queues
- Lambda Functions
- Amazon EventBridge (cho các tình huống nâng cao)

Tính năng này rất quan trọng để xây dựng các quy trình làm việc tự động, hướng sự kiện trong AWS.