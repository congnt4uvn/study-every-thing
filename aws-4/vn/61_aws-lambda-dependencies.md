# AWS Lambda Functions - Quản lý Dependencies và Đóng gói

## Tổng quan
Tài liệu này hướng dẫn cách làm việc với các thư viện phụ thuộc bên ngoài trong AWS Lambda functions, vượt xa các hàm đơn giản để áp dụng vào thực tế.

## Khái niệm chính

### Dependencies bên ngoài
Trong các Lambda function thực tế, bạn thường cần:
- Các thư viện và gói mở rộng
- X-Ray SDK để theo dõi
- Database clients (các client kết nối cơ sở dữ liệu)
- Các thư viện bên thứ ba khác

### Đóng gói theo từng ngôn ngữ

#### JavaScript/Node.js
- Sử dụng **NPM** để quản lý gói
- Dependencies được lưu trong thư mục `node_modules`
- Bao gồm `node_modules` cùng với code khi đóng gói

#### Python
- Sử dụng **PIP** để quản lý gói
- Sử dụng target options để cài đặt dependencies
- Đóng gói dependencies cùng với code Python

#### Java
- Bao gồm các file **.jar** liên quan
- Gộp tất cả dependencies với code ứng dụng

## Quy trình triển khai

### Bước 1: Đóng gói Code
- Kết hợp code và tất cả dependencies lại với nhau
- Tạo file **ZIP** chứa mọi thứ

### Bước 2: Upload lên Lambda
Hai tùy chọn tùy thuộc vào kích thước:

1. **Upload trực tiếp** (< 50 MB)
   - Upload file ZIP trực tiếp lên Lambda
   
2. **Upload qua S3** (≥ 50 MB)
   - Trước tiên upload lên Amazon S3
   - Sau đó tham chiếu vị trí S3 từ Lambda

## Lưu ý quan trọng

### Native Libraries (Thư viện gốc)
- Phải được biên dịch trên **Amazon Linux**
- Đảm bảo tương thích với môi trường runtime của Lambda
- Sử dụng Lambda layers cho các native dependencies có thể tái sử dụng

### AWS SDK
- **Được cài đặt sẵn** trong mọi Lambda function
- Không cần đóng gói AWS SDK cùng code
- Tiết kiệm kích thước gói và thời gian upload

## Thực hành tốt nhất
1. Giữ kích thước gói tối thiểu
2. Sử dụng Lambda Layers cho các dependencies dùng chung
3. Xóa các file không cần thiết trước khi nén
4. Test gói ở local trước khi triển khai
5. Giám sát kích thước gói để không vượt quá giới hạn

## Tóm tắt
- Luôn nén code + dependencies lại với nhau
- Chọn phương thức upload dựa trên kích thước gói (ngưỡng 50 MB)
- Native libraries cần biên dịch trên Amazon Linux
- AWS SDK có sẵn - không cần đóng gói
