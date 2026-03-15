# Tài Liệu Học Tập AWS API Gateway và Lambda

## Tổng Quan
Tài liệu này trình bày các kiến thức cơ bản về tích hợp AWS API Gateway với Lambda functions, hướng dẫn cách tạo RESTful APIs để kích hoạt các hàm serverless.

## Các Loại API trong API Gateway

AWS API Gateway cung cấp nhiều loại API:

1. **HTTP APIs** - APIs RESTful nhẹ, độ trễ thấp
2. **WebSocket APIs** - Dành cho giao tiếp hai chiều thời gian thực
3. **REST APIs** - APIs đầy đủ tính năng (công khai hoặc riêng tư)

Tài liệu này tập trung vào **REST APIs**.

## Các Loại Endpoint API

Khi tạo REST API, bạn có thể chọn một trong ba loại endpoint:

### Regional (Khu vực)
- Triển khai trong một AWS region duy nhất
- Tốt nhất cho ứng dụng phục vụ người dùng trong một khu vực địa lý cụ thể
- Độ trễ thấp hơn cho người dùng trong khu vực

### Edge-Optimized (Tối ưu hóa biên)
- Triển khai trên nhiều edge locations sử dụng CloudFront
- API vẫn nằm trong một region nhưng được phân phối tại các điểm biên
- Tốt nhất cho người dùng phân tán về mặt địa lý
- Tự động định tuyến đến edge location gần nhất

### Private (Riêng tư)
- Chỉ có thể truy cập trong VPC của bạn
- Không được công khai ra internet
- Tốt nhất cho ứng dụng nội bộ và microservices

## Các Loại Tích Hợp

API Gateway hỗ trợ năm loại tích hợp:

1. **Lambda Function** - Gọi các AWS Lambda functions
2. **HTTP** - Chuyển tiếp requests đến HTTP endpoints
3. **Mock** - Trả về responses mà không cần tích hợp backend (hữu ích cho testing)
4. **AWS Service** - Tích hợp trực tiếp với các dịch vụ AWS (bất kỳ dịch vụ nào, bất kỳ region nào)
5. **VPC Link** - Kết nối đến tài nguyên riêng tư trong VPC của bạn

## Tạo Lambda Function cho API Gateway

### Cấu Trúc Lambda Function Cơ Bản

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda',
        'headers': {
            'Content-Type': 'application/json'
        }
    }
```

### Các Thành Phần Chính:
- **statusCode**: Mã trạng thái HTTP (200 cho thành công)
- **body**: Nội dung phản hồi
- **headers**: HTTP headers (Content-Type chỉ định định dạng phản hồi)

## Quy Trình Tích Hợp Từng Bước

### 1. Tạo API trong API Gateway
- Chọn loại REST API
- Chọn loại endpoint (Regional, Edge-optimized, hoặc Private)
- Đặt tên cho API của bạn (ví dụ: "MyFirstAPI")

### 2. Tạo Method
- Click "Create method"
- Chọn HTTP verb (GET, POST, PUT, DELETE, v.v.)
- Chọn loại tích hợp (Lambda Function)

### 3. Tạo Lambda Function
- Truy cập AWS Lambda console
- Tạo function mới (ví dụ: "api-gateway-route-gets")
- Chọn runtime (Python 3.11 hoặc các runtime được hỗ trợ khác)
- Deploy mã function

### 4. Kết Nối API Gateway với Lambda
- Copy Lambda function ARN (Amazon Resource Name)
- Paste ARN vào cài đặt tích hợp API Gateway
- Bật **Lambda Proxy Integration** để truyền đầy đủ request/response

## Lambda Proxy Integration

Khi được bật, Lambda Proxy Integration:
- Truyền chi tiết request đầy đủ đến Lambda (headers, query params, body, v.v.)
- Yêu cầu Lambda trả về HTTP response được định dạng đúng
- Đơn giản hóa việc xử lý request/response

## Các Tùy Chọn Cấu Hình

### Cài Đặt Timeout
- Timeout mặc định có thể được cấu hình
- Quan trọng cho các hoạt động chạy lâu
- Cân bằng giữa trải nghiệm người dùng và chi phí

## Kiểm Tra Tích Hợp

### Kiểm Tra trong Lambda Console
1. Tạo test event
2. Cấu hình event payload
3. Lưu và thực thi test
4. Xác minh phản hồi (status code, body, headers)

### Kiểm Tra trong API Gateway
1. Sử dụng tính năng test tích hợp sẵn
2. Gửi các sample requests
3. Xác minh tích hợp hoạt động từ đầu đến cuối

## Các Phương Pháp Hay Nhất

1. **Sử dụng Lambda Proxy Integration** - Đơn giản hóa xử lý request/response
2. **Đặt Timeout Phù Hợp** - Cân bằng hiệu suất và chi phí
3. **Chọn Loại Endpoint Đúng** - Dựa trên vị trí địa lý của người dùng
4. **Trả Về Status Codes Đúng** - Tuân theo chuẩn HTTP
5. **Bao Gồm Content-Type Headers** - Đảm bảo clients phân tích responses đúng cách
6. **Kiểm Tra Kỹ Lưỡng** - Kiểm tra cả Lambda và API Gateway riêng biệt

## Các Trường Hợp Sử Dụng Phổ Biến

- **RESTful APIs** - Các thao tác CRUD cho ứng dụng web/mobile
- **Webhooks** - Nhận sự kiện từ các dịch vụ bên ngoài
- **Microservices** - Xây dựng kiến trúc serverless có khả năng mở rộng
- **API Backends** - Cung cấp năng lượng cho ứng dụng mobile và web
- **Xử Lý Dữ Liệu** - Kích hoạt chuyển đổi dữ liệu qua HTTP requests

## Những Điểm Chính Cần Nhớ

- API Gateway cung cấp nhiều loại API và cấu hình endpoint
- Lambda functions có thể dễ dàng được tích hợp làm dịch vụ backend
- Proxy integration đơn giản hóa việc xử lý request/response
- Bạn có thể công khai bất kỳ dịch vụ AWS nào thông qua API Gateway
- Loại endpoint Regional phù hợp cho các ứng dụng theo khu vực
- Kiểm tra đúng cách ở mỗi lớp đảm bảo tích hợp đáng tin cậy

## Các Bước Tiếp Theo

1. Thử nghiệm với các HTTP methods khác nhau (POST, PUT, DELETE)
2. Thêm request validation và transformation
3. Triển khai authentication và authorization
4. Thiết lập custom domain names
5. Bật API caching để tăng hiệu suất
6. Cấu hình throttling và usage plans
7. Giám sát với CloudWatch logs và metrics
