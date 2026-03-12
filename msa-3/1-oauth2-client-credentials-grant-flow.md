# Luồng Xác Thực OAuth2 Client Credentials Grant Type

## Tổng Quan

Tài liệu này giải thích về Luồng OAuth2 Client Credentials Grant Type, một cơ chế xác thực quan trọng cho kiến trúc microservices. Luồng này được thiết kế đặc biệt cho giao tiếp giữa các máy chủ với nhau mà không có sự tham gia của người dùng cuối.

## Khi Nào Sử Dụng Client Credentials Grant Flow

Sử dụng loại grant flow này trong các trường hợp sau:
- Khi hai backend API cần giao tiếp với nhau
- Khi hai máy chủ backend khác nhau đang cố gắng giao tiếp
- Khi hai ứng dụng cần tương tác mà không có sự tham gia của người dùng cuối
- **Quan trọng**: KHÔNG có ứng dụng UI hoặc người dùng cuối tham gia trong luồng này

## Các Thành Phần Chính (Actors)

### 1. Máy Chủ Ủy Quyền (Auth Server)
- Chịu trách nhiệm xác thực ứng dụng client
- Cấp phát access token sau khi xác thực thành công
- Trong mạng lưới microservices của chúng ta, chúng ta sử dụng **Keycloak** để thiết lập auth server

### 2. Resource Server (Máy Chủ Tài Nguyên)
- Máy chủ lưu trữ các tài nguyên được bảo vệ
- Trong triển khai của chúng ta, **Gateway Server** đóng vai trò là resource server
- Hoạt động như edge server cho mạng lưới microservices
- Xác thực access token trước khi phản hồi các yêu cầu
- Chỉ phản hồi các yêu cầu có access token hợp lệ được cấp bởi auth server

### 3. Ứng Dụng Client
- Ứng dụng yêu cầu truy cập vào các tài nguyên được bảo vệ
- Có thể là ứng dụng backend khác, API, hoặc microservice bên ngoài
- Phải xác thực với auth server để có được access token
- Không có người dùng cuối tham gia trong trường hợp này

## Sơ Đồ Luồng

```
Bước 1: Client → Auth Server
        Yêu cầu: Access Token
        Thông tin xác thực: Client ID + Client Secret
        Lưu ý: Không có người dùng cuối tham gia

Bước 2: Auth Server → Client
        Phản hồi: Access Token (sau khi xác thực)

Bước 3: Client → Resource Server
        Yêu cầu: Tài nguyên được bảo vệ
        Header: Access Token

Bước 4: Resource Server → Auth Server
        Xác thực: Kiểm tra Access Token (ở phía sau)

Bước 5: Resource Server → Client
        Phản hồi: Tài nguyên được bảo vệ (nếu được ủy quyền)
```

## Chi Tiết Các Bước Trong Luồng

### Bước 1: Client Yêu Cầu Access Token
Ứng dụng client yêu cầu access token từ auth server với các thông tin sau:
- **Client ID**: Định danh duy nhất cho ứng dụng client
- **Client Secret**: Thông tin xác thực bí mật
- **Scope**: Các quyền/authorities cụ thể được yêu cầu (ví dụ: "email")
- **Grant Type**: Đặt thành "client_credentials"

**Lưu Ý Quan Trọng:**
- Thông tin xác thực client được lấy trong quá trình đăng ký với auth server
- Các scope phải khớp với những gì đã được cấu hình trong auth server cho client đó
- Client không thể yêu cầu các scope tùy ý; chúng phải được cấu hình trước bởi admin của auth server

### Bước 2: Auth Server Cấp Phát Access Token
- Auth server xác thực thông tin xác thực client được cung cấp
- Nếu hợp lệ, nó cấp phát access token cho ứng dụng client
- Vì không có người dùng cuối, auth server không yêu cầu thông tin xác thực của người dùng cuối
- Điều này làm cho nó trở thành **loại grant flow đơn giản nhất trong OAuth2**

### Bước 3: Client Gửi Yêu Cầu Đến Resource Server
Ứng dụng client gửi yêu cầu đến resource server bao gồm:
- Access token (thường ở trong Authorization header)
- Tài nguyên cụ thể mà nó muốn truy cập

