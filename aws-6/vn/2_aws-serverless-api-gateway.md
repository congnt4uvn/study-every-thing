# AWS Serverless - Tài Liệu Học Tập API Gateway

## Tổng Quan

Tài liệu này bao gồm kiến trúc serverless của AWS tập trung vào API Gateway, Lambda functions và tích hợp DynamoDB.

## Hành Trình Serverless

### Các Thành Phần Cốt Lõi
- **Lambda Functions**: Dịch vụ tính toán serverless
- **DynamoDB**: Cơ sở dữ liệu NoSQL cho backend API
- **CRUD Operations**: Các thao tác Create, Read, Update, Delete trên bảng

## Các Cách Gọi Lambda Functions

### Phương Pháp Gọi Lambda Functions

1. **Client Gọi Trực Tiếp**
   - Client trực tiếp gọi Lambda function
   - Yêu cầu quyền IAM
   - Không khuyến nghị cho API công khai

2. **Application Load Balancer (ALB)**
   - Đóng vai trò trung gian giữa client và Lambda
   - Hiển thị Lambda function dưới dạng HTTP endpoint
   - Chức năng HTTP cơ bản

3. **API Gateway** (Khuyến Nghị)
   - Dịch vụ serverless từ AWS
   - Tạo REST APIs công khai và có thể truy cập
   - Client giao tiếp với API Gateway, sau đó proxy request đến Lambda functions

## Tại Sao Sử Dụng API Gateway?

### Ưu Điểm So Với ALB

API Gateway cung cấp nhiều hơn chỉ là một HTTP endpoint:

- **Authentication & Authorization**: Nhiều tùy chọn bảo mật
- **Usage Plans**: Kiểm soát quyền truy cập và hạn ngạch API
- **Development Stages**: Quản lý môi trường dev, test và production
- **API Versioning**: Hỗ trợ nhiều phiên bản API mà không làm hỏng clients
- **Request Throttling**: Bảo vệ chống lại yêu cầu quá mức
- **API Keys**: Quản lý quyền truy cập của client
- **Request/Response Transformation**: Xác thực và chuyển đổi dữ liệu
- **Caching**: Cache các response API để có hiệu suất tốt hơn
- **SDK Generation**: Tự động tạo client SDKs
- **WebSocket Support**: Khả năng streaming thời gian thực
- **Standards Support**: Import/export sử dụng Swagger hoặc OpenAPI 3.0

## Ứng Dụng Serverless Hoàn Chỉnh

**API Gateway + Lambda = Giải Pháp Serverless Hoàn Chỉnh**

Lợi ích:
- Không cần quản lý hạ tầng
- Tự động mở rộng quy mô
- Mô hình thanh toán theo sử dụng
- Tính khả dụng cao được tích hợp sẵn

## Các Tích Hợp API Gateway

### 1. Tích Hợp Lambda Function (Phổ Biến Nhất)
- Gọi Lambda functions
- Cách dễ nhất để hiển thị REST API
- Ứng dụng serverless hoàn chỉnh
- Backend được hỗ trợ bởi Lambda

### 2. Tích Hợp HTTP
- Hiển thị bất kỳ HTTP endpoint nào ở backend
- Ví dụ:
  - HTTP APIs tại chỗ (on-premises)
  - Application Load Balancer trên cloud
  
**Trường Hợp Sử Dụng:**
- Tận dụng giới hạn tốc độ (rate limiting)
- Thêm caching
- Triển khai xác thực người dùng
- Quản lý API keys

### 3. Tích Hợp AWS Service
- Hiển thị bất kỳ AWS API nào thông qua API Gateway
- Tích hợp trực tiếp với các dịch vụ AWS

**Ví Dụ:**
- Khởi động Step Function workflows
- Đăng messages vào SQS
- Stream dữ liệu vào Kinesis

**Trường Hợp Sử Dụng:**
- Thêm lớp xác thực
- Triển khai APIs công khai
- Triển khai kiểm soát tốc độ
- Tránh hiển thị AWS credentials

## Ví Dụ Thực Tế: Kinesis Data Streams

### Tình Huống
Gửi dữ liệu vào Kinesis Data Streams một cách an toàn mà không cần AWS credentials

### Kiến Trúc
```
Clients → API Gateway → Kinesis Data Streams
```

### Lợi Ích
- Thu thập dữ liệu an toàn
- Không cần AWS credentials cho clients
- Xác thực được xử lý bởi API Gateway
- Giới hạn tốc độ và giám sát

## Những Điểm Chính Cần Nhớ

1. API Gateway là phương pháp ưu tiên để hiển thị Lambda functions công khai
2. Cung cấp các tính năng cấp doanh nghiệp (bảo mật, throttling, caching)
3. Hỗ trợ nhiều loại tích hợp (Lambda, HTTP, AWS Services)
4. Thành phần thiết yếu cho ứng dụng serverless hoàn chỉnh
5. Có thể hoạt động như một proxy an toàn cho các dịch vụ AWS

## Các Bước Tiếp Theo

- Khám phá các deployment stages của API Gateway
- Học về các mô hình bảo mật của API Gateway
- Thực hành tạo REST APIs với backend Lambda
- Hiểu về request/response transformations
- Triển khai các chiến lược caching
