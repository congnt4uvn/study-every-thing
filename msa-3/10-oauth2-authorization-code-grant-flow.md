# Luồng OAuth2 Authorization Code Grant

## Tổng Quan

Trong kiến trúc microservices, khi làm việc với ứng dụng UI hoặc ứng dụng di động có sự tham gia của người dùng cuối, chúng ta nên sử dụng **Luồng Authorization Code Grant Type** thay vì Client Credentials Grant Type Flow.

## Khi Nào Sử Dụng Authorization Code Grant Flow

- **Ứng Dụng UI**: Ứng dụng web có giao diện người dùng
- **Ứng Dụng Di Động**: Ứng dụng iOS, Android hoặc mobile khác
- **Kịch Bản Có Người Dùng**: Bất kỳ tình huống nào có người dùng cuối tương tác với ứng dụng client

Điều này khác với Client Credentials Grant Type Flow, được sử dụng cho giao tiếp backend-to-backend không có sự tham gia của người dùng cuối.

## Bốn Vai Trò Trong OAuth2

1. **User (Người dùng)**: Người dùng cuối sở hữu tài nguyên
2. **Client (Ứng dụng)**: Ứng dụng khách (ví dụ: Stack Overflow)
3. **Authorization Server (Máy chủ xác thực)**: Phát hành token và xác thực thông tin đăng nhập
4. **Resource Server (Máy chủ tài nguyên)**: Lưu trữ các tài nguyên được bảo vệ (ví dụ: GitHub)

### Ví Dụ Thực Tế
Stack Overflow sử dụng luồng grant type này để truy cập thông tin GitHub của bạn. Bạn (người dùng) xác thực với GitHub (auth server), và Stack Overflow (client) sau đó có thể truy cập thông tin của bạn từ máy chủ GitHub (resource server).

## Các Bước Trong Authorization Code Grant Flow

### Bước 1: Người Dùng Yêu Cầu Truy Cập
Người dùng cuối điều hướng đến ứng dụng client qua trình duyệt hoặc ứng dụng di động và yêu cầu truy cập tài nguyên của họ được lưu trữ trên resource server.

### Bước 2: Chuyển Hướng Đến Authorization Server
Ứng dụng client chuyển hướng người dùng đến trang đăng nhập của auth server.

**Tham Số Yêu Cầu:**
- `client_id`: Định danh ứng dụng client
- `redirect_uri`: URL nơi người dùng sẽ được chuyển hướng sau khi xác thực
- `scope`: Quyền được yêu cầu (ví dụ: đọc ảnh, truy cập hồ sơ)
- `state`: Token được tạo ngẫu nhiên để ngăn chặn tấn công CSRF
- `response_type=code`: Chỉ ra rằng authorization code grant flow đang được sử dụng

### Bước 3: Xác Thực Người Dùng
Người dùng nhập thông tin đăng nhập trực tiếp trên trang đăng nhập của auth server, chứng minh danh tính của họ và cung cấp sự đồng ý cho ứng dụng client truy cập tài nguyên của họ.

**Quan Trọng**: Người dùng không bao giờ chia sẻ thông tin đăng nhập trực tiếp với ứng dụng client.

### Bước 4: Phát Hành Authorization Code
Sau khi auth server xác thực thông tin đăng nhập của người dùng, nó phát hành một **authorization code tạm thời** (không phải access token) và chuyển hướng về ứng dụng client.

Phản hồi bao gồm:
- `code`: Authorization code
- `state`: Giá trị state giống như đã gửi ở Bước 2 (phải khớp để ngăn chặn tấn công CSRF)

### Bước 5: Đổi Code Lấy Access Token
Ứng dụng client thực hiện yêu cầu backend đến auth server với:
- `grant_type=authorization_code`
- `code`: Authorization code từ Bước 4
- `client_id`: Định danh ứng dụng client
- `client_secret`: Mật khẩu ứng dụng client
- `redirect_uri`: Redirect URI đã sử dụng ở Bước 2

### Bước 6: Phát Hành Access Token
Nếu authorization code và thông tin đăng nhập client hợp lệ, auth server sẽ phát hành một **access token**.

