# AWS Lambda Destinations (Điểm Đến Lambda)

## Tổng Quan
Lambda Destinations là tính năng được giới thiệu vào tháng 11 năm 2019, cho phép bạn gửi kết quả của các lần gọi Lambda bất đồng bộ đến nhiều dịch vụ AWS khác nhau.

## Vấn Đề Cần Giải Quyết
Trước khi có Lambda Destinations, rất khó để:
- Theo dõi xem các lần gọi bất đồng bộ hoặc event mappers đã thành công hay thất bại
- Truy xuất dữ liệu từ các thao tác này
- Xử lý kết quả một cách có hệ thống

## Giải Pháp: Lambda Destinations
Lambda Destinations cho phép bạn gửi kết quả của một lần gọi bất đồng bộ hoặc lỗi của event mapper đến các dịch vụ AWS cụ thể.

## Lần Gọi Bất Đồng Bộ (Asynchronous Invocations)

### Các Tùy Chọn Điểm Đến
Bạn có thể định nghĩa điểm đến cho cả:
- **Sự kiện thành công** - khi xử lý hoàn tất thành công
- **Sự kiện thất bại** - khi xử lý thất bại

### Các Đích Được Hỗ Trợ
- **Amazon SQS** (Simple Queue Service - Dịch vụ Hàng Đợi)
- **Amazon SNS** (Simple Notification Service - Dịch vụ Thông Báo)
- **AWS Lambda** (một Lambda function khác)
- **Amazon EventBridge** (CloudWatch Events - Sự Kiện)

### Ví Dụ Luồng Hoạt Động
```
Sự kiện S3 → Lambda Function (bất đồng bộ)
  ├─ Thành công → Điểm đến (SQS/SNS/Lambda/EventBridge)
  └─ Thất bại → Điểm đến (SQS/SNS/Lambda/EventBridge)
```

## So Sánh Destinations vs Dead Letter Queues (DLQ)

### Dead Letter Queues (DLQ) - Cách Tiếp Cận Cũ
- Chỉ xử lý các sự kiện **thất bại**
- Đích giới hạn: chỉ SQS và SNS

### Lambda Destinations - Cách Tiếp Cận Được Đề Xuất
- Xử lý cả sự kiện **thành công** và **thất bại**
- Nhiều tùy chọn điểm đến hơn: SQS, SNS, Lambda, và EventBridge
- Có thể sử dụng cùng với DLQ (nhưng nên ưu tiên Destinations)

**Khuyến Nghị:** Sử dụng Lambda Destinations thay vì DLQ cho các triển khai mới.

## Event Source Mapping (Ánh Xạ Nguồn Sự Kiện)

### Trường Hợp Sử Dụng
Khi một batch sự kiện từ các nguồn streaming không thể xử lý được và bị loại bỏ.

### Các Đích Được Hỗ Trợ (chỉ cho lỗi)
- Amazon SQS
- Amazon SNS

### Ví Dụ Luồng Hoạt Động
```
Kinesis Data Stream → Event Source Mapping → Lambda
  └─ Lỗi Xử Lý → Điểm đến (SQS/SNS)
```

### Hành Vi
Thay vì chặn toàn bộ quá trình xử lý stream, các batch thất bại sẽ được gửi đến điểm đến đã cấu hình, cho phép stream tiếp tục xử lý các bản ghi mới.

## Lợi Ích Chính
1. **Khả năng quan sát tốt hơn** - Theo dõi cả thành công và thất bại
2. **Linh hoạt hơn** - Nhiều tùy chọn điểm đến
3. **Xử lý lỗi được cải thiện** - Ngăn chặn việc chặn stream
4. **Kiến trúc hiện đại** - Mới hơn và nhiều tính năng hơn DLQ

## Thực Hành Tốt Nhất
- Sử dụng Destinations thay vì DLQ cho các triển khai mới
- Cấu hình các điểm đến riêng biệt cho các tình huống thành công và thất bại
- Đối với các nguồn streaming (Kinesis, DynamoDB Streams), cấu hình điểm đến lỗi để ngăn chặn việc chặn
- Xem xét sử dụng EventBridge cho các kịch bản định tuyến sự kiện phức tạp

## Mẹo Học Tập
- Hiểu sự khác biệt giữa lần gọi bất đồng bộ và event source mappings
- Nhớ rằng Destinations hỗ trợ 4 đích trong khi DLQ chỉ hỗ trợ 2
- Thực hành cấu hình destinations trong AWS Console hoặc sử dụng Infrastructure as Code (CloudFormation/Terraform)

## Thuật Ngữ Quan Trọng
- **Asynchronous Invocations**: Lần gọi bất đồng bộ
- **Event Source Mapping**: Ánh xạ nguồn sự kiện
- **Dead Letter Queue (DLQ)**: Hàng đợi thư chết (nơi lưu tin nhắn/sự kiện thất bại)
- **Destination**: Điểm đến
- **Event batch**: Lô sự kiện
