# Kiểm Thử OAuth2 Authorization Code Grant Flow Với Postman

## Tổng Quan

Hướng dẫn này trình bày cách kiểm thử luồng OAuth2 Authorization Code Grant Type để truy cập các tài nguyên được bảo mật phía sau gateway server bằng Postman. Phương pháp này cho phép bạn mô phỏng ứng dụng UI hoặc mobile mà không cần xây dựng thực sự.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Postman
- Keycloak Authorization Server đang chạy
- Gateway Server được cấu hình như OAuth2 Resource Server
- Các microservices (Accounts, Cards, Loans) đang chạy phía sau gateway

## Cấu Hình Postman Cho Authorization Code Flow

### Bước 1: Tạo Các POST Request

Tạo ba POST request khác nhau trong Postman với tiền tố "auth code":
- Auth Code - Accounts
- Auth Code - Cards  
- Auth Code - Loans

### Bước 2: Cấu Hình Authorization

Đối với mỗi request, điều hướng đến tab **Authorization** và cấu hình như sau:

1. **Type**: Chọn `OAuth 2.0`
2. **Header Prefix**: Giữ nguyên là `Bearer`
3. **Token Name**: Nhập tên mô tả (ví dụ: `auth_code_access_token`)
4. **Grant Type**: Chọn `Authorization Code`

### Bước 3: Cấu Hình Các Tham Số OAuth2

Điền các thông tin sau trong phần "Configure New Token":

| Tham Số | Giá Trị | Mô Tả |
|---------|---------|-------|
| **Callback URL** | Tự động tạo bởi Postman | Không thể thay đổi khi sử dụng browser authorization |
| **Auth URL** | Keycloak authorization endpoint | URL nơi người dùng nhập thông tin đăng nhập |
| **Access Token URL** | Keycloak token endpoint | URL để đổi authorization code lấy access token |
| **Client ID** | Client ID của bạn | ID ứng dụng client đã đăng ký |
| **Client Secret** | Client secret của bạn | Mật khẩu ứng dụng client |
| **Scope** | `openid email profile` | Các scope bắt buộc |
| **State** | Giá trị alphanumeric ngẫu nhiên | Biến bảo vệ CSRF |
| **Client Authentication** | Send client credentials in body | Cách gửi thông tin xác thực |

### Tùy Chọn Cấu Hình Quan Trọng

- ✅ **Bật "Authorize using browser"**: Cho phép Postman chuyển hướng đến trang đăng nhập Keycloak trong trình duyệt mặc định của bạn

## Kiểm Thử Authorization Code Flow

### Bước 1: Chuẩn Bị Môi Trường

**Quan trọng**: Đóng tất cả các cửa sổ trình duyệt trước khi tiếp tục. Điều này đảm bảo bạn không vô tình sử dụng thông tin đăng nhập admin đã được cache thay vì thông tin người dùng cuối.

### Bước 2: Lấy Access Token

1. Nhấn nút **"Get New Access Token"**
2. Postman sẽ mở trình duyệt mặc định của bạn
3. Nhập thông tin đăng nhập người dùng cuối vào trang đăng nhập Keycloak
   - Tên đăng nhập: `madan` (ví dụ)
   - Mật khẩu: `12345` (ví dụ)
4. Nhấn **"Sign In"**

### Diễn Ra Phía Sau

Khi bạn đăng nhập:
1. Postman nhận authorization code từ Keycloak
2. Postman tự động đổi authorization code để lấy access token
3. Access token được hiển thị trong Postman

### Bước 3: Sử Dụng Access Token

1. Chọn tùy chọn **"Use Token"**
2. Nhấn **"Send"** để thực hiện API request

## Khắc Phục Lỗi: 403 Forbidden

Nếu bạn nhận được lỗi `403 Forbidden`, có nghĩa là người dùng thiếu role bắt buộc.

### Gán Role Cho Người Dùng

1. **Đóng phiên trình duyệt của người dùng cuối**
2. **Đăng nhập vào Keycloak Admin Console**
   - URL: URL admin Keycloak
   - Tên đăng nhập: `admin`
   - Mật khẩu: `admin`

3. **Điều hướng đến Users**
   - Vào mục **Users**
   - Chọn người dùng (ví dụ: `madan`)

4. **Gán Roles**
   - Nhấn vào tab **"Role Mapping"**
   - Nhấn **"Assign Role"**
   - Chọn các role cần thiết:
     - `accounts`
     - `cards`
     - `loans`
   - Nhấn **"Assign"**

### Lưu Ý Quan Trọng

- Đối với **người dùng cuối**: Sử dụng tab **Role Mapping**
- Đối với **ứng dụng** (Client Credentials flow): Sử dụng tab **Service Roles**

## Kiểm Thử Tất Cả Microservices

### Kiểm Thử Accounts API

