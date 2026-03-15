# Tài Liệu Học AWS Kiến Trúc Serverless

## Tổng Quan
Tài liệu này bao gồm các dịch vụ AWS thiết yếu để xây dựng ứng dụng serverless, bao gồm lưu trữ dữ liệu, hàm xử lý, API và xác thực người dùng.

## Các Dịch Vụ AWS

### 1. AWS Lambda
**Mục đích:** Dịch vụ tính toán serverless chạy code mà không cần quản lý server

**Tính năng chính:**
- Thực thi theo sự kiện
- Tự động mở rộng quy mô
- Trả phí theo lần thực thi
- Hỗ trợ nhiều ngôn ngữ lập trình
- Không cần quản lý server

**Trường hợp sử dụng:**
- Xử lý backend
- API backends
- Chuyển đổi dữ liệu
- Xử lý file thời gian thực

### 2. Amazon DynamoDB
**Mục đích:** Dịch vụ cơ sở dữ liệu NoSQL được quản lý hoàn toàn

**Tính năng chính:**
- Hiệu suất cao ở mọi quy mô
- Bảo mật và sao lưu tích hợp
- Bộ nhớ đệm trong RAM
- Tự động mở rộng
- Mô hình dữ liệu key-value và document

**Thực hành tốt nhất:**
- Thiết kế partition key hiệu quả
- Sử dụng index cho truy vấn linh hoạt
- Bật auto-scaling để tối ưu chi phí
- Triển khai chiến lược backup

### 3. Amazon API Gateway
**Mục đích:** Dịch vụ được quản lý hoàn toàn để tạo, xuất bản và quản lý REST API

**Tính năng chính:**
- Tạo RESTful API
- Hỗ trợ WebSocket APIs
- Chuyển đổi request/response
- Giới hạn tốc độ và throttling
- Tích hợp với Lambda functions
- Phiên bản API

**Lợi ích:**
- Phơi bày Lambda functions ra thế giới
- Không cần quản lý hạ tầng
- Giám sát và ghi log tích hợp
- Hỗ trợ tên miền tùy chỉnh

### 4. Amazon Cognito
**Mục đích:** Dịch vụ xác thực và ủy quyền người dùng

**Tính năng chính:**
- Đăng ký và đăng nhập người dùng
- Nhà cung cấp danh tính xã hội (Google, Facebook, v.v.)
- Xác thực đa yếu tố (MFA)
- User pools và identity pools
- Xác thực dựa trên token an toàn

**Triển khai:**
- User Pools: Quản lý thư mục người dùng
- Identity Pools: Cấp quyền truy cập tài nguyên AWS
- Tích hợp với API Gateway cho các endpoint được bảo mật

## Mô Hình Kiến Trúc Serverless

```
Yêu cầu từ Người dùng
    ↓
Amazon Cognito (Xác thực)
    ↓
API Gateway (REST API Endpoint)
    ↓
AWS Lambda (Logic nghiệp vụ)
    ↓
DynamoDB (Lưu trữ dữ liệu)
```

## Ưu Điểm Của Serverless

1. **Không Cần Quản Lý Server:** Tập trung vào code, không phải hạ tầng
2. **Tự Động Mở Rộng:** Xử lý lưu lượng truy cập tự động
3. **Trả Tiền Theo Sử Dụng:** Chỉ trả cho thời gian tính toán thực tế
4. **Tính Sẵn Sàng Cao:** Dự phòng tích hợp sẵn
5. **Ra Mắt Nhanh Hơn:** Phát triển và triển khai nhanh chóng

## Các Bước Bắt Đầu

1. **Thiết lập bảng DynamoDB** để lưu trữ dữ liệu
2. **Tạo Lambda functions** cho logic nghiệp vụ
3. **Cấu hình API Gateway** để phơi bày REST endpoints
4. **Triển khai Cognito** cho xác thực người dùng
5. **Kiểm tra và triển khai** API của bạn lên cloud

## Thực Hành Tốt Nhất

- Thiết kế Lambda functions không trạng thái
- Sử dụng biến môi trường cho cấu hình
- Triển khai xử lý lỗi phù hợp
- Giám sát với CloudWatch
- Sử dụng IAM roles cho bảo mật
- Tạo phiên bản cho API của bạn
- Triển khai CI/CD pipelines

## Tài Nguyên Học Thêm

- AWS Free Tier: Thực hành với tài nguyên miễn phí
- AWS Documentation: Hướng dẫn toàn diện
- AWS Training: Lộ trình chứng chỉ chính thức
- Diễn đàn Cộng đồng: AWS Developer Forums

## Kết Luận

Bằng cách kết hợp Lambda, DynamoDB, API Gateway và Cognito, bạn có thể xây dựng các ứng dụng serverless có khả năng mở rộng và bảo mật mà không cần quản lý hạ tầng. Kiến trúc này cho phép phát triển và triển khai API lên cloud một cách nhanh chóng.

---
*Ngày tạo: 15 tháng 3, 2026*
