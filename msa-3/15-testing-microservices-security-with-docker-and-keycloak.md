# Kiểm Thử Bảo Mật Microservices với Docker và Keycloak

## Tổng Quan

Hướng dẫn này trình bày cách kiểm thử cấu hình bảo mật OAuth2 trong kiến trúc microservices sử dụng Docker Compose, Spring Cloud Gateway và Keycloak làm máy chủ ủy quyền.

## Yêu Cầu Trước Khi Bắt Đầu

- Docker Desktop đã cài đặt và đang chạy
- Postman để kiểm thử API
- Hiểu biết cơ bản về các luồng OAuth2
- Các microservices (Accounts, Cards, Loans) đã cấu hình với Spring Security

## Khởi Động Dịch Vụ với Docker Compose

### Chạy Docker Compose

Thực thi lệnh Docker Compose để khởi động tất cả containers:

```bash
docker-compose up
```

### Xác Minh Trạng Thái Container

1. Kiểm tra Docker Desktop để xác nhận tất cả containers đang chạy
2. Xác minh container Keycloak đang chạy trên cổng **7080**
3. Lưu ý rằng các microservices Accounts, Cards và Loans **không có ánh xạ cổng ra bên ngoài**
4. Các microservices này chỉ có thể truy cập được trong mạng Docker

### Kiểm Thử Truy Cập Trực Tiếp

Khi cố gắng truy cập trực tiếp vào các microservices:

- **Accounts** (cổng 8080): Bị từ chối kết nối
- **Cards** (cổng 9000): Bị từ chối kết nối
- **Loans** (cổng 8090): Bị từ chối kết nối

Điều này xác nhận rằng các microservices được cô lập trong mạng Docker và chỉ có thể truy cập thông qua Gateway.

## Kiểm Thử Bảo Mật Gateway

### Các Endpoint Công Khai (Permit All)

Kiểm thử các GET API thông qua Gateway được cấu hình với `permitAll()`:

1. **API Accounts**: Trả về phản hồi thành công
2. **API Cards**: Trả về phản hồi thành công
3. **API Loans**: Trả về phản hồi thành công

Các endpoint này hoạt động mà không cần xác thực, xác nhận cấu hình permit-all đang hoạt động.

### Các Endpoint Được Bảo Mật

Cố gắng truy cập các endpoint được bảo mật (ví dụ: API Tạo Tài Khoản) mà không có xác thực sẽ trả về:

```
HTTP 401 Unauthorized
```

Điều này xác nhận bảo mật đã được cấu hình đúng cách.

## Cấu Hình Keycloak để Kiểm Thử

### Tại Sao Phải Cấu Hình Lại Keycloak?

Khi Docker Compose tạo container Keycloak mới:
- Các cấu hình client và user trước đó bị mất
- Cơ sở dữ liệu H2 nội bộ được đặt lại (chế độ phát triển)
- Trong môi trường production, sử dụng cơ sở dữ liệu bên ngoài để lưu trữ lâu dài

### Truy Cập Bảng Điều Khiển Quản Trị Keycloak

1. Điều hướng đến: `http://localhost:7080`
2. Nhấp vào **Administration Console**
3. Đăng nhập với thông tin: `admin` / `admin`

## Kiểm Thử Luồng Client Credentials Grant

### Bước 1: Tạo Client trong Keycloak

1. Điều hướng đến **Clients** → **Create Client**
2. **Client ID**: `easybank-callcenter-cc`
3. Nhấp **Next**
4. Bật **Client Authentication**
5. Tắt **Standard Flow** và **Direct Access Grants**
6. Bật **Service Account Roles**
7. Nhấp **Next** → **Save**

### Bước 2: Cấu Hình Client Secret

1. Vào tab **Credentials**
2. Sao chép client secret được tạo
3. Cập nhật client secret trong các request Postman

### Bước 3: Tạo Realm Roles

Tạo các vai trò sau trong **Realm Roles**:

1. **ACCOUNTS**
2. **LOANS**
3. **CARDS**

### Bước 4: Gán Roles cho Client

1. Vào **Clients** → Chọn `easybank-callcenter-cc`
2. Điều hướng đến tab **Service Account Roles**
3. Nhấp **Assign Role**
4. Chọn: ACCOUNTS, CARDS, LOANS
5. Nhấp **Assign**

