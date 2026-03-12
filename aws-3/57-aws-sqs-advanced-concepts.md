# AWS SQS Các Khái Niệm Nâng Cao - Cấp Độ Nhà Phát Triển

## Tổng Quan

Hướng dẫn này bao gồm các khái niệm nâng cao về Amazon SQS (Simple Queue Service) cần thiết cho các nhà phát triển, bao gồm long polling, SQS Extended Client, và các thao tác API chính.

## Long Polling (Polling Dài)

### Long Polling Là Gì?

Khi một consumer yêu cầu message từ SQS, nó có tùy chọn chờ đợi messages đến nếu queue trống. Đây được gọi là **long polling**.

### Cách Long Polling Hoạt Động

1. Một SQS queue đang trống
2. Consumer thực hiện một poll request đến SQS queue
3. Thay vì trả về ngay lập tức, consumer sẽ chờ đợi
4. Nếu một message đến trong thời gian chờ, nó sẽ được consumer nhận ngay lập tức

### Lợi Ích Của Long Polling

- **Giảm API Calls**: Ít request hơn đến SQS queue
- **Giảm CPU Usage**: Ít chu kỳ xử lý hơn được yêu cầu
- **Giảm Latency**: Messages được nhận ngay lập tức khi đến
- **Tiết Kiệm Chi Phí**: Ít API calls hơn nghĩa là chi phí thấp hơn

### Cấu Hình

- **Khoảng Thời Gian**: 1 đến 20 giây (khuyến nghị 20 giây)
- **Cài Đặt Queue Level**: Có thể bật ở cấp độ queue cho tất cả consumers
- **Cài Đặt API Level**: Có thể đặt cho mỗi API call sử dụng tham số `ReceiveMessageWaitTimeSeconds`

### Khi Nào Sử Dụng Long Polling

Sử dụng long polling khi:
- Consumers đang thực hiện quá nhiều API calls đến SQS queue
- Bạn muốn giảm chi phí và chu kỳ CPU
- Bạn cần giảm độ trễ

**Quan Trọng**: Khuyến nghị sử dụng long polling thay vì short polling trong các ứng dụng của bạn.

## SQS Extended Client

### Thách Thức

Giới hạn kích thước message tối đa trong SQS là **1,024 kilobytes** (1 MB). Làm thế nào để gửi các messages lớn hơn, chẳng hạn như file 1 GB?

### Giải Pháp: SQS Extended Client

**SQS Extended Client** là một thư viện Java cho phép gửi các messages lớn bằng cách sử dụng Amazon S3 làm kho lưu trữ cho dữ liệu lớn.

### Cách Hoạt Động

1. **Phía Producer**:
   - Producer muốn gửi một message lớn
   - Message lớn được upload lên Amazon S3
   - Một message metadata nhỏ với con trỏ đến đối tượng S3 được gửi đến SQS queue

2. **Phía Consumer**:
   - Consumer đọc message metadata nhỏ từ SQS
   - Sử dụng thư viện SQS Extended Client, nó truy xuất message lớn từ S3

### Kiến Trúc

- **SQS Queue**: Chứa các messages metadata nhỏ
- **Amazon S3 Bucket**: Chứa các đối tượng lớn
- **Extended Client Library**: Xử lý sự phối hợp giữa SQS và S3

### Ví Dụ Use Case

**Xử Lý Video**: 
- Thay vì gửi toàn bộ file video qua SQS
- Upload file video lên Amazon S3
- Gửi một message con trỏ nhỏ đến SQS
- Consumer truy xuất video từ S3 sử dụng con trỏ

Pattern này cho phép bạn chứa bất kỳ kích thước message nào.

## Các Thao Tác API SQS

### APIs Quản Lý Queue

#### CreateQueue
- **Mục Đích**: Tạo một queue mới
- **Tham Số Chính**: `MessageRetentionPeriod` - đặt thời gian messages được giữ trước khi bị loại bỏ

#### DeleteQueue
- **Mục Đích**: Xóa một queue và tất cả messages của nó cùng lúc

#### PurgeQueue
- **Mục Đích**: Xóa tất cả messages trong queue mà không xóa queue

### APIs Thao Tác Message

#### SendMessage
- **Mục Đích**: Gửi một message đến queue
- **Tham Số Chính**: `DelaySeconds` - gửi messages với độ trễ

#### ReceiveMessage
- **Mục Đích**: Poll để nhận messages từ queue
- **Tham Số Chính**:
  - `MaxNumberOfMessages`: Mặc định là 1, có thể đặt lên đến 10 để nhận một batch messages
  - `ReceiveMessageWaitTimeSeconds`: Bật long polling bằng cách chỉ định thời gian chờ

#### DeleteMessage
- **Mục Đích**: Xóa một message sau khi nó đã được xử lý bởi consumer

#### ChangeMessageVisibility
- **Mục Đích**: Thay đổi message timeout nếu bạn cần thêm thời gian để xử lý message

### Batch API Operations

Để giảm số lượng API calls và giảm chi phí, bạn có thể sử dụng batch operations cho:
- `SendMessage`
- `DeleteMessage`
- `ChangeMessageVisibility`

## Thực Hành: Cấu Hình Long Polling

### Bước 1: Cấu Hình Queue Settings
1. Điều hướng đến SQS queue của bạn trong AWS Console
2. Chỉnh sửa queue settings
3. Tìm cài đặt "Receive message wait time" (hiện tại 0 = short polling)
4. Đặt nó thành một giá trị từ 1 đến 20 giây (ví dụ: 20 giây)
5. Lưu cấu hình queue

### Bước 2: Test Long Polling
1. Vào "Send and receive messages"
2. Khởi động một consumer
3. Consumer sẽ chờ messages (chỉ một API call được thực hiện)
4. Gửi một message (ví dụ: "hello world")
5. Message được nhận ngay lập tức với độ trễ cực thấp

### Cách Hoạt Động
- Consumer ở chế độ long polling
- Nó chờ messages từ SQS do cài đặt wait time
- Khi một message đến, nó được gửi ngay lập tức đến consumer đang chờ
- Điều này chứng minh lợi ích độ trễ thấp của long polling

## Tóm Tắt

- **Long Polling**: Giảm API calls, giảm chi phí, giảm độ trễ (1-20 giây, tốt nhất là 20)
- **SQS Extended Client**: Cho phép gửi messages lớn (>1 MB) bằng cách sử dụng S3 làm storage
- **APIs Chính**: CreateQueue, DeleteQueue, PurgeQueue, SendMessage, ReceiveMessage, DeleteMessage, ChangeMessageVisibility
- **Batch Operations**: Sử dụng batch APIs để giảm chi phí và số lượng API call
- **Best Practice**: Luôn ưu tiên long polling hơn short polling để hiệu quả tốt hơn

## Mẹo Thi Chứng Chỉ

- Nếu bạn thấy câu hỏi về API calls quá nhiều đến SQS gây tốn tiền và chu kỳ CPU → **Sử Dụng Long Polling**
- Để gửi files lớn (video, hình ảnh, v.v.) → **Sử Dụng SQS Extended Client với S3**
- Nhớ rằng `MaxNumberOfMessages` có thể đặt lên đến 10 để nhận batch
- `ReceiveMessageWaitTimeSeconds` bật long polling ở cấp độ API