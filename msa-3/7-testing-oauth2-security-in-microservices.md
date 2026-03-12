# Kiểm Thử Bảo Mật OAuth2 trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách kiểm thử cấu hình bảo mật OAuth2 trong kiến trúc microservices Spring Boot, tập trung vào việc bảo mật các API thông qua Gateway Server với xác thực access token.

## Yêu Cầu Tiên Quyết

Trước khi kiểm thử, đảm bảo tất cả các ứng dụng sau được khởi động theo thứ tự:

1. **Config Server** - Quản lý cấu hình
2. **Eureka Server** - Khám phá dịch vụ
3. **Microservices**:
   - Accounts (Tài khoản)
   - Loans (Khoản vay)
   - Cards (Thẻ)
4. **Gateway Server** - API Gateway có bảo mật

## Kiểm Thử GET APIs Không Bảo Mật

### Tổng Quan
Tất cả các GET APIs trong microservices được cấu hình để hoạt động mà không cần xác thực.

### Các Test Cases

#### 1. Accounts Microservice - Contact Info
- **Endpoint**: `/contact-info`
- **Phương thức**: GET
- **Xác thực**: Không yêu cầu
- **Kết quả mong đợi**: 200 OK với phản hồi thành công
- **Xác nhận**: Xác nhận không cần bảo mật cho các thao tác GET trên accounts microservice

#### 2. Cards Microservice - Java Version
- **Endpoint**: `/java-version`
- **Phương thức**: GET
- **Xác thực**: Không yêu cầu
- **Kết quả mong đợi**: 200 OK với phản hồi thành công

#### 3. Loans Microservice - Build Info
- **Endpoint**: `/build-info`
- **Phương thức**: GET
- **Xác thực**: Không yêu cầu
- **Kết quả mong đợi**: 200 OK với phản hồi thành công

## Kiểm Thử POST APIs Được Bảo Mật

### Không Có Xác Thực

#### Create Account API (Không Được Phép)
- **Endpoint**: `/create`
- **Phương thức**: POST
- **Xác thực**: Không có
- **Kết quả mong đợi**: 401 Unauthorized (Không được phép)
- **Lý do**: Không cung cấp access token
- **Xác nhận**: Xác nhận Gateway Server đang hoạt động bảo mật đúng cách

### Với Xác Thực OAuth2

#### Cấu Hình OAuth2 trong Postman

1. **Chọn Loại Xác Thực**:
   - Điều hướng đến tab Authorization
   - Chọn `OAuth 2.0` từ dropdown Type

2. **Cấu Hình OAuth2 Settings**:
   - **Token Name**: `clientcredentials_access_token`
   - **Grant Type**: `Client Credentials`
   - **Access Token URL**: Sử dụng endpoint OpenID Connect Token
   - **Client ID**: Client ID đã đăng ký của bạn
   - **Client Secret**: Client secret của bạn
   - **Scope**: Các scope cần thiết
   - **Client Authentication**: Gửi client credentials trong body

3. **Lấy Access Token**:
   - Click "Get New Access Token"
   - Xác thực sẽ hoàn tất
   - Token sẽ được tạo
   - Click "Use Token" để áp dụng vào request

4. **Cấu Hình Token**:
   - **Token Type**: Access Token (không phải ID Token)
   - **Add to**: Request Header
   - **Header Prefix**: Bearer

#### Kiểm Thử Create Account API (Được Phép)

- **Endpoint**: `/create`
- **Phương thức**: POST
- **Xác thực**: Bearer token (OAuth2)
- **Headers**: Authorization: Bearer {access_token}
- **Body**: Dữ liệu tạo tài khoản
- **Kết quả mong đợi**: 200 OK với phản hồi thành công
- **Các Lần Gọi Tiếp Theo**: Có thể trả về 400 Bad Request nếu khách hàng đã đăng ký

#### Kiểm Thử với Token Không Hợp Lệ

