# AWS Lambda Execution Roles và Permissions

## Tổng quan

Một IAM Role phải được gắn vào Lambda function để cấp quyền truy cập các dịch vụ và tài nguyên AWS.

## Managed Policies cho Lambda

AWS cung cấp một số managed policies có thể tái sử dụng cho các tình huống Lambda phổ biến:

- **AWSLambdaBasicExecutionRole** - Cho phép tải logs lên CloudWatch
- **AWSLambdaKinesisExecutionRole** - Cho phép đọc từ Kinesis streams
- **AWSLambdaDynamoDBExecutionRole** - Cho phép đọc từ DynamoDB streams
- **AWSLambdaSQSQueueExecutionRole** - Cho phép đọc từ SQS queues
- **AWSLambdaVPCAccessExecutionRole** - Cho phép triển khai Lambda functions bên trong VPC
- **AWSXRayDaemonWriteAccess** - Cho phép tải trace data lên X-Ray

## Custom Policies

Bạn có thể tạo custom policies riêng cho Lambda functions dựa trên yêu cầu cụ thể.

## Event Source Mapping

Khi sử dụng event source mapping để gọi function, Lambda sẽ đọc dữ liệu từ event source. Do đó, bạn phải sử dụng execution role với quyền đọc event data.

Khi Lambda được gọi trực tiếp bởi các dịch vụ khác (không qua event source mapping), bạn không cần quyền IAM Role cụ thể cho việc gọi hàm.

## Best Practice (Thực hành tốt nhất)

**Tạo một Lambda execution role cho mỗi function** để tuân theo nguyên tắc least privilege và duy trì sự phân tách rõ ràng các quyền.

## Resource-Based Policies

Resource-based policies được sử dụng để cấp quyền cho các AWS accounts hoặc services khác gọi Lambda function của bạn. Điều này tương tự như S3 bucket policies.

### Quy tắc Access Control

Một IAM principal có thể truy cập Lambda function của bạn nếu **một trong các điều kiện sau** đúng:

1. IAM policy được gắn vào principal cho phép nó
2. Resource-based policy trên Lambda function cho phép nó

## Sự khác biệt chính

- **Execution Role (IAM Role)**: Cấp quyền cho Lambda truy cập các dịch vụ AWS khác
- **Resource-Based Policy**: Cấp quyền cho các services/accounts khác gọi Lambda

## Tóm tắt

- Gắn IAM roles vào Lambda functions cho quyền outbound (đi ra)
- Sử dụng managed policies khi có thể
- Tạo một execution role cho mỗi function theo best practice
- Sử dụng resource-based policies cho kiểm soát truy cập inbound (đi vào)
- Event source mappings yêu cầu execution role permissions để đọc dữ liệu
