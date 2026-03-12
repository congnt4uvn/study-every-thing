# Lấy Access Token từ Keycloak Auth Server

## Tổng quan

Hướng dẫn này trình bày cách một ứng dụng client kết nối với máy chủ xác thực Keycloak để lấy access token bằng cách sử dụng OAuth2 Client Credentials Grant Flow.

## Yêu cầu trước

- Keycloak server đang chạy (ví dụ: localhost:7080)
- Ứng dụng client đã được đăng ký trong Keycloak
- Postman hoặc công cụ kiểm thử API tương tự

## Tìm Token Endpoint

### Bước 1: Truy cập Realm Settings

1. Đăng nhập vào Keycloak admin console
   - Thông tin đăng nhập mặc định: `admin` / `admin`
2. Điều hướng đến **Realm Settings**
3. Cuộn xuống phần **Endpoints**
4. Nhấp vào **OpenID Endpoint Configuration**

Điều này sẽ hiển thị tất cả các URL endpoint được máy chủ xác thực hỗ trợ.

### Bước 2: Xác định Token Endpoint

Tìm **token_endpoint** trong cấu hình. Định dạng URL endpoint là:

```
http://localhost:7080/realms/master/protocol/openid-connect/token
```

## Yêu cầu Access Token bằng Postman

### Cấu hình Request

1. **Phương thức**: POST
2. **URL**: `http://localhost:7080/realms/master/protocol/openid-connect/token`
3. **Loại Body**: `x-www-form-urlencoded`

### Tham số Request

Các tham số sau phải được bao gồm trong request body:

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| `grant_type` | `client_credentials` | Loại luồng OAuth2 grant type đang sử dụng |
| `client_id` | Username client của bạn | Định danh client đã tạo ở bài trước |
| `client_secret` | Secret key của client | Khóa bí mật cho ứng dụng client |
| `scope` | `openid email profile` | Các scope được yêu cầu cho access token |

### Ví dụ Request Body

```
grant_type=client_credentials
client_id=your-client-id
client_secret=your-client-secret
scope=openid email profile
```

## Hiểu về Client Scopes trong Keycloak

### Default Scopes

Keycloak tự động gán các scope mặc định cho clients:
- `address`
- `email`
- `phone`
- `profile`
- `roles`

Các scope mặc định này không cần phải tạo hoặc gán thủ công.

### OpenID Scope

Scope `openid` được tự động cung cấp cho tất cả các client sử dụng OpenID Connect. Bạn không cần gán nó một cách rõ ràng, nhưng nên bao gồm nó trong yêu cầu token.

### Custom Scopes

Nếu bạn cần các scope tùy chỉnh cụ thể cho client của mình:
1. Điều hướng đến **Client Scopes** trong Keycloak admin console
2. Tạo client scope mới
3. Gán nó cho client của bạn

## Phản hồi Token

### Phản hồi thành công

Khi bạn gửi request, bạn sẽ nhận được phản hồi chứa:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 60,
  "token_type": "Bearer",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

- **access_token**: JWT token để truy cập các tài nguyên được bảo vệ
- **expires_in**: Thời gian hết hạn token (mặc định: 60 giây)
- **token_type**: Luôn là "Bearer" đối với OAuth2
- **id_token**: Token bổ sung chứa thông tin về user/client

### Thời gian hết hạn Token

Mặc định, access token hết hạn sau 60 giây. Điều này có thể được cấu hình trong Keycloak admin console nếu cần.

## Tác động của Scope đến Tokens

### Với OpenID Scope

Khi bao gồm `openid` trong tham số scope, bạn nhận được:
- Access Token
- ID Token

### Không có OpenID Scope

Khi bỏ qua `openid` (chỉ sử dụng `email profile`), bạn nhận được:
- Chỉ Access Token
- Không có ID Token

**Khuyến nghị**: Luôn bao gồm scope `openid` để nhận thông tin toàn diện về client hoặc end user của bạn.

## Hiểu về JWT Tokens

### JWT là gì?

JWT (JSON Web Token) là định dạng token nhỏ gọn, an toàn cho URL, được sử dụng để truyền thông tin một cách bảo mật giữa các bên.

### Giải mã JWT Tokens

Để hiểu nội dung của JWT token:

1. Truy cập [jwt.io](https://jwt.io)
2. Dán JWT token đã mã hóa của bạn
3. Xem thông tin đã được giải mã

### Cấu trúc Access Token

#### Header
- `alg`: Thuật toán được sử dụng để tạo token
- `typ`: Loại token (JWT)
- `kid`: Key ID

#### Payload
- `exp`: Timestamp hết hạn
- `iat`: Timestamp phát hành
- `iss`: Nhà phát hành
- `client_id`: Định danh client
- `scope`: Các scope được cấp
- `roles`: Các vai trò của client
- `email_verified`: Trạng thái xác minh email
- `preferred_username`: Tên người dùng ưa thích
- `client_host`: Thông tin host của client

### Nội dung ID Token

ID token chứa thông tin tương tự:
- `client_id`
- `client_host`
- `preferred_username`

Hầu hết các chi tiết trùng lặp với access token, nhưng ID token có thể được nâng cao với các chi tiết bổ sung về ứng dụng client nếu cần.

## Triển khai thực tế

### Sử dụng Postman để kiểm thử

Trong demo này, Postman mô phỏng ứng dụng client gọi đến máy chủ xác thực.

### Triển khai Production

Trong các dự án thực tế, ứng dụng client sẽ:
1. Gọi token endpoint theo cách lập trình từ mã Java/Spring Boot
2. Phân tích phản hồi token
3. Trích xuất access token
4. Sử dụng access token để gọi các resource server

### Ví dụ về luồng

```
Ứng dụng Client → Auth Server (Token Request)
                 ← Access Token Response
Ứng dụng Client → Resource Server (với Access Token)
                 ← Protected Resource
```

## Tóm tắt

- Ứng dụng client phải biết URL của token endpoint
- Client Credentials Grant Flow yêu cầu: grant_type, client_id, client_secret và scope
- Access token ở định dạng JWT và mặc định hết hạn sau 60 giây
- Bao gồm scope `openid` cung cấp cả access token và ID token
- Trong production, ứng dụng client gọi các endpoint này theo cách lập trình từ mã backend
- Access token được sử dụng để xác thực các request đến resource server

## Tài nguyên bổ sung

Để biết thêm thông tin chi tiết về JWT tokens và Spring Security, hãy xem xét đăng ký khóa học Spring Security toàn diện.

---

**Bước tiếp theo**: Tìm hiểu cách sử dụng access token đã lấy được để bảo mật microservices và gọi các resource server được bảo vệ.