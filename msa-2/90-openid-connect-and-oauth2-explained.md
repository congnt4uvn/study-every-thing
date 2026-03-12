# Hiểu về OpenID Connect và OAuth2

## Tổng quan

Tài liệu này giải thích mối quan hệ giữa OpenID Connect (OIDC) và OAuth2 framework, làm rõ những hiểu lầm phổ biến và trình bày cách hai công nghệ này hoạt động cùng nhau để cung cấp giải pháp quản lý định danh và truy cập toàn diện trong kiến trúc microservices.

## Những hiểu lầm phổ biến

Nhiều developers thường hiểu sai rằng:
- OpenID Connect là sự thay thế cho OAuth2
- OpenID Connect tốt hơn OAuth2
- Bạn nên dùng OIDC thay vì OAuth2

**Sự thật là**: OpenID Connect được xây dựng **trên nền tảng** OAuth2, không phải để thay thế. Bạn không thể có OpenID Connect mà không có OAuth2.

## OAuth2 Framework

### Mục đích
OAuth2 được xây dựng chủ yếu để hỗ trợ **ủy quyền (authorization)**, không phải xác thực (authentication).

### Các khái niệm chính

**Authentication vs Authorization:**
- **Authentication (Xác thực)**: Xác nhận người dùng hợp lệ bằng cách kiểm tra thông tin đăng nhập
- **Authorization (Ủy quyền)**: Thực thi các quyền và kiểm soát truy cập dựa trên vai trò sau khi xác thực

OAuth2 cho phép ứng dụng:
- Cung cấp quyền truy cập tạm thời cho ứng dụng bên thứ ba
- Cấp quyền truy cập hạn chế vào tài nguyên được bảo vệ
- Kiểm soát quyền truy cập thông qua scopes

### OAuth2 trong thực tế: Ví dụ Stack Overflow

Xem xét kịch bản xác thực Stack Overflow sử dụng GitHub:

1. Người dùng không có tài khoản Stack Overflow
2. Stack Overflow xác thực người dùng thông qua thông tin đăng nhập GitHub
3. GitHub cấp access token với giả định Stack Overflow chỉ cần thông tin email
4. Đằng sau hậu trường, Stack Overflow sử dụng access token này cho xác thực
5. Stack Overflow tạo tài khoản sử dụng địa chỉ email từ GitHub

Kịch bản này tiết lộ một "lỗ hổng" - các tổ chức tìm cách sử dụng OAuth2 cho cả xác thực và ủy quyền, mặc dù nó chỉ được thiết kế cho ủy quyền.

## Sự cần thiết của OpenID Connect

### Tại sao OIDC được tạo ra?

Vì các tổ chức đang sử dụng OAuth2 cho cả xác thực và ủy quyền mà không có phương pháp chuẩn, nhiều vấn đề nổi lên:

- Access tokens không cung cấp thông tin cụ thể về người dùng cuối
- Không có cách chuẩn để chia sẻ thông tin người dùng
- Các tổ chức sử dụng các phương pháp khác nhau (nhúng email, số điện thoại trong access tokens, v.v.)
- Thiếu tiêu chuẩn toàn ngành để chia sẻ thông tin định danh

### OpenID Connect là gì?

OpenID Connect là một **giao thức được xây dựng trên OAuth2** có các đặc điểm:

- Cung cấp khả năng xác thực
- Giới thiệu **ID Token** mới chứa thông tin người dùng
- Thiết lập tiêu chuẩn ngành để chia sẻ chi tiết định danh

## Kiến trúc công nghệ

```
┌─────────────────────────────────┐
│   OpenID Connect (OIDC)         │  ← Xác thực
│   (Lớp định danh)               │
├─────────────────────────────────┤
│   OAuth2 Framework              │  ← Ủy quyền
│   (Lớp ủy quyền)                │
├─────────────────────────────────┤
│   HTTP Protocol                 │  ← Giao thức cơ sở
└─────────────────────────────────┘
```

## So sánh OAuth2 và OpenID Connect

| Khía cạnh | OAuth2 | OpenID Connect |
|-----------|--------|----------------|
| **Mục đích chính** | Ủy quyền | Xác thực |
| **Loại Token** | Access Token | Access Token + ID Token |
| **Tập trung vào** | Quản lý truy cập | Quản lý định danh |
| **Ví dụ Scope** | read, write, admin | openid, profile, email, address |

### Khái niệm biểu đồ Venn

```
┌──────────────┐         ┌──────────────┐
│   OpenID     │         │   OAuth2     │
│   Connect    │         │              │
│              │         │              │
│   Xác thực   │◄──────►│  Ủy quyền    │
│              │   IAM   │              │
│  Quản lý     │         │  Quản lý     │
│  Định danh   │         │  Truy cập    │
└──────────────┘         └──────────────┘
```