- **Hành động**: Làm hỏng access token (xóa một số ký tự)
- **Kết quả mong đợi**: 401 Unauthorized
- **Xác nhận**: Resource server (Gateway) xác thực access token đúng cách

#### Kiểm Thử Create Card API

- **Endpoint**: `/create` (Cards microservice)
- **Phương thức**: POST
- **Xác thực**: OAuth 2.0 với client credentials
- **Cấu hình**: Giống như accounts (token name, grant type, client credentials, scope)
- **Các bước**:
  1. Lấy access token mới
  2. Click "Proceed"
  3. Sử dụng token
  4. Gửi request
- **Kết quả mong đợi**: 200 OK với phản hồi thành công

#### Kiểm Thử Create Loan API

- **Endpoint**: `/create` (Loans microservice)
- **Phương thức**: POST
- **Xác thực**: OAuth 2.0 với client credentials
- **Các bước**:
  1. Lấy access token mới
  2. Click "Proceed"
  3. Sử dụng token
  4. Gửi request
- **Kết quả mong đợi**: 200 OK với phản hồi thành công

## Kiểm Thử Composite APIs

### Fetch Customer Details

- **Endpoint**: `/fetchCustomerDetails`
- **Phương thức**: GET
- **Xác thực**: Không yêu cầu (HTTP GET)
- **Phản hồi**: Trả về dữ liệu tổng hợp bao gồm:
  - Chi tiết tài khoản
  - Chi tiết khoản vay
  - Chi tiết thẻ
- **Kết quả mong đợi**: 200 OK với thông tin khách hàng đầy đủ

## Những Điểm Chính

### Cấu Hình Bảo Mật

1. **GET APIs**: Không yêu cầu xác thực - cho phép truy cập công khai vào các thao tác đọc
2. **POST APIs**: Yêu cầu OAuth2 access token - thực thi ủy quyền cho các thao tác ghi
3. **Gateway Server**: Hoạt động như OAuth2 Resource Server, xác thực tất cả access token đến

### Lợi Ích của Postman

- **Quản Lý Token Tự Động**: Postman xử lý việc tạo và làm mới token
- **Không Cần Copy/Paste Thủ Công**: Token được tự động chèn vào request headers
- **Làm Mới Token Dễ Dàng**: Click để lấy token mới và tự động thay thế token hết hạn
- **Tạo Header Đúng Cách**: Tự động thêm prefix Bearer vào authorization header

### Best Practices Khi Kiểm Thử

1. Bắt đầu với các endpoint không bảo mật để xác minh kết nối cơ bản
2. Kiểm thử các endpoint được bảo mật mà không có token để xác minh bảo mật được thực thi (lỗi 401)
3. Cấu hình OAuth2 đúng cách trong công cụ kiểm thử
4. Kiểm thử với token hợp lệ để xác minh truy cập được ủy quyền
5. Kiểm thử với token không hợp lệ/bị làm hỏng để xác minh việc xác thực token
6. Kiểm thử tất cả microservices để đảm bảo triển khai bảo mật nhất quán

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

- **401 Unauthorized**: Thiếu hoặc access token không hợp lệ
- **400 Bad Request**: Dữ liệu đã tồn tại hoặc request body không hợp lệ
- **Token Hết Hạn**: Lấy access token mới sử dụng cấu hình OAuth2 của Postman
- **Client Cấu Hình Sai**: Xác minh client ID, secret, scope và token URL

## Kết Luận

Kiểm thử này chứng minh một kiến trúc microservices được bảo mật đúng cách, trong đó:
- Gateway Server hoạt động như một OAuth2 Resource Server tập trung
- Các thao tác GET là công khai
- Các thao tác POST yêu cầu OAuth2 access token hợp lệ
- Xác thực token ngăn chặn truy cập trái phép
- Postman đơn giản hóa quy trình kiểm thử OAuth2

Triển khai này bảo mật thành công microservices sử dụng luồng OAuth2 Client Credentials grant flow.