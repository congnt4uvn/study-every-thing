# Hướng Dẫn Thực Hành AWS SNS

## Giới Thiệu

Hướng dẫn thực hành này sẽ giúp bạn làm quen với Amazon Simple Notification Service (SNS), bao gồm cách tạo topic, thiết lập subscription và gửi thông báo.

## Tạo Topic SNS Đầu Tiên

### Bước 1: Truy Cập Dịch Vụ SNS

Điều hướng đến Simple Notification Service trong AWS Console để tạo topic đầu tiên của bạn.

### Bước 2: Chọn Loại Topic

Khi tạo topic, bạn có hai tùy chọn:

#### Topic Tiêu Chuẩn (Standard Topic)
- **Thứ Tự Message**: Sắp xếp message theo kiểu best-effort (cố gắng tối đa)
- **Phân Phối**: Phân phối message ít nhất một lần
- **Throughput**: Thông lượng cao nhất về số lần publish mỗi giây
- **Endpoint Được Hỗ Trợ**: 
  - Amazon SQS
  - AWS Lambda
  - HTTPS
  - SMS
  - Email
  - Ứng dụng di động

#### Topic FIFO
- **Thứ Tự Message**: Đảm bảo thứ tự message được bảo toàn nghiêm ngặt
- **Phân Phối**: Phân phối chính xác một lần
- **Throughput**: Thông lượng cao lên đến 300 lần publish mỗi giây
- **Endpoint Được Hỗ Trợ**: Chỉ hỗ trợ Amazon SQS queue
- **Quy Ước Đặt Tên**: Tên topic phải kết thúc bằng `.fifo`

Trong hướng dẫn này, chúng ta sẽ tạo một topic **Tiêu Chuẩn** có tên `MyFirstTopic`.

## Cấu Hình SNS Topic

### Access Policy (Chính Sách Truy Cập)

Access policy xác định ai và cái gì có thể ghi vào SNS topic. Điều này tương tự như:
- S3 bucket policies
- SQS access queue policies

**Ví Dụ Use Case**: Bạn có thể cấu hình S3 bucket để ghi các sự kiện vào SNS topic, sau đó SNS topic sẽ gửi dữ liệu đến các SQS queue.

Trong hướng dẫn cơ bản này, chúng ta sẽ sử dụng access policy cơ bản mặc định mà không cần cấu hình nâng cao.

### Mã Hóa (Encryption)

Bạn có tùy chọn mã hóa các message trong topic (không được cấu hình trong hướng dẫn này).

## Tạo Subscription

Sau khi tạo topic, ban đầu bạn sẽ có không subscription nào. Hãy cùng tạo một subscription.

### Các Protocol Có Sẵn

SNS hỗ trợ nhiều protocol subscription:
- Kinesis Data Firehose
- Amazon SQS
- AWS Lambda
- Email
- Email-JSON
- HTTP
- HTTPS
- SMS

**Quan Trọng**: Hãy nhớ các protocol này cho kỳ thi chứng chỉ AWS.

### Thiết Lập Email Subscription

1. **Chọn Protocol**: Chọn "Email"
2. **Nhập Endpoint**: Cung cấp địa chỉ email (ví dụ: stephanetheteacher@mailinator.com)
3. **Tạo Subscription**: Subscription sẽ ở trạng thái "Pending Confirmation" (Chờ xác nhận)

### Subscription Filter Policy (Tùy Chọn)

Bạn có thể thiết lập subscription filter policy để lọc những message nào được gửi đến các subscription cụ thể. Điều này hữu ích khi:
- Bạn có nhiều subscriber
- Các subscriber khác nhau chỉ cần nhận các tập con message từ SNS topic

Trong hướng dẫn này, chúng ta sẽ không thiết lập filter policy, cho phép tất cả message được phân phối.

## Xác Nhận Subscription

1. Kiểm tra hộp thư email của bạn
2. Bạn sẽ nhận được email xác nhận từ AWS SNS
3. Nhấp vào "Confirm subscription" trong email
4. Làm mới AWS Console để thấy trạng thái subscription thay đổi từ "Pending Confirmation" thành "Confirmed"

## Kiểm Tra SNS Topic

### Publish Message

1. Điều hướng đến SNS topic của bạn
2. Nhấp "Publish message"
3. Nhập message thử nghiệm (ví dụ: "hello world")
4. Nhấp "Publish message"

### Xác Minh Việc Phân Phối Message

1. Kiểm tra hộp thư email của bạn
2. Bạn sẽ nhận được một AWS notification message
3. Email sẽ chứa message bạn đã publish ("hello world")

Điều này xác nhận rằng SNS đang hoạt động chính xác!

## Pattern Nâng Cao: SQS Fan-Out

Để triển khai SQS fan-out pattern:
1. Chọn SQS làm subscription protocol
2. Thiết lập nhiều SQS queue làm receiver
3. Mỗi queue sẽ nhận message từ SNS topic

## Dọn Dẹp

### Xóa Tài Nguyên

Để tránh các chi phí không cần thiết:

1. **Xóa Subscription**:
   - Điều hướng đến subscription của bạn
   - Nhấp "Delete"

2. **Xóa Topic**:
   - Đi đến Topics trong menu bên trái
   - Chọn topic của bạn
   - Nhấp "Delete"
   - Gõ "delete me" để xác nhận xóa

## Kết Luận

Hướng dẫn này đã trình bày các thao tác cơ bản của AWS SNS, bao gồm:
- Tạo topic tiêu chuẩn và hiểu về FIFO topic
- Thiết lập email subscription
- Cấu hình access policy
- Publish và nhận message
- Hiểu về các subscription protocol

SNS là một dịch vụ mạnh mẽ để triển khai các pattern pub/sub messaging trong kiến trúc AWS.

---

**Bước Tiếp Theo**: Khám phá thêm các tính năng nâng cao của SNS và các pattern tích hợp với các dịch vụ AWS khác.