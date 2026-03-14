# AWS CloudFormation với Lambda và X-Ray

## Tổng Quan
Tài liệu này trình bày cách tạo và triển khai các hàm AWS Lambda sử dụng CloudFormation template với tính năng X-Ray tracing được kích hoạt.

## Cấu Trúc CloudFormation Template

### Tham Số (Parameters)
CloudFormation template sử dụng ba tham số để chỉ định vị trí mã nguồn của Lambda function:

1. **S3 Bucket Parameter** - Chỉ định S3 bucket nơi lưu trữ mã nguồn hàm
2. **S3 Key Parameter** - Chỉ định object key (đường dẫn) trong bucket
3. **S3 Object Version Parameter** - Chỉ định phiên bản của object

Các tham số này giúp CloudFormation xác định vị trí và lấy file zip của Lambda function từ Amazon S3.

### Tài Nguyên (Resources)

#### 1. Lambda Execution Role (IAM Role)
Một IAM role chuyên dụng cung cấp các quyền cần thiết cho Lambda function:

- **Trust Policy**: Cho phép dịch vụ Lambda assume role này
- **Permissions Policy** với nhiều statement:
  - **CloudWatch Logs**: Các action cho việc ghi log thực thi hàm
  - **X-Ray**: Các action để gửi traces đến AWS X-Ray cho distributed tracing
  - **S3 Operations**: Các thao tác `Get*` và `List*` để đọc từ Amazon S3

#### 2. Cấu Hình Lambda Function
Tài nguyên Lambda function bao gồm:

- **Handler**: `Index.handler` - Điểm vào (entry point) của hàm
- **Role**: Tham chiếu đến Lambda execution role ARN sử dụng hàm `GetAtt`
- **Code Location**: Lấy từ S3 sử dụng ba tham số đã định nghĩa trước đó
  - S3 Bucket (tham chiếu đến parameter)
  - S3 Key (tham chiếu đến parameter)
  - S3 Object Version (tham chiếu đến parameter)
- **Runtime**: Node.js 14.x
- **Timeout**: 10 giây
- **Tracing Configuration**: X-Ray được kích hoạt với mode là `Active`

## Các Tính Năng Chính

### Tích Hợp X-Ray
X-Ray tracing được kích hoạt thông qua:
1. Quyền IAM trong execution role cho các thao tác X-Ray
2. Cấu hình tracing trong Lambda function với mode được đặt là `Active`

### Lợi Ích của Infrastructure as Code
- Cấu hình hoàn chỉnh của Lambda function được định nghĩa trong CloudFormation
- Triển khai có thể tái tạo (reproducible deployments)
- Infrastructure được quản lý phiên bản (version-controlled)
- Dễ dàng cập nhật và bảo trì

## Quy Trình Triển Khai
1. Chuẩn bị mã nguồn Lambda function và upload lên S3
2. Tạo CloudFormation template (ví dụ: `lambda-xray.yaml`)
3. Triển khai template sử dụng AWS CloudFormation
4. CloudFormation sẽ tạo:
   - IAM execution role với các quyền cần thiết
   - Lambda function với X-Ray tracing được kích hoạt

## Best Practices (Thực Hành Tốt Nhất)
- Sử dụng parameters để làm cho template có thể tái sử dụng
- Luôn kích hoạt X-Ray để có khả năng quan sát tốt hơn
- Đặt timeout phù hợp cho use case của bạn
- Tuân theo nguyên tắc least privilege cho IAM roles
- Quản lý phiên bản mã nguồn Lambda của bạn trong S3

---

*Ghi Chú Học Tập: Hiểu cách định nghĩa Lambda functions trong CloudFormation templates giúp thực hiện triển khai tự động, nhất quán và quản lý infrastructure tốt hơn.*
