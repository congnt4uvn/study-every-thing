# Tài Liệu Học Tập AWS Lambda

## AWS Lambda là gì?

AWS Lambda là dịch vụ điện toán serverless cho phép bạn chạy code mà không cần cung cấp hoặc quản lý máy chủ.

## So sánh EC2 và Lambda

### Amazon EC2
- **Máy chủ ảo** trên cloud
- Phải được **cung cấp** với memory và CPU cụ thể
- **Chạy liên tục** bất kể có sử dụng hay không
- Cần **Auto Scaling groups** để mở rộng quy mô
- Cần quản lý thủ công việc bật/tắt để tối ưu hóa

### AWS Lambda
- **Hàm ảo** - không cần quản lý máy chủ
- Chỉ cần cung cấp code và các hàm tự động chạy
- **Giới hạn thời gian** - tối đa 15 phút mỗi lần thực thi
- **Chạy theo nhu cầu** - chỉ chạy khi được gọi
- **Tự động mở rộng quy mô** - AWS tự động cung cấp thêm functions khi cần

## Lợi ích chính của AWS Lambda

### 1. Tiết kiệm Chi phí
- **Chỉ trả tiền cho những gì bạn sử dụng**
  - Số lượng requests (lần gọi)
  - Thời gian tính toán (compute time)
- **Gói miễn phí hào phóng**
  - 1 triệu Lambda requests mỗi tháng
  - 400,000 GB-giây thời gian tính toán

### 2. Không cần Quản lý Máy chủ
- Không cần cung cấp hoặc bảo trì máy chủ
- Tập trung vào code, không phải hạ tầng

### 3. Tự động Mở rộng Quy mô
- Tự động scale dựa trên nhu cầu
- Xử lý tăng concurrency mà không cần can thiệp thủ công

### 4. Thực thi Theo Yêu cầu
- Functions chỉ chạy khi được gọi
- Không tính phí khi functions không hoạt động
- Thay đổi lớn so với EC2 instances luôn chạy truyền thống

### 5. Tích hợp AWS
- Tích hợp với nhiều dịch vụ AWS
- Dễ dàng xây dựng kiến trúc serverless phức tạp

## Các Trường hợp Sử dụng Lambda
- Ứng dụng điều khiển theo sự kiện (event-driven)
- Xử lý file theo thời gian thực
- APIs và microservices
- Chuyển đổi dữ liệu
- Tác vụ theo lịch trình
- Backend cho IoT

## Những Điểm Chính Cần Nhớ
✓ Điện toán serverless - không cần quản lý máy chủ  
✓ Tiết kiệm chi phí - trả tiền theo mỗi lần thực thi  
✓ Tự động mở rộng quy mô  
✓ Thực thi ngắn (tối đa 15 phút)  
✓ Tích hợp liền mạch với các dịch vụ AWS
