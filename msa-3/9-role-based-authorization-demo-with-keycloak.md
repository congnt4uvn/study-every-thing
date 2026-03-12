# Demo Phân Quyền Dựa Trên Vai Trò với Keycloak và Spring Boot Gateway

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và kiểm thử phân quyền dựa trên vai trò trong kiến trúc microservices Spring Boot sử dụng OAuth 2.0 Client Credentials Grant Flow với Keycloak làm máy chủ phân quyền.

## Yêu Cầu Tiên Quyết

- Máy chủ phân quyền Keycloak đã được cấu hình
- Spring Boot Gateway được cấu hình làm OAuth2 Resource Server
- Postman để kiểm thử API
- Ứng dụng client đã được đăng ký với Keycloak (eazybank-callcenter)

## Kiểm Thử Phân Quyền với Accounts API

### Bước 1: Tạo Tài Khoản

1. Mở Postman và điều hướng đến endpoint `accounts/api/create`
2. Cập nhật số điện thoại trong request body để tránh trùng lặp
   - Thay đổi từ `687` thành `688`
3. Chuyển đến tab **Authorization**
4. Nhấp vào **Get New Access Token**
   - Keycloak sẽ đính kèm thông tin vai trò vào access token
5. Nhấp **Use Token**
6. Nhấp **Send** để gửi request

**Kết Quả Mong Đợi:** HTTP 201 - Tài khoản được tạo thành công

## Xử Lý Lỗi Phân Quyền

### Kiểm Thử Cards API Không Có Vai Trò Phù Hợp

1. Điều hướng đến Cards API trong Postman
2. Thử tạo thông tin thẻ với cùng số điện thoại
3. Nhấp **Get New Access Token**
4. Nhấp **Proceed** và **Use Token**
5. Nhấp **Send**

**Kết Quả Mong Đợi:** HTTP 403 Forbidden

**Giải Thích:**
- HTTP 401: Unauthorized (xác thực thất bại)
- HTTP 403: Forbidden (đã xác thực nhưng không đủ quyền)

## Cấu Hình Vai Trò Trong Keycloak

### Thêm Vai Trò CARDS

1. Mở **Keycloak Administration Console**
2. Điều hướng đến **Realm roles**
3. Nhấp **Create role**
4. Nhập các thông tin sau:
   - **Name:** `CARDS` (phân biệt chữ hoa chữ thường)
   - **Description:** `Cards Role`
5. Nhấp **Save**

### Gán Vai Trò Cho Ứng Dụng Client

1. Chuyển đến **Clients**
2. Chọn `eazybank-callcenter`
3. Điều hướng đến **Service account roles**
4. Nhấp **Assign role**
5. Chọn vai trò `CARDS`
6. Nhấp **Assign**

### Kiểm Thử Với Access Token Mới

1. Quay lại Postman
2. Nhấp **Get New Access Token** (token này sẽ bao gồm vai trò CARDS)
3. Nhấp **Use Token**
4. Xác minh token trên [jwt.io](https://jwt.io)
   - Bạn sẽ thấy cả hai vai trò `Accounts` và `Cards` trong payload của token
5. Nhấp **Send**

**Kết Quả Mong Đợi:** HTTP 200/201 - Phản hồi thành công

## Cấu Hình Phân Quyền Loans API

### Kiểm Thử Loans API Không Có Vai Trò Phù Hợp

1. Điều hướng đến Loans API
2. Sử dụng số điện thoại `688`
3. Lấy access token mới
4. Nhấp **Send**

**Kết Quả Mong Đợi:** HTTP 403 Forbidden (thiếu vai trò LOANS)

### Thêm Vai Trò LOANS

1. Mở **Keycloak Administration Console**
2. Điều hướng đến **Realm roles**
3. Nhấp **Create role**
4. Nhập các thông tin sau:
   - **Name:** `LOANS` (phân biệt chữ hoa chữ thường - rất quan trọng!)
   - **Description:** `Loans Description`
5. Nhấp **Save**

### Gán Vai Trò LOANS

1. Chuyển đến **Clients**
2. Chọn `eazybank-callcenter`
3. Điều hướng đến **Service account roles**
4. Nhấp **Assign role**
5. Chọn vai trò `LOANS`
6. Nhấp **Assign**

### Kiểm Thử Với Quyền Đã Cập Nhật

1. Quay lại Postman
2. Nhấp **Get New Access Token**
3. Nhấp **Proceed** và **Use Token**
4. Nhấp **Send**

**Kết Quả Mong Đợi:** HTTP 200/201 - Phản hồi thành công

## Những Điểm Chính Cần Ghi Nhớ

### Xác Thực vs Phân Quyền

- **Xác Thực (401):** Xác minh danh tính của người dùng/client
- **Phân Quyền (403):** Xác minh người dùng/client có quyền phù hợp

### OAuth 2.0 Client Credentials Flow

- Phù hợp cho giao tiếp máy-máy (machine-to-machine)
- Access token chứa thông tin vai trò
- Keycloak đóng vai trò là máy chủ phân quyền
- Gateway đóng vai trò là resource server

### Thực Hành Tốt Nhất

1. **Phân Biệt Chữ Hoa Chữ Thường:** Tên vai trò phân biệt chữ hoa chữ thường - đảm bảo khớp chính xác
2. **Làm Mới Token:** Luôn lấy access token mới sau khi thay đổi vai trò
3. **Xác Minh Token:** Sử dụng công cụ như jwt.io để kiểm tra nội dung token
4. **Yêu Cầu Phức Tạp:** Các tình huống thực tế có thể yêu cầu phân cấp vai trò phức tạp hơn

### Kiến Trúc Bảo Mật

- **Keycloak:** Máy chủ phân quyền trung tâm quản lý vai trò và token
- **Spring Boot Gateway:** OAuth2 Resource Server thực thi phân quyền
- **Ứng Dụng Client:** Sử dụng client credentials để lấy access token
- **Microservices:** Được bảo vệ bằng kiểm soát truy cập dựa trên vai trò

## Học Thêm

Để tìm hiểu sâu hơn về các khái niệm Spring Security, bao gồm:
- Cơ chế xác thực nâng cao
- Bảo mật cấp độ phương thức
- Logic phân quyền tùy chỉnh
- Thực hành tốt nhất về bảo mật

Hãy cân nhắc đăng ký một khóa học Spring Security chuyên sâu.

## Kết Luận

Bản demo này đã trình bày việc triển khai phân quyền dựa trên vai trò sử dụng:
- OAuth 2.0 Client Credentials Grant Flow
- Keycloak làm Máy Chủ Phân Quyền
- Spring Boot Gateway làm Resource Server
- Kiểm soát truy cập dựa trên vai trò cho microservices

Các nguyên tắc tương tự có thể được áp dụng cho các yêu cầu bảo mật phức tạp hơn trong môi trường production.

---

**Các Bước Tiếp Theo:** Tiếp tục khám phá các OAuth 2.0 grant flow bổ sung và các mẫu bảo mật nâng cao trong kiến trúc microservices.