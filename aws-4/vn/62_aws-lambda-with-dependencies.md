# AWS Lambda với Dependencies - Tài Liệu Học Tập

## Tổng Quan
Hướng dẫn này giới thiệu cách tạo và triển khai AWS Lambda functions với các external dependencies sử dụng CloudShell và NPM.

## Khái Niệm Chính

### AWS Lambda
- Dịch vụ điện toán serverless
- Chạy code mà không cần cung cấp máy chủ
- Có thể bao gồm các dependencies và packages bên ngoài

### CloudShell
- Terminal dựa trên trình duyệt kết nối với tài khoản AWS
- Được cấu hình sẵn với AWS CLI và các công cụ phát triển
- NPM đã được cài đặt sẵn để quản lý packages

### NPM (Node Package Manager)
- Quản lý packages và dependencies cho Node.js
- Được sử dụng để cài đặt các thư viện cần thiết cho Lambda functions

## Quy Trình Từng Bước

### 1. Truy Cập CloudShell
- Điều hướng đến CloudShell trong AWS Console
- Cung cấp môi trường terminal sẵn sàng sử dụng

### 2. Tạo Thư Mục Lambda
```bash
mkdir lambda
cd lambda
```

### 3. Cài Đặt Text Editor (Tùy Chọn)
```bash
sudo yum install -y nano
```

### 4. Tạo File index.js
```bash
nano index.js
```

Code của Lambda function bao gồm:
- **X-Ray SDK Core**: Để distributed tracing
- **AWS SDK**: Tương tác với các dịch vụ AWS (S3 trong trường hợp này)
- **ListBuckets Operation**: Trả về danh sách các S3 buckets

### 5. Cài Đặt Dependencies
```bash
npm install aws-xray-sdk
```

Lệnh này cài đặt X-Ray SDK locally, sẽ được đóng gói cùng với Lambda function để triển khai.

## Các Thành Phần Chính

### index.js
- Handler chính của Lambda function
- Yêu cầu `xray-sdk-core` để tracing
- Sử dụng AWS SDK để giao tiếp với Amazon S3
- Thực thi operation ListBuckets

### Dependencies
- `aws-xray-sdk`: Cần thiết cho khả năng distributed tracing
- Phải được đóng gói cùng Lambda function để triển khai

## Lưu Ý Quan Trọng
- Dependencies phải được cài đặt locally trước khi đóng gói
- CloudShell cung cấp môi trường thuận tiện cho việc phát triển Lambda
- Function cần có quyền IAM phù hợp để truy cập S3

## Mục Tiêu Học Tập
✓ Tạo Lambda functions với external dependencies  
✓ Sử dụng CloudShell cho việc phát triển AWS  
✓ Quản lý Node.js packages với NPM  
✓ Đóng gói dependencies cùng Lambda functions  
✓ Tích hợp AWS X-Ray để tracing  
✓ Làm việc với AWS SDK trong Lambda functions  

## Các Bước Tiếp Theo
- Đóng gói Lambda function cùng dependencies
- Upload lên dịch vụ AWS Lambda
- Cấu hình IAM roles và permissions
- Kiểm tra việc thực thi function
- Giám sát với AWS X-Ray