### Bước 5: Kiểm Thử với Postman

1. Lấy access token mới sử dụng client credentials
2. Kiểm thử **API Tạo Accounts**: ✓ Phản hồi thành công
3. Kiểm thử **API Tạo Cards**: ✓ Phản hồi thành công
4. Kiểm thử **API Tạo Loans**: ✓ Phản hồi thành công
5. Kiểm thử **API GET Accounts** (lấy tất cả thông tin): ✓ Phản hồi thành công

## Kiểm Thử Luồng Authorization Code Grant

### Bước 1: Tạo Client cho Authorization Code Flow

1. Điều hướng đến **Clients** → **Create Client**
2. **Client ID**: Sao chép từ cấu hình Postman
3. Nhấp **Next**
4. Bật **Client Authentication**
5. Tắt **Direct Access Grants**
6. Bật **Standard Flow**
7. Nhấp **Next**

### Bước 2: Cấu Hình Redirect URLs

1. **Valid Redirect URIs**: `*` (để kiểm thử; sử dụng URL cụ thể trong production)
2. **Web Origins**: `*`
3. Nhấp **Save**
4. Vào tab **Credentials** và sao chép client secret
5. Cập nhật client secret trong Postman

### Bước 3: Tạo End User

1. Điều hướng đến **Users** → **Create User**
2. **Username**: `madan`
3. **Email**: `tutor@eazybank.com`
4. Bật **Email Verified**
5. Nhấp **Create**

### Bước 4: Đặt Mật Khẩu cho User

1. Vào tab **Credentials**
2. Nhấp **Set Password**
3. **Password**: `12345`
4. Tắt toggle **Temporary**
5. Nhấp **Save**

### Bước 5: Gán Roles cho User

1. Vào tab **Role Mapping**
2. Nhấp **Assign Role**
3. Chọn: ACCOUNTS, CARDS, LOANS
4. Nhấp **Assign**

### Bước 6: Kiểm Thử Authorization Code Flow

1. Trong Postman, nhấp **Get New Access Token**
2. Trình duyệt mở trang đăng nhập Keycloak
3. Nhập thông tin đăng nhập: `madan` / `12345`
4. Nhấp **Sign In**
5. Được chuyển hướng trở lại Postman
6. Nhấp **Proceed** và **Use Token**

### Bước 7: Kiểm Thử APIs

1. **API Accounts**: ✓ Phản hồi thành công
2. **API Cards**: ✓ Phản hồi thành công (cập nhật client secret trước)
3. **API Loans**: ✓ Phản hồi thành công (cập nhật client secret trước)

## Lợi Ích Bảo Mật

Kiến trúc đã triển khai cung cấp:

1. **Cô Lập Mạng**: Các microservices không được phơi bày ra thế giới bên ngoài
2. **Bảo Vệ Gateway**: Chỉ Gateway có thể giao tiếp với các dịch vụ backend
3. **Bảo Mật OAuth2**: Cả hai luồng client credentials và authorization code đều hoạt động
4. **Kiểm Soát Truy Cập Dựa trên Vai Trò**: Ủy quyền chi tiết với realm roles

## Tóm Tắt

✅ Tất cả containers chạy thành công trong mạng Docker
✅ Các microservices được cô lập khỏi truy cập bên ngoài
✅ Cấu hình bảo mật Gateway hoạt động
✅ Luồng Client Credentials Grant đã được kiểm thử và xác minh
✅ Luồng Authorization Code Grant đã được kiểm thử và xác minh
✅ Ủy quyền dựa trên vai trò hoạt động đúng cách

## Mã Nguồn

Tất cả các thay đổi được thảo luận trong hướng dẫn này có sẵn trong repository GitHub dưới thư mục **section12**.

## Các Bước Tiếp Theo

- Triển khai các tính năng bảo mật bổ sung
- Cấu hình Keycloak cho môi trường production với cơ sở dữ liệu bên ngoài
- Khám phá các kịch bản ủy quyền nâng cao
- Triển khai xử lý refresh token

---

**Chúc Mừng!** Bây giờ bạn đã hiểu cách bảo mật microservices sử dụng OAuth2, Spring Security và Keycloak. Đây là một cột mốc quan trọng trong hành trình microservices của bạn.