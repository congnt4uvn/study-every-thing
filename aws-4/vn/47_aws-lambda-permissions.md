# Hướng Dẫn Học AWS Lambda Permissions

## Tổng Quan
Mỗi Lambda function đều phải có một IAM role được gắn kèm. Hiểu được sự khác biệt giữa execution roles và resource-based policies là rất quan trọng khi làm việc với AWS Lambda.

## Lambda Execution Roles (Vai trò thực thi)

### Basic Execution Role
- Tự động được gắn vào các Lambda function được tạo qua console
- Cung cấp quyền cho Lambda function để thực hiện các hành động
- **Các quyền quan trọng bao gồm:**
  - Tạo CloudWatch log groups
  - Gửi log events đến CloudWatch Logs
  - Điều này cho phép Lambda functions ghi lại các logs thực thi

### Ví dụ: SQS Lambda Execution Role
Khi Lambda cần poll (truy vấn) SQS queues, execution role phải bao gồm:
- Nhận messages từ SQS
- Xóa messages từ SQS
- Lấy queue attributes

**Quan trọng:** Trong mô hình này, Lambda đang chủ động kéo dữ liệu từ SQS, không phải được SQS gọi đến.

## Resource-Based Policies (Chính sách dựa trên tài nguyên)

Resource-based policies xác định **ai có thể invoke** Lambda function của bạn. Các policies này được gắn trực tiếp vào Lambda function.

### Ví dụ S3 Trigger
Khi S3 invoke một Lambda function:
- Resource-based policy cho phép service `s3.amazonaws.com` invoke function
- Các điều kiện chỉ định:
  - Source account ID
  - Source ARN (S3 bucket cụ thể)
- **Mô hình:** S3 đẩy events đến Lambda

### Ví dụ EventBridge Trigger
Khi EventBridge invoke một Lambda function:
- Resource-based policy cho phép service `events.amazonaws.com` invoke function
- Các điều kiện chỉ định:
  - Source ARN (EventBridge rule cụ thể)
- **Mô hình:** EventBridge đẩy events đến Lambda

## Sự Khác Biệt Chính

| Khía cạnh | Execution Role | Resource-Based Policy |
|-----------|----------------|----------------------|
| **Mục đích** | Quyền cho Lambda truy cập các AWS services khác | Quyền cho các services khác invoke Lambda |
| **Hướng** | Lambda → Services Khác | Services Khác → Lambda |
| **Ví dụ Use Cases** | Lambda đọc từ SQS, ghi vào DynamoDB | S3 trigger Lambda, EventBridge invoke Lambda |
| **Vị trí** | Phần IAM Roles | Cấu hình Lambda function |

## Các Mô Hình Quan Trọng Cần Nhớ

### Mô Hình Push (Sử dụng Resource-Based Policy)
- S3 → Lambda
- EventBridge → Lambda
- API Gateway → Lambda
- Các services **invoke** Lambda trực tiếp

### Mô Hình Poll (Sử dụng Execution Role)
- Lambda → SQS
- Lambda → Kinesis
- Lambda → DynamoDB Streams
- Lambda **polls** (truy vấn) để lấy dữ liệu từ các services này

## Xem Policies trong AWS Console

### Execution Role
1. Điều hướng đến Lambda function
2. Vào **Configuration** → **Permissions**
3. Click vào tên execution role
4. Xem các policies đã gắn

### Resource-Based Policy
1. Điều hướng đến Laravel function
2. Vào **Configuration** → **Permissions**
3. Cuộn xuống "Resource-based policy statements"
4. Click "View policy" để xem JSON

## Best Practices (Thực hành tốt nhất)
- Luôn sử dụng nguyên tắc least privilege (ít quyền nhất)
- Thường xuyên kiểm tra Lambda execution roles
- Sử dụng resource-based policies cho cross-account access
- Theo dõi CloudWatch Logs để phát hiện lỗi liên quan đến permissions
- Giữ IAM policies cụ thể chỉ cho các actions cần thiết

## Tóm Tắt
Hiểu khi nào sử dụng execution roles và khi nào sử dụng resource-based policies là rất quan trọng:
- **Execution roles** = Lambda có thể làm gì với các services khác
- **Resource-based policies** = Các services khác có thể làm gì với Lambda

Ghi nhớ: SQS đặc biệt vì Lambda poll nó, do đó không sử dụng resource-based policies mà yêu cầu quyền execution role thích hợp.
