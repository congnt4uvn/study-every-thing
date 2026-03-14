# Tích hợp AWS Lambda và Application Load Balancer

## Tổng quan
Hướng dẫn này trình bày cách tích hợp AWS Lambda functions với Application Load Balancer (ALB) để tạo endpoint HTTP serverless.

## Mục tiêu
- Tạo Lambda function
- Cấu hình Application Load Balancer
- Thiết lập target group cho tích hợp Lambda
- Thiết lập giao tiếp an toàn giữa ALB và Lambda

## Yêu cầu trước khi bắt đầu
- Tài khoản AWS với quyền phù hợp
- Hiểu biết cơ bản về các dịch vụ AWS
- Quen thuộc với Python (cho Lambda function)

## Triển khai từng bước

### 1. Tạo Lambda Function

**Cấu hình Function:**
- **Tên:** Lambda-alb
- **Runtime:** Python 3.x
- **Mục đích:** Backend xử lý các request từ ALB

**Các bước:**
1. Truy cập AWS Lambda console
2. Nhấp "Create function"
3. Nhập tên function: `Lambda-alb`
4. Chọn runtime: Python version 3
5. Nhấp "Create function"

### 2. Tạo Application Load Balancer

**Cấu hình ALB:**
- **Tên:** demo-Lambda-alb
- **Loại:** Application Load Balancer
- **Scheme:** Internet-facing (Hướng ra Internet)
- **Loại địa chỉ IP:** IPv4
- **Availability Zones:** Triển khai trên 3 AZs để có độ sẵn sàng cao

**Các bước:**
1. Truy cập EC2 > Load Balancers
2. Nhấp "Create Load Balancer"
3. Chọn "Application Load Balancer"
4. Cấu hình các thiết lập cơ bản với tên và scheme
5. Chọn 3 availability zones để đảm bảo dự phòng

### 3. Cấu hình Security Group

**Thiết lập Security Group:**
- **Tên:** DemoLambdaALBSG
- **Inbound Rules (Quy tắc đầu vào):**
  - Giao thức: HTTP
  - Cổng: 80
  - Nguồn: 0.0.0.0/0 (mọi nơi IPv4)

**Các bước:**
1. Tạo security group mới
2. Đặt tên: `DemoLambdaALBSG`
3. Thêm inbound rule cho HTTP (port 80) từ mọi nguồn
4. Tạo security group
5. Gán cho load balancer

### 4. Tạo Target Group

**Cấu hình Target Group:**
- **Tên:** demo-tg-lambda
- **Loại Target:** Lambda function
- **Dịch vụ liên kết:** Chỉ Application Load Balancer

**Các bước:**
1. Truy cập Target Groups
2. Nhấp "Create target group"
3. Chọn loại target: "Lambda function"
4. Nhập tên: `demo-tg-lambda`
5. Nhấp "Next"
6. Chọn Lambda function: `Lambda-alb`
7. Nhấp "Create target group"

### 5. Cấu hình Listener

**Thiết lập Listener:**
- **Giao thức:** HTTP
- **Cổng:** 80
- **Hành động mặc định:** Chuyển tiếp đến target group `demo-tg-lambda`

**Các bước:**
1. Trong cấu hình ALB, thiết lập listener
2. Cấu hình lắng nghe trên port 80 (HTTP)
3. Đặt hành động mặc định là chuyển tiếp request đến `demo-tg-lambda`
4. Hoàn thành việc tạo ALB
5. Đợi quá trình provisioning hoàn tất

## Luồng kiến trúc

```
Request từ Internet (HTTP:80)
    ↓
Application Load Balancer (demo-Lambda-alb)
    ↓
Security Group (DemoLambdaALBSG)
    ↓
Target Group (demo-tg-lambda)
    ↓
Lambda Function (Lambda-alb)
```

## Các khái niệm chính

### Application Load Balancer (ALB)
- Load balancer tầng 7 (Layer 7)
- Định tuyến lưu lượng HTTP/HTTPS
- Có thể gọi Lambda functions trực tiếp
- Cung cấp tự động mở rộng và độ sẵn sàng cao

### Lambda Target Groups
- Loại target group đặc biệt cho tích hợp serverless
- Tự động xử lý việc gọi Lambda
- Không cần quản lý các EC2 instances
- Chỉ trả phí cho thời gian thực thi Lambda thực tế

### Lợi ích của tích hợp ALB + Lambda
1. **Serverless:** Không cần quản lý hạ tầng
2. **Tiết kiệm chi phí:** Trả theo từng request
3. **Có khả năng mở rộng:** Tự động scale dựa trên lưu lượng
4. **Độ sẵn sàng cao:** Triển khai Multi-AZ
5. **Đơn giản:** Tích hợp trực tiếp không cần API Gateway

## Thực hành tốt nhất

1. **Triển khai Multi-AZ:** Luôn triển khai ALB trên nhiều availability zones
2. **Security Groups:** Hạn chế lưu lượng đầu vào chỉ từ các nguồn cần thiết
3. **Cấu hình Lambda:** Đặt timeout và memory phù hợp
4. **Giám sát:** Bật CloudWatch logs cho cả ALB và Lambda
5. **Kiểm thử:** Xác minh sức khỏe target group trước khi đưa vào production

## Các bước tiếp theo

Sau khi thiết lập:
1. Cấu hình code Lambda function để xử lý sự kiện từ ALB
2. Kiểm thử tích hợp sử dụng ALB DNS name
3. Giám sát CloudWatch logs cho requests và responses
4. Tối ưu hóa hiệu suất Lambda function
5. Cân nhắc thêm custom domains và SSL certificates

## Xử lý sự cố

**Các vấn đề thường gặp:**
- Target group hiển thị trạng thái không khỏe mạnh (unhealthy)
- Lỗi timeout của Lambda function
- Security group chặn lưu lượng
- Vấn đề về quyền IAM

**Giải pháp:**
- Xác minh Lambda function đã được đăng ký trong target group
- Tăng timeout của Lambda nếu cần
- Kiểm tra quy tắc security group
- Đảm bảo IAM roles và policies phù hợp

## Kết luận

Tích hợp Lambda với Application Load Balancer cung cấp giải pháp serverless mạnh mẽ để xử lý HTTP requests mà không cần quản lý servers. Thiết lập này lý tưởng cho microservices, APIs, và các ứng dụng web cần tự động mở rộng quy mô.