### Bước 7: Truy Cập Tài Nguyên Được Bảo Vệ
Ứng dụng client gửi yêu cầu đến resource server kèm theo access token. Resource server xác thực token với auth server và trả về tài nguyên được yêu cầu nếu hợp lệ.

## Tại Sao Cần Hai Yêu Cầu?

Bạn có thể thắc mắc tại sao authorization code grant flow yêu cầu hai yêu cầu thay vì phát hành access token ngay sau khi xác thực người dùng.

### Lý Do Bảo Mật

1. **Có Sự Tham Gia Của Trình Duyệt**: Do trình duyệt và ứng dụng di động có liên quan, có nguy cơ cao bị đánh cắp token
2. **Bảo Mật Hai Lớp**: 
   - Lớp đầu tiên: Xác thực người dùng
   - Lớp thứ hai: Xác thực ứng dụng client
3. **Ngăn Chặn Lộ Token**: Access token không bao giờ bị lộ trên thanh địa chỉ của trình duyệt

Điều này làm cho giao tiếp giữa auth server và ứng dụng client an toàn hơn.

## Đã Lỗi Thời: Implicit Grant Flow

Trước đây, có một **Implicit Grant Type Flow** phát hành access token trong một bước duy nhất mà không cần authorization code trung gian. Tuy nhiên, luồng này đã bị **loại bỏ** do các vấn đề bảo mật.

**Khuyến Nghị Hiện Tại**: Luôn sử dụng Authorization Code Grant Type Flow cho các tình huống có người dùng tham gia.

## Demo Thực Hành: OAuth2 Playground

Bạn có thể kiểm tra Authorization Code Grant Flow bằng cách sử dụng trang web OAuth2 Playground:

### Các Bước Demo:

1. **Đăng Ký Ứng Dụng Client**
   - Nhấp "Register a client application"
   - Ghi chú `client_id` và `client_secret` được tạo
   - Ghi chú thông tin đăng nhập người dùng thử nghiệm được tạo

2. **Xây Dựng Authorization URL**
   - Đặt `response_type=code`
   - Bao gồm `client_id`
   - Chỉ định `redirect_uri`
   - Yêu cầu scopes (ví dụ: photo, offline_access)
   - Ghi chú giá trị `state` được tạo ngẫu nhiên

3. **Authorize (Ủy Quyền)**
   - Nhấp "Authorize" để chuyển hướng đến trang đăng nhập
   - Nhập thông tin đăng nhập người dùng thử nghiệm
   - Cung cấp sự đồng ý cho ứng dụng

4. **Xác Minh State và Code**
   - Xác minh giá trị `state` khớp với giá trị ban đầu
   - Ghi chú `authorization code` đã nhận

5. **Đổi Lấy Token**
   - Yêu cầu POST với:
     - `grant_type=authorization_code`
     - `client_id` và `client_secret`
     - `redirect_uri`
     - `code` (authorization code)
   - Nhận access token trong phản hồi

## Những Điểm Cần Nhớ

- Sử dụng Authorization Code Grant Flow cho các ứng dụng có người dùng cuối tham gia
- Luồng bao gồm hai bước xác thực để tăng cường bảo mật
- Người dùng không bao giờ chia sẻ thông tin đăng nhập với ứng dụng client
- Tham số `state` ngăn chặn tấn công CSRF
- Authorization code là tạm thời và phải được đổi lấy access token
- Implicit grant flow đã lỗi thời; sử dụng authorization code flow thay thế

## Thực Hành Tốt Nhất

1. Luôn xác thực tham số `state` để ngăn chặn tấn công CSRF
2. Sử dụng HTTPS cho tất cả giao tiếp
3. Lưu trữ client secrets một cách an toàn
4. Triển khai cơ chế làm mới token phù hợp
5. Đặt thời gian hết hạn token hợp lý
6. Chỉ yêu cầu các scope cần thiết

---

**Lưu ý**: Tài liệu này dựa trên việc triển khai OAuth2 framework trong kiến trúc microservices Spring Boot.