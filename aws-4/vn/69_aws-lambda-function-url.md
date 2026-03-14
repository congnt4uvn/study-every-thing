# Hướng Dẫn Học AWS Lambda Function URL

## Tổng Quan
AWS Lambda Function URL cung cấp một endpoint HTTP(S) chuyên dụng cho Lambda function của bạn, cho phép bạn gọi nó trực tiếp mà không cần API Gateway.

## Hướng Dẫn Từng Bước

### 1. Tạo Lambda Function
- Tên function: `lambda-demo-url`
- Runtime: Python 3.9
- Nhấn **Create function**

### 2. Kiểm Tra Function
1. Nhấn vào **Test**
2. Tạo một Test Event mới
3. Thêm tên: `test`
4. Nhấn **Save**
5. Chạy test

**Kết Quả Mong Đợi:**
```json
{
  "statusCode": 200,
  "body": "Hello from Lambda"
}
```

### 3. Xuất Bản Phiên Bản
1. Nhấn **Publish new version**
2. Tên phiên bản: `version 1`
3. Điều này tạo ra một phiên bản bất biến của function

### 4. Tạo Alias
1. Tạo một alias mới
2. Tên alias: `dev`
3. Trỏ nó đến `version 1`
4. Nhấn **Save**

> **Lưu ý:** Alias `dev` bây giờ trỏ đến version 1

### 5. Tạo Function URL
1. Cuộn xuống hoặc chọn **Function URL** từ menu bên trái
2. Nhấn **Create Function URL**

#### Các Tùy Chọn Cấu Hình:

**Loại Xác Thực:**
- **IAM** - Yêu cầu thông tin xác thực AWS
- **NONE** - Truy cập công khai (chọn tùy chọn này)

**Resource Policy:**
- Tự động tạo khi sử dụng xác thực NONE
- Cho phép bất kỳ ai truy cập Lambda Function URL
- AuthType được đặt thành NONE

**CORS (Tùy Chọn):**
- Cấu hình Cross-Origin Resource Sharing nếu cần
- Chỉ định các origin được phép
- Chỉ định các header được hiển thị
- Không bắt buộc cho thiết lập cơ bản

### 6. Truy Cập Function Của Bạn
1. Sao chép Function URL (URL này vĩnh viễn cho alias)
2. Mở URL trong trình duyệt web
3. Bạn sẽ thấy: `Hello from Lambda`

## Các Khái Niệm Chính

### Lợi Ích Của Function URL
- Endpoint HTTP(S) trực tiếp cho Lambda
- Không cần API Gateway
- URL vĩnh viễn cho mỗi alias
- Các tùy chọn xác thực đơn giản

### Các Loại Xác Thực
- **IAM**: Truy cập bảo mật với thông tin xác thực AWS
- **NONE**: Truy cập công khai (yêu cầu resource policy)

### Resource Policy
- Tự động tạo với Function URL
- Kiểm soát quyền truy cập vào Lambda function
- Đảm bảo cấu hình bảo mật phù hợp

### Cấu Hình CORS
- Cho phép các yêu cầu cross-origin
- Cấu hình các origin được phép
- Cấu hình các header được hiển thị
- Tùy chọn cho các tình huống cơ bản

## Thực Hành Tốt Nhất
1. Sử dụng alias để quản lý các môi trường khác nhau (dev, staging, prod)
2. Chọn loại xác thực phù hợp dựa trên trường hợp sử dụng
3. Chỉ cấu hình CORS khi cần thiết
4. Kiểm tra function trước khi xuất bản phiên bản
5. Sử dụng versioning cho triển khai production

## Các Trường Hợp Sử Dụng Phổ Biến
- Webhooks
- REST APIs đơn giản
- Microservices
- Public endpoints
- Tích hợp với các dịch vụ bên ngoài
