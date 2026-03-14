# AWS Lambda và Mạng VPC

## Tổng Quan
Tài liệu này trình bày cách các hàm AWS Lambda tương tác với Virtual Private Clouds (VPCs) và cách cấu hình chúng để truy cập các tài nguyên riêng tư.

## Triển Khai Lambda Mặc Định

Theo mặc định, các hàm Lambda được khởi chạy **bên ngoài VPC của bạn** - chúng hoạt động trong VPC do AWS sở hữu.

### Lambda Có Thể Truy Cập Gì Theo Mặc Định:
- ✅ Các trang web công khai
- ✅ Các API bên ngoài
- ✅ Các dịch vụ AWS như DynamoDB

### Lambda Không Thể Truy Cập Gì Theo Mặc Định:
- ❌ Các EC2 instances trong VPC của bạn
- ❌ Cơ sở dữ liệu RDS trong private subnets
- ❌ Các ElastiCache clusters
- ❌ Internal Elastic Load Balancers

## Triển Khai Lambda Trong VPC Của Bạn

Để truy cập các tài nguyên riêng tư trong VPC, bạn phải cấu hình Lambda chạy trong VPC của mình.

### Yêu Cầu Cấu Hình:
1. **VPC ID** - Chỉ định VPC của bạn
2. **Subnets** - Xác định subnets sẽ sử dụng
3. **Security Group** - Gán security group cho Lambda

### Cách Hoạt Động:

Khi bạn cấu hình Lambda cho VPC access, AWS tự động tạo một **Elastic Network Interface (ENI)** trong các subnets bạn đã chọn.

#### IAM Role Bắt Buộc:
- **Lambda VPC Access Execution Role** - Lambda cần role này để tạo ENI

### Luồng Mạng:

```
Lambda Function → ENI (với Lambda Security Group) → Tài nguyên Riêng tư (ví dụ: RDS)
```

### Cấu Hình Security Group:

Để Lambda truy cập các tài nguyên như RDS:
- **RDS security group** phải cho phép lưu lượng inbound từ **Lambda security group**
- Tương tự như cách bạn cấu hình quyền truy cập cho các EC2 instances

## Những Điểm Quan Trọng Cần Nhớ:

1. Các hàm Lambda chạy bên ngoài VPC của bạn theo mặc định
2. Cấu hình VPC là bắt buộc để truy cập tài nguyên riêng tư
3. Lambda tạo ENI trong subnets của bạn (không nhìn thấy được)
4. Các quy tắc security group phù hợp là thiết yếu cho kết nối
5. Lambda cần quyền IAM thích hợp để tạo ENIs

## Các Trường Hợp Sử Dụng:

- Truy cập cơ sở dữ liệu RDS riêng tư
- Kết nối với các ElastiCache clusters
- Giao tiếp với internal load balancers
- Tương tác với các EC2 instances trong private subnets