Khi kết hợp, chúng tạo ra **IAM (Identity and Access Management - Quản lý Định danh và Truy cập)**.

## Cách OpenID Connect hoạt động

### OpenID Scope

Để kích hoạt OpenID Connect:
1. Gửi tham số scope với giá trị `openid`
2. Authorization server phát hiện scope này
3. Server cấp **hai tokens**:
   - **Access Token**: Để truy cập tài nguyên được bảo vệ
   - **ID Token**: Chứa thông tin định danh người dùng

Không có scope `openid`, bạn chỉ nhận được access token (luồng OAuth2 chuẩn).

## Ba lợi ích chính của OIDC

### 1. Scopes chuẩn hóa

Cách chuẩn để yêu cầu thông tin người dùng thông qua scopes:

- **`openid`**: Xác thực cơ bản
- **`profile`**: Thông tin hồ sơ người dùng
- **`email`**: Chi tiết địa chỉ email
- **`address`**: Thông tin địa chỉ

### 2. Tokens theo chuẩn JWT

Cả Access Token và ID Token đều tuân theo chuẩn **JWT (JSON Web Token)**, đảm bảo:
- Định dạng token nhất quán
- Thông tin người dùng tự chứa
- Xác minh chữ ký mật mã
- Khả năng tương tác giữa các hệ thống

### 3. Endpoint /userinfo chuẩn hóa

OpenID Connect cung cấp endpoint chuẩn: `/userinfo`

Ứng dụng client có thể gọi endpoint này bất cứ lúc nào để lấy:
- Chi tiết về người dùng đã đăng nhập
- Thông tin resource owner
- Dữ liệu hồ sơ

## Triển khai trong Microservices

Khi triển khai OAuth2 và OpenID Connect trong microservices:

1. **Cấu hình Authorization Server**: Thiết lập để hỗ trợ cả OAuth2 và OIDC
2. **Yêu cầu Tokens**: Bao gồm scope `openid` trong các yêu cầu ủy quyền
3. **Nhận Tokens**: Nhận cả access token và ID token
4. **Sử dụng ID Token**: Trích xuất thông tin định danh người dùng
5. **Sử dụng Access Token**: Truy cập tài nguyên microservice được bảo vệ
6. **Gọi /userinfo**: Lấy thông tin người dùng bổ sung khi cần

## Best Practices (Thực hành tốt nhất)

1. **Sử dụng cả hai cùng nhau**: Kết hợp OAuth2 và OIDC cho khả năng IAM hoàn chỉnh
2. **Yêu cầu Scopes phù hợp**: Chỉ yêu cầu các scopes bạn cần
3. **Xác thực Tokens**: Luôn xác thực chữ ký JWT
4. **Lưu trữ Token an toàn**: Lưu trữ tokens một cách an toàn ở phía client
5. **Token hết hạn**: Xử lý làm mới token một cách phù hợp

## Những điểm chính cần nhớ

✅ **NÊN:**
- Hiểu rằng OIDC được xây dựng trên OAuth2
- Sử dụng OIDC + OAuth2 cùng nhau cho quản lý định danh và truy cập
- Sử dụng scopes chuẩn hóa để yêu cầu thông tin người dùng

❌ **KHÔNG NÊN:**
- Nói OIDC là sự thay thế cho OAuth2
- Tuyên bố OIDC tốt hơn OAuth2
- Sử dụng OIDC mà không hiểu OAuth2

## Kết luận

OpenID Connect và OAuth2 là các công nghệ bổ sung cho nhau:

- **OAuth2** cung cấp nền tảng cho ủy quyền và kiểm soát truy cập
- **OpenID Connect** thêm xác thực và quản lý định danh lên trên
- Cùng nhau, chúng cung cấp khả năng **IAM (Identity and Access Management)** toàn diện

Bằng cách kết hợp các tiêu chuẩn này, ứng dụng client có thể:
- Xác thực người dùng một cách an toàn
- Kiểm soát quyền truy cập vào tài nguyên
- Quản lý thông tin định danh người dùng
- Tuân theo các giao thức tiêu chuẩn ngành

Hiểu cả hai công nghệ và mối quan hệ của chúng là rất quan trọng để xây dựng kiến trúc microservices hiện đại, an toàn với Spring Boot và các frameworks khác.

---

**Các chủ đề liên quan:**
- JWT (JSON Web Tokens)
- Spring Security OAuth2
- Bảo mật Microservices
- Xác thực API Gateway
- Xác thực Service-to-Service