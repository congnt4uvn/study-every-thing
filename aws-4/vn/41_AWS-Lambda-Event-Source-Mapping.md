# AWS Lambda Event Source Mapping

## Tổng Quan

Event Source Mapping là một trong ba cách Lambda có thể xử lý sự kiện trong AWS, bên cạnh xử lý bất đồng bộ (asynchronous) và đồng bộ (synchronous).

## Các Dịch Vụ Áp Dụng

Event Source Mapping áp dụng cho:
- **Kinesis Data Streams**
- **SQS và SQS FIFO queues**
- **DynamoDB Streams**

## Cách Hoạt Động

### Khái Niệm Cốt Lõi

Điểm chung của các dịch vụ này là **các bản ghi cần được poll (truy vấn) từ nguồn**. Lambda chủ động yêu cầu dịch vụ để lấy các bản ghi, thay vì nhận chúng một cách thụ động.

### Luồng Xử Lý

1. Dịch vụ Lambda được cấu hình để đọc từ một nguồn (ví dụ: Kinesis)
2. Một **Event Source Mapping** được tạo nội bộ
3. Event Source Mapping poll dịch vụ (ví dụ: Kinesis)
4. Dịch vụ trả về một batch các bản ghi
5. Event Source Mapping gọi hàm Lambda một cách **đồng bộ** với event batch

```
[Kinesis] <-- polling -- [Event Source Mapping] --> [Hàm Lambda]
                                                     (gọi đồng bộ)
```

## Hai Loại

### 1. Streams (Luồng Dữ Liệu)
Áp dụng cho:
- Kinesis Data Streams
- DynamoDB Streams

#### Đặc Điểm Của Streams

- **Iterator cho mỗi shard**: Event Source Mapping tạo một iterator cho mỗi Kinesis shard hoặc DynamoDB Stream shard
- **Thứ tự xử lý**: Các item được xử lý theo thứ tự ở cấp độ shard
- **Vị trí bắt đầu có thể cấu hình**: 
  - Chỉ đọc các item mới
  - Đọc từ đầu shard
  - Đọc từ một timestamp cụ thể
- **Đọc không phá hủy**: Các item đã xử lý KHÔNG bị xóa khỏi streams, cho phép các consumer khác đọc cùng dữ liệu

### 2. Queues (Hàng Đợi)
Áp dụng cho:
- SQS
- SQS FIFO queues

## Những Điểm Quan Trọng

✓ Hàm Lambda được gọi **đồng bộ** với Event Source Mapping
✓ Lambda **poll** (kéo) dữ liệu từ nguồn thay vì nhận thông báo đẩy
✓ Xử lý duy trì thứ tự ở cấp độ shard đối với streams
✓ Dữ liệu vẫn còn trong streams sau khi xử lý, cho phép nhiều consumer

## Trường Hợp Sử Dụng

Event Source Mapping lý tưởng cho:
- Xử lý dữ liệu streaming từ Kinesis
- Xử lý messages từ SQS queues
- Phản ứng với thay đổi cơ sở dữ liệu qua DynamoDB Streams
- Các tình huống yêu cầu xử lý có thứ tự theo shard
- Mô hình nhiều consumer khi dữ liệu cần được giữ lại sau khi xử lý