### Bước 4: Resource Server Xác Thực Token
- Resource server nhận access token
- Ở phía sau, nó xác thực token với auth server
- Nó kiểm tra xem client có đủ đặc quyền cho tài nguyên được yêu cầu hay không

### Bước 5: Resource Server Phản Hồi
Nếu xác thực thành công và client có đặc quyền phù hợp:
- Resource server xử lý yêu cầu
- Trong trường hợp của chúng ta, gateway server có thể gọi các microservices khác (ví dụ: Accounts Microservice)
- Phản hồi được gửi lại cho ứng dụng client

## Ví Dụ Kịch Bản: Easy Bank Microservices

Trong kiến trúc microservices của Easy Bank:

1. **Gateway Server** = Resource Server
2. **Keycloak** = Auth Server
3. **Dịch vụ/API bên ngoài** = Ứng dụng Client

**Ví dụ Luồng:**
- Một dịch vụ bên ngoài muốn tạo tài khoản
- Nó xác thực với Keycloak và nhận access token
- Nó gửi yêu cầu đến Gateway Server với access token
- Gateway xác thực token và kiểm tra đặc quyền
- Nếu được ủy quyền, Gateway gọi Accounts Microservice
- Gateway chuyển tiếp phản hồi lại cho dịch vụ bên ngoài

## Các Tham Số Yêu Cầu Chính

Khi yêu cầu access token từ auth server:

| Tham số | Mô tả | Ví dụ |
|---------|-------|-------|
| client_id | Định danh duy nhất cho client | "external-app-001" |
| client_secret | Thông tin xác thực bí mật | "secret123xyz" |
| grant_type | Phải là "client_credentials" | "client_credentials" |
| scope | Các quyền/authorities được yêu cầu | "email", "profile" |

## Quản Lý Scope

- Các scope tương tự như authorities trong Spring Security
- Chúng xác định những gì ứng dụng client có thể truy cập
- Các scope phải được cấu hình trước trong auth server bởi quản trị viên
- Client chỉ có thể yêu cầu các scope đã được gán cho client ID của nó
- Yêu cầu các scope không được ủy quyền sẽ dẫn đến lỗi

## Đặc Điểm Quan Trọng

✅ **Grant flow OAuth2 đơn giản nhất**
- Không yêu cầu tương tác của người dùng cuối
- Không có resource owner tham gia
- Quá trình xác thực đơn giản

✅ **Giao Tiếp Server-to-Server**
- Được thiết kế đặc biệt cho giao tiếp backend-to-backend
- Không có sự tham gia của ứng dụng UI

✅ **Lợi Ích Bảo Mật**
- Xác thực tập trung thông qua auth server
- Kiểm soát truy cập dựa trên token
- Ủy quyền dựa trên scope

❌ **Khi KHÔNG Nên Sử Dụng**
- KHÔNG sử dụng khi có người dùng cuối tham gia
- KHÔNG sử dụng cho các ứng dụng UI
- KHÔNG sử dụng khi người dùng cần cấp sự đồng ý

## Triển Khai Trong Spring Boot Microservices

Để triển khai luồng này trong microservices của bạn:

1. Thiết lập Keycloak làm auth server của bạn
2. Cấu hình Gateway Server của bạn làm resource server
3. Đăng ký các ứng dụng client trong Keycloak với các scope phù hợp
4. Cấu hình Spring Security để xác thực token
5. Triển khai xử lý ngoại lệ và phản hồi lỗi phù hợp

## Kết Luận

Client Credentials Grant Type Flow là cơ chế xác thực hoàn hảo cho giao tiếp server-to-server trong kiến trúc microservices. Nó cung cấp một cách an toàn, chuẩn hóa để các dịch vụ backend xác thực và truy cập các tài nguyên được bảo vệ mà không cần sự tham gia của người dùng cuối.

---

**Các Bước Tiếp Theo**: Trong các bài giảng sắp tới, chúng ta sẽ khám phá các luồng OAuth2 grant phức tạp hơn và triển khai luồng này trong mạng lưới microservices Easy Bank của chúng ta với demo thực tế.