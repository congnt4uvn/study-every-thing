# AWS Lambda trong VPC - Tài Liệu Học Tập

## Tổng Quan
Tài liệu này hướng dẫn cách triển khai các hàm AWS Lambda trong Virtual Private Cloud (VPC) và hiểu rõ các vấn đề về mạng.

## Thực Hành Từng Bước: Lambda trong VPC

### 1. Tạo Lambda Function
- Truy cập bảng điều khiển AWS Lambda
- Tạo function mới từ scratch
- Tên function: `Lambda VPC`
- Runtime: Python 3.8
- Tạo function

### 2. Tạo Security Group cho Lambda
- Vào bảng điều khiển EC2
- Truy cập Security Groups
- Tạo security group mới:
  - Tên: `Lambda SG`
  - Gắn vào VPC của bạn
  - Không cần inbound rules
  - Outbound rules mặc định
- Mục đích: Để gắn vào Lambda function khi triển khai trong VPC

### 3. Cấu Hình VPC cho Lambda
- Vào tab Configuration của Lambda function
- Chọn VPC từ menu bên trái
- Click Edit để gắn Lambda function vào VPC

## Các Khái Niệm Mạng Quan Trọng

### Giới Hạn Truy Cập Internet
⚠️ **Cảnh báo**: Khi bạn kết nối Lambda function với VPC trong tài khoản của mình:
- **Function KHÔNG có quyền truy cập internet** theo mặc định
- Ngay cả khi triển khai trong public subnets, Lambda không thể truy cập internet trực tiếp

### Yêu Cầu để Truy Cập Internet
Để cung cấp quyền truy cập internet cho Lambda function được kết nối với VPC:
1. Triển khai Lambda trong **private subnets**
2. Thiết lập **NAT Gateway** hoặc **NAT Instance** trong public subnet
3. Định tuyến lưu lượng đi ra (outbound traffic) qua NAT Gateway/Instance

### Trường Hợp Sử Dụng Phổ Biến
Lambda functions thường được triển khai trong VPC để:
- Thực hiện các thao tác cục bộ trong VPC
- Truy cập các tài nguyên riêng tư (RDS, ElastiCache, v.v.)
- Duy trì mạng an toàn và cô lập

## Điểm Chính Cần Nhớ
- Lambda functions trong VPC cần cấu hình mạng phù hợp
- Chỉ có public subnets không cung cấp quyền truy cập internet cho Lambda
- Sử dụng private subnets + NAT Gateway cho Lambda có internet trong VPC
- Security groups kiểm soát quyền truy cập vào Lambda functions trong VPC