1. Đóng phiên trình duyệt admin
2. Nhấn **"Get New Access Token"**
3. Nhập thông tin đăng nhập người dùng cuối (`madan` / `12345`)
4. Nhấn **"Use Token"**
5. Nhấn **"Send"**
6. ✅ Sẽ nhận được phản hồi thành công

### Kiểm Thử Cards API

1. Điều hướng đến Cards API request (tiền tố: `auth code`)
2. Xác minh các cài đặt authorization đã được cấu hình
3. Nhấn **"Get New Access Token"**
4. Nhập thông tin đăng nhập và sign in
5. Nhấn **"Use Token"**
6. Nhấn **"Send"**
7. ✅ Sẽ nhận được phản hồi thành công

### Kiểm Thử Loans API

1. Điều hướng đến Loans API request (tiền tố: `auth code`)
2. Nhấn **"Get New Access Token"**
3. Nhập thông tin đăng nhập và sign in
4. Nhấn **"Use Token"**
5. Nhấn **"Send"**
6. ✅ Sẽ nhận được phản hồi thành công

## Kiểm Thử Các Endpoint Công Khai

### Lấy Thông Tin Customer (Không Cần Xác Thực)

Một số endpoint có thể được cấu hình là công khai (permitAll):

1. Điều hướng đến request **"Accounts Get Permit All"**
2. Thực hiện GET request đến `fetchCustomerDetails` với tham số số điện thoại
3. Không cần xác thực
4. ✅ Sẽ nhận được phản hồi với dữ liệu accounts, loans và cards

## Những Điểm Chính Cần Nhớ

### Gateway Server Như Resource Server

Gateway Server hoạt động như một **Resource Server** trong kiến trúc OAuth2. Điều này có nghĩa:

- ✅ Không cần thay đổi cấu hình Gateway Server cho các loại grant type khác nhau
- ✅ Hoạt động với cả **Client Credentials** flow và **Authorization Code** flow
- ✅ Một cấu hình duy nhất xử lý nhiều tình huống xác thực

### Các Loại Grant Type Flow Phổ Biến Nhất

Hai loại grant type flow được sử dụng phổ biến nhất trong bảo mật microservices là:

1. **Client Credentials Grant Type** - Cho giao tiếp máy-với-máy
2. **Authorization Code Grant Type** - Cho các ứng dụng hướng người dùng

## Các Bước Tiếp Theo

### Chuẩn Bị Cho Docker Deployment

1. **Dừng tất cả các ứng dụng đang chạy**
2. **Cập nhật file pom.xml** trong tất cả microservices:
   - Thay đổi tag từ `S11` sang `S12`
   - Phản ánh phần hiện tại (Section 12)

3. **Tạo Docker images** cho tất cả microservices
4. **Cập nhật Docker Compose file** với cấu hình mới

### Quy Trình Build Docker

```bash
# Build Docker images cho mỗi microservice
mvn clean package -DskipTests
docker build -t microservice-name:S12 .
```

## Tóm Tắt

Hướng dẫn này đã bao gồm:
- ✅ Cấu hình Postman cho OAuth2 Authorization Code flow
- ✅ Kiểm thử các endpoint được bảo mật với xác thực phù hợp
- ✅ Gán roles cho người dùng trong Keycloak
- ✅ Hiểu Gateway Server như Resource Server
- ✅ Kiểm thử nhiều microservices với bảo mật OAuth2
- ✅ Xử lý cả các endpoint được xác thực và công khai

## Best Practices (Thực Hành Tốt Nhất)

1. **Luôn đóng các phiên trình duyệt** khi chuyển đổi giữa kiểm thử admin và người dùng cuối
2. **Sử dụng tên token mô tả rõ ràng** trong Postman để dễ dàng nhận diện
3. **Cấu hình roles đúng cách** trong Keycloak trước khi kiểm thử
4. **Kiểm thử tất cả endpoints** để đảm bảo bảo mật hoàn chỉnh
5. **Tài liệu hóa cấu hình OAuth2** của bạn để nhóm tham khảo

## Thuật Ngữ Kỹ Thuật

- **OAuth2**: Giao thức ủy quyền tiêu chuẩn
- **Authorization Code**: Mã ủy quyền tạm thời dùng để đổi lấy access token
- **Access Token**: Token truy cập để gọi các API được bảo mật
- **Grant Type**: Loại luồng ủy quyền
- **Resource Server**: Server chứa các tài nguyên được bảo vệ
- **Gateway Server**: Server cổng điều hướng requests
- **Keycloak**: Máy chủ xác thực và ủy quyền
- **CSRF (Cross-Site Request Forgery)**: Tấn công giả mạo yêu cầu từ trang web khác

---

*Tài liệu này là một phần của việc triển khai bảo mật microservices sử dụng Spring Boot, OAuth2, và Keycloak.*