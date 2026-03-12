

FILE: 1-oauth2-client-credentials-grant-flow.md


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




FILE: 10-oauth2-authorization-code-grant-flow.md


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




FILE: 100-microservices-course-completion-congratulations.md


# Hoàn Thành Khóa Học Microservices - Xin Chúc Mừng!

## Thông Điệp Hoàn Thành Khóa Học

Hooray! Cuối cùng, bạn đã hoàn thành toàn bộ khóa học về microservices.

Xin chúc mừng lớn từ phía tôi.

## Những Gì Bạn Đã Đạt Được

Bạn giờ đây đã là bậc thầy về microservices. Bạn biết cách xây dựng microservices sử dụng **Spring**, **Spring Boot**, **Docker**, và **Kubernetes**.

Bạn cũng là một trong số ít các lập trình viên biết cách xây dựng microservices bằng cách tuân theo tất cả các best practices (thực hành tốt nhất).

### Các Kỹ Năng Chính Bạn Đã Thành Thạo

- **Xây dựng discovery server của riêng bạn** - Bạn hiểu về các mẫu service discovery và cách triển khai
- **Xây dựng edge server của riêng bạn** - Bạn có thể tạo API gateway và edge services
- **Bảo mật microservices của bạn** - Bạn biết cách triển khai bảo mật trong các hệ thống phân tán
- **Xây dựng event-driven microservices** - Bạn hiểu các mẫu giao tiếp bất đồng bộ

## Hành Trình Phía Trước Của Bạn

Có rất nhiều điều chúng ta đã thảo luận trong suốt khóa học này, và bạn đã là một người học rất tốt. Với sự kiên nhẫn tuyệt vời, bạn đã hoàn thành toàn bộ khóa học này.

Tôi thực sự muốn ghi nhận sự kiên nhẫn của bạn trong việc hoàn thành khóa học này.

Giờ đây, tôi rất tự tin rằng bạn có thể vượt qua bất kỳ cuộc phỏng vấn microservices nào và bạn đã sẵn sàng để đảm nhận vai trò lập trình viên microservices trong bất kỳ dự án hoặc tổ chức nào đang cố gắng xây dựng microservices.

### Các Bước Tiếp Theo

Hãy coi khóa học này như bước đệm ban đầu hướng tới hành trình microservices của bạn. Với kiến thức mà bạn đã có được trong khóa học này, hãy tiếp tục khám phá thế giới microservices.

Hãy chia sẻ kiến thức cho những người khác về microservices.

## Trước Khi Bạn Rời Đi - Những Yêu Cầu Đặc Biệt

Trước khi bạn kết thúc khóa học, tôi có một vài yêu cầu:

### 1. Chia Sẻ Phản Hồi Của Bạn

Yêu cầu đầu tiên là nếu bạn chưa cung cấp phản hồi có giá trị của mình cho khóa học, vui lòng dành một phút và cung cấp phản hồi có giá trị, chi tiết và mang tính xây dựng cho khóa học trên Udemy.

Đánh giá của bạn sẽ giúp khóa học tiếp cận được tất cả các sinh viên tiềm năng đang cố gắng học microservices.

### 2. Kết Nối Cá Nhân

Nếu bạn muốn gửi lời cảm ơn cá nhân hoặc muốn chia sẻ phản hồi cá nhân với tôi, vui lòng gửi tin nhắn cho tôi trên Udemy hoặc bạn có thể gửi tin nhắn cho tôi trên LinkedIn.

Bất kể kênh nào bạn cảm thấy thoải mái, vui lòng chia sẻ phản hồi có giá trị của bạn với tôi.

### 3. Khám Phá Thêm Các Khóa Học

Và yêu cầu tiếp theo là vui lòng truy cập trang web của tôi **easybytes.com**. Có rất nhiều khóa học khác từ tôi. Nếu bạn quan tâm đến bất kỳ khóa học nào, vui lòng đăng ký vào chúng.

## Lời Cuối Cùng

Với điều này, tôi kết thúc khóa học này với niềm tự hào nhỏ nhoi rằng tôi có thể giúp đỡ bạn trong hành trình microservices của bạn.

Tôi muốn gửi lời cảm ơn chân thành từ trái tim tôi vì đã cho tôi cơ hội này.

Tôi hy vọng con đường của chúng ta sẽ gặp lại nhau trong tương lai.

**Cảm ơn và chúc bạn tất cả những điều tốt đẹp nhất.**

**Tạm biệt.**

---

## Các Chủ Đề Khóa Học Đã Đề Cập

- Spring Framework & Spring Boot
- Kiến Trúc Microservices
- Docker Containerization (Đóng gói Container)
- Kubernetes Orchestration (Điều phối)
- Service Discovery (Khám phá dịch vụ)
- API Gateway/Edge Server
- Bảo Mật Microservices
- Kiến Trúc Hướng Sự Kiện (Event-Driven)
- Best Practices (Thực hành tốt nhất) cho Phát triển Microservices

---

*Khóa học này đã chuẩn bị cho bạn trở thành một lập trình viên microservices thành thạo. Hãy tiếp tục học hỏi và xây dựng những hệ thống phân tán tuyệt vời!*




FILE: 11-oauth2-authorization-code-grant-flow-implementation.md


# Triển khai OAuth2 Authorization Code Grant Flow trong Microservices

## Giới thiệu

Trong bài giảng này, chúng ta sẽ tìm hiểu cách hoạt động của **Authorization Code Grant Flow** trong kiến trúc microservices EasyBank. Loại grant này được sử dụng đặc biệt khi có sự tham gia của người dùng cuối trong quy trình xác thực.

## Tổng quan Kiến trúc

Authorization code grant flow bao gồm các thành phần chính sau:

- **Ứng dụng Client**: Ứng dụng web UI hoặc ứng dụng di động
- **Người dùng cuối**: Người sử dụng ứng dụng client
- **Gateway Server**: Đóng vai trò là resource server (edge server)
- **Auth Server**: Máy chủ ủy quyền Keycloak
- **Microservices**: Các dịch vụ backend riêng lẻ

## Mô tả Luồng xử lý

### Quy trình Tổng quan

1. **Yêu cầu ban đầu**: Người dùng cuối thực hiện một hành động trong ứng dụng client cần dữ liệu từ mạng microservices.

2. **Chuyển hướng đến trang đăng nhập**: Do Gateway server hoạt động như resource server, ứng dụng client chuyển hướng người dùng cuối đến trang đăng nhập của máy chủ xác thực Keycloak.

3. **Xác thực**: Người dùng cuối nhập thông tin xác thực của họ trên trang đăng nhập Keycloak.

4. **Authorization Code**: Sau khi xác thực thành công, Keycloak cấp một authorization code cho ứng dụng web.

5. **Yêu cầu Access Token**: Ở hậu trường, ứng dụng client thực hiện một yêu cầu khác để lấy access token bằng authorization code.

6. **Yêu cầu API**: Ứng dụng client chuyển tiếp yêu cầu đến Gateway server cùng với access token.

7. **Xác thực Token**: Gateway server xác thực access token bằng cách kết nối với Keycloak.

8. **Xử lý Yêu cầu**: Sau khi được xác thực, Gateway chuyển tiếp yêu cầu đến các microservices riêng lẻ.

9. **Luồng Phản hồi**: Microservices xử lý yêu cầu và gửi phản hồi trở lại qua Gateway đến ứng dụng client.

10. **Hiển thị**: Ứng dụng client hiển thị thông tin cho người dùng cuối.

## Luồng Chi tiết Từng Bước

### Bước 1: Yêu cầu Chưa được Ủy quyền
Ứng dụng client cố gắng gọi API trên Spring Cloud Gateway mà không có xác thực thay mặt cho người dùng cuối.

**Phản hồi từ Gateway**: "Tôi chỉ có thể xử lý các yêu cầu có access token. Vui lòng lấy token từ máy chủ xác thực."

### Bước 2: Yêu cầu Access Token
Ứng dụng client yêu cầu auth server cấp access token.

**Phản hồi từ Auth Server**: "Tôi không thể cấp access token như vậy được. Để nhận access token từ tôi, bạn (client) và đối tác của bạn (người dùng cuối) phải đăng ký với tôi và được admin phê duyệt."

### Bước 3: Đăng ký
Ứng dụng client và người dùng cuối đăng ký với Keycloak và nhận được các phê duyệt cần thiết, thiết lập thông tin xác thực của họ.

### Bước 4: Chuyển hướng Đăng nhập
Ứng dụng client chuyển tiếp người dùng cuối đến trang đăng nhập của Keycloak, chỉ gửi **client ID** (không gửi client secret).

### Bước 5: Xác thực Người dùng và Đồng ý
Người dùng cuối:
- Nhập thông tin xác thực của họ trên trang đăng nhập
- Cung cấp sự đồng ý cho ứng dụng client truy cập tài nguyên thay mặt họ

### Bước 6: Cấp Authorization Code
Sau khi xác thực tất cả các chi tiết, auth server gửi một **authorization code** cho ứng dụng client.

### Bước 7: Trao đổi Token
Ứng dụng client gọi auth server ở hậu trường với:
- Client ID
- Client secret
- Authorization code

### Bước 8: Nhận Access Token
Nếu tất cả các chi tiết đều chính xác, auth server cấp access token.

**Cảnh báo Quan trọng**: "Access token này thuộc về người dùng cuối, không phải ứng dụng client. Vui lòng không lạm dụng dữ liệu bạn lấy về liên quan đến người dùng cuối."

### Bước 9: Gọi API Được Bảo mật
Ứng dụng client gọi một API được bảo mật trên Spring Cloud Gateway, bao gồm access token nhận được ở Bước 8.

### Bước 10: Xác thực Token
Resource server (Gateway) xác thực access token bằng cách kết nối với máy chủ xác thực Keycloak.

### Bước 11: Chuyển tiếp Yêu cầu
Khi access token được xác nhận là hợp lệ, Spring Cloud Gateway chuyển tiếp yêu cầu đến các microservices riêng lẻ.

### Bước 12: Phản hồi từ Microservices
Các microservices riêng lẻ xử lý yêu cầu và phản hồi với kết quả thành công.

### Bước 13: Phản hồi Cuối cùng
Gateway chuyển tiếp phản hồi đến ứng dụng client, ứng dụng này hiển thị dữ liệu cho người dùng cuối.

## Khi nào Sử dụng Authorization Code Grant Flow

Sử dụng loại grant này **khi có sự tham gia của người dùng cuối** trong quy trình xác thực. Điều này lý tưởng cho:
- Ứng dụng web có đăng nhập người dùng
- Ứng dụng di động yêu cầu xác thực người dùng
- Bất kỳ tình huống nào mà người dùng cần cung cấp sự đồng ý rõ ràng

## Những Điểm Chính cần Ghi nhớ

- Authorization code grant flow cung cấp cách an toàn để xác thực người dùng cuối
- Nó bao gồm nhiều bước để đảm bảo bảo mật: đăng ký, xác thực, đồng ý và xác thực token
- Access token thuộc về người dùng cuối, không phải ứng dụng client
- Spring Cloud Gateway hoạt động như resource server, xác thực token trước khi chuyển tiếp yêu cầu
- Keycloak đóng vai trò là authorization server quản lý xác thực và cấp token

## Các Bước Tiếp theo

Với sự hiểu biết về authorization code grant flow này, bước tiếp theo là triển khai loại grant type flow này trong mạng microservices của chúng ta.

---

**Tóm tắt**: Bài giảng này đã trình bày OAuth2 Authorization Code Grant Flow từ nhiều góc độ khác nhau, minh họa cách các ứng dụng client, người dùng cuối, resource servers và authorization servers tương tác để cung cấp quyền truy cập an toàn vào tài nguyên microservices.




FILE: 12-creating-client-and-user-details-in-keycloak.md


# Tạo Client và User Details trong Keycloak cho Authorization Code Grant Flow

## Tổng quan

Trong bài giảng này, chúng ta sẽ tạo thông tin client và end user bên trong Keycloak authorization server để triển khai luồng OAuth2 Authorization Code grant trong mạng lưới microservices Easy Bank của chúng ta.

## Tại sao cần tạo Client mới?

Trước đây, chúng ta đã tạo một client có tên `easy-bank-callcenter-cc` cho **Client Credentials grant type flow**. Tuy nhiên, chúng ta không thể tái sử dụng client này vì:

- Nó được cấu hình đặc biệt cho Client Credentials grant type
- Authorization Code grant type yêu cầu các thiết lập cấu hình khác
- Chúng ta cần tạo một client riêng biệt với các thiết lập phù hợp cho Authorization Code flow

## Tạo Client Application

### Bước 1: Tạo Client mới

1. Điều hướng đến mục **Clients** trong Keycloak
2. Nhấp vào **Create Client**

### Bước 2: Cấu hình Client - Thiết lập chung

- **Client Type**: OpenID Connect
- **Client ID**: `easybank-callcenter-ac` (ac viết tắt của Authorization Code)
- **Name**: Easy Bank Call Center UI app
- **Description**: Easy Bank Call Center UI app

### Bước 3: Cấu hình Client - Thiết lập khả năng

Trên trang cấu hình khả năng:

1. **Enable Client Authentication**: ✓ (đã chọn)
2. **Select Standard Flow**: ✓ (đã chọn)
   - Đây đại diện cho Authorization Code grant type flow trong đặc tả OAuth2
3. **Bỏ chọn tất cả các luồng grant type khác**

> **Quan trọng**: Đảm bảo chỉ có Standard Flow được chọn.

### Bước 4: Cấu hình Client - URLs

#### Valid Redirect URI

Trong tình huống lý tưởng, bạn nên chỉ định URL chính xác nơi authorization server sẽ chuyển hướng end user sau khi xác thực thành công (ví dụ: trang dashboard hoặc profile).

**Mục đích**: 
- Xác định nơi client application sẽ nhận authorization code
- Ngăn chặn các lỗ hổng bảo mật nơi hacker có thể chuyển hướng access token đến các trang web độc hại

**Cấu hình**:
- Môi trường production: Chỉ định URL chuyển hướng chính xác
- Môi trường phát triển/thử nghiệm: Sử dụng `*` (dấu sao) để cho phép bất kỳ redirect URI nào

#### Post Logout Redirect URI

Có thể bỏ qua nếu bạn chưa có ứng dụng UI đầy đủ.

#### Web Origins

**Mục đích**: 
- Xử lý Cross-Origin Resource Sharing (CORS)
- Trong thực tế, ứng dụng client của bạn có thể được triển khai trên domain/cổng khác với authorization server hoặc microservices
- Trình duyệt mặc định chặn giao tiếp cross-origin trừ khi backend server cho phép rõ ràng

**Cấu hình**:
- Môi trường phát triển/thử nghiệm: Sử dụng `*` (dấu sao) để chấp nhận traffic từ bất kỳ domain/cổng nào
- Môi trường production: Chỉ định tên domain thực tế nơi client application của bạn được triển khai

> **Lưu ý**: Để biết thêm chi tiết về CORS và bảo mật cross-origin, tham khảo các khóa học Spring Security.

### Bước 5: Lưu và lấy thông tin xác thực

Sau khi lưu cấu hình, bạn có thể xem:
- **Client ID**: `easybank-callcenter-ac`
- **Client Secret**: (hiển thị trong tab credentials)

## Tạo End User Details

### Bước 1: Điều hướng đến Users

1. Đi đến tab **Users** trong Keycloak
2. Hiện tại, chỉ có admin user tồn tại

### Bước 2: Tạo User mới

Nhấp vào **Create User** và cấu hình:

- **Username**: `madan`
- **Email**: `tutor@eazybytes.com`
- **Email Verified**: Yes ✓
- **First Name**: Madan
- **Last Name**: Reddy

Nhấp **Create** để lưu user.

### Bước 3: Thiết lập mật khẩu User

1. Điều hướng đến tab **Credentials** cho user vừa tạo
2. Nhấp **Set Password**
3. Cấu hình mật khẩu:
   - **Password**: `12345`
   - **Confirm Password**: `12345`
   - **Temporary**: No (bỏ chọn)

> **Quan trọng**: Nếu "Temporary" được bật, user sẽ buộc phải thay đổi mật khẩu khi đăng nhập lần đầu.

4. Nhấp **Save** và xác nhận bằng cách nhấp **Save Password**

## Đăng ký User trong môi trường Production

### Câu hỏi thường gặp: Ai tạo End Users?

Trong các ứng dụng thực tế, quản trị viên không tạo thủ công từng user. Thay vào đó:

### Tích hợp Keycloak REST API

Keycloak cung cấp các REST API toàn diện cho phép:
- Các ứng dụng đã xác thực kết nối với Keycloak
- Tự động tạo user thông qua API calls
- Đăng ký user tự phục vụ

### Ví dụ triển khai

1. Tạo trang signup trong ứng dụng web của bạn
2. User nhập thông tin xác thực vào form signup
3. Ứng dụng gửi request đến Keycloak REST API
4. Keycloak tự động tạo tài khoản user

### Tài liệu Keycloak REST API

Để khám phá các REST API có sẵn:

1. Truy cập [trang web Keycloak](https://www.keycloak.org)
2. Nhấp vào **Docs**
3. Tìm mục **Administration REST API**

Tài liệu bao gồm:
- Tất cả REST API endpoints được hỗ trợ
- Đặc tả định dạng request
- Chi tiết định dạng response
- Tài liệu API đầy đủ cho tất cả các hành động admin UI

> **Lưu ý**: Tất cả các hành động có sẵn trong Keycloak admin UI cũng có sẵn thông qua REST APIs.

## Tóm tắt

Chúng ta đã hoàn thành thành công:

1. ✓ Tạo client details (`easybank-callcenter-ac`) được cấu hình cho Authorization Code grant flow
2. ✓ Cấu hình redirect URIs và web origins cho bảo mật và xử lý CORS
3. ✓ Tạo end user details (username: `madan`) trong Keycloak authorization server
4. ✓ Thiết lập thông tin xác thực user để xác thực

## Các bước tiếp theo

Với cả client details và end user details đã được đăng ký trong authorization server, chúng ta đã sẵn sàng triển khai Authorization Code grant type flow trong mạng lưới microservices của chúng ta.

---

*Cảm ơn bạn, và hẹn gặp lại trong bài giảng tiếp theo!*




FILE: 13-oauth2-authorization-code-flow-testing-with-postman.md


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




FILE: 14-testing-microservices-security-with-docker-compose.md


# Kiểm Thử Bảo Mật Microservices với Docker Compose

## Tổng Quan

Hướng dẫn này bao gồm cách kiểm thử các thay đổi liên quan đến bảo mật trong microservices bằng cách sử dụng Docker containers và Docker Compose. Bạn sẽ học cách bảo mật các microservices nội bộ để chúng chỉ có thể được truy cập thông qua edge server (API Gateway), ngăn chặn truy cập trực tiếp từ các ứng dụng client.

## Yêu Cầu Trước Khi Bắt Đầu

- Docker Desktop đã được cài đặt và đang chạy
- Các images của microservices đã được build với tags phù hợp
- Các file cấu hình Docker Compose
- Kiến thức về Keycloak authorization server

## Chuẩn Bị Docker Images

Tất cả các images của microservices đã được tạo với tag name là `SQL` và đẩy lên Docker Hub. Bạn có thể xác minh điều này bằng cách:

1. Mở Docker Desktop
2. Kiểm tra các images có tag `SQL`
3. Xác minh các tags tương tự tồn tại trong repository Docker Hub của bạn

## Các Thay Đổi Cấu Hình Docker Compose

### 1. Cập Nhật Tags của Images

Bước đầu tiên là cập nhật tags của images từ phiên bản trước (ví dụ: `S11`) sang phiên bản hiện tại (`S12`) cho tất cả các services trong file Docker Compose.

**Vị trí**: File Docker Compose của production profile

### 2. Thêm Service Keycloak

Một service Keycloak mới đã được thêm vào cấu hình Docker Compose:

```yaml
keycloak:
  image: <keycloak-image>
  container_name: keycloak
  ports:
    - "7080:8080"
  environment:
    - KEYCLOAK_ADMIN=<admin-username>
    - KEYCLOAK_ADMIN_PASSWORD=<admin-password>
  command: start-dev
  extends:
    service: network-deploy-service
```

**Chi Tiết Cấu Hình Quan Trọng:**
- **Ánh Xạ Cổng**: Keycloak chạy trên cổng `8080` bên trong Docker network và expose traffic ra thế giới bên ngoài ở cổng `7080`
- **Biến Môi Trường**: 
  - `KEYCLOAK_ADMIN`: Tên đăng nhập admin
  - `KEYCLOAK_ADMIN_PASSWORD`: Mật khẩu admin
- **Command**: `start-dev` - Sử dụng database nội bộ của Keycloak cho môi trường phát triển local
- **Network**: Extends `network-deploy-service` để đảm bảo Keycloak khởi động trong cùng network (easybank network) với các services khác

### 3. Services Giám Sát và Quan Sát

Không có thay đổi nào được thực hiện cho các services sau:
- Read/Write services
- Prometheus
- Minio
- Tempo
- Grafana
- Gateway
- Config Server
- Eureka Server

### 4. Bảo Mật Các Microservices Nội Bộ

**Thay Đổi Bảo Mật Quan Trọng**: Đã xóa ánh xạ cổng khỏi các microservices nội bộ.

**Trước đây:**
```yaml
accounts:
  ports:
    - "8080:8080"
```

**Sau khi thay đổi:**
```yaml
accounts:
  # Không có ánh xạ cổng
```

**Tác Động:**
- Các microservices Accounts, Loans và Cards không còn được expose ra thế giới bên ngoài
- Các services này chỉ có thể được truy cập bởi các services khác trong cùng Docker network bằng cách sử dụng service names và cổng nội bộ (ví dụ: `accounts:8080`)
- Các ứng dụng client phải đi qua API Gateway để truy cập các services này

### 5. Cấu Hình Gateway Server

Đã thêm một biến môi trường mới vào Gateway service cho việc xác thực OAuth2 JWT:

```yaml
gateway:
  environment:
    - SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI=http://keycloak:8080/realms/<realm-name>/protocol/openid-connect/certs
```

**Lưu Ý Quan Trọng:**
- Sử dụng service name `keycloak` thay vì `localhost` để giao tiếp nội bộ trong Docker network
- Sử dụng cổng `8080` (cổng nội bộ Docker network) thay vì `7080` (cổng exposed ra bên ngoài)
- File `application.yml` sử dụng `localhost:7080` cho truy cập bên ngoài, nhưng các Docker services sử dụng `keycloak:8080` cho giao tiếp nội bộ

## Các Profiles Cấu Hình

Các thay đổi tương tự đã được áp dụng cho tất cả các Docker Compose profiles:
- Default profile
- Production profile
- Các custom profiles khác

## Khởi Động Các Services

### Danh Sách Kiểm Tra Trước Khi Chạy

Trước khi chạy Docker Compose, đảm bảo:
1. ✅ Tất cả các instances đang chạy local trong IDE của bạn đã được dừng
2. ✅ Tất cả containers trong Docker Desktop đã được dừng
3. ✅ Bất kỳ Keycloak containers độc lập nào đã được dừng (để tránh xung đột cổng)

### Chạy Docker Compose

Thực thi lệnh sau trong terminal của bạn:

```bash
docker compose up -d
```

**Hành Vi Mong Đợi:**
- Tất cả containers sẽ khởi động, bao gồm cả Keycloak
- Quá trình này mất khoảng 2-3 phút
- Các services sẽ khả dụng trên Easy Bank network

## Lợi Ích Về Kiến Trúc

Cấu hình này cung cấp một số lợi ích về bảo mật:

1. **Cô Lập Network**: Các microservices nội bộ không thể truy cập trực tiếp từ bên ngoài Docker network
2. **Gateway Pattern**: Tất cả traffic bên ngoài phải đi qua API Gateway
3. **Bảo Mật OAuth2**: JWT tokens được xác thực bằng public certificates của Keycloak
4. **Service Discovery**: Các services giao tiếp sử dụng service names trong Docker network

## Xử Lý Sự Cố

- **Xung Đột Cổng**: Đảm bảo không có services khác đang sử dụng cổng 7080 hoặc 8080
- **Kết Nối Keycloak**: Xác minh Gateway có thể kết nối tới Keycloak tại `keycloak:8080`
- **Vấn Đề Network**: Đảm bảo tất cả services đều ở trên cùng một Docker network

## Các Bước Tiếp Theo

Tiếp tục kiểm thử các thay đổi bảo mật trong môi trường Docker để xác minh:
- Kiểm soát truy cập thông qua Gateway
- Xác thực JWT token
- Giao tiếp giữa các microservices trong Docker network

---

**Lưu Ý**: Cấu hình này được thiết kế cho mục đích phát triển và kiểm thử. Cần áp dụng thêm các biện pháp bảo mật cho môi trường production.




FILE: 15-testing-microservices-security-with-docker-and-keycloak.md


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




FILE: 16-event-driven-microservices-introduction.md


# Xây Dựng Microservices Hướng Sự Kiện (Event-Driven)

## Giới Thiệu

Phần này giới thiệu **Thử thách #10: Xây dựng Microservices hướng sự kiện**. Chúng ta sẽ khám phá microservices hướng sự kiện là gì, tại sao chúng quan trọng, và cách triển khai chúng trong kiến trúc microservices của bạn.

## Hiểu Về Temporal Coupling (Khớp Nối Thời Gian)

### Loose Coupling vs Temporal Coupling

**Loose Coupling (Khớp nối lỏng lẻo)** là nguyên tắc thiết kế trong đó chúng ta xây dựng logic nghiệp vụ ứng dụng trong các microservices riêng biệt để chúng có thể:
- Phát triển độc lập
- Triển khai độc lập
- Mở rộng độc lập

Ví dụ, trong khóa học chúng ta đã tách:
- Logic tài khoản → Accounts microservice
- Logic thẻ → Cards microservice
- Logic vay → Loans microservice

**Temporal Coupling (Khớp nối thời gian)** xảy ra khi một service gọi đến service khác và mong đợi nhận phản hồi ngay lập tức trước khi tiếp tục xử lý.

### Ví Dụ Về Temporal Coupling

Xét hai microservices:
- **Microservice1** (người gọi) phụ thuộc vào **Microservice2** (người được gọi)
- Khi Microservice1 gọi đến Microservice2, nó liên tục chờ đợi phản hồi
- Bất kỳ hành vi chậm trễ nào của Microservice2 đều ảnh hưởng trực tiếp đến hiệu suất của Microservice1

**Điểm chính:** Temporal coupling xảy ra với giao tiếp đồng bộ (synchronous communication), đặc biệt khi sử dụng REST APIs.

## Tránh Temporal Coupling

### Giải Pháp: Giao Tiếp Bất Đồng Bộ

Để tránh temporal coupling, chúng ta nên sử dụng **giao tiếp bất đồng bộ (asynchronous communication)** bất cứ khi nào có thể trong mạng lưới microservices. Giao tiếp đồng bộ không phải lúc nào cũng cần thiết - nhiều tình huống thực tế có thể được thực hiện hiệu quả với các mẫu bất đồng bộ.

## Các Cách Tiếp Cận Giao Tiếp Đồng Bộ

### 1. Phương Pháp Imperative (Mệnh Lệnh)
- Một thread chuyên dụng được gán cho giao tiếp
- Thread bị **chặn (blocked)** trong khi chờ phản hồi
- Thread ở trạng thái idle cho đến khi Microservice2 phản hồi
- Sử dụng thread kém hiệu quả

### 2. Phương Pháp Reactive (Phản Ứng)
- Một thread khởi tạo cuộc gọi đến Microservice2
- Thread quay lại thread pool sau khi gọi
- Thread xử lý request tiếp theo có sẵn
- Thread chỉ được gán khi phản hồi đến
- Sử dụng thread hiệu quả hơn

**Quan trọng:** Cả hai phương pháp vẫn sử dụng giao tiếp đồng bộ - Microservice1 không thể tiếp tục logic nghiệp vụ tiếp theo cho đến khi nhận được phản hồi từ Microservice2.

## Khi Nào Sử Dụng Giao Tiếp Đồng Bộ

Giao tiếp đồng bộ phù hợp cho **các tình huống nghiệp vụ quan trọng** yêu cầu phản hồi ngay lập tức cho người dùng cuối.

### Ví Dụ: Ứng Dụng Ngân Hàng
- Người dùng nhấp vào nút để kiểm tra số dư tài khoản hiện tại
- Người dùng mong đợi nhìn thấy phản hồi ngay lập tức trên màn hình
- Giao tiếp đồng bộ là cần thiết trong trường hợp này

## Microservices Hướng Sự Kiện

### Sự Kiện (Event) Là Gì?

**Sự kiện (Event)** là một sự cố xảy ra bên trong microservices của bạn, biểu thị:
- Sự chuyển đổi trạng thái
- Một cập nhật trong hệ thống

Khi một sự kiện xảy ra, các bên liên quan phải được thông báo.

### Ví Dụ Thực Tế: Ứng Dụng Thương Mại Điện Tử

Xét quy trình xử lý đơn hàng của Amazon:

1. **Order Microservice**: Khi người dùng hoàn tất thanh toán, đơn hàng được xác nhận
2. **Sự kiện được kích hoạt**: Order microservice tạo ra một sự kiện/thông báo
3. **Delivery Microservice**: Nhận thông báo
4. **Lợi ích chính**: Order microservice không chờ đợi quá trình giao hàng hoàn thành

**Đây là giao tiếp bất đồng bộ:**
- Order microservice gửi thông báo
- Công việc của nó đã hoàn thành
- Không chờ đợi phản hồi từ delivery microservice

## Xây Dựng Microservices Hướng Sự Kiện

Để triển khai microservices hướng sự kiện, bạn cần:

### Các Thành Phần Kiến Trúc
1. **Event-Driven Architecture**: Mẫu thiết kế để tạo và tiêu thụ sự kiện
2. **Asynchronous Communication**: Truyền thông điệp không chặn
3. **Event Brokers**: Phần mềm trung gian để phân phối sự kiện

### Hệ Sinh Thái Spring Cloud

Tận dụng các dự án Spring Cloud sau:
- **Spring Cloud Function**: Để xây dựng các event handler
- **Spring Cloud Stream**: Để xây dựng microservices hướng sự kiện

## Tóm Tắt

Microservices hướng sự kiện mang lại:
- ✅ Giảm temporal coupling
- ✅ Khả năng mở rộng tốt hơn
- ✅ Cải thiện khả năng phục hồi của hệ thống
- ✅ Sử dụng tài nguyên hiệu quả hơn

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá chi tiết thế giới của microservices hướng sự kiện!

---

**Bước Tiếp Theo:** Tìm hiểu cách triển khai kiến trúc hướng sự kiện sử dụng Spring Cloud Function và Spring Cloud Stream.




FILE: 17-event-driven-microservices-models.md


# Các Mô Hình Microservices Hướng Sự Kiện

## Giới Thiệu

Khi xây dựng microservices hướng sự kiện trong môi trường production, có hai mô hình chính được sử dụng rộng rãi trong ngành:

1. **Mô Hình Publisher-Subscriber (Pub/Sub)**
2. **Mô Hình Event Streaming**

Tài liệu này sẽ khám phá cả hai mô hình, sự khác biệt giữa chúng và khi nào nên sử dụng từng phương pháp.

## Mô Hình Publisher-Subscriber (Pub/Sub)

### Tổng Quan

Mô hình Pub/Sub xoay quanh các subscription (đăng ký) trong đó:

- **Producers (Nhà sản xuất)** tạo ra các sự kiện
- Sự kiện được phân phối đến tất cả **subscribers (người đăng ký)** quan tâm để tiêu thụ
- Mỗi subscriber nhận các sự kiện mà họ đã đăng ký

### Đặc Điểm Chính

- Một khi sự kiện được nhận và tiêu thụ bởi consumers, **nó không thể được phát lại**
- Subscribers mới tham gia sau sẽ **không có quyền truy cập vào các sự kiện trong quá khứ**
- Sự kiện được tiêu thụ theo thời gian thực khi chúng xảy ra
- Lý tưởng cho các tình huống không yêu cầu phát lại sự kiện lịch sử

### Triển Khai

Mô hình Pub/Sub thường được triển khai sử dụng **RabbitMQ**, một lựa chọn rất phổ biến cho pattern này.

## Mô Hình Event Streaming

### Tổng Quan

Tương tự như Pub/Sub, mô hình Event Streaming bao gồm producers và consumers, nhưng có sự khác biệt về kiến trúc đáng kể.

### Đặc Điểm Chính

- Sự kiện được **ghi vào log theo cách tuần tự**
- Producers phát hành sự kiện khi chúng xảy ra
- Sự kiện được **lưu trữ theo thứ tự rõ ràng**
- Consumers có thể **đọc từ bất kỳ phần nào của luồng sự kiện**
- **Sự kiện có thể được phát lại**, cho phép clients tham gia bất cứ lúc nào
- Subscribers mới có thể nhận **tất cả các sự kiện trong quá khứ**

### Khả Năng Phát Lại Sự Kiện

Khả năng phát lại sự kiện là điểm khác biệt chính:

- Consumers có tính linh hoạt để đọc dữ liệu lịch sử
- Subscribers có thể tham gia tại bất kỳ thời điểm nào và truy cập các sự kiện trong quá khứ
- Tính năng phát lại có thể được tắt nếu cần

### Triển Khai

**Apache Kafka** là một nền tảng mạnh mẽ được sử dụng rộng rãi cho xử lý event streaming.

## Lựa Chọn Mô Hình Phù Hợp

### Khi Nào Sử Dụng Pub/Sub

- Kịch bản kinh doanh của bạn **không yêu cầu** consumers đọc các sự kiện trong quá khứ
- Tiêu thụ sự kiện theo thời gian thực là đủ
- Yêu cầu kiến trúc đơn giản hơn
- Chi phí lưu trữ thấp hơn

### Khi Nào Sử Dụng Event Streaming

- Consumers cần khả năng **phát lại các sự kiện trong quá khứ**
- Subscribers mới yêu cầu quyền truy cập vào dữ liệu lịch sử
- Cần các pattern event sourcing
- Audit trails và phát lại sự kiện là yêu cầu kinh doanh

### Lưu Ý Quan Trọng

**Không có phương pháp tốt hay xấu** - sự lựa chọn phụ thuộc vào các kịch bản kinh doanh và yêu cầu cụ thể của bạn.

## Kế Hoạch Triển Khai Khóa Học

Khóa học này sẽ đề cập đến cả hai mô hình trong các phần riêng biệt:

### Phần 1: Xây Dựng Event-Driven Microservices với RabbitMQ

Chúng ta sẽ khám phá triển khai mô hình Pub/Sub sử dụng RabbitMQ, bao gồm:
- Cài đặt và cấu hình RabbitMQ
- Triển khai Producer và Consumer
- Các pattern định tuyến message và exchange

### Phần 2: Xây Dựng Event-Driven Microservices với Apache Kafka

Chúng ta sẽ khám phá triển khai mô hình Event Streaming sử dụng Apache Kafka, bao gồm:
- Kiến trúc và các khái niệm Kafka
- Các pattern event streaming
- Consumer groups và phân vùng (partitioning)

## Tóm Tắt

Cả hai mô hình hướng sự kiện đều cung cấp khả năng mạnh mẽ để xây dựng microservices có khả năng mở rộng:

- **Mô Hình Pub/Sub (RabbitMQ)**: Tốt nhất cho phân phối sự kiện theo thời gian thực mà không cần yêu cầu phát lại
- **Mô Hình Event Streaming (Apache Kafka)**: Tốt nhất khi cần phát lại sự kiện và truy cập dữ liệu lịch sử

Chọn mô hình phù hợp nhất với yêu cầu kinh doanh và các ràng buộc kỹ thuật của bạn.

---

**Các Bước Tiếp Theo**: Trong các bài giảng tiếp theo, chúng ta sẽ bắt đầu khám phá mô hình Pub/Sub với chi tiết triển khai RabbitMQ.




FILE: 18-asynchronous-communication-with-pub-sub-model.md


# Giao Tiếp Bất Đồng Bộ với Mô Hình Pub/Sub trong Microservices

## Tổng Quan

Tài liệu này giải thích cách triển khai giao tiếp bất đồng bộ sử dụng mô hình Publish/Subscribe (Pub/Sub) trong kiến trúc microservices với Spring Boot và RabbitMQ.

## Kiến Trúc Hiện Tại

Hệ sinh thái microservices của chúng ta hiện bao gồm:
- **Accounts Microservice** - Xử lý các thao tác CRUD trên tài khoản
- **Cards Microservice** - Quản lý các thao tác thẻ
- **Loans Microservice** - Quản lý các thao tác khoản vay

Các microservices này hiện đang sử dụng **giao tiếp đồng bộ** cho các thao tác nghiệp vụ quan trọng yêu cầu phản hồi ngay lập tức cho người dùng cuối.

## Tại Sao Cần Giao Tiếp Bất Đồng Bộ?

Trong khi giao tiếp đồng bộ là cần thiết cho các thao tác quan trọng, một số tình huống được hưởng lợi từ xử lý bất đồng bộ:
- Gửi thông báo (SMS/Email)
- Các tác vụ xử lý nền
- Tách rời các dịch vụ phụ thuộc
- Cải thiện khả năng phục hồi của hệ thống

## Kịch Bản: Tạo Tài Khoản với Thông Báo Bất Đồng Bộ

### Vấn Đề

Khi tạo tài khoản mới, hai thao tác xảy ra:
1. **Quan trọng**: Tạo tài khoản và lưu vào cơ sở dữ liệu (yêu cầu phản hồi ngay lập tức)
2. **Không quan trọng**: Gửi thông báo cho người dùng (có thể xử lý bất đồng bộ)

Chúng ta không muốn Accounts microservice phải xử lý tất cả logic giao tiếp trực tiếp.

### Giải Pháp: Pub/Sub với RabbitMQ

Chúng ta sẽ triển khai một **Message Microservice** mới chuyên xử lý các giao tiếp, sử dụng RabbitMQ làm event broker.

## Luồng Triển Khai

### Bước 1-2: Tạo Tài Khoản (Đồng Bộ)
```
Người dùng → Accounts Microservice → Cơ sở dữ liệu
```
- Người dùng gửi yêu cầu tạo tài khoản mới
- Accounts microservice tạo tài khoản trong cơ sở dữ liệu
- Phản hồi ngay lập tức được gửi cho người dùng: "Tài khoản đã được tạo thành công"

### Bước 3: Phát Hành Event (Bắt Đầu Bất Đồng Bộ)
```
Accounts Microservice → Event Broker (RabbitMQ) → Queue
```
- Accounts microservice phát hành một event đến event broker
- Event chứa thông tin chi tiết về việc tạo tài khoản
- Event được đặt vào một queue

### Bước 4: Tiêu Thụ Event
```
Queue → Message Microservice → Người dùng (SMS/Email)
```
- Message microservice liên tục giám sát queue
- Khi phát hiện event, nó đọc chi tiết event
- Gửi thông báo SMS/Email cho người dùng

### Bước 5-6: Luồng Xác Nhận (Bất Đồng Bộ Ngược)
```
Message Microservice → Event Broker → Queue Khác
```
- Sau khi xử lý, Message microservice phát hành một event xác nhận
- Event được đặt vào queue mà Accounts microservice đang giám sát

### Bước 7: Cập Nhật Trạng Thái
```
Queue → Accounts Microservice → Cập Nhật Cơ sở dữ liệu
```
- Accounts microservice nhận thông báo
- Cập nhật cột cơ sở dữ liệu: "Giao tiếp đã được gửi cho khách hàng"

## Lợi Ích Chính

### 1. **Ghép Nối Lỏng Lẻo**
- Các microservices không biết về nhau trực tiếp
- Chúng chỉ tương tác với event broker
- Dễ dàng thêm subscribers mới mà không cần sửa đổi publishers

### 2. **Khả Năng Phục Hồi**
- Nếu Message microservice chậm hoặc ngừng hoạt động, Accounts microservice không bị ảnh hưởng
- Các event được xếp hàng cho đến khi consumers sẵn sàng
- Không có lỗi dây chuyền

### 3. **Tách Biệt Các Mối Quan Tâm**
- Accounts microservice tập trung vào quản lý tài khoản
- Message microservice tập trung vào giao tiếp
- Trách nhiệm đơn lẻ rõ ràng

### 4. **Khả Năng Mở Rộng**
- Có thể mở rộng Message microservice độc lập dựa trên tải thông báo
- Nhiều instances có thể tiêu thụ từ cùng một queue

## Ngăn Xếp Công Nghệ

- **Event Broker**: RabbitMQ (Mô hình Pub/Sub)
- **Framework**: Spring Boot
- **Pattern**: Kiến trúc Hướng Sự Kiện
- **Mô Hình Giao Tiếp**: Tin nhắn bất đồng bộ

## Các Thành Phần Kiến Trúc

### Accounts Microservice
- Phát hành các event tạo tài khoản
- Đăng ký nhận các event xác nhận giao tiếp
- Cập nhật trạng thái tài khoản trong cơ sở dữ liệu

### Message Microservice (Mới)
- Đăng ký nhận các event tạo tài khoản
- Gửi thông báo SMS/Email
- Phát hành các event xác nhận giao tiếp

### Event Broker (RabbitMQ)
- Quản lý các message queues
- Định tuyến events giữa publishers và subscribers
- Đảm bảo giao hàng tin nhắn đáng tin cậy

## Những Cân Nhắc Quan Trọng

1. **Khi Nào Sử Dụng Giao Tiếp Đồng Bộ**
   - Các thao tác nghiệp vụ quan trọng yêu cầu phản hồi ngay lập tức
   - Các thao tác mà tính nhất quán là bắt buộc
   - Các thao tác hướng người dùng cần phản hồi tức thì

2. **Khi Nào Sử Dụng Giao Tiếp Bất Đồng Bộ**
   - Các tác vụ nền không quan trọng
   - Thông báo và cảnh báo
   - Các quy trình chạy lâu
   - Đồng bộ hóa dữ liệu giữa các dịch vụ

## Các Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ đề cập:
- Thiết lập RabbitMQ làm event broker
- Cấu hình queues và exchanges
- Triển khai publishers trong Accounts microservice
- Triển khai subscribers trong Message microservice
- Xử lý lỗi và cơ chế thử lại
- Giám sát và khả năng quan sát

## Kết Luận

Bằng cách triển khai mô hình Pub/Sub với RabbitMQ, chúng ta đạt được một kiến trúc microservices có khả năng phục hồi, mở rộng và bảo trì tốt hơn. Mẫu giao tiếp bất đồng bộ cho phép chúng ta tách rời các dịch vụ trong khi vẫn duy trì độ tin cậy của hệ thống.




FILE: 19-rabbitmq-introduction-and-asynchronous-communication.md


# Giới Thiệu RabbitMQ và Giao Tiếp Bất Đồng Bộ

## Tổng Quan

Hướng dẫn này cung cấp phần giới thiệu về RabbitMQ và cách triển khai giao tiếp bất đồng bộ sử dụng message broker này trong kiến trúc microservices. Chúng ta sẽ khám phá các khái niệm cơ bản của RabbitMQ, các khái niệm chính và cách nó tạo điều kiện giao tiếp giữa các microservices.

## RabbitMQ Là Gì?

**RabbitMQ** là một message broker mã nguồn mở được công nhận rộng rãi và sử dụng bởi đa số các công ty trên toàn thế giới. Nó tuân theo giao thức **AMQP (Advanced Message Queuing Protocol)** và cung cấp khả năng giao tiếp nhắn tin bất đồng bộ linh hoạt giữa các ứng dụng.

### Các Tính Năng Chính

- Mã nguồn mở và được áp dụng rộng rãi
- Tuân theo giao thức AMQP
- Hỗ trợ nhắn tin bất đồng bộ linh hoạt
- Gần đây đã bổ sung khả năng event streaming
- Có thể phát lại events/messages trong các phiên bản gần đây

## RabbitMQ so với Apache Kafka

Mặc dù RabbitMQ gần đây đã giới thiệu khả năng event streaming cho phép phát lại các events hoặc messages, Apache Kafka vẫn là lựa chọn thống trị cho các kịch bản event streaming. Điều này là do Kafka đã chiếm phần lớn thị trường trước khi RabbitMQ triển khai các tính năng này.

**Sự Khác Biệt Chính trong Mô Hình Pub/Sub:**
- RabbitMQ truyền thống: Không thể phát lại events hoặc messages
- Phiên bản RabbitMQ gần đây: Đã thêm khả năng event streaming
- Apache Kafka: Được xây dựng cho event streaming ngay từ đầu

## Các Khái Niệm Cốt Lõi và Thuật Ngữ

### 1. Producer (Publisher - Nhà Sản Xuất)

**Producer** là thực thể hoặc service chịu trách nhiệm gửi events hoặc messages đến message broker. Trong mô hình pub/sub với RabbitMQ, chúng ta thường gọi events là "messages" vì RabbitMQ là một message broker.

**Tên gọi khác:** Publisher (vì nó xuất bản messages đến message broker)

### 2. Consumer (Subscriber - Người Tiêu Thụ)

**Consumer** là thực thể hoặc service chịu trách nhiệm nhận messages từ message broker và xử lý chúng.

**Tên gọi khác:** Subscriber (vì nó đăng ký với message broker để được thông báo khi có messages đến)

### 3. Message Broker

**Message broker** là thành phần middleware nhận messages từ producers và chuyển chúng đến các consumers phù hợp. RabbitMQ là một message broker như vậy, và có nhiều message broker khác có sẵn trong ngành.

### Tổng Quan Kiến Trúc

```
Producer → Message Broker → Consumer
```

**Lưu Ý Quan Trọng:**
- Message broker có thể xử lý nhiều producers và consumers cùng lúc
- Không giới hạn ở giao tiếp một-một
- Kiến trúc có khả năng mở rộng và linh hoạt

## Mô Hình Nhắn Tin AMQP

Mô hình nhắn tin AMQP hoạt động dựa trên hai nguyên tắc chính:

### 1. Exchanges (Sàn Giao Dịch)

Khi producer muốn gửi message đến message broker, nó sẽ gửi message đến một **exchange** bên trong message broker. Exchange xác định queue nào sẽ nhận bản sao của message dựa trên các quy tắc định tuyến đã chỉ định.

### 2. Queues (Hàng Đợi)

**Queues** là nơi lưu trữ messages cho đến khi consumers lấy chúng. Consumers đăng ký với các queues cụ thể để nhận messages.

### Kiến Trúc Luồng Message

```
Producer → Exchange → Queue(s) → Consumer(s)
```

**Luồng Chi Tiết:**

1. **Producer** gửi message đến một **Exchange**
2. **Exchange** xác định **Queue(s)** nào sẽ nhận message dựa trên quy tắc định tuyến
3. Message được đẩy vào **Queue(s)** phù hợp
4. **Consumer(s)** đã đăng ký với các queues đó sẽ nhận message
5. Sau khi message được đọc, nó thường được xóa khỏi queue

### Tính Linh Hoạt trong Kiến Trúc

- **Nhiều Exchanges và Queues:** Message broker có thể chứa bất kỳ số lượng exchanges và queues nào
- **Nhiều Consumers trên một Queue:** Bất kỳ số lượng consumers nào có thể đăng ký với một queue duy nhất
- **Nhiều Queues cho một Consumer:** Một consumer có thể đăng ký với nhiều queues

## Trường Hợp Sử Dụng: Accounts và Message Microservices

Trong triển khai của chúng ta, chúng ta đang thiết lập giao tiếp bất đồng bộ giữa **accounts microservice** và **message microservice** sử dụng RabbitMQ như một event broker.

### Tại Sao Chọn RabbitMQ?

- Message broker tiêu chuẩn ngành
- Mã nguồn mở và được tài liệu hóa tốt
- Không phụ thuộc ngôn ngữ (hoạt động với Java, Python và các ngôn ngữ khác)
- Độ tin cậy đã được chứng minh trong môi trường production

### Không Phụ Thuộc Ngôn Ngữ

RabbitMQ không chỉ dành riêng cho Java. Bạn có thể sử dụng nó bất kể ngôn ngữ lập trình của bạn:
- **Microservice 1** có thể được viết bằng Python
- **Microservice 2** có thể được viết bằng Java
- Cả hai có thể giao tiếp liền mạch thông qua RabbitMQ

## Tài Nguyên Học Tập

Để biết thông tin chi tiết hơn về RabbitMQ, hãy truy cập trang web chính thức:

**Trang Web:** [rabbitmq.com](https://rabbitmq.com)

### Các Hướng Dẫn Có Sẵn

Trang web chính thức cung cấp tài liệu và hướng dẫn toàn diện:

- **Hướng Dẫn Bắt Đầu**
- **Các Hướng Dẫn RabbitMQ:**
  - Hello World
  - Queues (Hàng đợi)
  - Mô hình Pub/Sub
  - Routing (Định tuyến)
  - Khả năng Event Streaming
  - Mẫu Request-Reply

## Các Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ:

1. Tìm hiểu sâu về sự khác biệt giữa RabbitMQ và Apache Kafka
2. Triển khai giao tiếp bất đồng bộ sử dụng RabbitMQ
3. Xây dựng các ví dụ thực tế với Spring Boot microservices
4. Khám phá các mẫu và best practices nâng cao của RabbitMQ

## Kết Luận

RabbitMQ là một message broker mã nguồn mở mạnh mẽ cho phép giao tiếp bất đồng bộ linh hoạt giữa các microservices. Hiểu các khái niệm cốt lõi của nó—producers, consumers, exchanges và queues—là điều cần thiết để triển khai các kiến trúc hướng sự kiện mạnh mẽ. Trong phần tiếp theo, chúng ta sẽ triển khai các khái niệm này với các ví dụ thực tế sử dụng Spring Boot và Java.

---

**Lưu Ý:** Tài liệu này là một phần của loạt bài về kiến trúc microservices tập trung vào các mẫu giao tiếp bất đồng bộ với RabbitMQ và Spring Boot.




FILE: 2-securing-microservices-with-oauth2-client-credentials.md


# Bảo Mật Microservices với OAuth2 Client Credentials Grant Flow

## Tổng Quan

Hướng dẫn này giải thích cách bảo mật kiến trúc microservices Spring Boot sử dụng OAuth2 Client Credentials Grant Type Flow. Chúng ta sẽ tập trung vào việc bảo vệ Gateway Server (Edge Server) - điểm vào của mạng lưới microservices.

## Các Thành Phần Kiến Trúc

### 1. Ứng Dụng Client
- Dịch vụ bên ngoài, API, hoặc backend server
- Cố gắng kết nối với mạng lưới microservices
- Phải đăng ký với authorization server

### 2. Authorization Server (Keycloak)
- Quản lý xác thực và phân quyền
- Phát hành access token cho các client đã đăng ký
- Xác thực access token

### 3. Gateway Server (Resource Server)
- Hoạt động như edge server cho microservices
- Xác thực access token trước khi chuyển tiếp yêu cầu
- Định tuyến yêu cầu đến các microservices nội bộ

### 4. Microservices Nội Bộ
- Các microservices: Accounts, Loans, và Cards
- Được bảo vệ phía sau firewall/Docker network
- Không thể truy cập trực tiếp từ bên ngoài

## Luồng OAuth2 Client Credentials

### Quy Trình Từng Bước

#### Bước 1: Client Yêu Cầu Access Token
```
Client → Auth Server
- Gửi: Client ID và Client Secret
- Nhận: Access Token (và ID Token nếu hỗ trợ OpenID)
```

Ứng dụng client phải:
- Đăng ký với Keycloak
- Được phê duyệt bởi quản trị viên Keycloak
- Nhận thông tin xác thực hợp lệ (Client ID và Client Secret)

#### Bước 2: Client Gọi Gateway Kèm Access Token
```
Client → Gateway Server
- Gửi: Yêu cầu API + Access Token
```

#### Bước 3: Gateway Xác Thực Access Token
```
Gateway → Auth Server
- Gửi: Access Token để xác thực
- Nhận: Xác nhận hợp lệ
```

Gateway Server:
- Nhận access token từ client
- Xác thực với authorization server
- Đảm bảo chỉ những client đã xác thực mới được tiếp tục

#### Bước 4: Chuyển Tiếp Yêu Cầu
```
Gateway → Internal Microservices
- Chuyển tiếp yêu cầu đã xác thực đến microservices Accounts/Loans/Cards
```

#### Bước 5: Trả Về Kết Quả
```
Internal Microservices → Gateway → Client
- Kết quả chảy ngược qua gateway về client
```

## Quyết Định Thiết Kế Bảo Mật

### Tại Sao Chỉ Bảo Mật Gateway?

**Câu hỏi**: Tại sao không biến các microservices riêng lẻ (Accounts, Loans, Cards) thành resource servers?

**Trả lời**: 

1. **Cô Lập Mạng**: Các microservices nội bộ được triển khai phía sau:
   - Firewalls
   - Docker networks
   - Kubernetes clusters
   
   Điều này ngăn chặn truy cập trực tiếp từ bên ngoài.

2. **Ảnh Hưởng Hiệu Suất**: Biến tất cả microservices thành resource servers sẽ:
   - Yêu cầu xác thực access token cho mọi request
   - Bao gồm cả giao tiếp nội bộ giữa các microservices
   - Gây ra overhead hiệu suất không cần thiết
   - Tăng độ phức tạp của hệ thống

3. **Kiến Trúc Đơn Giản Hóa**: 
   - Chỉ Gateway cần xác thực token
   - Giao tiếp nội bộ vẫn hiệu quả
   - Phân tách trách nhiệm tốt hơn

### Bảo Mật Mạng

Các client bên ngoài **không thể** gọi trực tiếp các microservices nội bộ vì:
- Microservices được triển khai trong mạng cô lập (Docker/Kubernetes)
- Chỉ Gateway Server tồn tại trong cùng mạng
- Client không có lựa chọn nào khác ngoài định tuyến qua Gateway

### Bảo Mật Microservices Nội Bộ

Mặc dù các microservices nội bộ không phải là OAuth2 resource servers, chúng vẫn nên được bảo mật bằng:
- Service mesh security (ví dụ: Istio)
- mTLS (Mutual TLS)
- Network policies
- Các phương pháp tiêu chuẩn công nghiệp khác (được đề cập khi triển khai Kubernetes)

## Khi Nào Sử Dụng Client Credentials Grant Type

Grant type này phù hợp khi:
- ✅ Hai ứng dụng backend/APIs giao tiếp với nhau
- ✅ Không có người dùng cuối tham gia
- ✅ Không có ứng dụng frontend tham gia
- ✅ Giao tiếp máy-với-máy (machine-to-machine)
- ✅ Xác thực dịch vụ-với-dịch vụ (service-to-service)

KHÔNG phù hợp khi:
- ❌ Người dùng cuối cần xác thực
- ❌ Ứng dụng trình duyệt tham gia
- ❌ Cần sự đồng ý của người dùng

## Các Bước Triển Khai

Các chủ đề sau sẽ được đề cập trong các bài giảng tiếp theo:

1. **Thiết Lập Keycloak làm Authorization Server**
   - Cài đặt và cấu hình
   - Thiết lập Realm và client

2. **Cấu Hình Spring Cloud Gateway làm Resource Server**
   - Thêm dependencies OAuth2
   - Cấu hình bảo mật
   - Thiết lập xác thực token

3. **Đăng Ký Ứng Dụng Client trong Keycloak**
   - Tạo client credentials
   - Cấu hình quyền và scope

4. **Kiểm Thử OAuth2 Flow**
   - Lấy access tokens
   - Thực hiện các yêu cầu đã xác thực
   - Xử lý hết hạn token

## Tóm Tắt

- Gateway Server hoạt động như điểm vào duy nhất và resource server
- Các ứng dụng client phải lấy access token từ Keycloak
- Access token được xác thực trước khi yêu cầu đến microservices nội bộ
- Các microservices nội bộ được bảo vệ bởi cô lập mạng
- Phương pháp này cân bằng giữa bảo mật, hiệu suất và sự đơn giản

## Những Điểm Chính Cần Nhớ

1. **Client Credentials Grant Type** hoàn hảo cho giao tiếp API-to-API
2. **Bảo mật cấp Gateway** cung cấp xác thực tập trung
3. **Cô lập mạng** bảo vệ các microservices nội bộ
4. **Tối ưu hiệu suất** bằng cách tránh xác thực token dư thừa
5. **Best practices công nghiệp** cho bảo mật microservices

---

*Bài Giảng Tiếp Theo: Thiết Lập Keycloak Authorization Server*




FILE: 20-spring-cloud-function-for-event-driven-microservices.md


# Spring Cloud Function cho Microservices Hướng Sự Kiện

## Giới Thiệu về Message Microservice

Để bắt đầu triển khai giao tiếp bất đồng bộ với sự trợ giúp của RabbitMQ, trước tiên chúng ta cần tạo **message microservice**.

Message microservice này chịu trách nhiệm cho:
- Nhận tin nhắn từ message broker
- Gửi thông tin liên lạc đến người dùng cuối qua SMS và email

## Tại Sao Sử Dụng Spring Cloud Function?

Thay vì xây dựng microservice này bằng cách tiếp cận truyền thống với các REST services (các annotation như RestController, GetMapping, PostMapping), chúng ta sẽ tận dụng **Spring Cloud Function**.

### Spring Cloud Function là gì?

Spring Cloud Function hỗ trợ phát triển logic nghiệp vụ bằng cách sử dụng các hàm (functions). Các nhà phát triển chỉ cần viết logic nghiệp vụ của họ bên trong các hàm, và các vấn đề về cơ sở hạ tầng sẽ được Spring Cloud Function framework đảm nhiệm.

## Các Giao Diện Function Chuẩn

Spring Cloud Function tận dụng các giao diện function chuẩn được giới thiệu trong Java 8:

### 1. Supplier (Nhà Cung Cấp)
- **Định nghĩa**: Một hàm hoặc biểu thức lambda tạo ra đầu ra mà không yêu cầu bất kỳ đầu vào nào
- **Còn được gọi là**: Producer (Nhà sản xuất), Publisher (Nhà xuất bản), hoặc Source (Nguồn)
- **Đặc điểm**: 
  - Không yêu cầu đầu vào
  - Luôn tạo ra đầu ra
  - Cung cấp đầu ra mà không cần đầu vào

### 2. Function (Hàm)
- **Định nghĩa**: Nhận đầu vào và tạo ra đầu ra
- **Còn được gọi là**: Processor (Bộ xử lý)
- **Đặc điểm**:
  - Nhận một đầu vào
  - Xử lý đầu vào
  - Tạo ra đầu ra

### 3. Consumer (Người Tiêu Dùng)
- **Định nghĩa**: Một hàm hoặc biểu thức lambda tiêu thụ đầu vào nhưng không tạo ra đầu ra
- **Còn được gọi là**: Subscriber (Người đăng ký) hoặc Sink (Bồn chứa)
- **Đặc điểm**:
  - Luôn có đầu vào
  - Không bao giờ tạo ra đầu ra
  - Chỉ tiêu thụ dữ liệu

## Ưu Điểm của Spring Cloud Function

### 1. Linh Hoạt trong Các Mô Hình Triển Khai
- **Mặc định**: Tất cả các hàm tự động được phơi bày dưới dạng REST APIs
- **Event Brokers**: Có thể tích hợp với RabbitMQ, Apache Kafka bằng cách thêm Spring Cloud Stream
- **Serverless**: Có thể được đóng gói cho AWS Lambda và các môi trường serverless khác

### 2. Các Phương Pháp Phát Triển
- Phương pháp Reactive (Phản ứng)
- Phương pháp Imperative (Mệnh lệnh)
- Phương pháp Hybrid (Kết hợp)

### 3. Các Hàm POJO Đơn Giản
- Logic nghiệp vụ được triển khai với các hàm POJO đơn giản
- Nhiều hàm có thể được kết hợp để đạt được đầu ra mong muốn

### 4. Tùy Chọn Triển Khai Đa Dạng
- HTTP endpoints với REST services
- Stream dữ liệu bằng cách tích hợp với Apache Kafka hoặc RabbitMQ sử dụng Spring Cloud Stream
- Triển khai standalone cho các môi trường mục tiêu như AWS Lambda

### 5. Độc Lập với Cơ Sở Hạ Tầng
Logic nghiệp vụ tương tự được viết bằng functions có thể được sử dụng như:
- REST APIs
- Ứng dụng streaming dữ liệu
- Triển khai serverless

## Tại Sao Chọn Spring Cloud Function Thay Vì REST APIs Truyền Thống?

Khi xây dựng với REST APIs truyền thống, bạn chỉ giới hạn ở các tình huống mà REST được hỗ trợ. Spring Cloud Function cung cấp:

- **Linh hoạt**: Dễ dàng di chuyển giữa các công nghệ với cấu hình tối thiểu
- **Tách rời**: Chu kỳ phát triển của logic nghiệp vụ được tách rời khỏi các runtime targets cụ thể
- **Khả năng thích ứng**: Khi yêu cầu về cơ sở hạ tầng thay đổi, chỉ cần thay đổi tối thiểu
- **Tập trung**: Các nhà phát triển tập trung vào logic nghiệp vụ; cơ sở hạ tầng được xử lý thông qua cấu hình trong `application.yml`

## Trường Hợp Sử Dụng Tốt Nhất: Kiến Trúc Hướng Sự Kiện

Spring Cloud Function phù hợp nhất cho kiến trúc hướng sự kiện vì:
- Functions cung cấp tính linh hoạt để triển khai logic nghiệp vụ ở bất cứ đâu
- Dễ dàng di chuyển giữa các công nghệ
- Yêu cầu thay đổi cấu hình tối thiểu
- Cùng một code có thể chạy như web endpoint, stream processor, hoặc task

## Hỗ Trợ Nền Tảng

Spring Cloud Function hỗ trợ tích hợp với các nhà cung cấp cloud lớn:
- **AWS Lambda**
- **Microsoft Azure Functions**
- **Google Cloud Functions**
- **Apache OpenWhisk**

## Các Tùy Chọn Triển Khai

1. **Ứng dụng Web Standalone**: Triển khai như ứng dụng web truyền thống
2. **Ứng dụng Streaming Standalone**: Triển khai cho xử lý streaming dữ liệu
3. **Packaged Function**: Đóng gói và triển khai lên nhiều nền tảng khác nhau
4. **Nền tảng Serverless**: Triển khai lên AWS Lambda, Azure, Google Cloud Functions

## Mục Tiêu Triển Khai

Spring Cloud Function thúc đẩy và triển khai:
- Logic nghiệp vụ thông qua functions
- Tách rời chu kỳ phát triển khỏi các runtime targets cụ thể
- Cùng một code chạy như:
  - Web endpoints (REST APIs)
  - Stream processors
  - Tasks
  - Ứng dụng standalone (local hoặc môi trường PaaS)

## Các Bước Tiếp Theo

Trong các bài giảng sắp tới, chúng ta sẽ xây dựng message microservice của mình bằng cách tận dụng Spring Cloud Function, minh họa cách triển khai microservices hướng sự kiện bằng framework mạnh mẽ này.

---

*Phương pháp này đảm bảo các microservices của chúng ta linh hoạt, dễ bảo trì và sẵn sàng cho kiến trúc cloud-native hiện đại.*




FILE: 21-creating-message-microservice-with-spring-cloud-functions.md


# Tạo Message Microservice với Spring Cloud Functions

## Tổng quan
Hướng dẫn này sẽ giúp bạn tạo một message microservice sử dụng Spring Cloud Functions. Microservice này sẽ xử lý chức năng nhắn tin cho ứng dụng EazyBank, cho phép giao tiếp qua email và SMS.

## Yêu cầu tiên quyết
- Java 17
- Maven
- Spring Boot 3.1.2 (hoặc phiên bản ổn định mới nhất)
- IntelliJ IDEA

## Bước 1: Tạo khung dự án

### Sử dụng Spring Initializr
1. Truy cập vào [start.spring.io](https://start.spring.io)
2. Cấu hình dự án với các thiết lập sau:
   - **Project**: Maven
   - **Language**: Java
   - **Spring Boot Version**: 3.1.2 (hoặc phiên bản ổn định hiện tại)
   
### Metadata dự án
- **Group**: `com.easybytes`
- **Artifact**: `message`
- **Name**: `message`
- **Description**: Microservice hỗ trợ messaging trong EazyBank
- **Package Name**: `com.easybytes.message` (tự động điền)
- **Packaging**: JAR
- **Java Version**: 17

## Bước 2: Thêm Dependencies

### Spring Cloud Function Dependency
Tìm kiếm "function" trong phần dependencies và thêm **Spring Cloud Function**.

**Spring Cloud Function là gì?**
- Hỗ trợ triển khai business logic thông qua functions
- Hỗ trợ mô hình lập trình thống nhất trên các nhà cung cấp serverless
- Khả năng chạy độc lập (standalone), local hoặc trên PaaS
- Triết lý viết một lần, triển khai mọi nơi

### Dependencies được bao gồm
Khi bạn click "Explore", bạn sẽ thấy:
- `spring-boot-starter`
- `spring-cloud-function-context` (dependency quan trọng)
- Các dependencies cho testing

### Tải xuống dự án
Click nút "Download" để tải xuống Maven project có tên "message".

## Bước 3: Thiết lập Workspace

### Tổ chức cấu trúc dự án
1. Tạo một thư mục mới cho phần phát triển Section 13
2. Sao chép thư mục Section 12 (chứa code phần trước)
3. Đổi tên thành `section13`
4. Xóa thư mục `.idea`
5. Giải nén và dán dự án message đã tải xuống vào section13

### Mở trong IntelliJ IDEA
1. Click nút **Open**
2. Điều hướng đến: `storage/workspaces/microservices/section13`
3. Click **Open**
4. Load tất cả các Maven projects

## Bước 4: Tạo DTO Package và Record Class

### Tạo DTO Package
Điều hướng đến thư mục source của messages microservice và tạo:
```
com.eazybytes.message.dto
```

Package này sẽ chứa các class để nhận messages từ message broker.

### Tạo AccountsMessageDto Record

**Tại sao sử dụng Record?**
Java records cung cấp:
- Tự động tạo getter
- Các trường bất biến (final mặc định)
- Cú pháp ngắn gọn
- Đảm bảo an toàn luồng (thread-safe) cho data carriers

**Định nghĩa Record:**
Tạo record `AccountsMessageDto` với các trường sau:
- `accountNumber` - Số tài khoản khách hàng
- `name` - Tên khách hàng
- `email` - Địa chỉ email (để gửi email)
- `mobileNumber` - Số điện thoại (để gửi SMS)

**Luồng dữ liệu:**
Accounts microservice gửi messages đến message broker theo định dạng DTO này, message service sẽ nhận và xử lý.

**Best Practice:**
Thêm Javadoc comments để giải quyết warnings và tài liệu hóa code đúng cách.

## Bước 5: Tạo Functions Package

### Tạo Functions Package
Tạo một package mới trong `com.eazybytes.message`:
```
com.eazybytes.message.functions
```

Package này sẽ chứa tất cả các functions cần thiết cho business logic.

### Tạo MessageFunctions Class
1. Tạo một class mới: `MessageFunctions`
2. Thêm annotation `@Configuration` lên trên class
3. Class này sẽ xử lý tất cả các thao tác messaging đến người dùng cuối

## Bước 6: Triển khai Business Logic

Trong bài giảng tiếp theo, chúng ta sẽ tiếp tục triển khai business logic sử dụng Spring Cloud Functions.

## Các khái niệm chính

### Lợi ích của Spring Cloud Function
- **Sẵn sàng Serverless**: Triển khai lên AWS Lambda, Azure Functions, Google Cloud Functions
- **Độc lập nền tảng**: Cùng một đoạn code hoạt động trên nhiều cloud providers khác nhau
- **Chạy độc lập**: Có thể chạy như một ứng dụng Spring Boot thông thường
- **Triển khai linh hoạt**: Phát triển local, PaaS, hoặc serverless

### Mục đích của Message Microservice
- Xử lý giao tiếp với khách hàng
- Gửi thông báo qua email
- Gửi thông báo qua SMS
- Xử lý messages từ accounts microservice thông qua message broker

## Tóm tắt
Trong hướng dẫn này, chúng ta đã:
1. Tạo dự án Spring Boot với Spring Cloud Function dependency
2. Thiết lập workspace và cấu trúc dự án
3. Tạo DTO record class để nhận messages
4. Chuẩn bị functions package cho việc triển khai business logic

## Các bước tiếp theo
- Triển khai business logic dựa trên functions
- Cấu hình tích hợp message broker
- Thiết lập khả năng gửi email và SMS
- Kiểm thử message microservice

---

**Lưu ý**: Đây là phần thiết lập nền tảng. Việc triển khai thực tế các messaging functions sẽ được đề cập trong các bài giảng tiếp theo.




FILE: 22-spring-cloud-functions-business-logic-implementation.md


# Triển Khai Logic Nghiệp Vụ với Spring Cloud Functions

## Tổng Quan

Hướng dẫn này trình bày cách định nghĩa logic nghiệp vụ sử dụng Spring Cloud Functions trong kiến trúc microservices. Chúng ta sẽ tạo một class `MessageFunctions` xử lý thông báo email và SMS sử dụng các khái niệm lập trình hàm (functional programming).

## Yêu Cầu Tiên Quyết

- Hiểu về Lambda Expressions trong Java 8
- Quen thuộc với Functional Interfaces
- Kiến thức cơ bản về Spring Cloud Functions
- Hiểu về các mẫu giao tiếp bất đồng bộ (asynchronous communication)

## Tạo Class MessageFunctions

### Thiết Lập Logger

Đầu tiên, tạo một class có tên `MessageFunctions` với biến logger để theo dõi việc thực thi function:

```java
public class MessageFunctions {
    private static final Logger log = LoggerFactory.getLogger(MessageFunctions.class);
    
    // Các functions cho logic nghiệp vụ sẽ được định nghĩa tại đây
}
```

## Hiểu Về Function Interface

Interface `Function` từ Java Core Library (`java.util.function`) chấp nhận hai tham số kiểu:
- **T**: Kiểu đầu vào (Input)
- **R**: Kiểu trả về (Output)

Interface này được đánh dấu với annotation `@FunctionalInterface`, nghĩa là nó yêu cầu một lambda expression chấp nhận đầu vào và trả về đầu ra.

## Triển Khai Email Function

### Định Nghĩa Function

Tạo một email function xử lý thông điệp tài khoản:

```java
@Bean
public Function<AccountsMessageDto, AccountsMessageDto> email() {
    return accountsMessageDto -> {
        log.info("Sending email with the details: {}", accountsMessageDto);
        return accountsMessageDto;
    };
}
```

### Các Điểm Chính:
- **Đầu vào**: `AccountsMessageDto` - Nhận thông điệp từ accounts microservice thông qua message broker
- **Đầu ra**: `AccountsMessageDto` - Trả về cùng một object để thực hiện function composition
- **Annotation @Bean**: Đảm bảo Spring Cloud Functions giám sát function này
- **Logic Nghiệp Vụ**: Ghi log thao tác gửi email (việc triển khai gửi email thực tế được bỏ qua để tập trung vào các khái niệm Spring Cloud)

## Triển Khai SMS Function

### Định Nghĩa Function

Tạo một SMS function cũng xử lý thông điệp tài khoản:

```java
@Bean
public Function<AccountsMessageDto, Long> sms() {
    return accountsMessageDto -> {
        log.info("Sending SMS with the details: {}", accountsMessageDto);
        return accountsMessageDto.accountNumber();
    };
}
```

### Các Điểm Chính:
- **Đầu vào**: `AccountsMessageDto` - Nhận dữ liệu từ email function đã được kết hợp
- **Đầu ra**: `Long` - Trả về số tài khoản để thông báo cho accounts microservice
- **Getters của Record Class**: Vì `AccountsMessageDto` là một record class, các phương thức getter không có tiền tố "get". Sử dụng `accountNumber()` trực tiếp thay vì `getAccountNumber()`

## Chiến Lược Function Composition

### Tại Sao Kết Hợp Các Functions?

Kiến trúc triển khai function composition để tạo một pipeline xử lý logic:

1. **Accounts Microservice** → Gửi thông điệp đến message broker
2. **Message Broker** → Gọi function `email`
3. **Email Function** → Xử lý và chuyển tiếp đến function `sms`
4. **SMS Function** → Gửi xác nhận trở lại accounts microservice

### Luồng Dữ Liệu:

```
AccountsMessageDto → [Email Function] → AccountsMessageDto → [SMS Function] → Long (accountNumber)
```

### Tại Sao Trả Về AccountsMessageDto Từ Email Function?

Email function trả về cùng object `AccountsMessageDto` vì:
- SMS function cần tất cả thông tin từ thông điệp gốc
- Function composition yêu cầu các kiểu output/input khớp nhau giữa các functions được kết nối
- Điều này cho phép luồng dữ liệu mượt mà qua pipeline xử lý

### Tại Sao Trả Về Long Từ SMS Function?

SMS function trả về số tài khoản vì:
- Nó báo hiệu việc hoàn thành quy trình thông báo
- Accounts microservice có thể sử dụng điều này để cập nhật database
- Một cột mới có thể theo dõi xem việc giao tiếp đã được gửi thành công hay chưa
- Cho phép xác nhận bất đồng bộ về việc gửi thông điệp

## Các Functional Interfaces Khác

Spring Cloud Functions hỗ trợ thêm các functional interfaces từ `java.util.function`:

### Supplier Interface

```java
@FunctionalInterface
public interface Supplier<T> {
    T get();
}
```

**Trường Hợp Sử Dụng**: Khi bạn cần tạo output mà không cần chấp nhận bất kỳ input nào

### Consumer Interface

```java
@FunctionalInterface
public interface Consumer<T> {
    void accept(T t);
}
```

**Trường Hợp Sử Dụng**: Khi bạn cần chấp nhận input mà không trả về bất kỳ output nào

## Tóm Tắt

Trong triển khai này, chúng ta đã tạo:
1. **Email Function**: Chấp nhận `AccountsMessageDto`, ghi log chi tiết email, trả về `AccountsMessageDto`
2. **SMS Function**: Chấp nhận `AccountsMessageDto`, ghi log chi tiết SMS, trả về `Long` (số tài khoản)
3. **Function Composition**: Email và SMS functions hoạt động như một đơn vị logic duy nhất
4. **Giao Tiếp Bất Đồng Bộ**: Các functions giao tiếp qua message broker cho kiến trúc tách rời

## Các Bước Tiếp Theo

- Kiểm thử các functions với message broker (RabbitMQ)
- Cấu hình Spring Cloud Stream bindings
- Triển khai function composition trong application properties
- Thêm cột database để theo dõi trạng thái giao tiếp

## Những Điểm Chính Cần Nhớ

- Spring Cloud Functions tận dụng các functional interfaces của Java 8
- Các functions có thể được kết hợp để tạo các pipeline xử lý phức tạp
- Annotation `@Bean` là bắt buộc để Spring Cloud Functions giám sát các functions của bạn
- Function composition yêu cầu xem xét cẩn thận các kiểu input/output
- Các functional interfaces khác nhau (Function, Supplier, Consumer) phục vụ các trường hợp sử dụng khác nhau

---

**Lưu Ý**: Triển khai này tập trung vào các khái niệm Spring Cloud Functions. Logic gửi email/SMS thực tế nên được triển khai dựa trên yêu cầu cụ thể và các nhà cung cấp dịch vụ của bạn.




FILE: 23-spring-cloud-functions-rest-api-guide.md


# Spring Cloud Functions: Hướng Dẫn Triển Khai REST API

## Tổng Quan

Hướng dẫn này trình bày sức mạnh và tính linh hoạt của Spring Cloud Functions trong việc xây dựng microservices hướng sự kiện. Bạn sẽ học cách viết logic nghiệp vụ dưới dạng các hàm và công khai chúng theo nhiều cách - REST APIs, xử lý sự kiện, hoặc serverless functions.

## Hiểu Về Spring Cloud Functions

Spring Cloud Functions cho phép lập trình viên viết logic nghiệp vụ dưới dạng các hàm đơn giản mà không cần lo lắng về cơ sở hạ tầng bên dưới. Các hàm này có thể:

- Được công khai như REST APIs
- Tích hợp với event brokers (RabbitMQ, Kafka)
- Triển khai lên các nền tảng serverless (AWS Lambda)

## Thêm Hỗ Trợ REST API

Để công khai các hàm của bạn thành REST APIs, thêm dependency sau vào `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-function-web</artifactId>
</dependency>
```

Thay thế dependency `spring-cloud-function-context` bằng `spring-cloud-starter-function-web`.

## Các Bước Triển Khai

### 1. Cấu Hình Maven

Sau khi thêm dependency:
1. Reload các thay đổi Maven
2. Build project
3. Khởi động ứng dụng ở chế độ debug

Ứng dụng sẽ khởi động trên cổng mặc định 8080.

### 2. Tự Động Công Khai Hàm

Khi ứng dụng khởi động, Spring Cloud Functions tự động:
- Nhận diện tất cả các function beans
- Công khai chúng thành REST endpoints
- Ánh xạ tên hàm thành đường dẫn API

### 3. Kiểm Thử Các Hàm Riêng Lẻ

#### Hàm Email

**Endpoint:** `POST http://localhost:8080/email`

**Request Body:**
```json
{
    "accountNumber": "1234567890",
    "name": "Nguyễn Văn A",
    "email": "nguyen@example.com",
    "mobileNumber": "0123456789"
}
```

Hàm nhận đối tượng `AccountsMsgDto` và xử lý gửi email.

**Response:** Trả về cùng đối tượng `AccountsMsgDto` đã gửi trong request.

**Console Output:** "Sending email with the details..."

#### Hàm SMS

**Endpoint:** `POST http://localhost:8080/sms`

**Request Body:**
```json
{
    "accountNumber": "1234567890",
    "name": "Nguyễn Văn A",
    "email": "nguyen@example.com",
    "mobileNumber": "0123456789"
}
```

Hàm SMS trả về số tài khoản (kiểu Long) làm kết quả đầu ra.

**Response:** Chỉ trả về giá trị số tài khoản.

**Console Output:** "Sending SMS with the details..."

## Kết Hợp Các Hàm (Function Composition)

### Cấu Hình

Tạo hoặc sửa file `application.yml`:

```yaml
server:
  port: 9010

spring:
  application:
    name: message
  cloud:
    function:
      definition: email|sms
```

### Các Điểm Cấu Hình Chính

- **Cấu Hình Cổng:** Đặt là 9010 để tránh xung đột với accounts microservice (cổng 8080)
- **Tên Ứng Dụng:** "message" - dùng để nhận diện service
- **Function Definition:** Sử dụng ký tự pipe `|` để kết hợp nhiều hàm thành một đơn vị logic duy nhất

### Cách Hoạt Động Của Function Composition

Ký tự pipe (`|`) cho phép bạn kết hợp bất kỳ số lượng hàm nào:
- Các hàm thực thi tuần tự
- Đầu ra của hàm này trở thành đầu vào cho hàm tiếp theo
- Tên endpoint kết hợp được tạo bằng cách nối các tên hàm

### Endpoint Hàm Kết Hợp

**Endpoint:** `POST http://localhost:9010/emailsms`

Khi gọi hàm kết hợp:
1. Gửi request theo định dạng mà hàm đầu tiên (email) yêu cầu
2. Cả hai hàm thực thi như một đơn vị logic duy nhất
3. Hàm email xử lý trước, sau đó đến hàm SMS
4. Kết quả cuối cùng là đầu ra từ hàm cuối cùng trong chuỗi (số tài khoản)

**Request Mẫu:**
```json
{
    "accountNumber": "1234567890",
    "name": "Nguyễn Văn A",
    "email": "nguyen@example.com",
    "mobileNumber": "0123456789"
}
```

**Kết Quả Mẫu:**
- Console logs: "Sending email..." theo sau là "Sending SMS..."
- Response: Số tài khoản (từ đầu ra của hàm SMS)

### Kiểm Thử Hàm Kết Hợp

1. Xóa console để thấy logs mới
2. Gọi endpoint `emailsms`
3. Quan sát cả hai log statements xuất hiện
4. Nhận số tài khoản trong response

Điều này xác nhận cả hai hàm đã thực thi như một đơn vị logic duy nhất.

## Lợi Ích Chính

1. **Không Cần Phát Triển REST API Thủ Công:** Các hàm tự động trở thành REST endpoints chỉ bằng cách thêm một dependency
2. **Tính Linh Hoạt:** Cùng một hàm có thể hoạt động như REST APIs, event handlers, hoặc serverless functions
3. **Dễ Dàng Kết Hợp:** Kết hợp nhiều hàm bằng ký tự pipe mà không cần code thêm
4. **Tùy Chọn Triển Khai:** Triển khai lên nhiều nền tảng khác nhau mà không cần thay đổi code

## Gọi Riêng Lẻ vs Kết Hợp

### Các Hàm Riêng Lẻ
- Ứng dụng client có thể gọi các hàm cụ thể một cách độc lập
- Dùng endpoint `email` cho giao tiếp chỉ qua email
- Dùng endpoint `sms` cho giao tiếp chỉ qua SMS
- Mỗi endpoint vẫn khả dụng ngay cả khi đã cấu hình function composition

### Các Hàm Kết Hợp
- Gọi nhiều hàm như một đơn vị logic duy nhất
- Dùng tên endpoint kết hợp (`emailsms`) để kích hoạt cả hai phương thức giao tiếp
- Các hàm thực thi tuần tự như đã định nghĩa trong cấu hình
- Không ảnh hưởng đến khả năng sử dụng các hàm riêng lẻ

## Điều Kỳ Diệu Của Spring Cloud Functions

**Không Cần REST Controller:** Bạn không cần viết bất kỳ REST controllers hoặc API endpoints thủ công. Chỉ cần:
1. Viết logic nghiệp vụ của bạn dưới dạng các hàm
2. Thêm dependency `spring-cloud-starter-function-web`
3. Các hàm tự động trở thành REST APIs

**Sức Mạnh:** Abstraction này cho phép bạn tập trung vào logic nghiệp vụ trong khi Spring Cloud Functions xử lý cơ sở hạ tầng.

## Bước Tiếp Theo: Tích Hợp Hướng Sự Kiện

Mặc dù REST APIs hữu ích cho việc demo, sức mạnh thực sự nằm ở việc tích hợp với event brokers:

1. **Tích Hợp Spring Cloud Stream:** Kết hợp Spring Cloud Functions với Spring Cloud Stream
2. **Tích Hợp RabbitMQ:** Kết nối các hàm với message brokers
3. **Kiến Trúc Hướng Sự Kiện:** Xây dựng microservices thực sự reactive

### Chuẩn Bị Cho Tích Hợp Event Broker

Để chuyển từ REST APIs sang kiến trúc hướng sự kiện:

1. Comment dependency `spring-cloud-starter-function-web`
2. Giữ lại các properties function definition (sẽ dùng với event brokers)
3. Các properties trong `application.yml` sẽ được tái sử dụng cho cấu hình event broker

```xml
<!-- Comment để chuyển sang phương pháp hướng sự kiện -->
<!--
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-function-web</artifactId>
</dependency>
-->
```

**Lưu ý:** Bạn không cần xóa các properties - chúng sẽ được tận dụng khi tích hợp với event brokers.

## Khoảnh Khắc "Wow"

Khi Spring Cloud Functions được tích hợp với Spring Cloud Stream và RabbitMQ, bạn sẽ trải nghiệm sức mạnh thực sự của kiến trúc này:
- Cùng một logic nghiệp vụ hoạt động trên nhiều cơ sở hạ tầng khác nhau
- Chuyển đổi giữa REST APIs, event brokers, hoặc serverless mà không cần thay đổi code
- Abstraction hoàn hảo cho các ứng dụng cloud-native hiện đại

## Kết Luận

Spring Cloud Functions cung cấp một abstraction mạnh mẽ để xây dựng logic nghiệp vụ với các đặc điểm:
- **Độc lập với cơ sở hạ tầng:** Hoạt động trên nhiều nền tảng khác nhau
- **Dễ dàng kiểm thử:** Các hàm đơn giản dễ dàng unit test
- **Linh hoạt trong triển khai:** Triển khai như REST APIs, event handlers, hoặc serverless
- **Hoàn hảo cho microservices hướng sự kiện:** Phù hợp tự nhiên với kiến trúc reactive

Sự kết hợp của Spring Cloud Functions với Spring Cloud Stream và RabbitMQ tạo ra nền tảng vững chắc cho kiến trúc microservices hiện đại.

## Những Điểm Chính Cần Nhớ

1. Viết logic nghiệp vụ dưới dạng các hàm đơn giản
2. Thêm một dependency để công khai như REST APIs
3. Kết hợp các hàm bằng ký tự pipe
4. Cùng một code hoạt động cho REST, events, hoặc serverless
5. Tập trung vào logic nghiệp vụ, không phải cơ sở hạ tầng

## Tài Liệu Tham Khảo

- Tài Liệu Spring Cloud Functions
- Spring Cloud Stream
- Tích Hợp RabbitMQ
- Các Mẫu Microservices Hướng Sự Kiện
- AWS Lambda với Spring Cloud Functions




FILE: 24-spring-cloud-stream-introduction.md


# Spring Cloud Stream: Xây Dựng Microservices Hướng Sự Kiện

## Tổng Quan

Spring Cloud Stream là một framework được thiết kế để tạo các ứng dụng có khả năng mở rộng, hướng sự kiện và streaming. Nó cung cấp một lớp trừu tượng cho phép các nhà phát triển tập trung vào logic nghiệp vụ trong khi framework xử lý các tác vụ liên quan đến cơ sở hạ tầng như tích hợp với các message broker như RabbitMQ hoặc Apache Kafka.

## Spring Cloud Stream Là Gì?

Spring Cloud Stream cho phép bạn chuyển đổi messaging microservice của mình thành một ứng dụng hướng sự kiện hoặc streaming. Mục đích chính của framework này là:

- Cho phép các nhà phát triển tập trung vào logic nghiệp vụ
- Xử lý các tác vụ cơ sở hạ tầng tự động
- Cung cấp tích hợp với các event broker khác nhau
- Mang lại trải nghiệm nhất quán cho nhà phát triển bất kể middleware nào được sử dụng

## Tích Hợp Với Spring Cloud Functions

Chúng ta biết rằng Spring Cloud Functions cho phép chúng ta:
- Xây dựng logic nghiệp vụ bên trong các function
- Expose các function dưới dạng REST APIs bằng cách thêm dependency vào `pom.xml`

Tuy nhiên, khi bạn cần tích hợp các function của mình với các event broker như RabbitMQ hoặc Apache Kafka, **Spring Cloud Stream** trở nên thiết yếu.

## Ưu Điểm Chính

### 1. Lớp Trừu Tượng
Spring Cloud Stream hoạt động như một lớp trừu tượng, cung cấp trải nghiệm nhất quán cho các nhà phát triển bất kể middleware nào được sử dụng đằng sau.

### 2. Chuyển Đổi Middleware Dễ Dàng
- Sử dụng RabbitMQ? Chỉ cần thêm dependency RabbitMQ vào `pom.xml`
- Chuyển sang Apache Kafka? Chỉ cần thay thế dependency và cập nhật một vài thuộc tính
- **Không cần thay đổi logic nghiệp vụ hoặc code Java**

### 3. Chuyển Đổi Liền Mạch
Việc chuyển đổi từ sản phẩm này sang sản phẩm khác (ví dụ: từ RabbitMQ sang Apache Kafka hoặc Google Pub/Sub) diễn ra liền mạch. Các nhà phát triển không cần:
- Xóa các interface và class đặc thù của middleware
- Học chi tiết về sản phẩm mới
- Viết lại logic nghiệp vụ

## Các Tích Hợp Được Hỗ Trợ

Spring Cloud Stream hỗ trợ nhiều tích hợp, bao gồm:

### Được Hỗ Trợ Trực Tiếp:
- RabbitMQ
- Apache Kafka
- Kafka Streams
- Amazon Kinesis

### Được Đối Tác Duy Trì:
- Google Pub/Sub
- Solace Pub/Sub
- Azure Event Hubs
- Apache RocketMQ
- AWS SQS
- AWS SNS
- Azure Service Bus

## Các Thành Phần Cốt Lõi

Spring Cloud Stream đạt được chức năng của mình thông qua ba thành phần quan trọng:

### 1. Destination Binders
- **Mục đích**: Cung cấp tích hợp thực tế với các hệ thống messaging bên ngoài
- **Chức năng**: Tích hợp microservice/ứng dụng của bạn với RabbitMQ, Apache Kafka, hoặc bất kỳ sản phẩm messaging nào khác

### 2. Destination Bindings
- **Mục đích**: Hoạt động như một cầu nối giữa hệ thống messaging bên ngoài và code ứng dụng
- **Các loại**:
  - **Output Destination Binding**: Được sử dụng khi kích hoạt sự kiện từ microservice của bạn (gửi message đến exchange)
  - **Input Destination Binding**: Chịu trách nhiệm đọc message từ queue

### 3. Message
- **Mục đích**: Định nghĩa cấu trúc dữ liệu được sử dụng bởi producer và consumer để giao tiếp với nhau
- **Ví dụ**: Trong message microservice, chấp nhận đầu vào ở định dạng account messages

## Luồng Kiến Trúc

```
Ứng Dụng Spring Boot
    ↓
Functions (Logic Nghiệp Vụ)
    ↓
Lớp Destination Bindings (Spring Cloud Stream)
    ↓
Destination Binders
    ↓
Message Broker (RabbitMQ/Kafka/v.v.)
```

### Ví Dụ Về Luồng Message:

**Luồng Output (Publish Sự Kiện):**
1. Code ứng dụng → Output Destination Binding
2. Output Destination Binding → Exchange
3. Exchange → Queue (dựa trên các quy tắc routing)

**Luồng Input (Consume Sự Kiện):**
1. Exchange → Queue
2. Queue → Input Destination Binding
3. Input Destination Binding → Functions (xử lý message)

## Trước và Sau Spring Cloud Stream

### Trước Spring Cloud Stream:
- Các nhà phát triển expose logic nghiệp vụ thông qua REST APIs sử dụng `@RestController`, `@GetMapping`, `@PostMapping`
- Thêm nhiều dependency đặc thù của RabbitMQ
- Sử dụng các class và interface đặc thù của RabbitMQ
- Chuyển sang Apache Kafka yêu cầu:
  - Xóa các interface và class liên quan đến RabbitMQ
  - Học các interface và class đặc thù của Apache Kafka
  - Refactor code đáng kể

### Sau Spring Cloud Stream:
- Viết logic nghiệp vụ trong các function
- Thêm một dependency duy nhất trong `pom.xml`
- Thay đổi một vài thuộc tính
- Chuyển đổi liền mạch giữa các hệ thống messaging khác nhau
- **Không cần thay đổi logic nghiệp vụ**

## Bắt Đầu

Để triển khai Spring Cloud Stream:

1. Tạo một ứng dụng Spring Boot
2. Định nghĩa các business function của bạn
3. Thêm dependency Spring Cloud Stream
4. Thêm dependency binder cụ thể (RabbitMQ, Kafka, v.v.)
5. Cấu hình các thuộc tính cho hệ thống messaging của bạn
6. Framework sẽ xử lý phần còn lại!

## Tóm Tắt Lợi Ích

- **Phát Triển Đơn Giản Hóa**: Tập trung vào logic nghiệp vụ, không phải cơ sở hạ tầng
- **Linh Hoạt**: Dễ dàng chuyển đổi giữa các hệ thống messaging
- **Khả Năng Mở Rộng**: Xây dựng microservices hướng sự kiện có khả năng mở rộng cao
- **Nhất Quán**: Cùng một trải nghiệm nhà phát triển trên các middleware khác nhau
- **Giảm Đường Cong Học Tập**: Không cần học sâu về các API đặc thù của middleware

## Tài Nguyên

Để biết thêm thông tin, truy cập [tài liệu chính thức của Spring Cloud Stream](https://spring.io/projects/spring-cloud-stream).

---

Spring Cloud Stream làm cho việc xây dựng microservices hướng sự kiện trở nên đơn giản và dễ bảo trì, cho phép các team tập trung vào việc cung cấp giá trị kinh doanh thay vì quản lý độ phức tạp của cơ sở hạ tầng.




FILE: 25-integrating-spring-cloud-stream-with-rabbitmq.md


# Tích hợp Spring Cloud Stream với RabbitMQ trong Microservices

## Tổng quan

Hướng dẫn này trình bày cách tích hợp Spring Cloud Stream với RabbitMQ để kích hoạt giao tiếp theo mô hình sự kiện giữa các microservices. Chúng ta sẽ cấu hình hai microservices:
- **Message Microservice**: Nhận và xử lý tin nhắn từ RabbitMQ
- **Accounts Microservice**: Gửi tin nhắn đến RabbitMQ khi tài khoản mới được tạo

## Yêu cầu

- Microservices Spring Boot
- RabbitMQ message broker
- Hiểu biết cơ bản về kiến trúc hướng sự kiện

## Bước 1: Cấu hình Message Microservice

### 1.1 Cập nhật Dependencies

Đầu tiên, dừng message microservice đang chạy và cập nhật file `pom.xml`.

**Xóa dependency cũ:**
```xml
<!-- Xóa spring-cloud-function-context -->
```

**Thêm Spring Cloud Stream dependencies:**
```xml
<dependencies>
    <!-- Dependency chính của Spring Cloud Stream -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream</artifactId>
    </dependency>
    
    <!-- RabbitMQ binder cho Spring Cloud Stream -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream-binder-rabbit</artifactId>
    </dependency>
    
    <!-- Dependencies cho testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream-test-binder</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Lưu ý:** Spring Cloud Stream đã bao gồm các dependencies của Spring Cloud Function, nên chúng ta không cần thêm riêng.

### 1.2 Thêm Google Jib Plugin

Thêm Google Jib plugin để tạo Docker images:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>com.google.cloud.tools</groupId>
            <artifactId>jib-maven-plugin</artifactId>
            <configuration>
                <to>
                    <image>eazybytes/${project.artifactId}:S13</image>
                </to>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 1.3 Cấu hình application.yml

Thêm các thuộc tính sau vào `application.yml`:

```yaml
spring:
  cloud:
    function:
      definition: emailsms
    stream:
      bindings:
        emailsms-in-0:
          destination: send-communication
          group: ${spring.application.name}
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    connection-timeout: 10s
```

**Giải thích cấu hình:**

- **Tên Binding (`emailsms-in-0`)**: Quy ước đặt tên mặc định của Spring Cloud Stream
  - `emailsms`: Tên function
  - `in`: Input binding (đầu vào)
  - `0`: Chỉ số bắt đầu
  
- **Destination**: Tên queue trong RabbitMQ (`send-communication`)
  - Input bindings kết nối với **queues**
  - Function sẽ tiêu thụ tin nhắn từ queue này

- **Group**: Sử dụng tên application để tránh tên queue được tạo ngẫu nhiên

- **RabbitMQ Connection**: Chi tiết kết nối chuẩn cho RabbitMQ local

## Bước 2: Cấu hình Accounts Microservice

### 2.1 Cập nhật Dependencies

Mở `pom.xml` trong accounts microservice và thêm:

```xml
<dependencies>
    <!-- Spring Cloud Stream -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream</artifactId>
    </dependency>
    
    <!-- RabbitMQ Binder -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-stream-binder-rabbit</artifactId>
    </dependency>
</dependencies>
```

Cập nhật tag Docker image trong cấu hình Jib plugin:
```xml
<image>eazybytes/${project.artifactId}:S13</image>
```

### 2.2 Tạo AccountsMessageDto Record Class

Tạo record class mới trong package `dto`:

```java
package com.eazybank.accounts.dto;

public record AccountsMessageDto(
    Long accountNumber,
    String name,
    String email,
    String mobileNumber
) {}
```

### 2.3 Cấu hình application.yml

Thêm các thuộc tính sau:

```yaml
spring:
  cloud:
    stream:
      bindings:
        sendCommunication-out-0:
          destination: send-communication
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    connection-timeout: 10s
```

**Giải thích cấu hình:**

- **Tên Binding (`sendCommunication-out-0`)**: 
  - `sendCommunication`: Tên binding tùy chỉnh
  - `out`: Output binding (đầu ra)
  - `0`: Chỉ số

- **Destination**: Tên exchange trong RabbitMQ (`send-communication`)
  - Output bindings kết nối với **exchanges**
  - Tin nhắn gửi đến binding này sẽ được publish lên exchange

### 2.4 Triển khai Logic Gửi Tin nhắn

Cập nhật class `AccountServiceImpl`:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.stream.function.StreamBridge;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class AccountServiceImpl implements IAccountService {
    
    private static final Logger log = LoggerFactory.getLogger(AccountServiceImpl.class);
    
    private AccountRepository accountRepository;
    private CustomerRepository customerRepository;
    private StreamBridge streamBridge;
    
    @Override
    public void createAccount(CustomerDto customerDto) {
        Customer customer = CustomerMapper.mapToCustomer(customerDto, new Customer());
        Customer savedCustomer = customerRepository.save(customer);
        
        Account account = createNewAccount(savedCustomer);
        Account savedAccount = accountRepository.save(account);
        
        // Gửi tin nhắn thông báo
        sendCommunication(savedAccount, savedCustomer);
    }
    
    private void sendCommunication(Account account, Customer customer) {
        AccountsMessageDto accountsMessageDto = new AccountsMessageDto(
            account.getAccountNumber(),
            customer.getName(),
            customer.getEmail(),
            customer.getMobileNumber()
        );
        
        log.info("Đang gửi yêu cầu thông báo cho chi tiết: {}", accountsMessageDto);
        
        boolean result = streamBridge.send("sendCommunication-out-0", accountsMessageDto);
        
        log.info("Yêu cầu thông báo có được xử lý thành công không?: {}", result);
    }
}
```

**Chi tiết triển khai:**

1. **StreamBridge**: Bean được inject từ Spring Cloud Stream để gửi tin nhắn
2. **Phương thức send()**: 
   - Tham số đầu: Tên output binding (`sendCommunication-out-0`)
   - Tham số thứ hai: Object tin nhắn (`AccountsMessageDto`)
3. **Giá trị trả về**: Boolean cho biết tin nhắn có được gửi thành công đến RabbitMQ
4. **Logging**: Theo dõi quá trình gửi tin nhắn để debug

## Kiến trúc Luồng Tin nhắn

```
Accounts Microservice
    |
    | (tạo tài khoản)
    v
Phương thức sendCommunication()
    |
    | (StreamBridge.send())
    v
RabbitMQ Exchange (send-communication)
    |
    | (định tuyến tin nhắn)
    v
RabbitMQ Queue (send-communication)
    |
    | (tiêu thụ tin nhắn)
    v
Message Microservice (hàm emailsms)
```

## Khái niệm chính

### Input vs Output Bindings

- **Input Bindings** (`-in-`): 
  - Tiêu thụ tin nhắn từ **queues**
  - Sử dụng trong message microservice
  - Kết nối functions với nguồn tin nhắn

- **Output Bindings** (`-out-`): 
  - Publish tin nhắn lên **exchanges**
  - Sử dụng trong accounts microservice
  - Gửi tin nhắn đến RabbitMQ

### Ánh xạ Destination

- **Queue Destination**: Sử dụng với input bindings (consumers)
- **Exchange Destination**: Sử dụng với output bindings (producers)

### Thuộc tính Group

- Đảm bảo đặt tên queue nhất quán
- Ngăn RabbitMQ thêm giá trị ngẫu nhiên vào tên queue
- Sử dụng tên application để tổ chức

## Kiểm thử Tích hợp

1. **Khởi động RabbitMQ**: Đảm bảo RabbitMQ đang chạy trên `localhost:5672`
2. **Khởi động Message Microservice**: Sẽ tạo queue và bắt đầu tiêu thụ
3. **Khởi động Accounts Microservice**: Sẵn sàng gửi tin nhắn
4. **Tạo Tài khoản Mới**: Kích hoạt tạo tài khoản qua REST API
5. **Xác minh**: Kiểm tra console RabbitMQ để theo dõi luồng tin nhắn và logs để xử lý

## Tổng kết

Chúng ta đã tích hợp thành công Spring Cloud Stream với RabbitMQ trong microservices:

- ✅ Đã thêm Spring Cloud Stream và RabbitMQ binder dependencies
- ✅ Đã cấu hình input bindings trong message microservice (consumer)
- ✅ Đã cấu hình output bindings trong accounts microservice (producer)
- ✅ Đã triển khai logic gửi tin nhắn với StreamBridge
- ✅ Đã thiết lập thuộc tính kết nối RabbitMQ
- ✅ Đã tạo giao tiếp hướng sự kiện giữa các microservices

Các microservices hiện đã sẵn sàng cho giao tiếp hướng sự kiện thông qua RabbitMQ!




FILE: 26-event-driven-microservices-rabbitmq-demo.md


# Microservices Hướng Sự Kiện với RabbitMQ - Hướng Dẫn Demo

## Tổng Quan

Hướng dẫn này trình bày cách triển khai giao tiếp bất đồng bộ giữa các microservices sử dụng RabbitMQ làm message broker. Chúng ta sẽ kích hoạt các sự kiện từ Accounts microservice đến Message microservice bằng framework Spring Cloud Stream.

## Yêu Cầu Tiên Quyết

- Docker Desktop chạy trên hệ thống local
- RabbitMQ Docker container
- Spring Boot microservices với Spring Cloud Stream
- Keycloak Authorization Server
- Postman để test API

## Các Thành Phần Kiến Trúc

### Microservices
- **Config Server**: Quản lý cấu hình tập trung
- **Eureka Server**: Service discovery và registration
- **Accounts Microservice**: Xử lý các thao tác tài khoản và phát hành events
- **Message Microservice**: Tiêu thụ events và gửi thông báo email/SMS
- **Gateway Server**: Hoạt động như OAuth2 resource server với Spring Security

### Hạ Tầng
- **RabbitMQ**: Message broker cho giao tiếp bất đồng bộ
- **Keycloak**: OAuth2 authorization server
- **Docker**: Container runtime

## Thiết Lập Demo Từng Bước

### 1. Khởi Động RabbitMQ

Đầu tiên, khởi động RabbitMQ bằng Docker:

```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:management
```

**Tham số:**
- `-d`: Chạy ở chế độ detached (chạy nền)
- `-p 5672:5672`: Cổng giao thức AMQP
- `-p 15672:15672`: Cổng giao diện quản lý

**Xác Minh:**
- Kiểm tra Docker Desktop để thấy RabbitMQ container đang chạy
- Truy cập RabbitMQ console tại: `http://localhost:15672`
- Thông tin đăng nhập mặc định: `guest` / `guest`

### 2. Khởi Động Microservices

Khởi động các microservices theo thứ tự sau:

1. **Config Server**
   - Mở main class của Config Server
   - Chạy ở chế độ debug

2. **Eureka Server**
   - Khởi động sau khi Config Server đã hoạt động
   - Chạy ở chế độ debug

3. **Accounts Microservice**
   - Mở main class `AccountsApplication`
   - Chạy ở chế độ debug

4. **Message Microservice**
   - Mở main class `MessageApplication`
   - Chạy ở chế độ debug

5. **Gateway Server**
   - Khởi động như OAuth2 resource server
   - Được bảo mật bằng Spring Security

**Lưu ý:** Không cần khởi động Cards và Loans microservices cho demo này.

### 3. Khởi Động Keycloak

Khởi động container Keycloak đã tồn tại:

```bash
docker start <keycloak-container-name>
```

**Quan trọng:** Đừng xóa container Keycloak để giữ lại thông tin client, roles và người dùng. Chỉ dừng nó khi không cần thiết.

## Cấu Hình RabbitMQ Console

### Truy Cập Console

Truy cập `http://localhost:15672` và đăng nhập với:
- Username: `guest`
- Password: `guest`

### Các Thành Phần Chính

#### Exchanges
- **Tên**: `send-communication`
- **Nguồn**: Được định nghĩa trong `application.yml` của Accounts Microservice như là destination
- **Mục đích**: Định tuyến messages đến queue phù hợp

#### Queues
- **Tên**: `send-communication.message`
- **Binding**: Kết nối với exchange `send-communication`
- **Nguồn**: Được định nghĩa trong `application.yml` của Message Microservice

#### Cấu Hình Bindings

**Message Microservice (Input Binding):**
```yaml
spring:
  cloud:
    stream:
      bindings:
        input:
          destination: send-communication
          group: message
```

Tên queue được tạo bằng cách nối: `destination` + `.` + `group` = `send-communication.message`

#### Bindings Tự Động Tạo

Spring Cloud Stream tự động tạo output bindings dựa trên định nghĩa function:
- **Output Binding**: `emailsms-out-0`
- **Nguồn**: Composed function definition có tên `emailsms`
- **Trạng thái**: Chưa bind với queue nào (exchange rỗng)

## Kiểm Thử Triển Khai

### 1. Lấy Access Token

Sử dụng Keycloak để lấy OAuth2 token bằng Client Credentials flow:

1. Truy cập Keycloak Admin Console: `http://localhost:7080`
2. Đăng nhập với: `admin` / `admin`
3. Điều hướng đến: Clients → `EazyBankCallCenterCC`
4. Vào tab Credentials
5. Copy client secret

### 2. Kiểm Thử API với Postman

**Collection:** Gateway Security
**API:** `Accounts_POST_ClientCredentials`

**Các Bước:**
1. Cấu hình client credentials trong Postman
2. Lấy access token mới
3. Tạo tài khoản với số điện thoại test (ví dụ: kết thúc bằng 688)
4. Gửi POST request

**Kết Quả Mong Đợi:**
- HTTP Status: `201 Created`
- Response Time: ~51 milliseconds (ngay lập tức)
- Message được gửi thành công đến RabbitMQ

### 3. Giám Sát Luồng Xử Lý

#### Console Accounts Microservice
```
Sending communication request for the details...
Is the communication request successfully triggered: true
```

#### RabbitMQ Console
- Điều hướng đến Exchanges → `send-communication`
- Kiểm tra biểu đồ để thấy message spike
- Xác minh message đã nhận

#### Console Message Microservice
```
Sending email with the details...
Sending SMS with the details...
```

## Minh Họa Giao Tiếp Bất Đồng Bộ

### Demo Chế Độ Chậm

Để minh họa tính chất bất đồng bộ:

1. **Đặt Breakpoint**
   - Đặt breakpoint trong hàm email của Message Microservice
   - Đây là hàm đầu tiên được kích hoạt khi nhận message

2. **Tạo Tài Khoản Mới**
   - Sử dụng số điện thoại kết thúc bằng 687
   - Lấy access token mới
   - Gửi POST request

3. **Quan Sát Hành Vi**
   - Accounts microservice trả về response ngay lập tức (51ms)
   - Breakpoint của Message microservice bị kích hoạt nhưng chưa xử lý
   - **Điểm Chính**: Accounts microservice không đợi Message microservice

4. **Hiểu Về Luồng Xử Lý**
   - Accounts microservice đưa message vào RabbitMQ
   - Tiếp tục với logic business còn lại
   - Trả về response ngay lập tức
   - Message microservice xử lý độc lập

5. **Nhả Breakpoint**
   - Message microservice tiếp tục xử lý
   - Logs email và SMS xuất hiện
   - Xử lý diễn ra bất đồng bộ (có thể là 1 phút, 2 phút, hoặc thậm chí 1 ngày sau)

## Các Khái Niệm Chính

### Lợi Ích Giao Tiếp Bất Đồng Bộ

1. **Loose Coupling**: Accounts microservice không biết về Message microservice
2. **Xử Lý Độc Lập**: Mỗi service hoạt động theo tốc độ riêng
3. **Khả Năng Chịu Lỗi**: Nếu Message service bị down, Accounts service vẫn hoạt động
4. **Khả Năng Mở Rộng**: Các services có thể scale độc lập
5. **Hiệu Suất**: Response ngay lập tức cho client mà không đợi xử lý downstream

### Vai Trò Message Broker

RabbitMQ hoạt động như trung gian:
- Accounts microservice chỉ biết về message broker
- Message microservice chỉ biết về message broker
- Không có giao tiếp trực tiếp service-to-service
- Broker xử lý routing và delivery message

## Cải Tiến Tương Lai

### Giao Tiếp Bất Đồng Bộ Hai Chiều

Các bước tiếp theo bao gồm triển khai giao tiếp ngược:

1. Message microservice gửi thông báo trả lại cho Accounts microservice
2. Thông báo được gửi sau khi hoàn thành xử lý email/SMS
3. Accounts microservice cập nhật bản ghi của mình
4. Thời gian: Có thể ngay lập tức hoặc trễ (phút, giờ, hoặc ngày)

**Lợi ích:** Audit trail hoàn chỉnh và theo dõi trạng thái qua các services.

## Cập Nhật Code

### Cải Thiện Log Statement

**Ban đầu:**
```java
// Is the communication request successfully processed?
```

**Sau khi cập nhật:**
```java
// Is the communication request successfully triggered?
```

**Lý do:** Phản ánh chính xác hơn rằng chúng ta đang kích hoạt request, không phải đợi xử lý hoàn tất.

## Best Practices

1. **Quản Lý Container**: Đừng xóa containers có cấu hình (như Keycloak)
2. **Thứ Tự Khởi Động Service**: Tuân theo phân cấp dependency (Config → Eureka → Services)
3. **Quản Lý Token**: Refresh access tokens khi hết hạn
4. **Debug Mode**: Sử dụng để troubleshooting tốt hơn trong quá trình phát triển
5. **Đặt Tên Message**: Sử dụng tên rõ ràng, nhất quán cho exchanges và queues

## Xử Lý Sự Cố

### Các Vấn Đề Thường Gặp

1. **401 Unauthorized**: Token hết hạn, lấy access token mới
2. **Connection Refused**: Đảm bảo Docker và tất cả services đang chạy
3. **No Message Received**: Kiểm tra cấu hình RabbitMQ bindings
4. **Service Not Starting**: Xác minh các dependent services đang chạy

## Kết Luận

Demo này giới thiệu sức mạnh của kiến trúc microservices hướng sự kiện sử dụng RabbitMQ. Pattern giao tiếp bất đồng bộ cho phép:

- Hiệu suất cao với responses ngay lập tức
- Kiến trúc linh hoạt với loose coupling
- Các services có khả năng mở rộng hoạt động độc lập
- Message delivery đáng tin cậy thông qua message broker

Triển khai này minh họa các patterns microservices thực tế được sử dụng trong môi trường production.

---

**Các Bước Tiếp Theo:** Triển khai giao tiếp bất đồng bộ hai chiều cho kiến trúc event-driven hoàn chỉnh.




FILE: 27-event-streaming-from-message-to-accounts-microservice.md


# Truyền Sự Kiện từ Message Microservice sang Accounts Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai truyền sự kiện hai chiều giữa các microservices sử dụng Spring Cloud Stream và Spring Cloud Functions. Cụ thể, chúng ta sẽ cấu hình Message microservice để gửi sự kiện đến Accounts microservice.

## Tình Trạng Triển Khai Hiện Tại

Trước đây, chúng ta đã triển khai truyền sự kiện theo một chiều:
- Sự kiện chảy từ Accounts microservice → Message microservice (bước 1-4)

Bây giờ chúng ta cần hoàn thành luồng hai chiều:
- Sự kiện chảy từ Message microservice → Accounts microservice

## Các Bước Cấu Hình

### 1. Cấu Hình Output Binding trong Message Microservice

Trong file `application.yml` của Message microservice, thêm output binding tương tự input binding hiện có:

```yaml
spring:
  cloud:
    stream:
      bindings:
        emailsms-in-0:
          destination: send-communication.message
        emailsms-out-0:
          destination: communication-sent
```

**Các Điểm Chính:**
- Định dạng tên output binding: `{tên-function}-out-0`
- Tiền tố tên function: `emailsms` (khớp với định nghĩa Spring Cloud Function)
- Destination: `communication-sent` (hoạt động như tên exchange trong RabbitMQ)
- Hậu tố `-out-0` chỉ ra output binding với chỉ số bắt đầu từ 0

### 2. Hiểu Về Ưu Điểm Của Spring Cloud Functions

**Không Cần Gửi Message Thủ Công!**

Không giống như Accounts microservice nơi chúng ta sử dụng `StreamBridge`:
```java
streamBridge.send("outputBinding", message);
```

Với Spring Cloud Functions, framework tự động:
- Phát hiện kiểu trả về của function
- Gửi giá trị trả về như một message đến exchange đã cấu hình
- Sử dụng cấu trúc kết hợp function để xác định output binding

Function `sms` trả về `Long` (số tài khoản), được tự động gửi đến exchange `communication-sent`.

## 3. Tạo Consumer Function trong Accounts Microservice

### Bước 3.1: Tạo Package Functions và Class

Tạo package mới: `com.eazybytes.accounts.functions`

Tạo file `AccountsFunctions.java`:

```java
package com.eazybytes.accounts.functions;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.util.function.Consumer;

@Configuration
public class AccountsFunctions {
    
    private static final Logger log = LoggerFactory.getLogger(AccountsFunctions.class);
    
    @Bean
    public Consumer<Long> updateCommunication(IAccountService accountService) {
        return accountNumber -> {
            log.info("Đang cập nhật trạng thái giao tiếp cho số tài khoản: {}", accountNumber);
            accountService.updateCommunicationStatus(accountNumber);
        };
    }
}
```

**Tại Sao Sử Dụng Consumer Interface?**
- **Consumer**: Nhận đầu vào, không trả về gì (trường hợp của chúng ta)
- **Supplier**: Không có đầu vào, trả về đầu ra
- **Function**: Nhận đầu vào, trả về đầu ra

### Bước 3.2: Thêm Cột Database

Cập nhật file `schema.sql`:

```sql
CREATE TABLE accounts (
    -- các cột hiện có...
    branch_address VARCHAR(200) NOT NULL,
    communication_switch BOOLEAN,
    -- các cột khác...
);
```

### Bước 3.3: Cập Nhật Entity Class

Thêm vào entity `Accounts`:

```java
@Column(name = "communication_switch")
private Boolean communicationSwitch;
```

### Bước 3.4: Thêm Phương Thức Service

Trong interface `IAccountService`:

```java
Boolean updateCommunicationStatus(Long accountNumber);
```

Trong `AccountServiceImpl`:

```java
@Override
public Boolean updateCommunicationStatus(Long accountNumber) {
    boolean isUpdated = false;
    if (accountNumber != null) {
        Accounts accounts = accountsRepository.findById(accountNumber)
            .orElseThrow(() -> new ResourceNotFoundException("Account", "AccountNumber", accountNumber.toString()));
        accounts.setCommunicationSwitch(true);
        accountsRepository.save(accounts);
        isUpdated = true;
    }
    return isUpdated;
}
```

### Bước 3.5: Cấu Hình Application Properties

Trong file `application.yml` của Accounts microservice:

```yaml
spring:
  cloud:
    function:
      definition: updateCommunication
    stream:
      bindings:
        updateCommunication-in-0:
          destination: communication-sent
          group: accounts
```

**Các Lưu Ý Quan Trọng:**
- Định nghĩa function: `updateCommunication` (khớp với tên bean function)
- Đối với nhiều functions độc lập, phân tách bằng dấu chấm phẩy: `function1;function2`
- Định dạng input binding: `{tên-function}-in-0`
- Tên group ngăn việc tạo hậu tố ngẫu nhiên cho queue

## Kiến Trúc Luồng Message

```
Message Microservice
    ↓ (trả về Long accountNumber từ function sms)
    ↓
RabbitMQ Exchange: communication-sent
    ↓
RabbitMQ Queue: communication-sent.accounts
    ↓
Accounts Microservice (function updateCommunication)
    ↓
Cập nhật communication_switch = true trong database
```

## Các Khái Niệm Chính

### Ưu Điểm Của Spring Cloud Function

1. **Xử Lý Message Tự Động**: Giá trị trả về được tự động gửi đến các destination đã cấu hình
2. **Code Sạch**: Không cần sử dụng StreamBridge thủ công
3. **Dễ Dàng Di Chuyển**: Chuyển đổi liền mạch giữa các nền tảng messaging
4. **Hỗ Trợ Kết Hợp**: Nhiều functions có thể được liên kết bằng ký hiệu pipe

### Quy Ước Đặt Tên Queue

Định dạng: `{destination}.{group}`

Ví dụ: `communication-sent.accounts`

- **Destination**: Từ cấu hình output binding
- **Group**: Ngăn hậu tố ngẫu nhiên, đảm bảo tên queue nhất quán

### Dependency Injection trong Phương Thức @Bean

```java
@Bean
public Consumer<Long> updateCommunication(IAccountService accountService) {
    // accountService được tự động inject - không cần @Autowired
}
```

Spring tự động inject các tham số trong phương thức `@Bean` khi runtime.

## Kiểm Thử

Trong bài giảng tiếp theo, chúng ta sẽ trình diễn:
1. Khởi động cả hai microservices
2. Kích hoạt sự kiện từ Accounts → Message
3. Message microservice xử lý và gửi phản hồi
4. Accounts microservice nhận phản hồi
5. Xác minh cập nhật database

## Tóm Tắt

- Triển khai truyền sự kiện hai chiều giữa các microservices
- Sử dụng Spring Cloud Functions để loại bỏ code boilerplate
- Cấu hình bindings phù hợp trong cả hai microservices
- Tạo Consumer function để xử lý messages đến
- Thêm cột database để theo dõi trạng thái giao tiếp
- Tận dụng việc tạo binding tự động của Spring Cloud Stream

## Thực Hành Tốt Nhất

1. Luôn sử dụng Spring Cloud Functions để có code sạch hơn và dễ bảo trì hơn
2. Khớp tên destination giữa output và input bindings
3. Sử dụng tên group để kiểm soát việc đặt tên queue
4. Chọn functional interface phù hợp (Consumer/Supplier/Function)
5. Để Spring xử lý dependency injection trong phương thức @Bean

## Lợi Ích Của Cách Tiếp Cận Này

- **Giảm Code Boilerplate**: Không cần viết code gửi message thủ công
- **Tính Linh Hoạt Cao**: Dễ dàng chuyển đổi giữa các hệ thống messaging (RabbitMQ, Kafka, etc.)
- **Dễ Bảo Trì**: Code rõ ràng, dễ hiểu và dễ mở rộng
- **Tích Hợp Tốt**: Tích hợp tự nhiên với Spring ecosystem

## Kết Luận

Việc triển khai truyền sự kiện hai chiều giữa microservices sử dụng Spring Cloud Stream và Spring Cloud Functions mang lại nhiều lợi ích về hiệu suất, khả năng bảo trì và tính linh hoạt. Cách tiếp cận này giúp giảm đáng kể lượng code cần viết và duy trì, đồng thời cung cấp một giải pháp mạnh mẽ cho kiến trúc event-driven microservices.




FILE: 28-asynchronous-communication-rabbitmq-demo-complete.md


# Demo Hoàn Chỉnh: Giao Tiếp Bất Đồng Bộ Giữa Các Microservices Với RabbitMQ

## Tổng Quan

Hướng dẫn này trình bày việc triển khai hoàn chỉnh giao tiếp bất đồng bộ giữa các microservices Accounts và Message sử dụng RabbitMQ trong kiến trúc microservices Spring Boot.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, hãy đảm bảo bạn có:
- RabbitMQ server đang chạy
- Accounts microservice
- Message microservice
- Gateway server application

## Bắt Đầu

### Bước 1: Khởi Động Lại Các Ứng Dụng

Sau khi thực hiện các thay đổi đáng kể đối với Accounts và Message microservices, hãy khởi động lại tất cả các ứng dụng:

1. **Accounts Microservice** - Khởi động lại đầu tiên
2. **Message Microservice** - Khởi động lại sau Accounts
3. **Gateway Server Application** - Khởi động lại cuối cùng (phụ thuộc vào Accounts microservice)

> **Quan trọng**: Luôn khởi động lại các microservices phụ thuộc khi khởi động lại Accounts microservice.

## Xác Minh Cấu Hình RabbitMQ

### Exchanges (Trao Đổi)

Truy cập vào RabbitMQ console và xác minh các exchanges sau:

1. **send-communication** - Exchange chính để gửi thông tin liên lạc
2. **communication-sent** - Exchange để cập nhật trạng thái liên lạc

> **Lưu ý**: Bạn có thể thấy một exchange mồ côi `emailsms-out-zero` nếu trước đó bạn không định nghĩa đích cho output bindings. Exchange này sẽ không xuất hiện trong các RabbitMQ container mới.

### Queues (Hàng Đợi)

Kiểm tra phần queues và streams:

- **communication-sent.accounts** - Hàng đợi được Accounts microservice theo dõi để nhận tin nhắn từ Message microservice

## Kiểm Thử Luồng Bất Đồng Bộ

### Bước 1: Lấy Access Token

Sử dụng Postman để lấy access token mới từ authentication server.

### Bước 2: Tạo Tài Khoản Mới

1. Gửi POST request để tạo tài khoản mới với số điện thoại (ví dụ: kết thúc bằng 687)
2. Phản hồi mong đợi: `201 Account created successfully`
3. Thời gian phản hồi: ~1 giây

### Bước 3: Quan Sát Xử Lý Bất Đồng Bộ

Phản hồi nhanh chỉ ra xử lý bất đồng bộ:
- Tạo tài khoản hoàn thành ngay lập tức
- Giao tiếp với người dùng cuối diễn ra ở chế độ nền
- Message microservice xử lý yêu cầu giao tiếp một cách độc lập

## Các Bước Xác Minh

### Kiểm Tra Trạng Thái Database Ban Đầu

1. Truy cập H2 console tại cổng `8080` (Accounts microservice)
2. Truy vấn bảng `accounts`
3. Quan sát giá trị cột `communication_switch`: `null`

Điều này cho thấy giao tiếp với người dùng cuối chưa hoàn thành.

### Theo Dõi Xử Lý Message

Khi Message microservice hoàn thành giao tiếp:
1. Nó stream một event đến Accounts microservice
2. Event kích hoạt cập nhật bảng accounts

### Xác Minh Trạng Thái Cuối Cùng

1. Chạy lại truy vấn trong H2 console
2. Cột `communication_switch` bây giờ hiển thị: `true`
3. Điều này xác nhận giao tiếp bất đồng bộ thành công

## Lợi Ích Của Kiến Trúc

### Triển Khai Event Streaming

Demo này triển khai thành công event streaming trong mạng lưới microservices EasyBank:

- **Giảm Sự Phụ Thuộc Thời Gian**: Các microservices không bị ràng buộc chặt chẽ về thời gian
- **Cải Thiện Khả Năng Mở Rộng**: Các services có thể xử lý requests độc lập
- **Độ Bền Tốt Hơn**: Lỗi ở một service không chặn các services khác
- **Xử Lý Bất Đồng Bộ**: Các tác vụ chạy lâu không chặn API responses

### Các Phương Pháp Tốt Nhất

1. **Tận Dụng Event Streaming**: Sử dụng khả năng event streaming bất cứ khi nào có thể
2. **Tách Rời Services**: Giảm sự phụ thuộc giữa các microservices
3. **Giám Sát Queues**: Thường xuyên kiểm tra RabbitMQ console để theo dõi tình trạng queue
4. **Kiểm Thử Bất Đồng Bộ**: Xác minh cả phản hồi tức thì và tính nhất quán cuối cùng

## Triển Khai Docker

### Chuẩn Bị

1. Tạo Docker images cụ thể cho triển khai này
2. Push images lên Docker Hub
3. Cập nhật file Docker Compose với các phiên bản image mới

### Kiểm Thử Trong Docker

Sử dụng file Docker Compose đã cập nhật để:
1. Khởi động tất cả các containers
2. Kiểm thử kịch bản hoàn chỉnh từ đầu đến cuối
3. Xác minh giao tiếp bất đồng bộ trong môi trường container

## Tóm Tắt

Triển khai này trình bày:
- ✅ Giao tiếp bất đồng bộ giữa các microservices
- ✅ Tích hợp RabbitMQ với Spring Cloud Stream
- ✅ Event streaming để cập nhật trạng thái
- ✅ Giảm sự phụ thuộc thời gian
- ✅ Triển khai sẵn sàng cho Docker

## Tài Liệu Tham Khảo

Để nhanh chóng ôn lại tất cả các bước đã đề cập, hãy tham khảo các slides và tài liệu đi kèm mô tả quy trình triển khai hoàn chỉnh.

## Các Bước Tiếp Theo

1. Xem xét cấu hình Docker Compose
2. Kiểm thử triển khai trong môi trường Docker
3. Giám sát các chỉ số RabbitMQ và hiệu suất queue
4. Triển khai các mẫu bất đồng bộ bổ sung khi cần thiết

---

**Lưu ý**: Hướng dẫn này là một phần của khóa học toàn diện về kiến trúc microservices bao gồm các mẫu event-driven với Spring Boot và RabbitMQ.




FILE: 29-testing-event-driven-microservices-with-docker-and-rabbitmq.md


# Kiểm Thử Microservices Hướng Sự Kiện với Docker và RabbitMQ

## Tổng Quan

Hướng dẫn này trình bày cách kiểm thử các microservices hướng sự kiện sử dụng RabbitMQ trong môi trường Docker. Chúng ta sẽ đề cập đến việc thiết lập hoàn chỉnh bao gồm Docker images, cấu hình Docker Compose và kiểm thử tích hợp với xác thực Keycloak.

## Thiết Lập Docker Images

### Các Docker Images Có Sẵn

Tất cả microservices đã được build với tag name `S13`. Các Docker images sau đây đã sẵn sàng:

- Config Server
- Eureka Server
- Accounts Microservice (Dịch vụ quản lý tài khoản)
- Loans Microservice (Dịch vụ quản lý khoản vay)
- Cards Microservice (Dịch vụ quản lý thẻ)
- Gateway Server
- **Message Microservice** (mới thêm - tổng cộng 7 images)

Tất cả images đã được đẩy lên Docker Hub và có thể sử dụng với tag `S13` tương ứng.

## Cấu Hình Docker Compose

### Cấu Hình Dịch Vụ RabbitMQ

File Docker Compose bao gồm dịch vụ RabbitMQ với cấu hình sau:

```yaml
services:
  rabbit:
    image: rabbitmq:management
    hostname: rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - microservices-network
```

### Cập Nhật Cấu Hình Microservices

Tất cả microservices đã được cập nhật từ tag `S12` lên `S13` bao gồm:

- Config Server
- Eureka Server
- Accounts Microservice
- Loans Microservice
- Cards Microservice
- Gateway Server

### Cấu Hình Accounts Microservice

Accounts microservice hiện phụ thuộc vào RabbitMQ:

```yaml
accounts:
  image: accounts:s13
  depends_on:
    - rabbit
  environment:
    SPRING_RABBITMQ_HOST: rabbit
    # Các thuộc tính mặc định khác (username, password, port) được định nghĩa trong application.yml
  networks:
    - microservices-network
```

### Cấu Hình Message Microservice

Cấu hình Message microservice mới:

```yaml
message:
  image: message:s13
  depends_on:
    - rabbit
  environment:
    SPRING_RABBITMQ_HOST: rabbit
  networks:
    - microservices-network
```

## Khởi Động Môi Trường

### Điều Kiện Tiên Quyết

1. Dừng tất cả các instances đang chạy trên local
2. Dừng các Docker containers hiện có (Keycloak, RabbitMQ, v.v.)
3. Xóa các containers không cần thiết hoặc cấu hình Grafana nếu tài nguyên hệ thống bị hạn chế

### Khởi Động Containers

Di chuyển đến thư mục chứa file Docker Compose (prod profile) và chạy lệnh:

```bash
docker compose up -d
```

Quá trình này mất khoảng 2 phút để hoàn thành.

## Xác Minh Console RabbitMQ

### Truy Cập RabbitMQ Management Console

1. Mở trình duyệt và truy cập: `http://localhost:15672`
2. Thông tin đăng nhập:
   - Username: `guest`
   - Password: `guest`

### Kiểm Tra Cấu Hình

Kiểm tra các thành phần sau được cấu hình đúng:

**Exchanges:**
- `communication-sent`
- `send-communication`

**Queues:**
- Hai queues như được định nghĩa trong cấu hình ứng dụng

## Cấu Hình Keycloak

### Tạo Client cho Client Credentials Grant Flow

1. Truy cập Keycloak console
2. Click **Create Client**
3. Cấu hình client:
   - Client ID: `EazyBankCallCenter-cc`
   - Bật **Client Authentication**
   - Tắt **Standard Flow**
   - Tắt **Direct Access Grants**
   - Bật **Service Account Roles**
4. Lưu và lấy credentials

### Tạo và Gán Roles

1. Tạo role mới: `accounts`
2. Điều hướng đến **Clients** → Chọn client mới tạo
3. Vào **Service Account Roles**
4. Click **Assign Role**
5. Gán role `accounts` cho client

## Kiểm Thử với Postman

### Lấy Access Token

1. Cấu hình Postman với client credentials
2. Click **Get Access Token**
3. Xác minh xác thực thành công
4. Sử dụng access token mới cho các API requests

### Tạo Một Tài Khoản

Gửi POST request để tạo tài khoản. Response thành công sẽ hiển thị chi tiết tài khoản bao gồm số điện thoại.

### Xác Minh Luồng Sự Kiện

#### Logs của Message Microservice

Kiểm tra logs container Message microservice để tìm:
- "Sending email with the details..." (Đang gửi email với chi tiết...)
- "Sending SMS with the details..." (Đang gửi SMS với chi tiết...)

#### Logs của Accounts Microservice

Kiểm tra logs container Accounts microservice để tìm:
1. "Sending communication requests to the details..." (Đang gửi yêu cầu thông tin liên lạc...)
2. "Communication request successfully triggered: true" (Yêu cầu thông tin liên lạc đã được kích hoạt thành công: true)
3. "Updating communication status for account number..." (Đang cập nhật trạng thái thông tin liên lạc cho số tài khoản...)

**Lưu ý:** H2 console không thể truy cập được vì Accounts microservice không được expose ra bên ngoài Docker network.

## Kho Mã Nguồn

Toàn bộ mã nguồn được thảo luận trong phần này có sẵn trong kho GitHub dưới thư mục `section_13` với commit message: "Event driven microservices using RabbitMQ, Spring Cloud Functions and Stream."

## Tiếp Theo

Hướng dẫn này đề cập đến việc triển khai RabbitMQ cho microservices hướng sự kiện. Phần tiếp theo sẽ khám phá cách triển khai microservices hướng sự kiện sử dụng **Apache Kafka**.

## Tóm Tắt

Bạn đã thành công:
- Thiết lập Docker images với tags S13
- Cấu hình Docker Compose với tích hợp RabbitMQ
- Tạo và cấu hình microservices để giao tiếp qua RabbitMQ
- Tích hợp xác thực Keycloak với client credentials flow
- Kiểm thử kiến trúc hướng sự kiện hoàn chỉnh trong môi trường Docker

Các microservices hướng sự kiện hiện đang hoạt động hoàn hảo trong Docker network, thể hiện giao tiếp bất đồng bộ giữa Accounts và Message microservices sử dụng RabbitMQ.




FILE: 3-setting-up-keycloak-authorization-server-with-docker.md


# Thiết Lập Keycloak Authorization Server Với Docker

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập máy chủ xác thực Keycloak sử dụng Docker để bảo mật các microservices với luồng OAuth 2.0 client credentials grant flow.

## Yêu Cầu Trước Khi Bắt Đầu

- Docker đã được cài đặt trên hệ thống
- Docker Compose đã được cấu hình cho microservices
- Java 17 trở lên (yêu cầu tối thiểu cho Keycloak)

## Tại Sao Chọn Keycloak?

Keycloak là giải pháp quản lý danh tính và truy cập mã nguồn mở, cung cấp đầy đủ chức năng dựa trên các tiêu chuẩn OpenID Connect và OAuth 2.0. Nó cho phép bạn bảo mật kiến trúc microservices với các giao thức xác thực và phân quyền tiêu chuẩn công nghiệp.

## Các Bước Cài Đặt

### 1. Truy Cập Tài Liệu Keycloak

Truy cập trang web Keycloak và nhấp vào "Get Started" để khám phá các tùy chọn cài đặt khác nhau. Đối với hệ thống đã cài đặt Docker, phương pháp cài đặt qua Docker được khuyến nghị.

### 2. Chạy Container Keycloak

Thực thi lệnh Docker sau để khởi động máy chủ Keycloak:

```bash
docker run -d -p 7080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  keycloak/keycloak start-dev
```

#### Giải Thích Lệnh:

- **`-d`**: Chạy container ở chế độ detached (chạy nền)
- **`-p 7080:8080`**: Ánh xạ cổng (bên ngoài:bên trong)
  - Cổng nội bộ: 8080 (mặc định của Keycloak)
  - Cổng bên ngoài: 7080 (để tránh xung đột với accounts microservice)
- **`-e KEYCLOAK_ADMIN=admin`**: Đặt tên người dùng admin
- **`-e KEYCLOAK_ADMIN_PASSWORD=admin`**: Đặt mật khẩu admin
- **`start-dev`**: Khởi động Keycloak ở chế độ phát triển

### 3. Cấu Hình Cổng

**Quan trọng**: Cổng mặc định của Keycloak (8080) có thể xung đột với các microservices khác (như accounts microservice). Bằng cách ánh xạ sang cổng 7080 bên ngoài, chúng ta tránh được xung đột cổng trong khi vẫn duy trì cấu hình cổng nội bộ tiêu chuẩn.

### 4. Xác Minh Cài Đặt

1. Kiểm tra Docker Desktop để xác nhận container đang chạy
2. Tìm container có tên "keycloak" đang expose traffic trên cổng 7080
3. Truy cập trang chủ Keycloak tại `http://localhost:7080`

## Truy Cập Admin Console

1. Điều hướng đến `http://localhost:7080`
2. Nhấp vào "Administration Console"
3. Đăng nhập với thông tin xác thực:
   - **Tên đăng nhập**: admin
   - **Mật khẩu**: admin

## Hiểu Về Keycloak Realms

### Realm Là Gì?

**Realm** trong Keycloak là một ranh giới hoặc không gian tên để quản lý một tập hợp:
- Người dùng (Users)
- Thông tin xác thực (Credentials)
- Vai trò (Roles)
- Nhóm (Groups)
- Ứng dụng client (Client applications)

### Master Realm Mặc Định

Keycloak cung cấp realm mặc định có tên "master" khi cài đặt. Realm này đóng vai trò là realm quản trị chính.

### Tạo Nhiều Realms

Bạn có thể tạo thêm các realm dựa trên yêu cầu môi trường:
- **Development (dev)**: Cho môi trường phát triển
- **Quality Assurance (qa)**: Cho môi trường kiểm thử
- **Production (prod)**: Cho môi trường sản xuất

### Tại Sao Cần Nhiều Realms?

Các môi trường khác nhau yêu cầu các bộ thông tin xác thực riêng biệt:
- Thông tin đăng nhập của team QA nên khác với production
- Thông tin đăng nhập development nên tách biệt khỏi production
- Mỗi môi trường duy trì ranh giới bảo mật riêng

## Chế Độ Development vs Production

### Chế Độ Development

Lệnh `start-dev` chạy Keycloak với:
- Cơ sở dữ liệu H2 nội bộ (phù hợp cho thử nghiệm)
- Cấu hình đơn giản
- Thiết lập nhanh chóng

### Các Cân Nhắc Cho Production

Đối với môi trường production, bạn nên:
- Cấu hình cơ sở dữ liệu bên ngoài chuyên dụng (PostgreSQL, MySQL, v.v.)
- Bật HTTPS/TLS
- Sử dụng cấu hình bảo mật phù hợp
- Thiết lập high availability nếu cần

## Các Tính Năng Chính

Keycloak cung cấp chức năng mở rộng bao gồm:
- Quản lý người dùng
- Quản lý client
- Kiểm soát truy cập dựa trên vai trò (RBAC)
- Single Sign-On (SSO)
- Identity brokering
- Tích hợp đăng nhập xã hội
- Xác thực đa yếu tố (MFA)
- Hỗ trợ OAuth 2.0 và OpenID Connect

## Khắc Phục Sự Cố

### Vấn Đề Thường Gặp

**Container không khởi động**: 
- Xác minh Java 17+ đã được cài đặt trên hệ thống
- Kiểm tra cổng 7080 chưa được sử dụng
- Xem lại Docker logs để biết lỗi cụ thể

**Truy cập bị từ chối**:
- Xác nhận bạn đang sử dụng đúng thông tin đăng nhập admin
- Kiểm tra các biến môi trường đã được đặt đúng

## Các Bước Tiếp Theo

Với Keycloak đã được thiết lập thành công, bạn có thể:
1. Tạo client credentials cho microservices của bạn
2. Cấu hình OAuth 2.0 client credentials grant flow
3. Tích hợp gateway server với Keycloak
4. Bảo mật giao tiếp giữa các microservices

## Kết Luận

Thiết lập Keycloak với Docker cung cấp một cách đơn giản để triển khai xác thực và phân quyền cấp doanh nghiệp cho kiến trúc microservices của bạn. Sự hỗ trợ cho các tiêu chuẩn OAuth 2.0 và OpenID Connect đảm bảo tính tương thích và bảo mật trên toàn bộ mạng lưới microservices Easy Bank.

## Tài Nguyên Bổ Sung

- Tài liệu chính thức của Keycloak
- OAuth 2.0 Client Credentials Flow
- Đặc tả OpenID Connect
- Các phương pháp hay nhất về quản lý Docker Container




FILE: 30-apache-kafka-vs-rabbitmq-comparison.md


# So Sánh Apache Kafka và RabbitMQ: Hướng Dẫn Chi Tiết

## Giới Thiệu

Trong kiến trúc microservices hiện đại, giao tiếp bất đồng bộ là yếu tố thiết yếu để xây dựng các hệ thống có khả năng mở rộng và phục hồi tốt. Trong khi RabbitMQ đã là lựa chọn phổ biến cho message broker, Apache Kafka đã nổi lên như một giải pháp mạnh mẽ cho kiến trúc hướng sự kiện (event-driven). Hướng dẫn này khám phá những điểm khác biệt chính giữa hai hệ thống nhắn tin này để giúp bạn đưa ra quyết định sáng suốt.

## Tổng Quan

Cả Apache Kafka và RabbitMQ đều là các hệ thống nhắn tin phổ biến, nhưng chúng có những khác biệt cơ bản về thiết kế, kiến trúc và các trường hợp sử dụng:

- **Apache Kafka**: Nền tảng streaming sự kiện phân tán
- **RabbitMQ**: Message broker truyền thống

## Các Điểm Khác Biệt Chính

### 1. Triết Lý Thiết Kế

**Apache Kafka**
- Được thiết kế như một nền tảng streaming sự kiện phân tán
- Xây dựng để xử lý khối lượng dữ liệu lớn
- Tối ưu hóa cho các tình huống có throughput cao
- Kiến trúc dựa trên event log

**RabbitMQ**
- Được thiết kế như một message broker
- Xử lý khối lượng dữ liệu nhỏ hơn một cách hiệu quả
- Xuất sắc trong các yêu cầu routing phức tạp
- Kiến trúc dựa trên queue (hàng đợi)

> **Lưu ý**: RabbitMQ đang phát triển để trở thành nền tảng streaming sự kiện trong các phiên bản gần đây, nhưng vẫn còn một chặng đường dài để đạt được khả năng của Apache Kafka.

### 2. Lưu Trữ Dữ Liệu

**Apache Kafka**
- Lưu trữ tất cả dữ liệu trên đĩa (disk)
- Có thể giữ lại dữ liệu trong thời gian dài
- Phù hợp cho việc lưu trữ và replay sự kiện dài hạn
- Lưu trữ trên đĩa đảm bảo tính bền vững của dữ liệu

**RabbitMQ**
- Lưu trữ dữ liệu trong bộ nhớ (memory)
- Tối ưu hóa cho các ứng dụng có độ trễ thấp
- Tin nhắn thường được tiêu thụ và xóa nhanh chóng
- Phù hợp hơn cho các mẫu nhắn tin tạm thời

### 3. Hiệu Suất

**Apache Kafka**
- Thường nhanh hơn với khối lượng dữ liệu lớn
- Tối ưu hóa cho các tình huống có throughput cao
- Xuất sắc cho xử lý luồng dữ liệu (stream processing)
- Xử lý hàng triệu tin nhắn mỗi giây

**RabbitMQ**
- Hiệu suất tốt hơn với routing phức tạp
- Độ trễ thấp hơn cho tin nhắn nhỏ
- Hiệu quả cho các mẫu request-response
- Lý tưởng cho các tình huống yêu cầu gửi tin nhắn ngay lập tức

### 4. Khả Năng Mở Rộng

**Apache Kafka**
- Kiến trúc có khả năng mở rộng cao
- Mở rộng theo chiều ngang bằng cách thêm Kafka broker vào cluster
- Không có giới hạn thực tế về kích thước cluster
- Có thể xử lý petabyte dữ liệu
- Phân vùng phân tán cho phép xử lý song song

**RabbitMQ**
- Khả năng mở rộng hạn chế hơn so với Kafka
- Mở rộng theo chiều dọc và ngang có thể thực hiện nhưng có ràng buộc
- Phù hợp hơn cho khối lượng dữ liệu vừa phải
- Khả năng clustering có sẵn nhưng phức tạp hơn

### 5. Bảo Trì và Vận Hành

**Apache Kafka**
- Phức tạp hơn trong việc thiết lập và bảo trì
- Yêu cầu chuyên môn về hệ thống phân tán
- Cần nhiều cấu hình và tinh chỉnh hơn
- Chi phí vận hành cao hơn

**RabbitMQ**
- Dễ dàng thiết lập và bảo trì hơn
- Mô hình vận hành đơn giản hơn
- Đường cong học tập thấp hơn
- Phù hợp cho các nhóm nhỏ

## Khi Nào Nên Chọn Apache Kafka

Chọn Apache Kafka khi bạn cần:

- **Throughput cao**: Xử lý hàng triệu sự kiện mỗi giây
- **Khối lượng dữ liệu lớn**: Xử lý gigabyte hoặc terabyte dữ liệu hàng ngày
- **Event sourcing**: Duy trì lịch sử đầy đủ của các sự kiện
- **Stream processing**: Xử lý và phân tích dữ liệu thời gian thực
- **Tính bền vững dữ liệu**: Lưu trữ sự kiện dài hạn và khả năng replay
- **Khả năng mở rộng theo chiều ngang**: Có thể mở rộng không giới hạn

### Các Trường Hợp Sử Dụng Điển Hình
- Phân tích và giám sát thời gian thực
- Tổng hợp log
- Kiến trúc event sourcing
- Ứng dụng xử lý luồng dữ liệu
- Data pipeline và quy trình ETL

## Khi Nào Nên Chọn RabbitMQ

Chọn RabbitMQ khi bạn cần:

- **Routing phức tạp**: Các mẫu định tuyến tin nhắn nâng cao
- **Độ trễ thấp**: Gửi tin nhắn ngay lập tức
- **Khối lượng dữ liệu vừa phải**: Xử lý lượng dữ liệu nhỏ hơn
- **Thiết lập đơn giản**: Dễ dàng cấu hình và bảo trì
- **Mẫu request-response**: Các mẫu nhắn tin truyền thống
- **Hàng đợi ưu tiên**: Ưu tiên hóa tin nhắn

### Các Trường Hợp Sử Dụng Điển Hình
- Hàng đợi tác vụ và công việc nền
- Giao tiếp request-response
- Các tình huống routing phức tạp
- Ứng dụng yêu cầu độ trễ thấp
- Giao tiếp microservices quy mô nhỏ

## Ma Trận Quyết Định

| Yếu Tố | Apache Kafka | RabbitMQ |
|--------|-------------|----------|
| **Khối Lượng Dữ Liệu** | Lớn (GB-TB mỗi ngày) | Nhỏ đến Trung bình (MB-GB mỗi ngày) |
| **Throughput** | Rất Cao | Trung bình đến Cao |
| **Độ Trễ** | Trung bình | Thấp |
| **Khả Năng Mở Rộng** | Không giới hạn | Có giới hạn |
| **Độ Phức Tạp** | Cao | Thấp đến Trung bình |
| **Routing** | Đơn giản | Phức tạp |
| **Lưu Trữ Dữ Liệu** | Dài hạn (ngày/tuần) | Ngắn hạn (phút/giờ) |
| **Bảo Trì** | Phức tạp | Đơn giản |

## Kết Luận

Cả Apache Kafka và RabbitMQ đều là các hệ thống nhắn tin xuất sắc hỗ trợ streaming sự kiện và giao tiếp bất đồng bộ giữa các microservices. Sự lựa chọn giữa chúng phụ thuộc hoàn toàn vào yêu cầu cụ thể của bạn:

- **Chọn Apache Kafka** nếu tổ chức của bạn xử lý khối lượng dữ liệu lớn hàng ngày và yêu cầu khả năng streaming sự kiện hiệu suất cao.

- **Chọn RabbitMQ** nếu bạn đang xử lý khối lượng dữ liệu vừa phải và cần một hệ thống nhắn tin với yêu cầu routing phức tạp, dễ bảo trì.

Tóm lại:
- **Hoạt động quy mô nhỏ** với dữ liệu vừa phải → RabbitMQ
- **Hoạt động quy mô lớn** với khối lượng dữ liệu cao → Apache Kafka

## Các Bước Tiếp Theo

Bây giờ bạn đã hiểu sự khác biệt giữa Apache Kafka và RabbitMQ, bước tiếp theo là tìm hiểu sâu hơn về kiến trúc Apache Kafka, các thành phần và cách triển khai microservices hướng sự kiện sử dụng nền tảng streaming mạnh mẽ này.

---

*Hướng dẫn này cung cấp nền tảng để hiểu khi nào nên sử dụng Apache Kafka so với RabbitMQ trong kiến trúc microservices của bạn được xây dựng với Java và Spring Boot.*




FILE: 31-apache-kafka-introduction-and-core-concepts.md


# Apache Kafka: Giới Thiệu và Các Khái Niệm Cốt Lõi

## Giới Thiệu

Apache Kafka là một nền tảng phát trực tuyến sự kiện (event streaming) phân tán mã nguồn mở được thiết kế để xử lý dữ liệu quy mô lớn theo thời gian thực. Nó có khả năng phát trực tuyến dữ liệu thời gian thực với thропропут cao, khả năng chịu lỗi và xử lý dữ liệu có thể mở rộng.

## Ví Dụ Thực Tế

Để hiểu Apache Kafka, hãy xem xét một hệ thống receiver giải trí tại nhà:

- **Receiver (Broker)**: Đóng vai trò là trung tâm kết nối các nguồn đầu vào khác nhau (DVD, Blu-ray, USB, ăng-ten TV) với các thiết bị đầu ra (tivi, loa)
- **Nguồn Đầu Vào (Producers)**: Đầu DVD, đầu Blu-ray, ổ USB, đầu thu TV
- **Thiết Bị Đầu Ra (Consumers)**: Tivi và loa

Receiver nhận dữ liệu từ nhiều nguồn và phát trực tuyến đến các thiết bị đích. Tương tự, Apache Kafka hoạt động như một broker giữa producers và consumers, phát trực tuyến lượng dữ liệu lớn một cách hiệu quả.

## Apache Kafka vs RabbitMQ

Mặc dù cả hai đều là message broker, Apache Kafka được thiết kế đặc biệt cho:
- **Phát trực tuyến dữ liệu khối lượng lớn**: Có thể xử lý lượng dữ liệu khổng lồ
- **Xử lý thời gian thực**: Khả năng phát trực tuyến dữ liệu theo thời gian thực
- **Khả năng mở rộng**: Được xây dựng để mở rộng theo chiều ngang trên nhiều server

Ngược lại, RabbitMQ phù hợp hơn cho việc xử lý lượng dữ liệu hạn chế với các mẫu hàng đợi thông điệp truyền thống.

## Các Thành Phần Cốt Lõi

### 1. Producers (Nhà Sản Xuất)

**Định nghĩa**: Các ứng dụng chịu trách nhiệm sản xuất dữ liệu hoặc sự kiện.

**Đặc điểm**:
- Kết nối với Kafka cluster
- Liên tục đẩy messages/events vào Kafka cluster
- Có thể có nhiều producers trong một ứng dụng
- Ghi dữ liệu vào các topics cụ thể

### 2. Kafka Cluster (Cụm Kafka)

**Định nghĩa**: Một tập hợp các server làm việc cùng nhau để tạo ra kết quả mong muốn.

**Đặc điểm**:
- Chứa nhiều brokers (servers)
- Khuyến nghị: Ít nhất 3 brokers trong môi trường production
- Các brokers được triển khai ở các vị trí địa lý khác nhau
- Đảm bảo sự dự phòng và chịu lỗi của dữ liệu

### 3. Brokers

**Định nghĩa**: Các Kafka server trong cluster xử lý lưu trữ và sao chép dữ liệu.

**Trách nhiệm**:
- Nhận dữ liệu từ producers
- Gán offset IDs cho messages
- Phục vụ messages cho consumers
- Sao chép dữ liệu qua nhiều brokers
- Lưu trữ topics và partitions

**Thực Hành Tốt**: Triển khai brokers ở các vị trí địa lý khác nhau để đảm bảo an toàn dữ liệu trong trường hợp thiên tai hoặc tai nạn.

### 4. Topics (Chủ Đề)

**Định nghĩa**: Một luồng dữ liệu logic, tương tự như exchanges trong RabbitMQ.

**Đặc điểm**:
- Producers gửi messages đến các topics cụ thể
- Được tổ chức theo trường hợp sử dụng (ví dụ: "send-communication", "refund-payment")
- Một broker có thể chứa nhiều topics
- Dữ liệu được phân phối qua các partitions trong topics

### 5. Partitions (Phân Vùng)

**Định nghĩa**: Các phân chia nhỏ trong một topic cho phép lưu trữ dữ liệu phân tán.

**Mục đích**:
- Cho phép lưu trữ lượng dữ liệu lớn trên nhiều brokers
- Cho phép xử lý song song các messages
- Phân phối dữ liệu dựa trên logic nghiệp vụ

**Ví Dụ Trường Hợp Sử Dụng**:
Đối với ứng dụng ngân hàng gửi thông tin khách hàng:
- Partition 0 (P0): Messages cho khách hàng ở New York
- Partition 1 (P1): Messages cho khách hàng ở Washington
- Partition 2 (P2): Messages cho các khu vực khác

**Lợi ích**:
- Khả năng mở rộng: Thêm brokers để xử lý nhiều dữ liệu hơn
- Hiệu suất: Xử lý messages song song
- Linh hoạt: Phân phối dữ liệu dựa trên yêu cầu nghiệp vụ

### 6. Offset IDs

**Định nghĩa**: Số thứ tự duy nhất được gán cho mỗi message trong một partition.

**Đặc điểm**:
- Bắt đầu từ 0 và tăng dần theo thứ tự (0, 1, 2, 3, ...)
- Tương tự như sequence IDs trong các hàng cơ sở dữ liệu
- Cho phép nhận dạng duy nhất các messages
- Kết hợp với topic và partition để tạo tính duy nhất toàn cục

**Tính Duy Nhất**: Sự kết hợp của Topic + Partition + Offset ID luôn là duy nhất trong Kafka.

**Theo Dõi Consumer**: Consumers sử dụng offset IDs để theo dõi messages nào đã được xử lý.

### 7. Replication (Sao Chép)

**Định nghĩa**: Quá trình sao chép dữ liệu qua nhiều brokers.

**Lợi ích**:
- **Chịu lỗi**: Dữ liệu tồn tại khi broker bị lỗi
- **Tính Sẵn Sàng Cao**: Hệ thống vẫn hoạt động trong khi có lỗi
- **An Toàn Dữ Liệu**: Messages được lưu trữ ở nhiều vị trí địa lý
- **Phục Hồi Thảm Họa**: Có bản sao lưu nếu broker chính bị lỗi

**Triển Khai**: Khi một message được lưu vào một broker, nó tự động được sao chép sang các brokers khác (ví dụ: từ Broker1 sang Broker2 hoặc Broker3).

### 8. Consumers (Người Tiêu Dùng)

**Định nghĩa**: Các ứng dụng kéo và xử lý messages từ các Kafka topics.

**Đặc điểm**:
- Liên tục kéo messages từ các topics và partitions đã đăng ký
- Xử lý dữ liệu theo thời gian thực
- Có thể được tổ chức thành consumer groups

### 9. Consumer Groups (Nhóm Consumer)

**Định nghĩa**: Nhóm logic các consumers làm việc cùng nhau để xử lý messages từ một topic.

**Mục đích**:
- Nhóm consumers theo trách nhiệm (ví dụ: tất cả consumers xử lý topic "send-communication")
- Cho phép xử lý message song song
- Cải thiện thропропут và hiệu suất

**Ví Dụ Cấu Hình**:
- Consumer Group A: Xử lý messages từ topic "send-communication"
  - Consumer 1: Xử lý messages Partition 0
  - Consumer 2: Xử lý messages Partition 1
  - Consumer 3: Xử lý messages Partition 2

**Lợi ích**: Xử lý song song các messages khi chúng đến từ producers.

### 10. Kafka Streams

**Định nghĩa**: Thư viện client cho phép xử lý luồng trong Kafka.

**Khả năng**:
- Sản xuất dữ liệu thời gian thực từ các ứng dụng
- Tiêu thụ và xử lý dữ liệu thời gian thực
- Xử lý luồng trực tiếp trong Kafka
- Xây dựng các pipeline dữ liệu phát trực tuyến thời gian thực

## Luồng Dữ Liệu trong Apache Kafka

1. **Producers** ghi messages/events vào các **Topics** cụ thể
2. **Topics** tổ chức dữ liệu thành **Partitions** qua nhiều **Brokers**
3. Mỗi message được gán một **Offset ID** trong partition của nó
4. Messages được **Sao chép** qua nhiều brokers để chịu lỗi
5. **Consumers** (được tổ chức trong **Consumer Groups**) kéo messages từ partitions
6. Consumers xử lý messages song song để có hiệu suất tối ưu

## Ưu Điểm Chính

1. **Khả năng mở rộng**: Xử lý bất kỳ lượng dữ liệu nào bằng cách thêm brokers
2. **Thропропут Cao**: Xử lý khối lượng lớn dữ liệu hiệu quả
3. **Chịu Lỗi**: Dữ liệu được sao chép qua nhiều brokers
4. **Xử Lý Thời Gian Thực**: Phát trực tuyến và xử lý dữ liệu theo thời gian thực
5. **Xử Lý Song Song**: Nhiều consumers xử lý dữ liệu đồng thời
6. **Dự Phòng Địa Lý**: Dữ liệu được lưu trữ ở nhiều vị trí
7. **Tính Sẵn Sàng Cao**: Hệ thống tiếp tục hoạt động trong khi có lỗi

## Thực Hành Tốt Nhất Trong Production

1. **Tối Thiểu 3 Brokers**: Đảm bảo ít nhất 3 brokers trong production
2. **Phân Bố Địa Lý**: Triển khai brokers ở các vị trí khác nhau
3. **Hệ Số Sao Chép**: Cấu hình sao chép phù hợp (tối thiểu 2)
4. **Chiến Lược Partition**: Thiết kế phân vùng dựa trên logic nghiệp vụ
5. **Consumer Groups**: Tổ chức consumers để xử lý song song
6. **Giám Sát**: Theo dõi offset IDs và độ trễ consumer

## Các Trường Hợp Sử Dụng

Apache Kafka lý tưởng để xây dựng:
- Pipeline dữ liệu phát trực tuyến thời gian thực
- Kiến trúc microservices hướng sự kiện
- Hệ thống tổng hợp log
- Nền tảng phân tích thời gian thực
- Hệ thống xử lý message
- Hệ thống theo dõi hoạt động

## Tóm Tắt

Apache Kafka là một nền tảng phát trực tuyến sự kiện phân tán mạnh mẽ cho phép:
- Xử lý dữ liệu khối lượng lớn, thời gian thực
- Lưu trữ và phân phối message chịu lỗi
- Kiến trúc có thể mở rộng cho nhu cầu dữ liệu tăng trưởng
- Xử lý song song thông qua partitions và consumer groups
- Dự phòng dữ liệu địa lý để phục hồi thảm họa

Phần giới thiệu này bao gồm các khái niệm cơ bản cần thiết để triển khai phát trực tuyến sự kiện trong microservices sử dụng Apache Kafka. Đối với triển khai production, cần có kiến thức sâu hơn về cấu hình, điều chỉnh và giám sát.

---

**Lưu ý**: Tài liệu này cung cấp giới thiệu cơ bản về các khái niệm Apache Kafka. Để có phạm vi toàn diện về các chủ đề nâng cao, hãy tham khảo tài liệu Apache Kafka chính thức và các khóa học Kafka chuyên môn.




FILE: 32-apache-kafka-producer-consumer-workflow.md


# Luồng Xử Lý Producer và Consumer trong Apache Kafka

## Tổng Quan

Tài liệu này giải thích chi tiết về luồng xử lý khi producer gửi message đến Apache Kafka và cách consumer đọc message từ Kafka broker. Hiểu rõ quy trình này rất quan trọng để triển khai kiến trúc microservices hướng sự kiện với Spring Cloud Stream.

## Luồng Xử Lý Producer

### 1. Cấu Hình Producer

Bước đầu tiên trong luồng producer là cấu hình. Việc này bao gồm thiết lập các thuộc tính quan trọng:

- **URL Endpoint của Kafka Broker**: Chuỗi kết nối để truy cập Kafka broker
- **Định Dạng Serialization**: Xác định cách message được serialize trước khi truyền
- **Cấu Hình Tùy Chọn**:
  - Thiết lập nén (compression) để giảm kích thước message
  - Cấu hình batching để tối ưu throughput

### 2. Chọn Topic

Sau khi producer được cấu hình, nó phải chọn topic đích để gửi message:

- Producer chỉ định topic nào sẽ nhận message
- Nếu topic chưa tồn tại, nó có thể được tạo động dựa trên cấu hình broker
- Việc chọn topic là bắt buộc cho mỗi thao tác gửi message

### 3. Gửi Message

Producer gửi message đến Kafka bằng các API của Kafka client library:

- **Topic Đích**: Chỉ định topic đích
- **Message Đã Serialize**: Nội dung message thực tế ở dạng đã serialize
- **Partition Key** (Tùy chọn): Một key xác định partition nào sẽ lưu trữ message

### 4. Gán Partition

Khi Kafka broker nhận được message, nó gán message cho một partition cụ thể:

- **Với Partition Key**: Nếu được cung cấp, Kafka sử dụng key để xác định partition đích
- **Không Có Partition Key**: Kafka sử dụng các thuật toán như Round Robin hoặc hashing để phân phối message đều trên các partition

Điều này đảm bảo phân phối tải cân bằng và duy trì thứ tự message trong partition.

### 5. Gán Offset và Lưu Trữ

Sau khi partition được xác định:

- Kafka gán một **offset ID** duy nhất cho message
- Message được thêm vào log của partition đã chọn
- Offset ID đóng vai trò như một định danh duy nhất trong partition

### 6. Sao Chép Message

Nếu tính năng replication được bật:

- Kafka sao chép message sang các broker khác dựa trên cấu hình replication
- Việc sao chép có thể diễn ra **không đồng bộ** hoặc **đồng bộ**
- Điều này đảm bảo khả năng chịu lỗi và tính sẵn sàng cao

### 7. Xác Nhận (Acknowledgment)

Bước cuối cùng trong luồng producer:

- Kafka broker gửi acknowledgment trả về cho producer
- Nếu có lỗi xảy ra, chúng được thông báo cho producer
- Producer có thể triển khai logic retry dựa trên chế độ acknowledgment

**Các Chế Độ Acknowledgment**:
- Chờ tất cả các replica hoàn thành
- Chỉ chờ leader replica hoàn thành

Producer có thể tiếp tục với logic nghiệp vụ của nó sau khi nhận được acknowledgment.

## Luồng Xử Lý Consumer

### 1. Gán Consumer Group

Trước khi tiêu thụ message, consumer phải:

- Tham gia vào một **consumer group**
- Consumer group cho phép xử lý song song và cân bằng tải
- Mỗi consumer group duy trì việc theo dõi offset riêng

### 2. Đăng Ký Topic

Consumer trong một group phải đăng ký topic:

- Chỉ định một hoặc nhiều topic để tiêu thụ message
- Việc đăng ký xác định các topic mà consumer quan tâm
- Nhiều consumer trong một group có thể đăng ký cùng các topic

### 3. Gán Partition

Kafka gán partition cho consumer trong một group:

- **Quy Tắc Quan Trọng**: Mỗi partition chỉ có thể được tiêu thụ bởi một consumer trong group
- Đảm bảo phân phối cân bằng partition giữa các consumer
- Cho phép xử lý song song các message

### 4. Quản Lý Offset

Consumer duy trì thông tin offset để theo dõi tiến trình:

- Ban đầu, offset là **null** đối với consumer mới
- Khi message được xử lý, consumer cập nhật offset của nó
- Việc theo dõi offset đảm bảo consumer biết message nào đã được xử lý
- Rất quan trọng để tiếp tục từ vị trí đúng sau khi xảy ra lỗi

### 5. Yêu Cầu Fetch

Consumer gửi yêu cầu fetch đến Kafka broker bao gồm:

- **Topic**: Topic nào để đọc
- **Partition**: Partition nào để tiêu thụ
- **Offset**: Điểm bắt đầu để lấy message
- **Batch Size**: Số lượng message cần fetch trong một yêu cầu

**Lưu Ý về Hiệu Suất**: Không giống RabbitMQ, Kafka consumer có thể fetch nhiều message (ví dụ: 100 message) trong một yêu cầu duy nhất, cải thiện đáng kể throughput khi xử lý khối lượng dữ liệu lớn.

### 6. Phản Hồi Fetch

Kafka broker xử lý yêu cầu fetch:

- Lấy các message được yêu cầu từ log của partition
- Trả về message cùng với offset và metadata của chúng
- Phản hồi chứa tất cả thông tin được yêu cầu trong một batch duy nhất

### 7. Xử Lý Message

Consumer xử lý message dựa trên logic nghiệp vụ:

- Biến đổi message theo nhu cầu
- Thực hiện tổng hợp hoặc tính toán
- Thực thi các thao tác cụ thể theo nghiệp vụ
- Xử lý bất kỳ biến đổi dữ liệu nào cần thiết

### 8. Commit Offset

Sau khi xử lý thành công, consumer commit offset:

- Thông báo cho Kafka rằng các message đến một offset cụ thể đã được xử lý
- Đảm bảo tiến trình được lưu trữ trong Kafka broker
- Cho phép tiếp tục từ vị trí đúng sau khi xảy ra lỗi hoặc khởi động lại

### 9. Vòng Lặp Polling Liên Tục

Consumer liên tục lặp lại các bước 5-8:

- Fetch message mới
- Xử lý chúng
- Commit offset
- Đảm bảo xử lý message gần như thời gian thực khi message mới đến

## Đơn Giản Hóa với Spring Cloud Stream

Mặc dù luồng xử lý Kafka có vẻ phức tạp, **Spring Cloud Stream** trừu tượng hóa phần lớn độ phức tạp này:

- **Không Cần Tạo Topic Thủ Công**: Framework xử lý việc quản lý topic
- **Xử Lý Partition Tự Động**: Không cần quản lý partition thủ công
- **Quản Lý Offset Đơn Giản**: Framework theo dõi offset tự động
- **Thân Thiện với Developer**: Tập trung vào logic nghiệp vụ thay vì cơ sở hạ tầng

Spring Cloud Stream làm cho việc triển khai Apache Kafka trong kiến trúc microservices trở nên đơn giản và thân thiện với developer, xử lý tất cả các phức tạp về cơ sở hạ tầng ở hậu trường.

## Điểm Chính Cần Nhớ

1. **Phía Producer**: Cấu Hình → Chọn Topic → Gửi Message → Gán Partition → Sao Chép → Xác Nhận
2. **Phía Consumer**: Tham Gia Group → Đăng Ký → Gán Partition → Quản Lý Offset → Fetch → Xử Lý → Commit → Lặp Lại
3. **Spring Cloud Stream** đơn giản hóa toàn bộ quy trình từ góc độ developer
4. **Xử lý theo batch của Kafka** cho phép throughput cao cho xử lý dữ liệu quy mô lớn
5. **Quản lý offset** rất quan trọng cho việc xử lý message đáng tin cậy và khôi phục sau lỗi

## Kết Luận

Hiểu rõ luồng xử lý producer và consumer của Apache Kafka là điều cần thiết để xây dựng microservices hướng sự kiện mạnh mẽ. Mặc dù cơ chế bên dưới rất tinh vi, Spring Cloud Stream cung cấp một lớp trừu tượng đơn giản cho phép developer tập trung vào logic nghiệp vụ thay vì độ phức tạp của cơ sở hạ tầng.

---

*Tài liệu này là một phần của loạt bài về kiến trúc microservices, bao gồm các mẫu hướng sự kiện với Spring Boot và Apache Kafka.*




FILE: 33-setting-up-apache-kafka-in-local-environment.md


# Cài Đặt Apache Kafka Trong Môi Trường Local

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện quá trình cài đặt và thiết lập Apache Kafka trong môi trường phát triển local để giao tiếp giữa các microservices.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Docker trên hệ thống local
- Hiểu biết cơ bản về kiến trúc microservices
- IntelliJ IDEA (hoặc IDE ưa thích)

## Bắt Đầu Với Apache Kafka

### Bước 1: Truy Cập Website Apache Kafka

1. Truy cập website chính thức của Apache Kafka: [kafka.apache.org](https://kafka.apache.org)
2. Khám phá các khả năng cốt lõi, hệ sinh thái và các trường hợp sử dụng của Kafka
3. Lưu ý rằng Apache Kafka được sử dụng bởi hơn 80% các công ty Fortune 100

### Bước 2: Truy Cập Hướng Dẫn Nhanh

1. Di chuột qua menu "Get Started"
2. Click vào "Quick Start"
3. Trang Quick Start cung cấp nhiều tùy chọn cài đặt khác nhau

### Bước 3: Cài Đặt Với Docker (Khuyến Nghị)

Cách dễ nhất để cài đặt Kafka là sử dụng Docker, phù hợp với việc sử dụng Docker trong suốt khóa học.

**Quan trọng:** Đảm bảo sao chép lệnh Docker dưới tiêu đề **JVM based**, không phải từ phần GraalVM.

#### Chạy Kafka Với Docker

Thực thi lệnh Docker trong terminal của bạn. Lệnh này sẽ:
- Khởi động Kafka trên cổng **9092** trong hệ thống local
- Khởi tạo Kafka broker
- Sẵn sàng cho các kết nối

#### Xác Minh

Sau vài giây, bạn sẽ thấy các console logs cho biết Kafka đang chờ kết nối tại cổng 9092.

### Bước 4: Cấu Hình Microservices

Sau khi Kafka đang chạy, bạn cần cấu hình nó trong các microservices:

1. **Message Microservice** - Cấu hình để tạo ra các events
2. **Account Microservice** - Cấu hình để tiêu thụ các events

Các services này sẽ giao tiếp bất đồng bộ bằng cách tận dụng khả năng event streaming của Kafka.

## Tích Hợp Docker Compose

Sau khi test thành công mọi thứ trong môi trường IntelliJ local, bạn có thể cập nhật file `docker-compose.yml` để bao gồm cài đặt Kafka nhằm dễ dàng triển khai và quản lý hơn.

## Các Điểm Chính

- Kafka chạy trên cổng **9092** theo mặc định
- Được sử dụng cho giao tiếp bất đồng bộ giữa các microservices
- Kích hoạt khả năng event streaming
- Được chấp nhận rộng rãi bởi các tổ chức doanh nghiệp
- Docker cung cấp phương pháp cài đặt dễ nhất

## Các Bước Tiếp Theo

- Cấu hình Spring Cloud Stream trong microservices của bạn
- Triển khai producers và consumers
- Test giao tiếp event-driven
- Cập nhật cấu hình Docker Compose

---

*Việc cài đặt này rất quan trọng để triển khai kiến trúc microservices hướng sự kiện với Apache Kafka.*




FILE: 34-migrating-from-rabbitmq-to-apache-kafka-in-spring-microservices.md


# Di Chuyển từ RabbitMQ sang Apache Kafka trong Spring Microservices

## Tổng Quan

Hướng dẫn này trình bày cách di chuyển các microservices Spring Boot từ RabbitMQ sang Apache Kafka cho giao tiếp bất đồng bộ. Quá trình di chuyển được đơn giản hóa bằng cách sử dụng Spring Cloud Stream và Spring Cloud Functions, chỉ yêu cầu thay đổi code tối thiểu.

## Yêu Cầu Tiên Quyết

- Dự án Spring Boot microservices (code Section 13)
- Apache Kafka chạy local trên cổng 9092
- IntelliJ IDEA với hỗ trợ Maven
- Plugin Kafkalytic (để giám sát Kafka cluster)
- Keycloak server (cho xác thực OAuth2)
- Docker Desktop

## Các Bước Di Chuyển

### 1. Thiết Lập Dự Án

Đầu tiên, tạo một thư mục workspace mới cho Section 14:

1. Sao chép code từ Section 13
2. Đổi tên thư mục thành `section14`
3. Xóa thư mục `.idea`
4. Mở dự án trong IntelliJ IDEA

### 2. Cập Nhật Maven Dependencies

#### Accounts Microservice

Mở file `pom.xml` trong Accounts microservice và thay thế dependency RabbitMQ:

**Trước đây:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-rabbit</artifactId>
</dependency>
```

**Sau khi thay đổi:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-kafka</artifactId>
</dependency>
```

Cập nhật tên tag từ `s13` thành `s14` và reload Maven.

#### Message Microservice

Thực hiện thay đổi dependency tương tự trong file `pom.xml` của Message microservice:

- Thay thế `spring-cloud-stream-binder-rabbit` bằng `spring-cloud-stream-binder-kafka`
- Cập nhật tên tag từ `s13` thành `s14`
- Reload các thay đổi Maven

### 3. Cập Nhật Cấu Hình Application

#### Cấu Hình Message Microservice

Mở file `application.yml` trong Message microservice:

1. **Xóa các properties RabbitMQ:**
   - Xóa tất cả chi tiết kết nối RabbitMQ

2. **Thêm cấu hình Kafka:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
```

#### Cấu Hình Accounts Microservice

Mở file `application.yml` trong Accounts microservice:

1. **Xóa các properties RabbitMQ:**
   - Xóa tất cả chi tiết kết nối RabbitMQ

2. **Thêm cấu hình Kafka:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
```

> **Lưu ý:** Nếu bạn có nhiều Kafka brokers trong một cluster, hãy liệt kê tất cả các broker endpoints dưới dạng các phần tử mảng.

### 4. Hoàn Thành Cấu Hình

Như vậy là xong! Không cần thay đổi code nào khác. Sức mạnh của Spring Cloud Stream trừu tượng hóa tất cả các vấn đề về cơ sở hạ tầng, giúp việc chuyển đổi từ RabbitMQ sang Kafka trở nên liền mạch.

## Kiểm Thử Quá Trình Di Chuyển

### 1. Khởi Động Các Services Cần Thiết

Khởi động tất cả các microservices theo thứ tự sau:

1. Config Server
2. Eureka Server
3. Accounts Application
4. Message Application
5. Gateway Server Application

Cả Accounts và Message microservices giờ đây sẽ kết nối với Kafka instance local.

### 2. Xác Minh Thiết Lập Kafka với Plugin Kafkalytic

1. Cài đặt plugin **Kafkalytic** từ marketplace IntelliJ IDEA
2. Click nút **Add** và cấu hình:
   - Broker: `localhost:9092`
3. Click **Test Connection** để xác minh kết nối
4. Click **OK** để lưu

#### Xác Minh Các Thành Phần Kafka:

- **Brokers:** Sẽ hiển thị 1 broker (localhost:9092)
- **Consumers:** Sẽ hiển thị 2 consumers
  - Message microservice (tiêu thụ từ Accounts)
  - Accounts microservice (tiêu thụ từ Message)
- **Topics:** Sẽ hiển thị:
  - `communication-sent`
  - `send-communication`
  - `__consumer_offsets` (topic nội bộ của Kafka)

### 3. Kiểm Tra Giao Tiếp Bất Đồng Bộ

#### Khởi Động Keycloak Server

1. Mở Docker Desktop
2. Khởi động container Keycloak hiện có
3. Truy cập Keycloak tại `http://localhost:7080`
4. Đăng nhập với thông tin: `admin` / `admin`
5. Điều hướng đến **Clients** và tìm `eazybank-callcenter-cc`
6. Sao chép client credentials

#### Đặt Breakpoint Debug

1. Mở Message microservice
2. Điều hướng đến class `MessageFunctions`
3. Đặt breakpoint trong hàm `email`

#### Thực Hiện Kiểm Thử API với Postman

1. Lấy access token:
   - Sử dụng client ID và credentials đã sao chép
   - Click **Get New Access Token**
2. Sử dụng access token để gọi **Create API** trong Accounts microservice
3. Click **Send**

#### Xác Minh Kết Quả

1. Breakpoint sẽ được kích hoạt trong hàm `email`
2. Kiểm tra H2 console của Accounts microservice:
   - Điều hướng đến H2 console
   - Click **Connect**
   - Truy vấn bảng `accounts`
   - **Trước khi thả breakpoint:** cột `communication_switch` = `null`
3. Thả breakpoint
4. Truy vấn lại bảng `accounts`
   - **Sau khi thả breakpoint:** cột `communication_switch` = `true`

Điều này xác nhận rằng giao tiếp bất đồng bộ end-to-end đang hoạt động với Apache Kafka!

## Lợi Ích Chính của Spring Cloud Stream

- **Trừu Tượng Hóa Cơ Sở Hạ Tầng:** Tất cả các vấn đề về cơ sở hạ tầng được xử lý tự động
- **Di Chuyển Dễ Dàng:** Chuyển đổi giữa các hệ thống messaging với thay đổi tối thiểu
- **Trải Nghiệm Nhà Phát Triển:** Cấu hình dependency và properties đơn giản
- **Cách Tiếp Cận Hiện Đại:** Tận dụng các kỹ thuật mới nhất trong Spring ecosystem

## Các Bước Tiếp Theo

### Kiểm Thử Môi Trường Docker

Để kiểm thử trong môi trường Docker:

1. Tạo Docker images cụ thể cho Section 14
2. Push images lên Docker Hub
3. Cập nhật file Docker Compose
4. Thực thi và xác thực các thay đổi trong môi trường Docker

## Thực Hành Tốt Nhất

1. **Luôn sử dụng Spring Cloud Functions và Spring Cloud Stream** cho messaging trong microservices
2. **Tránh các cách tiếp cận cũ** cho tích hợp RabbitMQ/Kafka
3. **Tận dụng các công cụ hiện đại của Spring ecosystem** để có trải nghiệm nhà phát triển tốt hơn
4. **Chia sẻ kiến thức** với các nhà phát triển khác về những kỹ thuật hiệu quả này

## Kết Luận

Di chuyển từ RabbitMQ sang Apache Kafka với Spring Cloud Stream cực kỳ đơn giản. Framework xử lý toàn bộ sự phức tạp, cho phép các nhà phát triển tập trung vào logic nghiệp vụ thay vì các vấn đề về cơ sở hạ tầng. Điều này thể hiện sức mạnh và tính linh hoạt của Spring Cloud Stream trong việc xây dựng các microservices hướng sự kiện.

## Tài Nguyên Bổ Sung

- Tài liệu Spring Cloud Stream
- Tài liệu Apache Kafka
- Hướng dẫn Spring Cloud Functions
- Tài liệu Plugin Kafkalytic




FILE: 35-migrating-microservices-from-rabbitmq-to-kafka-with-docker.md


# Chuyển đổi Microservices từ RabbitMQ sang Apache Kafka với Docker

## Tổng quan

Hướng dẫn này trình bày cách chuyển đổi các microservices hướng sự kiện từ RabbitMQ sang Apache Kafka, bao gồm cấu hình Docker Compose, tích hợp Spring Cloud Stream và kiểm thử toàn bộ hệ thống.

## Yêu cầu

- Docker và Docker Compose đã được cài đặt
- Microservices Spring Boot (dịch vụ Accounts và Message)
- Hiểu biết cơ bản về Apache Kafka và RabbitMQ
- Keycloak cho xác thực OAuth2

## Chuẩn bị Docker Images

### Xây dựng và Đẩy Images

Tất cả bảy ứng dụng microservice đã được xây dựng với tên tag **S14** và đẩy lên Docker Hub. Bạn có thể xác minh các images này bằng cách:

1. Truy cập kho lưu trữ Docker Hub
2. Kiểm tra các images được gắn tag **S14**
3. Xác nhận rằng tất cả các dịch vụ cần thiết đều có sẵn

## Cấu hình Apache Kafka trong Docker Compose

### Nguồn Cấu hình Kafka

Cấu hình Docker Kafka dựa trên hướng dẫn chính thức từ **developer.confluent.io**. Confluent là công ty hàng đầu chuyên về các giải pháp Kafka doanh nghiệp, làm cho cấu hình của họ đáng tin cậy và sẵn sàng cho môi trường production.

### Hiểu về Cấu hình

Cấu hình cơ bản bao gồm:

- **Tên service**: broker (mà chúng ta sẽ tùy chỉnh thành "kafka")
- **Image**: Docker image Apache Kafka chính thức
- **Hostname và Container name**: Để khám phá dịch vụ
- **Ánh xạ cổng**: Cấu hình cổng bên ngoài và bên trong
- **Biến môi trường**: Các tham số khởi động Kafka thiết yếu

### Các Điểm Cấu hình Quan trọng

Khi tùy chỉnh cấu hình Kafka:

1. **Tính nhất quán của Tên Service**: Bất kể tên service nào bạn chọn (ví dụ: "kafka") phải được sử dụng nhất quán trong:
   - Hostname
   - Container name
   - Tất cả các tham chiếu ánh xạ cổng
   - Các tham chiếu biến môi trường

2. **Cấu hình Broker**: `KAFKA_PROCESS_ROLES` nên giữ nguyên là "broker" ngay cả khi bạn thay đổi tên service, vì đây đề cập đến các vai trò nội bộ của Kafka (brokers và controllers).

## Cập nhật File Docker Compose

### Bước 1: Xóa Cấu hình RabbitMQ

Xóa tất cả các định nghĩa service RabbitMQ khỏi file docker-compose.

### Bước 2: Thêm Service Kafka

```yaml
services:
  kafka:
    image: apache/kafka:latest
    hostname: kafka
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_PROCESS_ROLES: broker,controller
      # Các biến môi trường Kafka bổ sung
      # Đảm bảo tất cả tham chiếu sử dụng 'kafka' làm hostname
    healthcheck:
      test: ["CMD", "nc", "-z", "kafka", "9092"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Bước 3: Cấu hình Health Check

Health check sử dụng netcat (`nc`) để xác minh Kafka đang chấp nhận kết nối trên cổng 9092:

```yaml
healthcheck:
  test: ["CMD", "nc", "-z", "kafka", "9092"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Bước 4: Cập nhật Các Service Phụ thuộc

#### Cấu hình Microservice Accounts

```yaml
accounts:
  depends_on:
    - kafka
  environment:
    SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS: kafka:9092
  # Các cấu hình khác...
```

#### Cấu hình Microservice Message

```yaml
message:
  depends_on:
    - kafka
  environment:
    SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS: kafka:9092
  # Các cấu hình khác...
```

### Bước 5: Cập nhật Tags của Image

Cập nhật tất cả các tags của service image từ **S13** lên **S14** để sử dụng phiên bản mới nhất.

## Cấu hình Ứng dụng Spring Boot

### Thay đổi Maven Dependency

Thay thế dependencies RabbitMQ bằng Kafka:

**Xóa:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-stream-rabbit</artifactId>
</dependency>
```

**Thêm:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-stream-kafka</artifactId>
</dependency>
```

### Cập nhật Application Properties

Cập nhật thông tin kết nối trong `application.yml` hoặc `application.properties`:

**Microservice Accounts:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: kafka:9092
```

**Microservice Message:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: kafka:9092
```

## Các Bước Triển khai

### Bước 1: Dừng Các Service Đang Chạy

Trước khi bắt đầu chuyển đổi:

1. **Dừng server Kafka local**: Nhấn `Ctrl+C` trong terminal đang chạy Kafka
2. **Dừng container Keycloak**: `docker stop <keycloak-container>`
3. **Dừng services IntelliJ**: Dừng tất cả microservices đang chạy trong IDE của bạn
4. **Xác minh không có xung đột**: Đảm bảo không có service nào đang sử dụng các cổng cần thiết

### Bước 2: Khởi động Docker Compose

Chạy lệnh sau để khởi động tất cả containers:

```bash
docker-compose up -d
```

Lệnh này sẽ khởi động tất cả microservices cùng với Kafka và Keycloak. Quá trình mất vài phút.

### Bước 3: Cấu hình Keycloak Client

1. **Truy cập Keycloak Admin Console**:
   - Điều hướng đến console quản trị Keycloak
   - Đăng nhập với thông tin admin

2. **Tạo Client Mới**:
   - Click "Create Client"
   - Client ID: `easybank-callcenter-cc`
   - Click "Next"

3. **Cấu hình Client Settings**:
   - Bật "Client Authentication"
   - Tắt "Standard Flow"
   - Tắt "Direct Access Grants"
   - Bật "Service Account Roles"
   - Click "Next" và "Save"

4. **Lấy Client Credentials**:
   - Điều hướng đến tab "Credentials"
   - Sao chép client secret để sử dụng trong Postman

5. **Gán Roles**:
   - Đi tới "Realm Roles"
   - Tạo role mới có tên "accounts"
   - Quay lại Clients → Your Client → "Service Account Roles"
   - Click "Assign Role"
   - Gán role "accounts"

## Kiểm thử Triển khai

### Bước 1: Lấy Access Token

Sử dụng Postman:

1. Cấu hình xác thực OAuth2
2. Sử dụng grant type client credentials
3. Client ID: `easybank-callcenter-cc`
4. Client Secret: (từ Keycloak)
5. Click "Get New Access Token"

### Bước 2: Kiểm thử API Endpoint

1. Thực hiện POST request đến accounts API
2. Bao gồm access token trong Authorization header
3. Gửi request và xác minh phản hồi thành công

### Bước 3: Xác minh Giao tiếp Kafka

#### Kiểm tra Logs của Message Microservice

```bash
docker logs <message-container-name>
```

Tìm kiếm:
- "Sending email with details..."
- "Sending SMS with details..."
- Thông tin offset consumer coordinator
- Các mục log đặc trưng của Kafka

#### Kiểm tra Logs của Accounts Microservice

```bash
docker logs <accounts-container-name>
```

Tìm kiếm:
- "Communication request successfully triggered: true"
- "Updating communication status for account number: XXX"

Các logs này xác nhận rằng giao tiếp bất đồng bộ giữa các microservices đang hoạt động qua Apache Kafka.

## Tóm tắt Các Thay đổi Chính

### 1. Maven Dependencies
- **Đã xóa**: `spring-cloud-starter-stream-rabbit`
- **Đã thêm**: `spring-cloud-starter-stream-kafka`

### 2. Cập nhật Cấu hình
- **Accounts Service**: Đã thêm cấu hình Kafka broker
- **Message Service**: Đã thêm cấu hình Kafka broker
- **Docker Compose**: Đã thay thế service RabbitMQ bằng Kafka

### 3. Thay đổi Hạ tầng
- **Đã xóa**: Service RabbitMQ khỏi Docker Compose
- **Đã thêm**: Service Kafka với health checks
- **Đã cập nhật**: Các phụ thuộc service để đợi Kafka

## Lợi ích của Apache Kafka

1. **Throughput Cao**: Hiệu suất tốt hơn cho xử lý message khối lượng lớn
2. **Độ bền**: Messages được lưu trữ vào đĩa để đảm bảo độ tin cậy
3. **Khả năng mở rộng**: Dễ dàng mở rộng theo chiều ngang với hỗ trợ partition
4. **Xử lý Stream**: Hỗ trợ native cho streaming dữ liệu thời gian thực
5. **Message Replay**: Khả năng xử lý lại messages từ bất kỳ điểm nào

## Xử lý Sự cố

### Kafka Không Khởi động
- Kiểm tra xung đột cổng (9092)
- Xác minh logs của Docker container
- Đảm bảo đủ tài nguyên hệ thống

### Microservices Không Kết nối
- Xác minh cấu hình `SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS`
- Kiểm tra kết nối mạng giữa các containers
- Đảm bảo Kafka healthy trước khi services khởi động

### Vấn đề Xác thực
- Xác minh Keycloak đang chạy và có thể truy cập
- Kiểm tra client credentials chính xác
- Đảm bảo các roles cần thiết đã được gán

## Kết luận

Migration này minh họa cách chuyển đổi từ RabbitMQ sang Apache Kafka trong kiến trúc microservices Spring Boot sử dụng:

- **Spring Cloud Functions**: Để triển khai business logic
- **Spring Cloud Stream**: Để trừu tượng hóa message broker
- **Docker Compose**: Để điều phối toàn bộ môi trường
- **OAuth2/Keycloak**: Để bảo mật microservices

Kiến trúc hướng sự kiện với Kafka cung cấp khả năng mở rộng và hiệu suất tốt hơn cho các ứng dụng doanh nghiệp trong khi duy trì sự tách biệt rõ ràng thông qua các abstraction của Spring Cloud.

## Tài nguyên

- [Hướng dẫn Confluent Kafka Docker](https://developer.confluent.io)
- Tài liệu Spring Cloud Stream
- Tài liệu Apache Kafka
- GitHub Repository: Phần 14 - Event Driven Microservices sử dụng Kafka

## Phản hồi

Phản hồi của bạn rất có giá trị! Vui lòng:
- Cung cấp đánh giá trên Udemy
- Gửi phản hồi qua LinkedIn hoặc email
- Truy cập [easybytes.com](https://easybytes.com) để biết chi tiết liên hệ
- Email: tutor@easybytes.com

---

*Hướng dẫn này là một phần của khóa học Microservices về kiến trúc hướng sự kiện với RabbitMQ và Apache Kafka.*




FILE: 36-container-orchestration-and-kubernetes-introduction.md


# Giới Thiệu Về Container Orchestration và Kubernetes

## Tổng Quan

Trong phần này, chúng ta sẽ khám phá một thách thức quan trọng trong kiến trúc microservices: **container orchestration** (điều phối container). Khi ứng dụng microservices phát triển với hàng trăm container chạy trong môi trường production, việc quản lý thủ công trở nên bất khả thi. Đây là lúc container orchestration phát huy vai trò.

## Hiểu Về Orchestration (Điều Phối)

### Ví Dụ Về Dàn Nhạc

Orchestration trong ngữ cảnh container được lấy cảm hứng từ dàn nhạc. Trong một buổi biểu diễn âm nhạc:
- Nhiều nhạc sĩ chơi các nhạc cụ khác nhau đồng thời
- Một **nhạc trưởng** đứng ở trung tâm, chỉ huy khi nào mỗi nhạc sĩ nên chơi, dừng hoặc tạm ngừng
- Nhạc trưởng đảm bảo sự hài hòa và phối hợp giữa tất cả người biểu diễn

Tương tự, trong microservices, chúng ta cần một "nhạc trưởng" để quản lý và điều phối tất cả các container.

## Container Orchestration Là Gì?

Container orchestration là việc quản lý tự động các ứng dụng được đóng gói trong container ở quy mô lớn. Trong kiến trúc microservices:

1. Chúng ta xây dựng ứng dụng Spring Boot
2. Đóng gói chúng thành Docker image
3. Chuyển đổi image thành container đang chạy bằng Docker server
4. Triển khai và quản lý các container này trong production

Trong khi quản lý 6-7 microservices có thể thực hiện thủ công, **môi trường production thường có hơn 100 microservices**, đòi hỏi orchestration tự động.

## Các Thách Thức Chính Trong Quản Lý Container

### 1. Triển Khai, Rollout và Rollback Tự Động

**Tại Sao Cần Tự Động Hóa:**
- Microservices bao gồm hàng trăm ứng dụng (so với monolithic chỉ có một)
- Triển khai thủ công không thể mở rộng
- Tự động hóa là thiết yếu cho hiệu quả

**Chiến Lược Rollout:**
- Triển khai phiên bản mới không có downtime
- Thay thế container từng cái một với Docker image mới nhất
- Ví dụ: Với accounts microservice có 3 container:
  1. Tạo container mới với image mới nhất
  2. Khi sẵn sàng, terminate container cũ
  3. Lặp lại cho các container còn lại
- **Triển khai zero-downtime** cho trải nghiệm người dùng tốt hơn

**Khả Năng Rollback:**
- Tự động quay lại phiên bản trước nếu phát hiện lỗi
- Quan trọng cho sự ổn định của production
- Giảm thiểu tác động của việc triển khai có lỗi

### 2. Khả Năng Tự Phục Hồi (Self-Healing)

**Yêu Cầu:**
- Kiểm tra sức khỏe (health check) định kỳ trên các container đang chạy
- Tự động phát hiện container không phản hồi hoặc phản hồi chậm
- Tự động terminate và thay thế container bị lỗi
- Không cần can thiệp thủ công

**Lợi Ích:**
- Cải thiện độ tin cậy
- Giảm thời gian downtime
- Tự động phục hồi từ lỗi

### 3. Auto-Scaling (Tự Động Mở Rộng)

**Thách Thức:**
- Mẫu traffic thay đổi đáng kể
- Scaling thủ công cho mỗi microservice là bất khả thi
- Cần quyết định scaling tự động và thông minh

**Chiến Lược Scaling:**
- Giám sát CPU utilization và các metric khác
- Tự động scale up khi traffic cao
- Scale down khi traffic thấp
- Tối ưu hóa tài nguyên

**Ví Dụ Thực Tế: Netflix**
- Traffic cao nhất vào tối thứ Sáu, thứ Bảy và Chủ Nhật
- Đột biến đột ngột trong kỳ nghỉ hoặc cuối tuần dài
- Scaling tự động đảm bảo streaming nội dung mượt mà
- Phân bổ tài nguyên động dựa trên nhu cầu

## Giải Pháp: Kubernetes

### Kubernetes Là Gì?

**Kubernetes** là một nền tảng container orchestration mã nguồn mở tự động hóa:
- Triển khai (Deployments)
- Rollout
- Scaling
- Quản lý các ứng dụng được đóng gói trong container

### Lịch Sử

- Ban đầu được phát triển bởi **Google**
- Sau đó được open-source
- Hiện được duy trì bởi **Cloud Native Computing Foundation (CNCF)**

### Tại Sao Kubernetes Quan Trọng Với Developers

Là một microservices developer, hiểu về Kubernetes là cần thiết:
- Bạn cần biết Kubernetes và Docker có khả năng gì
- Kiến thức cơ bản về Kubernetes được yêu cầu cho phát triển microservices hiệu quả
- Trong khi team DevOps thường quản lý Kubernetes trong production, developers được lợi từ việc hiểu cách nó hoạt động
- Kiến thức này cho phép cộng tác tốt hơn và quy trình phát triển hiệu quả hơn

### Khả Năng Chính

1. **Triển Khai Tự Động:** Đơn giản hóa quy trình triển khai
2. **Quản Lý Rollout:** Triển khai cập nhật không có downtime
3. **Rollback Tự Động:** Quay lại phiên bản ổn định khi có vấn đề
4. **Tự Phục Hồi:** Tự động thay thế container bị lỗi
5. **Auto-Scaling:** Điều chỉnh tài nguyên động dựa trên nhu cầu
6. **Load Balancing:** Phân phối traffic qua các container
7. **Quản Lý Container:** Kiểm soát tập trung tất cả container

## Kết Luận

Container orchestration với Kubernetes giải quyết các thách thức quan trọng trong kiến trúc microservices. Bằng cách tự động hóa triển khai, kích hoạt tự phục hồi, và cung cấp khả năng auto-scaling, Kubernetes cho phép các tổ chức quản lý ứng dụng được đóng gói trong container ở quy mô lớn một cách hiệu quả và đáng tin cậy.

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu hơn vào các khái niệm Kubernetes và triển khai thực tế cho phát triển microservices.

---

**Bước Tiếp Theo:** Tiếp tục bài giảng tiếp theo để tìm hiểu thêm về kiến trúc và các thành phần của Kubernetes.




FILE: 37-kubernetes-introduction-and-overview.md


# Giới Thiệu và Tổng Quan về Kubernetes

## Giới Thiệu

Kubernetes là một nền tảng điều phối container thiết yếu mà chúng ta sẽ sử dụng để triển khai và quản lý microservices. Hướng dẫn này cung cấp phần giới thiệu toàn diện về Kubernetes và các khái niệm cốt lõi của nó.

## Kubernetes là gì?

Kubernetes là một **hệ thống mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng được đóng gói trong container**. Nó đã trở thành nền tảng điều phối nổi tiếng nhất hiện có trên thị trường ngày nay.

### Các Ưu Điểm Chính

- **Trung Lập với Cloud**: Các khái niệm Kubernetes vẫn nhất quán bất kể bạn triển khai ở đâu - dù trên hệ thống local, AWS, GCP hay Azure
- **Đã Được Kiểm Nghiệm Thực Chiến**: Được phát triển và sử dụng nội bộ bởi Google trong hơn 15 năm trước khi được mã nguồn mở vào năm 2015
- **Sẵn Sàng Cho Production**: Cung cấp năng lượng cho các sản phẩm lớn của Google bao gồm YouTube, Google Photos và Gmail

## Lịch Sử và Bối Cảnh

Kubernetes được Google phát triển trong khoảng thời gian 15 năm như một dự án nội bộ. Vào khoảng năm 2015, Google quyết định mã nguồn mở công nghệ này để các tổ chức khác có thể hưởng lợi từ nó.

Thành tích đã được chứng minh trong việc xử lý lưu lượng truy cập khổng lồ của Google (không có ứng dụng nào trên thế giới nhận được lưu lượng truy cập nhiều hơn các sản phẩm của Google) cho thấy rằng Kubernetes có thể hỗ trợ bất kỳ tổ chức nào và xử lý bất kỳ lượng traffic nào.

## Khả Năng Cốt Lõi

### 1. Quản Lý Hệ Thống Phân Tán
Kubernetes giúp bạn chạy các hệ thống phân tán một cách linh hoạt, bao gồm:
- Ứng dụng cloud-native
- Kiến trúc microservices

### 2. Tự Động Mở Rộng và Chuyển Đổi Dự Phòng
- Tự động mở rộng ứng dụng dựa trên nhu cầu
- Xử lý chuyển đổi dự phòng ứng dụng một cách liền mạch
- Các mẫu triển khai đảm bảo không có downtime

### 3. Service Discovery và Cân Bằng Tải
Kubernetes hoạt động như một service discovery agent và cung cấp khả năng cân bằng tải tích hợp:
- **Thay Thế Eureka Server**: Khi sử dụng Kubernetes, bạn có thể loại bỏ nhu cầu về Eureka Server
- **Cân Bằng Tải Phía Server**: Khác với cân bằng tải phía client với Eureka, Kubernetes cung cấp cân bằng tải phía server
- Tự động phân phối traffic qua các microservices của bạn

### 4. Điều Phối Container và Storage
- Kiểm soát bất kỳ số lượng container nào
- Quản lý yêu cầu storage cho các container của bạn
- Phân bổ tài nguyên tự động

### 5. Tự Động Rollout và Rollback
- Triển khai phiên bản mới một cách an toàn
- Tự động rollback nếu phát hiện vấn đề

### 6. Tự Phục Hồi (Self-Healing)
- Tự động khởi động lại các container bị lỗi
- Thay thế và lên lịch lại các container khi node chết
- Ngừng các container không phản hồi với health check

### 7. Quản Lý Cấu Hình và Secret
- Quản lý cấu hình ứng dụng
- Lưu trữ và quản lý thông tin nhạy cảm (secrets) một cách an toàn
- Cập nhật cấu hình mà không cần build lại container image

## Tên Gọi "Kubernetes"

### Nguồn Gốc
Từ **Kubernetes** có nguồn gốc từ tiếng Hy Lạp, có nghĩa là "người lái tàu" hoặc "thủy thủ" - người điều khiển và điều hướng con tàu.

### Logo
Logo Kubernetes có hình bánh lái tàu, đại diện cho khái niệm người lái tàu. Giống như người lái tàu kiểm soát toàn bộ con tàu và điều hướng nó một cách an toàn, Kubernetes kiểm soát tất cả các container trong mạng lưới microservice của bạn.

### Phép Tương Tự Thực Tế
Trong thế giới thực, các container được vận chuyển trên tàu từ nơi này sang nơi khác, được kiểm soát bởi thuyền trưởng hoặc người lái tàu. Tương tự, Kubernetes kiểm soát các container (được phát triển với Docker hoặc các công nghệ containerization khác) và điều phối việc triển khai và quản lý chúng.

### Dạng Viết Tắt: K8s
Kubernetes thường được viết tắt là **K8s**:
- **K** = Chữ cái đầu tiên của Kubernetes
- **8** = Tám ký tự giữa K và s
- **s** = Chữ cái cuối cùng của Kubernetes

Khi bạn thấy "K8s" trong các blog hoặc website, nó đề cập đến Kubernetes.

## Tích Hợp với Microservices

Kubernetes cung cấp một số lợi thế khi làm việc với microservices:

1. **Loại bỏ nhu cầu về Eureka Server** trong service discovery
2. **Cung cấp cân bằng tải phía server** thay vì cân bằng tải phía client
3. **Xử lý điều phối container** cho tất cả các microservices
4. **Quản lý cấu hình** và secrets trên tất cả các services
5. **Đảm bảo tính khả dụng cao** và triển khai không downtime

## Kết Luận

Kubernetes là một nền tảng điều phối container mạnh mẽ, đã được chứng minh trong production, có thể đơn giản hóa đáng kể việc triển khai và quản lý các kiến trúc microservices. Cách tiếp cận trung lập với cloud của nó, kết hợp với sự hỗ trợ của Google và sự chấp nhận rộng rãi trong ngành, khiến nó trở thành lựa chọn tuyệt vời cho việc triển khai ứng dụng hiện đại.

Trong các bài giảng sắp tới, chúng ta sẽ khám phá cách thiết lập Kubernetes cho việc triển khai microservices và cách tận dụng các tính năng của nó để xây dựng các ứng dụng linh hoạt, có khả năng mở rộng.

---

**Bước Tiếp Theo**: Trong bài giảng tiếp theo, chúng ta sẽ đi sâu hơn vào kiến trúc Kubernetes và bắt đầu thiết lập Kubernetes cluster đầu tiên của chúng ta.




FILE: 38-kubernetes-gioi-thieu-kubernetes-la-gi.md


# Kubernetes là gì? - Giới thiệu nhanh

Trong bài giảng trước, tôi đã nói với các bạn rằng chúng ta sẽ sử dụng Kubernetes như một sản phẩm điều phối container (container orchestration).

Bây giờ, trong bài giảng này, hãy để tôi cố gắng giới thiệu nhanh về Kubernetes là gì.

## Tổng quan

Như chúng ta đã biết, Kubernetes là một hệ thống mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng được đóng gói trong container.

Đây là nền tảng điều phối (orchestration platform) nổi tiếng nhất hiện có trên thị trường.

Và một lợi thế nữa của Kubernetes là nó **trung lập với nền tảng đám mây** (cloud neutral).

Nếu bạn thiết lập cụm Kubernetes trong hệ thống local của mình hoặc trong AWS, GCP, Azure, bất kể bạn thiết lập ở đâu, các khái niệm của Kubernetes đều sẽ tương tự.

Đó là lý do tại sao chúng ta có thể gọi Kubernetes là một nền tảng trung lập với đám mây.

## Lịch sử và Nguồn gốc

Kubernetes này, như tôi đã nói, được phát triển và mã nguồn mở hóa bởi Google.

Vào khoảng năm 2015, Google đã quyết định mã nguồn mở hóa một trong những dự án nội bộ mà họ đã phát triển trong hơn 15 năm. Chỉ với các khái niệm Kubernetes này, đằng sau hậu trường, Google đã cố gắng chạy phần lớn các sản phẩm của họ như YouTube, Google Photos, Gmail.

Rất nhiều sản phẩm của Google tận dụng loại công nghệ Kubernetes này đằng sau hậu trường trong Google.

Và vì Kubernetes có rất nhiều tiềm năng, vào khoảng năm 2015, Google đã quyết định mã nguồn mở hóa nó để các tổ chức khác cũng có thể hưởng lợi từ framework này.

Tất nhiên, cái tên không phải là Kubernetes khi họ sử dụng nó trong Google. Khi họ cố gắng mã nguồn mở hóa sản phẩm nội bộ ra thế giới bên ngoài, thì họ đã đặt tên này, đó là Kubernetes.

Vì vậy, vì Kubernetes này đã giúp Google chạy các ứng dụng nội bộ của họ trong hơn 15 năm, chúng ta có thể tự tin nói rằng những sản phẩm này có thể giúp bất kỳ tổ chức nào và bất kỳ lượng traffic nào. Bởi vì không có ứng dụng nào trên thế giới nhận được nhiều traffic hơn các sản phẩm của Google.

Đó là lý do tại sao ngay lập tức, ngay khi điều này được phát hành cho mã nguồn mở, nhiều tổ chức đã áp dụng nó vào việc triển khai microservices của họ.

## Các khả năng chính

Vậy Kubernetes sẽ giúp bạn như thế nào:

- **Hệ thống phân tán**: Nó sẽ giúp bạn chạy các hệ thống phân tán một cách linh hoạt - các hệ thống phân tán như ứng dụng cloud native hoặc microservices.

- **Mở rộng tự động**: Nó có khả năng tự động mở rộng và xử lý failover cho ứng dụng của bạn.

- **Các mẫu triển khai**: Cung cấp các mẫu triển khai sẽ đảm bảo không có downtime cho ứng dụng của bạn.

### Service Discovery và Load Balancing

Ngoài những lợi thế này, Kubernetes cũng có khả năng hoạt động như một service discovery agent và cung cấp load balancing.

Khi chúng ta thảo luận về Eureka Server, tôi đã nói rằng với sự trợ giúp của Eureka Server, chúng ta đang thực hiện client side load balancing, trong khi với sự trợ giúp của Kubernetes, chúng ta có thể loại bỏ Eureka Server và chúng ta có thể giao việc load balancing cho Kubernetes.

Và với điều đó, chúng ta sẽ sử dụng **server side load balancing**.

Tôi sẽ chỉ cho bạn cách loại bỏ Eureka bất cứ khi nào chúng ta cố gắng sử dụng Kubernetes trong mạng lưới microservices trong các phần sắp tới.

### Điều phối Container và Storage

Và ngoài service discovery agent và load balancing, Kubernetes cũng có khả năng thực hiện điều phối container và storage.

Vì vậy, với sự trợ giúp của Kubernetes, chúng ta có thể kiểm soát bất kỳ số lượng container nào cùng với các yêu cầu storage của chúng.

### Các tính năng bổ sung

Và Kubernetes này cũng có khả năng:

- **Rollout và rollback tự động** - Như chúng ta đã thảo luận, nó cũng cung cấp khả năng tự phục hồi (self-healing).

- **Quản lý cấu hình** - Hơn nữa, với sự trợ giúp của Kubernetes, chúng ta cũng có thể cấu hình các properties và secrets cần thiết cho microservices của chúng ta.

## Tên gọi "Kubernetes"

Và cuối cùng, tôi muốn chia sẻ với bạn thông tin về cách tên Kubernetes được đặt cho framework này.

Từ **Kubernetes** có nguồn gốc từ tiếng Hy Lạp.

Trong tiếng Hy Lạp, ý nghĩa của Kubernetes là **người lái tàu hoặc phi công** (helmsman or pilot) người sẽ điều khiển con tàu.

Đó là lý do tại sao chúng ta có logo này cho Kubernetes.

Vì vậy, bất cứ khi nào bạn nhìn thấy logo này, xin lưu ý rằng nó liên quan đến Kubernetes, giống như cách người lái tàu kiểm soát toàn bộ con tàu về cách điều hướng. Rất giống nhau, với sự trợ giúp của Kubernetes, chúng ta có thể kiểm soát tất cả các container mà chúng ta có trong mạng lưới microservice của mình.

### So sánh với thế giới thực

Trong thế giới thực, các container sẽ được chuyên chở trong một con tàu như thế nào - trong một con tàu, tất cả các container của chúng ta sẽ được di chuyển từ nơi này sang nơi khác.

Và con tàu sẽ được kiểm soát như thế nào với sự trợ giúp của người lái tàu hoặc thuyền trưởng.

Vì vậy, với ví dụ thế giới thực đó, vì chúng ta sẽ kiểm soát các container được phát triển với sự trợ giúp của Docker hoặc bất kỳ công nghệ containerization nào khác, tên Kubernetes này đã được đặt cho dự án hoặc sản phẩm này.

### K8s - Dạng viết tắt

Đôi khi mọi người có thể gọi Kubernetes ở dạng viết tắt là **K8s**, vì vậy đây là cách viết tắt của Kubernetes.

Vậy tên viết tắt này xuất hiện như thế nào?

Nếu chúng ta cố gắng đếm số chữ cái giữa chữ cái đầu tiên **K** và chữ cái cuối cùng **S** trong từ Kubernetes, sẽ có **tám ký tự**.

Đó là lý do tại sao cái tên này xuất hiện, đó là K8s.

Vì vậy, bất cứ khi nào bạn thấy tên viết tắt trong bất kỳ blog hoặc trang web nào, xin lưu ý rằng họ đang đề cập đến sản phẩm Kubernetes.

## Tóm tắt

Tôi hy vọng bạn đã rõ ràng với phần giới thiệu nhanh về Kubernetes này.

Cảm ơn bạn và tôi sẽ gặp bạn trong bài giảng tiếp theo. Tạm biệt.




FILE: 39-kubernetes-architecture-and-components-detailed-guide.md


# Kiến Trúc và Thành Phần Kubernetes: Hướng Dẫn Chi Tiết

## Giới Thiệu

Trước khi triển khai các microservices vào Kubernetes cluster, điều quan trọng là phải hiểu cấu trúc bên trong của Kubernetes và các thành phần chịu tr책nhiệm cho việc triển khai tự động, rollout, scaling và các lợi ích khác mà Kubernetes cung cấp.

## Hiểu Về Kubernetes Cluster

Khi nói về Kubernetes, chúng ta đang đề cập đến một **cluster** - tập hợp các máy chủ hoặc máy ảo làm việc cùng nhau để cung cấp kết quả mong muốn cho người dùng cuối. Bên trong Kubernetes cluster, nhiều máy chủ hoặc máy ảo làm việc cùng nhau để đảm bảo các microservices hoạt động tốt mà không gặp sự cố.

### Tại Sao Chọn Kubernetes Thay Vì Docker Compose?

Bạn có thể thắc mắc: "Tại sao phải sử dụng thiết lập Kubernetes cluster phức tạp? Không thể triển khai microservices chỉ với Docker Compose sao?"

Mặc dù Docker Compose hữu ích, nhưng nó có những hạn chế đáng kể:

- **Giới Hạn Máy Chủ Đơn**: Docker Compose triển khai tất cả containers trên một máy chủ duy nhất
- **Vấn Đề Khả Năng Mở Rộng**: Ứng dụng production có thể có hàng trăm microservices không thể đặt hết trên một máy chủ
- **Không Có Tự Động Hóa**: Docker và Docker Compose thiếu khả năng triển khai tự động, rollout và scaling
- **Công Việc Thủ Công**: Chỉ sử dụng containers và Docker trong môi trường production đòi hỏi nhiều công việc thủ công

Kubernetes giải quyết các vấn đề này bằng cách cung cấp **môi trường phân tán đa máy chủ** nơi các microservices có thể được triển khai trên nhiều máy chủ (nodes) khác nhau trong cluster, với khả năng điều phối container tích hợp sẵn.

> **Hiểu Biết Quan Trọng**: Containers không giải quyết mọi vấn đề. Không có điều phối, việc quản lý containers trong môi trường production có thể trở nên quá tải.

## Kiến Trúc Kubernetes Cluster

Một Kubernetes cluster bao gồm hai loại nodes:

1. **Master Node (Control Plane)**: Chịu trách nhiệm kiểm soát và duy trì toàn bộ Kubernetes cluster
2. **Worker Nodes**: Chịu trách nhiệm xử lý traffic và chạy các microservices thực tế

## Các Thành Phần Của Master Node

Master Node (còn gọi là Control Plane) chứa một số thành phần quan trọng:

### 1. Kube API Server

**Kube API Server** là thành phần quản lý trung tâm:

- Cung cấp APIs để tương tác với Kubernetes cluster
- Tạo điều kiện giao tiếp giữa master nodes và worker nodes
- Nhận hướng dẫn từ các nguồn bên ngoài

**Các Cách Tương Tác Với Kubernetes Cluster:**
- **Admin UI**: Giao diện dashboard của Kubernetes
- **kubectl CLI**: Giao diện dòng lệnh để thực thi các lệnh Kubernetes

Người dùng cung cấp hướng dẫn cho Kubernetes thông qua cấu hình YAML, chỉ định các chi tiết như:
- Microservice nào cần triển khai
- Số lượng replicas cần thiết
- Docker image cần sử dụng

### 2. Scheduler

Thành phần **Scheduler**:

- Nhận yêu cầu từ Kube API Server
- Xác định worker node phù hợp nhất cho việc triển khai
- Thực hiện tính toán để xác định node tốt nhất dựa trên:
  - Băng thông khả dụng
  - Khối lượng công việc hiện tại
  - Tài nguyên khả dụng

**Quy Trình Ví Dụ:**
1. Người dùng chỉ thị: "Triển khai accounts microservice"
2. Kube API Server chuyển hướng dẫn đến Scheduler
3. Scheduler xác định worker node tối ưu
4. Scheduler gửi hướng dẫn triển khai về Kube API Server
5. Kube API Server giao tiếp với worker node được chọn

### 3. Controller Manager

**Controller Manager**:

- Liên tục theo dõi containers và worker nodes trong cluster
- Giám sát trạng thái sức khỏe của tất cả các thành phần
- Đảm bảo **trạng thái thực tế** khớp với **trạng thái mong muốn**
- Tự động thay thế các containers hoặc worker nodes có vấn đề

**Quản Lý Trạng Thái Mong Muốn:**
- Người dùng chỉ định: "Luôn chạy 3 instances của accounts microservice"
- Controller Manager thực hiện kiểm tra sức khỏe thường xuyên
- Nếu một instance bị lỗi, Controller Manager sẽ:
  - Chấm dứt container có vấn đề
  - Khởi chạy container mới để duy trì 3 instances khỏe mạnh

### 4. etcd

**etcd** đóng vai trò là bộ não của Kubernetes cluster:

- Hoạt động như cơ sở dữ liệu key-value phân tán
- Lưu trữ tất cả thông tin của Kubernetes cluster
- Duy trì dữ liệu cấu hình và trạng thái

**Ví Dụ Sử Dụng:**
- Controller Manager truy vấn etcd để hiểu số lượng replicas mong muốn
- Kube API Server ghi hướng dẫn của người dùng vào etcd
- Scheduler và các thành phần khác tham chiếu etcd trong các hoạt động

## Các Thành Phần Của Worker Node

Worker nodes chứa các thành phần chạy các workloads thực tế:

### 1. Kubelet

**Kubelet** là agent chạy trên tất cả worker nodes:

- Đóng vai trò cầu nối giao tiếp giữa master và worker nodes
- Nhận hướng dẫn triển khai từ master node thông qua Kube API Server
- Thực thi lệnh để triển khai và quản lý containers

**Ví Dụ:**
- Master node chỉ thị: "Triển khai accounts microservice với 3 replicas"
- Kubelet nhận và thực thi các hướng dẫn này

### 2. Container Runtime

**Container Runtime**:

- Cung cấp môi trường để chạy containers
- Thường là Docker, nhưng có thể là các container runtimes khác
- Phải được cài đặt trên tất cả worker nodes để cluster hoạt động

### 3. Pod

**Pod** là đơn vị triển khai nhỏ nhất trong Kubernetes:

- Được tạo bên trong worker nodes
- Chứa một hoặc nhiều containers
- Cung cấp sự cô lập giữa các microservices khác nhau

**Đặc Điểm Chính:**
- Worker nodes là các máy chủ/VMs lớn, nhưng containers không triển khai trực tiếp vào chúng
- Kubernetes tạo pods bên trong worker nodes
- Containers chạy bên trong pods

**Mô Hình Sử Dụng Pod:**

**Một Container Trên Mỗi Pod (Phổ Biến Nhất):**
- Mỗi microservice (accounts, cards, loans) chạy trong pod riêng
- Một container ứng dụng chính trên mỗi pod

**Nhiều Containers Trên Mỗi Pod (Sidecar Pattern):**
- Container ứng dụng chính + containers hỗ trợ/tiện ích
- Containers hỗ trợ giúp đỡ hoạt động của container chính
- Tất cả containers trong pod chia sẻ cùng một vòng đời

> **Quan Trọng**: Một pod thường chỉ chứa một container ứng dụng chính. Nhiều containers trong một pod được sử dụng cho các dịch vụ hỗ trợ (sidecar pattern).

### 4. Kube Proxy

**Kube Proxy** xử lý mạng:

- Cho phép containers giao tiếp với thế giới bên ngoài
- Tạo điều kiện giao tiếp giữa các containers trong cluster
- Có thể hạn chế giao tiếp chỉ trong nội bộ cluster

## Quy Trình Kubernetes Hoàn Chỉnh

Đây là cách tất cả các thành phần làm việc cùng nhau:

1. **Đầu Vào Người Dùng**: Hướng dẫn được cung cấp qua kubectl CLI hoặc Admin UI
2. **Kube API Server**: Nhận và xử lý hướng dẫn
3. **etcd**: Lưu trữ cấu hình và trạng thái mong muốn
4. **Scheduler**: Xác định worker node tối ưu cho triển khai
5. **Worker Node**: Kubelet nhận hướng dẫn triển khai
6. **Container Runtime**: Tạo và chạy containers bên trong pods
7. **Kube Proxy**: Xử lý mạng và phơi bày dịch vụ
8. **Controller Manager**: Liên tục giám sát và duy trì trạng thái mong muốn

## Khả Năng Mở Rộng và Tính Khả Dụng Cao

- **Nhiều Master Nodes**: Các cluster lớn yêu cầu nhiều master nodes
- **Nhiều Worker Nodes**: Có thể thêm bất kỳ số lượng worker nodes nào
- **Phân Phối Tải**: Tương tự như quản lý dự án (tỷ lệ 1 quản lý : 10 nhà phát triển)
- **Khả Năng Chịu Lỗi**: Cơ chế chuyển đổi dự phòng và phục hồi tự động

> **Lưu Ý**: Một master node đơn không thể xử lý số lượng worker nodes không giới hạn. Mở rộng master nodes của bạn tỷ lệ thuận với worker nodes.

## Tóm Tắt

Kubernetes cung cấp nền tảng điều phối container mạnh mẽ thông qua kiến trúc được thiết kế tốt:

- **Master Node (Control Plane)**: Quản lý cluster với Kube API Server, Scheduler, Controller Manager và etcd
- **Worker Nodes**: Chạy các workloads thực tế với Kubelet, Container Runtime, Pods và Kube Proxy
- **Tự Động Hóa**: Khả năng triển khai tự động, scaling và tự phục hồi
- **Khả Năng Mở Rộng**: Kiến trúc phân tán hỗ trợ hàng trăm microservices

Hiểu các thành phần này là rất quan trọng trước khi triển khai microservices vào Kubernetes cluster. Khi bạn làm việc thực hành với triển khai Kubernetes, các khái niệm này sẽ trở nên rõ ràng và thực tế hơn.

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- Tạo một Kubernetes cluster
- Triển khai microservices vào cluster
- Xem các khái niệm kiến trúc này trong thực tế

Đảm bảo xem lại các thành phần này và mối quan hệ của chúng trước khi tiếp tục để đảm bảo sự rõ ràng.

---

*Hướng dẫn này bao gồm kiến trúc cơ bản của Kubernetes để triển khai các Java Spring Boot microservices trong môi trường production.*




FILE: 4-registering-client-application-with-keycloak-auth-server.md


# Đăng Ký Ứng Dụng Client với Keycloak Auth Server

## Tổng Quan

Hướng dẫn này trình bày cách đăng ký một ứng dụng client bên ngoài với máy chủ ủy quyền Keycloak sử dụng luồng OAuth2 Client Credentials grant type. Điều này rất quan trọng cho việc giao tiếp backend-to-backend trong kiến trúc microservices.

## Yêu Cầu Tiên Quyết

- Máy chủ xác thực Keycloak đã được thiết lập trong mạng lưới microservices Easy Bank
- Quyền truy cập Admin vào bảng điều khiển Keycloak
- Hiểu biết về OAuth2 framework và OpenID Connect

## Kịch Bản

Một ứng dụng client bên ngoài (ví dụ: Ứng dụng Call Center của EasyBank) cần giao tiếp với mạng lưới microservices Easy Bank thông qua các API backend. Để thực hiện điều này, ứng dụng phải:

1. Đăng ký với máy chủ ủy quyền
2. Lấy thông tin đăng nhập client (Client ID và Client Secret)
3. Sử dụng các thông tin này để yêu cầu access token
4. Sử dụng access token để gọi gateway server (resource server)

## Quy Trình Đăng Ký

### Bước 1: Truy Cập Keycloak Admin Console

1. Đăng nhập vào bảng điều khiển quản trị Keycloak
2. Đảm bảo bạn đang ở đúng realm (realm mặc định cho Easy Bank)
3. Điều hướng đến mục **Clients** từ menu bên trái

### Bước 2: Tạo Client Mới

1. Nhấp vào nút **Create client**
2. Cấu hình các thiết lập sau:

#### Loại Client
- Chọn **OpenID Connect**
- Điều này tự động bao gồm hỗ trợ OAuth2 framework, vì OpenID Connect được xây dựng dựa trên OAuth2

#### Client ID
- Nhập một định danh client duy nhất: `easybank-callcenter-cc`
- Hậu tố `-cc` cho biết loại Client Credentials grant type
- Đây hoạt động như tên người dùng cho ứng dụng client

#### Tên và Mô Tả Client
- **Name**: EasyBank Call Center App
- **Description**: EasyBank Call Center App
- Những thông tin này cung cấp mô tả dễ hiểu về client

### Bước 3: Cấu Hình Thiết Lập Xác Thực

1. Nhấp **Next** để chuyển đến thiết lập xác thực

#### Bật Client Authentication
- **Bật**: Client authentication
- Điều này đảm bảo client phải tự xác thực bằng thông tin đăng nhập trước khi nhận access token
- Ngăn chặn các client không được ủy quyền truy cập vào auth server

#### Chọn Luồng Xác Thực
- **Bật**: Service Account Roles
- **Tắt**: Standard flow
- **Tắt**: Direct access grants

**Quan trọng**: Service Account Roles đặc biệt hỗ trợ luồng Client Credentials grant type, được thiết kế cho giao tiếp backend-to-backend qua REST APIs.

### Bước 4: Hoàn Tất Cấu Hình

1. Nhấp **Next** để tiến đến thiết lập cuối cùng
2. Để trống các trường sau:
   - Root URL
   - Home URL
3. Nhấp **Save** để tạo client

## Thông Tin Đăng Nhập Client

Sau khi lưu, client đã được đăng ký thành công với máy chủ ủy quyền.

### Lấy Client Secret

1. Điều hướng đến tab **Credentials** của client vừa tạo
2. **Client Secret** được tự động tạo bởi Keycloak
3. Nhấp vào biểu tượng con mắt để hiển thị secret

### Phương Thức Xác Thực

- **Phương thức mặc định**: Client ID và Secret
- Các phương thức thay thế có sẵn:
  - Signed JWT
  - Xác thực dựa trên certificate

## Sử Dụng Thông Tin Đăng Nhập Client

Để lấy access token, ứng dụng client bên ngoài phải cung cấp:

- **Client ID**: `easybank-callcenter-cc`
- **Client Secret**: (Secret được tạo từ Keycloak)

Những thông tin đăng nhập này sẽ được sử dụng trong luồng OAuth2 Client Credentials để yêu cầu access token từ máy chủ ủy quyền.

## Tóm Tắt

Bạn đã đăng ký thành công một ứng dụng client bên ngoài với máy chủ xác thực Keycloak. Client hiện đã được cấu hình để sử dụng luồng Client Credentials grant type cho giao tiếp backend-to-backend an toàn trong mạng lưới microservices Easy Bank.

## Bước Tiếp Theo

Trong phần tiếp theo, chúng ta sẽ trình bày cách lấy access token từ auth server bằng cách sử dụng thông tin đăng nhập client này.

---

**Các Chủ Đề Liên Quan:**
- Luồng OAuth2 Client Credentials Grant Flow
- Bảo Mật Microservices với OAuth2
- Thiết Lập Keycloak Authorization Server




FILE: 40-setting-up-local-kubernetes-cluster-with-docker-desktop.md


# Thiết Lập Kubernetes Cluster Cục Bộ với Docker Desktop

## Tổng Quan

Trong hướng dẫn này, chúng ta sẽ tìm hiểu cách thiết lập một Kubernetes cluster cục bộ sử dụng Docker Desktop. Cách tiếp cận này cung cấp môi trường Kubernetes giống production mà không cần đối mặt với độ phức tạp và chi phí của việc triển khai trên cloud trong giai đoạn học tập.

## Tại Sao Chọn Docker Desktop Thay Vì Minikube?

Mặc dù Minikube là lựa chọn phổ biến cho Kubernetes cluster cục bộ, chúng tôi khuyến nghị sử dụng Docker Desktop vì các lý do sau:

- **Tính Nhất Quán Của Lệnh**: Kubernetes trên Docker Desktop sử dụng các lệnh giống như Kubernetes cluster trong môi trường production
- **Không Có Sự Khác Biệt Về Kiến Thức**: Minikube có các lệnh đặc biệt khác với môi trường production
- **Tích Hợp Liền Mạch**: Nếu bạn đã cài đặt Docker Desktop, việc bật Kubernetes rất đơn giản

## Yêu Cầu Trước Khi Bắt Đầu

- Docker Desktop đã được cài đặt trên hệ thống của bạn
- Hiểu biết cơ bản về các khái niệm Kubernetes

## Các Bước Cài Đặt

### 1. Bật Kubernetes trong Docker Desktop

Làm theo các bước sau để bật Kubernetes:

1. Mở Docker Dashboard
2. Nhấp vào **Settings** (góc trên bên phải)
3. Chọn **Kubernetes** từ thanh bên trái
4. Đánh dấu vào **Enable Kubernetes**
5. **KHÔNG** đánh dấu vào "Show system containers" (trừ khi bạn cần xem các container nội bộ của Kubernetes)
6. Nhấp **Apply and Restart**

Docker Desktop sẽ khởi động lại và tạo một Kubernetes cluster cục bộ. Quá trình này có thể mất vài phút.

**Tài Liệu Tham Khảo**: https://docs.docker.com/desktop/kubernetes

### 2. Hiểu Về Cấu Hình Cluster Cục Bộ

Kubernetes cluster cục bộ được tạo bởi Docker Desktop có các đặc điểm sau:

- **Single Node Cluster**: Do hạn chế về tài nguyên hệ thống cục bộ (bộ nhớ và CPU), cluster chỉ bao gồm một node
- **Vai Trò Kết Hợp**: Node duy nhất này đóng vai trò cả master node và worker node
- **Container Ẩn**: Các container hệ thống của Kubernetes được ẩn khỏi các lệnh Docker như `docker ps` theo mặc định
- **Chỉ Báo Trạng Thái**: Khi Kubernetes đang chạy, bạn sẽ thấy chỉ báo trạng thái ở cuối Docker Desktop hiển thị "Kubernetes is running"

### 3. Xác Minh Cài Đặt Kubernetes

Sau khi cài đặt, bạn sẽ thấy hai chỉ báo trạng thái ở góc dưới bên trái của Docker Desktop:
- Docker engine đang chạy
- Kubernetes đang chạy

Bạn cũng sẽ thấy một phần **Kubernetes** mới trong menu Docker Desktop.

## Thiết Lập kubectl

`kubectl` là công cụ dòng lệnh được sử dụng để tương tác với các Kubernetes cluster. Docker Desktop tự động cài đặt kubectl trong quá trình thiết lập Kubernetes.

### Xác Minh Cài Đặt kubectl

Binary kubectl được cài đặt tại:
- **Mac**: Đường dẫn chuẩn do Docker Desktop thiết lập
- **Windows**: Đường dẫn chuẩn do Docker Desktop thiết lập

Đảm bảo vị trí này được thêm vào biến môi trường PATH của bạn (tương tự như JAVA_HOME và MAVEN_HOME).

### Kiểm Tra Các Lệnh kubectl

Chạy các lệnh sau để xác minh cài đặt của bạn:

#### 1. Lấy Danh Sách Contexts

```bash
kubectl config get-contexts
```

Lệnh này liệt kê tất cả các context Kubernetes có sẵn. Bạn sẽ thấy `docker-desktop` là context mặc định (được đánh dấu bằng dấu sao `*` trong cột CURRENT).

**Context**: Một môi trường cô lập cho phép ứng dụng client hoặc CLI của bạn tương tác với Kubernetes cluster.

#### 2. Lấy Danh Sách Clusters

```bash
kubectl config get-clusters
```

Lệnh này hiển thị tất cả các Kubernetes cluster đang chạy trên hệ thống cục bộ của bạn. Bạn sẽ thấy `docker-desktop` được liệt kê.

#### 3. Đặt Context Mặc Định (nếu cần)

Nếu bạn có nhiều context (ví dụ từ Minikube hoặc các cách cài đặt Kubernetes khác), hãy đặt Docker Desktop làm mặc định:

```bash
kubectl config use-context docker-desktop
```

**Lưu Ý**: Lệnh này chỉ cần thiết nếu bạn có nhiều context. Nếu docker-desktop đã được đánh dấu là current, bước này là tùy chọn.

#### 4. Xác Minh Nodes

```bash
kubectl get nodes
```

Lệnh này xác nhận số lượng node trong cluster của bạn. Bạn sẽ thấy một node được liệt kê, vì thiết lập cục bộ là single-node cluster.

**Ví Dụ Output**:
```
NAME             STATUS   ROLE           AGE   VERSION
docker-desktop   Ready    control-plane  5m    v1.x.x
```

## So Sánh Production vs Local Cluster

| Tính Năng | Local Cluster (Docker Desktop) | Production Cluster (Cloud) |
|-----------|-------------------------------|----------------------------|
| Số Lượng Nodes | 1 (kết hợp master + worker) | Nhiều (ví dụ: 1 master + 3 workers) |
| Sử Dụng Tài Nguyên | Giới hạn bởi hệ thống cục bộ | Có thể mở rộng theo yêu cầu |
| Chi Phí | Miễn phí | Trả theo sử dụng |
| Trường Hợp Sử Dụng | Phát triển, kiểm thử, học tập | Triển khai production |

## Xử Lý Sự Cố

Nếu các lệnh kubectl không hoạt động:

1. Xác minh kubectl đã được cài đặt: Kiểm tra xem binary kubectl có tồn tại trong đường dẫn cài đặt không
2. Cập nhật biến PATH: Đảm bảo thư mục cài đặt kubectl nằm trong PATH của hệ thống
3. Khởi động lại terminal: Đóng và mở lại terminal sau khi thay đổi PATH
4. Xác minh Docker Desktop: Đảm bảo Docker Desktop đang chạy và Kubernetes đã được bật

## Tắt Kubernetes

Nếu bạn cần tắt Kubernetes cluster:

1. Mở Docker Desktop Settings
2. Vào phần Kubernetes
3. Bỏ đánh dấu **Enable Kubernetes**
4. Nhấp **Apply and Restart**

## Bước Tiếp Theo

Bây giờ bạn đã có Kubernetes cluster cục bộ, bạn có thể:

- Khám phá các khái niệm Kubernetes một cách thực hành
- Triển khai microservices lên cluster
- Kiểm thử cấu hình trước khi chuyển sang môi trường cloud
- Học các lệnh kubectl trong môi trường an toàn

Sau khi đã quen thuộc với các khái niệm Kubernetes ở local, bạn có thể tiến hành tạo một Kubernetes cluster production-ready trong môi trường cloud với nhiều node.

## Tóm Tắt

Thiết lập Kubernetes cluster cục bộ với Docker Desktop cung cấp:
- Môi trường giống production để học tập
- Cách hiệu quả về chi phí để khám phá Kubernetes
- Quy trình thiết lập dễ dàng nếu Docker Desktop đã được cài đặt
- Cú pháp lệnh nhất quán với các cluster production

Thiết lập cục bộ này lý tưởng để hiểu các khái niệm Kubernetes trước khi triển khai lên môi trường cloud nơi thời gian chạy cluster sẽ phát sinh chi phí.

---

**Từ Khóa**: Kubernetes, Docker Desktop, kubectl, Local Cluster, Microservices, Container Orchestration, Môi Trường Phát Triển




FILE: 41-setting-up-kubernetes-dashboard-complete-guide.md


# Hướng Dẫn Cài Đặt Kubernetes Dashboard - Đầy Đủ Chi Tiết

## Giới Thiệu

Cho đến nay, chúng ta đã tương tác với Kubernetes cluster chủ yếu thông qua các lệnh kubectl từ terminal cục bộ. Tuy nhiên, có một cách tiếp cận mạnh mẽ khác: sử dụng Admin UI để tương tác với Kubernetes cluster và giám sát trạng thái tổng thể của nó.

Việc có quyền truy cập vào UI cho Kubernetes cluster của bạn sẽ làm cho việc quản lý cluster trở nên dễ dàng hơn rất nhiều. Trong hướng dẫn này, chúng ta sẽ đi qua toàn bộ quy trình thiết lập Kubernetes Dashboard - giao diện quản trị của Kubernetes.

## Tìm Hiểu Về Kubernetes Dashboard

Kubernetes Dashboard là giao diện người dùng dựa trên web cho phép bạn:
- Xem trạng thái tổng thể của Kubernetes cluster
- Quản lý và triển khai ứng dụng
- Giám sát tài nguyên và khối lượng công việc
- Khắc phục sự cố các ứng dụng container

**Lưu Ý Quan Trọng:** Dashboard UI không được triển khai mặc định trong bất kỳ Kubernetes cluster nào, vì vậy chúng ta cần thực hiện các bước cài đặt cụ thể.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, hãy đảm bảo bạn có:
- Docker Desktop được cài đặt với phiên bản mới nhất
- Kubernetes cluster cục bộ đang chạy
- Truy cập vào terminal với kubectl đã được cấu hình

## Cài Đặt Helm Package Manager

### Helm Là Gì?

Helm là trình quản lý gói (package manager) cho Kubernetes, tương tự như npm hoạt động trong hệ sinh thái JavaScript. Chúng ta sẽ sử dụng Helm để cài đặt Kubernetes Dashboard.

### Các Bước Cài Đặt Theo Hệ Điều Hành

#### Người Dùng macOS

Nếu bạn đã cài đặt Homebrew (package manager được khuyến nghị cho macOS):

```bash
brew install helm
```

#### Người Dùng Windows

1. Đầu tiên, cài đặt Chocolatey package manager bằng cách truy cập trang web chính thức
2. Làm theo hướng dẫn cài đặt trên trang web Chocolatey
3. Sau khi Chocolatey được cài đặt, chạy lệnh:

```powershell
choco install kubernetes-helm
```

### Xác Minh Cài Đặt Helm

Sau khi cài đặt, xác minh rằng Helm đã được cài đặt đúng cách:

```bash
helm version
```

Bạn sẽ thấy đầu ra hiển thị phiên bản hiện tại của Helm được cài đặt trên hệ thống của bạn.

## Cài Đặt Kubernetes Dashboard

### Bước 1: Thêm Helm Repository

Thực thi lệnh sau để thêm Kubernetes Dashboard Helm repository:

```bash
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
```

### Bước 2: Cài Đặt Dashboard

Chạy lệnh cài đặt:

```bash
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```

Quá trình cài đặt sẽ mất 2-3 phút. Sau khi hoàn thành, bạn sẽ thấy thông báo xác nhận.

**Lưu Ý:** Nếu gặp cảnh báo hoặc lỗi, hãy đảm bảo bạn có Docker Desktop mới nhất và Kubernetes cluster cục bộ đang chạy.

### Bước 3: Truy Cập Dashboard

Để expose dashboard nhằm truy cập cục bộ, chạy lệnh:

```bash
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```

**Quan Trọng:** Giữ cửa sổ terminal này mở. Việc đóng nó hoặc thực thi các lệnh khác sẽ dừng port forwarding, khiến dashboard không thể truy cập được.

### Bước 4: Mở Dashboard Trong Trình Duyệt

Truy cập dashboard tại: `https://localhost:8443`

Bạn có thể thấy cảnh báo chứng chỉ vì cluster tạo chứng chỉ tự ký (self-signed certificate). Đối với thử nghiệm cục bộ, điều này có thể chấp nhận được:
1. Nhấp vào "Show details" (Hiển thị chi tiết) hoặc "Advanced" (Nâng cao)
2. Nhấp vào "Visit this website" (Truy cập trang web này) hoặc "Proceed" (Tiếp tục)

Bây giờ bạn sẽ thấy trang đăng nhập Kubernetes Dashboard yêu cầu token.

## Lưu Ý Về Số Cổng

**Quan Trọng:** Trong các phiên bản hoặc phương pháp cài đặt khác nhau, dashboard có thể khả dụng trên các cổng khác nhau:
- Phương pháp hiện tại dựa trên Helm: Cổng **8443**
- Phương pháp cũ/không còn dùng: Cổng **8001**

Đừng lo lắng về sự khác biệt về số cổng trong các hướng dẫn hoặc video khác nhau.

## Tạo Admin User Và Xác Thực

### Bước 1: Tạo Service Account

Service Account là thông tin xác thực cho một người dùng cụ thể trong Kubernetes.

Tạo file có tên `dashboard-admin-user.yaml`:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

Áp dụng cấu hình:

```bash
kubectl apply -f dashboard-admin-user.yaml
```

### Bước 2: Tạo Cluster Role Binding

Để cấp quyền admin cho service account, tạo file có tên `dashboard-role-binding.yaml`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

Áp dụng cấu hình:

```bash
kubectl apply -f dashboard-role-binding.yaml
```

**Hiểu Về Cấu Hình:**
- **apiVersion**: Chỉ định phiên bản API cho RBAC (rbac.authorization.k8s.io/v1)
- **kind**: ClusterRoleBinding liên kết cluster role với một subject
- **roleRef**: Tham chiếu đến cluster-admin role (role được định nghĩa trước có quyền truy cập đầy đủ cluster)
- **subjects**: Chỉ định ServiceAccount để liên kết role

### Tùy Chọn Xác Thực 1: Token Tạm Thời

Tạo token tạm thời:

```bash
kubectl -n kubernetes-dashboard create token admin-user
```

Lệnh này tạo token ngắn hạn sẽ hết hạn nếu không được sử dụng.

### Tùy Chọn Xác Thực 2: Token Dài Hạn (Được Khuyến Nghị)

Để có token vĩnh viễn, tạo tài nguyên Secret.

Tạo file có tên `secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "admin-user"
type: kubernetes.io/service-account-token
```

Áp dụng cấu hình:

```bash
kubectl apply -f secret.yaml
```

Lấy token:

```bash
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```

**Quan Trọng:** Khi sao chép token, đừng bao gồm bất kỳ ký tự theo sau nào như `%`.

Lưu token này một cách an toàn - bạn có thể sử dụng nó nhiều lần để truy cập dashboard mà không cần tạo token mới mỗi lần.

## Truy Cập Dashboard

1. Dán token của bạn vào trang đăng nhập dashboard
2. Chọn tùy chọn "Token"
3. Nhấp "Sign In" (Đăng nhập)

Bây giờ bạn đã có quyền truy cập đầy đủ vào Kubernetes Dashboard!

## Hiểu Về Các Khái Niệm Kubernetes

### Namespaces

Namespaces là các khu vực bị cô lập trong Kubernetes cluster, tương tự như có môi trường dev, QA và production. Chúng giúp tổ chức và phân tách tài nguyên.

Namespace `kubernetes-dashboard` chứa tất cả các tài nguyên liên quan đến chính dashboard UI.

### Service Accounts

Service Accounts là thông tin xác thực cho các process chạy trong pods hoặc cho người dùng truy cập cluster. Chúng xác định danh tính và quyền hạn.

### Cluster Roles Và Bindings

- **ClusterRole**: Định nghĩa quyền hạn (những hành động nào có thể được thực hiện)
- **ClusterRoleBinding**: Gán roles cho users hoặc service accounts
- **cluster-admin**: Role được định nghĩa trước với quyền truy cập quản trị đầy đủ vào cluster

### Secrets

Secrets lưu trữ thông tin nhạy cảm như mật khẩu, tokens và keys một cách an toàn trong Kubernetes.

## Khám Phá Dashboard

Sau khi đăng nhập, bạn có thể khám phá:

### Điều Hướng

1. **Namespace Selector**: Chuyển đổi giữa các namespaces khác nhau (mặc định là "default")
2. **Workloads**: Xem Deployments, Pods, ReplicaSets, v.v.
3. **Service Accounts**: Trong namespace kubernetes-dashboard, bạn sẽ thấy tài khoản admin-user
4. **Cluster Role Bindings**: Xem các phân công role và quyền hạn

### Ví Dụ: Xem Các Thành Phần Dashboard

Điều hướng đến namespace `kubernetes-dashboard` để thấy:
- **Deployments**: Các instance đang chạy của ứng dụng dashboard
- **Pods**: Các instance riêng lẻ chạy mã dashboard
- **ReplicaSets**: Đảm bảo số lượng bản sao pod mong muốn

Các thành phần này tồn tại vì chính dashboard UI chạy như một ứng dụng trong Kubernetes.

### Hiểu Về Quyền Hạn

Để xem quyền hạn của admin-user:
1. Đi đến **Service Accounts** trong namespace kubernetes-dashboard
2. Nhấp vào **admin-user**
3. Điều hướng đến **Cluster Role Bindings**
4. Nhấp vào binding **admin-user**
5. Xem chi tiết role **cluster-admin**

Role cluster-admin hiển thị:
- **Resources**: `*` (tất cả tài nguyên)
- **Verbs**: `*` (tất cả hành động)
- **API Groups**: `*` (tất cả nhóm API)

Điều này có nghĩa là người dùng có quyền truy cập super-user với đầy đủ quyền hạn trên toàn bộ cluster.

## Thực Hành Tốt Nhất

1. **Bảo Mật**: Trong môi trường production, tránh sử dụng role cluster-admin. Tạo các role cụ thể với quyền hạn giới hạn dựa trên nguyên tắc quyền tối thiểu (principle of least privilege).

2. **Quản Lý Token**: Lưu trữ token dài hạn của bạn một cách an toàn. Đừng chia sẻ nó hoặc commit nó vào version control.

3. **Truy Cập Dashboard**: Trong production, sử dụng các cơ chế xác thực phù hợp và hạn chế truy cập dashboard thông qua network policies.

4. **Cập Nhật Thường Xuyên**: Thường xuyên cập nhật Helm, kubectl và Kubernetes Dashboard để có các bản vá bảo mật và tính năng mới.

## Khắc Phục Sự Cố

### Không Thể Truy Cập Dashboard
- Đảm bảo lệnh port-forward đang chạy
- Kiểm tra xem Kubernetes cluster của bạn có đang chạy không
- Xác minh Docker Desktop đã được cập nhật

### Lỗi Token Không Hợp Lệ
- Đảm bảo bạn đã sao chép toàn bộ token mà không có ký tự theo sau
- Xác minh token chưa hết hạn (nếu sử dụng token ngắn hạn)
- Xác nhận secret đã được tạo thành công

### Bị Từ Chối Quyền
- Xác minh ClusterRoleBinding đã được áp dụng đúng cách
- Kiểm tra xem service account có tồn tại trong namespace đúng không

## Tóm Tắt

Bạn đã thiết lập thành công Kubernetes Dashboard với:
1. ✅ Helm package manager đã được cài đặt
2. ✅ Kubernetes Dashboard đã được triển khai
3. ✅ Admin service account được tạo với quyền cluster-admin
4. ✅ Token xác thực dài hạn đã được tạo
5. ✅ Truy cập đầy đủ vào Kubernetes Dashboard UI

Dashboard cung cấp một cách trực quan để quản lý và giám sát Kubernetes cluster của bạn, bổ sung cho giao diện dòng lệnh kubectl.

## Các Bước Tiếp Theo

- Khám phá các tính năng và views khác nhau của dashboard
- Tìm hiểu chi tiết hơn về Helm
- Thực hành triển khai ứng dụng thông qua dashboard
- Nghiên cứu Kubernetes RBAC (Role-Based Access Control) cho bảo mật production

---

**Tài Liệu Tham Khảo:**
- [Tài Liệu Kubernetes Dashboard Chính Thức](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)
- [Trang Web Helm Chính Thức](https://helm.sh)
- Tài Liệu Kubernetes RBAC

Cảm ơn bạn đã theo dõi hướng dẫn này! Chúc bạn học Kubernetes vui vẻ!




FILE: 42-deploying-config-server-to-kubernetes-cluster.md


# Triển khai Config Server lên Kubernetes Cluster

## Tổng quan

Trong hướng dẫn này, chúng ta sẽ học cách triển khai microservice Config Server vào Kubernetes cluster cục bộ. Đây thường là microservice đầu tiên bạn nên triển khai khi thiết lập kiến trúc microservices trong Kubernetes, vì các dịch vụ khác phụ thuộc vào nó để quản lý cấu hình.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster cục bộ đang chạy thành công
- Các Docker image đã được build cho microservices (phần trước)
- Hiểu biết cơ bản về file cấu hình YAML

## Bắt đầu

### 1. Thiết lập cấu trúc dự án

Đầu tiên, tạo cấu trúc thư mục cần thiết cho các cấu hình Kubernetes:

```bash
# Di chuyển đến workspace của bạn
cd section_15

# Tạo thư mục Kubernetes
mkdir Kubernetes
cd Kubernetes
```

### 2. Tạo file Kubernetes Manifest

Tạo file YAML mới cho việc triển khai Config Server:

```bash
touch configserver.yaml
```

**Lưu ý:** Trên Windows, nếu lệnh `touch` không hoạt động, hãy tạo file thủ công trong thư mục của bạn.

## Hiểu về cấu hình Kubernetes

### Các khái niệm chính

- **Kubernetes Manifest Files**: Các file cấu hình cung cấp hướng dẫn cho Kubernetes về cách triển khai và expose microservices
- **Docker Compose vs Kubernetes**: Kubernetes không hiểu định dạng Docker Compose; nó yêu cầu cú pháp YAML riêng
- **Trách nhiệm DevOps**: Trong các dự án thực tế, đội ngũ DevOps hoặc platform thường viết các cấu hình này, nhưng developers nên hiểu cú pháp cơ bản

### Cấu trúc cấu hình

File Kubernetes manifest bao gồm hai phần chính:

1. **Deployment Configuration** - Định nghĩa cách triển khai microservice
2. **Service Configuration** - Định nghĩa cách expose microservice

## Cấu hình Deployment

### Cấu trúc cơ bản

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: configserver-deployment
  labels:
    app: configserver
spec:
  replicas: 1
  selector:
    matchLabels:
      app: configserver
  template:
    metadata:
      labels:
        app: configserver
    spec:
      containers:
      - name: configserver
        image: eazybytes/configserver:s14
        ports:
        - containerPort: 8071
```

### Phân tích cấu hình

#### API Version và Kind
- `apiVersion: apps/v1` - Phiên bản API bắt buộc cho các đối tượng Deployment
- `kind: Deployment` - Chỉ định đây là cấu hình Deployment (đối tượng Kubernetes được định nghĩa trước)

#### Metadata
- `name: configserver-deployment` - Tên duy nhất cho deployment
- `labels: app: configserver` - Nhãn để nhận diện và tổ chức tài nguyên

#### Specification (spec)

**Replicas**
- `replicas: 1` - Số lượng instance pod cần triển khai
- Tăng số này (ví dụ: 3) để triển khai nhiều instance cho tính khả dụng cao

**Selector**
- `matchLabels` - Kết nối các specification với deployment bằng cách khớp nhãn
- Phải khớp với các labels được định nghĩa trong metadata

**Template**
- Định nghĩa pod template để tạo containers
- Chứa các phần metadata và spec riêng

**Container Specifications**
- `name` - Tên container
- `image` - Docker image sử dụng (ví dụ: `eazybytes/configserver:s14`)
  - Registry mặc định là Docker Hub (docker.io)
  - Đối với các registry khác (AWS ECR, Azure ACR, v.v.), bao gồm URL registry đầy đủ
- `containerPort` - Cổng mà container sẽ lắng nghe (8071 cho Config Server)

**Multiple Containers**
- Để thêm helper/sidecar containers, thêm các mục danh sách bổ sung dưới `containers:`
- Mỗi container yêu cầu name, image và ports configuration riêng

## Cấu hình Service

### Cấu trúc cơ bản

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: configserver
spec:
  selector:
    app: configserver
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 8071
      targetPort: 8071
```

### Phân tích cấu hình

#### Separator (Dấu phân cách)
- `---` - Ba dấu gạch ngang phân tách nhiều cấu hình YAML trong một file
- Kubernetes coi mỗi phần như một cấu hình riêng biệt

#### API Version và Kind
- `apiVersion: v1` - Phiên bản API cho các đối tượng Service
- `kind: Service` - Chỉ định đây là cấu hình Service

#### Metadata
- `name: configserver` - Tên service (hoạt động như hostname trong cluster)
- **Quan trọng:** Tên này được các microservices khác sử dụng để giao tiếp với Config Server

#### Specification

**Selector**
- `app: configserver` - Liên kết service với các pods có nhãn khớp từ deployment

**Type**
- `LoadBalancer` - Expose service ra bên ngoài (external to Kubernetes cluster)
- Các loại khác: ClusterIP (chỉ internal), NodePort (external trên cổng node cụ thể)

**Ports**
- `protocol: TCP` - Giao thức giao tiếp (TCP cho web communication)
- `port: 8071` - Cổng được expose ra thế giới bên ngoài
- `targetPort: 8071` - Cổng mà container lắng nghe bên trong
- **Quan trọng:** `targetPort` phải khớp với `containerPort` trong cấu hình deployment

## Hệ thống khớp nhãn (Label Matching)

Nhãn rất quan trọng để kết nối các tài nguyên Kubernetes. Nhãn `app: configserver` phải nhất quán trong:

1. Deployment metadata labels (dòng 6)
2. Deployment selector matchLabels (dòng 11)
3. Template metadata labels (dòng 15)
4. Service selector (dòng 28)

Điều này đảm bảo Kubernetes ánh xạ đúng các services tới deployments và pods.

## Best Practices (Thực hành tốt nhất)

1. **Đặt tên duy nhất**: Sử dụng tên mô tả, duy nhất cho deployments và services
2. **Tính nhất quán của nhãn**: Đảm bảo nhãn khớp nhau trong các cấu hình deployment và service
3. **Tổ chức file đơn**: Sử dụng dấu phân cách `---` để giữ các cấu hình liên quan trong một file
4. **Đặt tên Service**: Tên service trở thành DNS entries; chọn cẩn thận cho giao tiếp giữa các services
5. **Quản lý Replica**: Bắt đầu với 1 replica và mở rộng dựa trên nhu cầu traffic

## Các bước tiếp theo

Với file Kubernetes manifest đã được tạo, bạn đã sẵn sàng để:
1. Triển khai Config Server lên Kubernetes cluster
2. Xác minh trạng thái triển khai
3. Test truy cập external tới Config Server
4. Triển khai các microservices bổ sung theo cùng một pattern

## Tóm tắt

Bạn đã học:
- Cách cấu trúc các file Kubernetes manifest cho việc triển khai microservice
- Sự khác biệt giữa cấu hình Deployment và Service
- Cách sử dụng nhãn để ánh xạ tài nguyên
- Cách expose services ra thế giới bên ngoài
- Tầm quan trọng của việc đặt tên nhất quán và cấu hình cổng

Nền tảng này sẽ giúp bạn triển khai tất cả các microservices trong kiến trúc của mình lên Kubernetes một cách hiệu quả.

## Tài nguyên bổ sung

- [Tài liệu chính thức Kubernetes - Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Tài liệu chính thức Kubernetes - Services](https://kubernetes.io/docs/concepts/services-networking/service/)




FILE: 43-deploying-and-verifying-config-server-in-kubernetes.md


# Triển Khai và Xác Minh Config Server trong Kubernetes - Hướng Dẫn Hoàn Chỉnh

## Tổng Quan

Hướng dẫn toàn diện này trình bày quy trình đầy đủ để triển khai microservice Config Server Spring Boot vào Kubernetes cluster cục bộ bằng cách sử dụng các file manifest Kubernetes. Chúng ta sẽ đề cập đến việc triển khai, xác minh qua nhiều phương pháp và kiểm tra kỹ lưỡng dịch vụ đang chạy.

## Yêu Cầu Tiên Quyết

- Kubernetes cluster cục bộ (ví dụ: Docker Desktop với Kubernetes đã bật)
- Công cụ kubectl CLI đã cài đặt và cấu hình
- Microservice Config Server với file manifest Kubernetes (`config-server.yaml`)
- Kubernetes Dashboard (tùy chọn, để xác minh trực quan)

## Phần 1: Xác Minh Trạng Thái Ban Đầu của Cluster

Trước khi triển khai Config Server, điều quan trọng là xác minh trạng thái hiện tại của Kubernetes cluster để đảm bảo namespace mặc định đang trống và sẵn sàng cho việc triển khai.

### Kiểm Tra Các Deployment Hiện Có

Chạy lệnh sau để liệt kê tất cả các deployment:

```bash
kubectl get deployments
```

**Kết Quả Mong Đợi:** "No resources found in default namespace"

Điều này xác nhận rằng hiện tại không có deployment nào trong namespace mặc định.

### Kiểm Tra Các Service Hiện Có

Kiểm tra các service hiện đang chạy trong cluster của bạn:

```bash
kubectl get services
```

**Kết Quả Mong Đợi:** Bạn chỉ nên thấy một service mặc định liên quan đến chính Kubernetes cluster. Không có service nào liên quan đến microservice.

### Kiểm Tra Replica Sets

Xác minh rằng không có replica set nào tồn tại:

```bash
kubectl get replicaset
```

**Kết Quả Mong Đợi:** "No resources found in default namespace"

### Xác Minh qua Kubernetes Dashboard

Bạn cũng có thể xác minh trạng thái trống bằng Kubernetes Dashboard:

1. Mở Kubernetes Dashboard của bạn
2. Đảm bảo bạn đã chọn namespace **default** từ menu dropdown
3. Nhấp vào **Deployments** - sẽ hiển thị "Nothing to display"
4. Kiểm tra **Pods** - sẽ hiển thị "Nothing to display"
5. Kiểm tra **Replica Sets** - sẽ hiển thị "Nothing to display"
6. Kiểm tra **Services** - chỉ nên hiển thị một service liên quan đến Kubernetes

Điều này xác nhận rằng namespace mặc định của bạn đã sạch và sẵn sàng cho việc triển khai.

## Phần 2: Triển Khai Config Server lên Kubernetes

### Bước 1: Điều Hướng đến Vị Trí File Manifest

Trước khi chạy lệnh triển khai, đảm bảo bạn đang ở trong thư mục chính xác nơi file manifest `config-server.yaml` của bạn được lưu trữ.

```bash
# Xác minh thư mục hiện tại
pwd

# Liệt kê các file để xác nhận config-server.yaml tồn tại
ls
```

### Bước 2: Áp Dụng Kubernetes Manifest

Thực thi lệnh sau để triển khai Config Server:

```bash
kubectl apply -f config-server.yaml
```

**Kết Quả Mong Đợi:**
```
deployment.apps/config-server-deployment created
service/config-server created
```

Output này xác nhận rằng cả deployment và service đã được tạo thành công.

**Lưu Ý:** Tất cả các lệnh Kubernetes được sử dụng trong hướng dẫn này sẽ được ghi lại trong kho GitHub để tham khảo trong tương lai.

## Phần 3: Xác Minh Việc Triển Khai

Sau khi áp dụng file manifest, xác minh rằng Config Server đã được triển khai thành công bằng nhiều phương pháp.

### Phương Pháp 1: Xác Minh Deployments

Kiểm tra trạng thái deployment:

```bash
kubectl get deployments
```

**Kết Quả Mong Đợi:**
```
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
config-server-deployment    1/1     1            1           30s
```

**Ý Nghĩa:**
- **NAME**: Tên deployment là `config-server-deployment`
- **READY**: Hiển thị `1/1`, nghĩa là trạng thái mong muốn là 1 replica và trạng thái thực tế cũng là 1
- Container đang ở trạng thái khỏe mạnh không có vấn đề gì

### Phương Pháp 2: Xác Minh Services

Kiểm tra cấu hình service:

```bash
kubectl get services
```

**Kết Quả Mong Đợi:**
```
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes      ClusterIP      10.96.0.1       <none>        443/TCP          5d
config-server   LoadBalancer   10.96.157.23    localhost     8071:30153/TCP   1m
```

**Thông Tin Chính:**
- **Tên Service**: `config-server`
- **Loại Service**: `LoadBalancer`
- **Cluster IP**: Địa chỉ IP nội bộ (ví dụ: 10.96.157.23) - chỉ truy cập được trong cluster
- **External IP**: `localhost` (vì đây là môi trường cục bộ)
- **Ánh Xạ Port**: 
  - Port bên ngoài: `8071` (truy cập được từ bên ngoài cluster)
  - NodePort: `30153` (tự động gán bởi Kubernetes)

**Lưu Ý Quan Trọng:**
- Cluster IP chỉ có ý nghĩa trong Kubernetes cluster
- Trong môi trường cục bộ, External IP hiển thị là `localhost`
- Trong môi trường cloud (AWS, Azure, GCP), bạn sẽ nhận được địa chỉ IP công khai thực tế
- Config Server được expose tại `localhost:8071`
- Port `30153` là NodePort tự động gán bởi Kubernetes (sẽ được giải thích trong các bài giảng sau về các loại service)

### Phương Pháp 3: Xác Minh Replica Sets

Kiểm tra trạng thái replica set:

```bash
kubectl get replicaset
```

**Kết Quả Mong Đợi:**
```
NAME                                  DESIRED   CURRENT   READY   AGE
config-server-deployment-7f8d9b5c4d   1         1         1       2m
```

**Ý Nghĩa:**
- **Desired**: 1 replica nên đang chạy
- **Current**: 1 replica hiện đang chạy
- **Ready**: 1 replica đã sẵn sàng phục vụ traffic

**Quan Trọng:** Nếu số lượng current là 0, Kubernetes sẽ tự động phát hiện điều này và tạo container mới để thay thế container bị lỗi. Đây là một phần của khả năng tự phục hồi (self-healing) của Kubernetes.

### Phương Pháp 4: Xác Minh Pods

Kiểm tra trạng thái pod:

```bash
kubectl get pods
```

**Kết Quả Mong Đợi:**
```
NAME                                        READY   STATUS    RESTARTS   AGE
config-server-deployment-7f8d9b5c4d-x9k2m   1/1     Running   0          3m
```

**Thông Tin Chính:**
- **Tên Pod**: Được tạo tự động với tên deployment làm tiền tố
- **Status**: `Running` - container đang chạy thành công
- **Ready**: `1/1` - tất cả container trong pod đã sẵn sàng

## Phần 4: Xác Minh Qua Kubernetes Dashboard

Kubernetes Dashboard cung cấp cách trực quan để xác minh và giám sát việc triển khai của bạn.

### Truy Cập Dashboard

Đảm bảo bạn đã cài đặt và có thể truy cập Kubernetes Dashboard. Chọn namespace **default**.

### 1. Kiểm Tra Services

Điều hướng đến phần **Services**:

- **Tên Service**: `config-server`
- **Loại**: `LoadBalancer`
- **External Endpoint**: `localhost:8071`

Điều này cho thấy service của bạn được expose đúng cách và có thể truy cập được.

### 2. Kiểm Tra Deployments

Điều hướng đến phần **Deployments**:

- **Deployment**: `config-server-deployment`
- Nhấp vào deployment để xem thông tin chi tiết:
  - Chi tiết pod
  - Container image được sử dụng
  - Nhãn được gán
  - Chi tiết cấu hình

### 3. Kiểm Tra Pods

Điều hướng đến phần **Pods** và nhấp vào pod config-server của bạn:

- Xem thông tin pod toàn diện
- Kiểm tra trạng thái và sức khỏe của pod
- **Tính Năng Quan Trọng**: Nhấp vào tùy chọn **"Logs"** để xem logs

### Xem Logs của Pod

Tính năng logs trong Kubernetes Dashboard rất quan trọng cho việc debug:

1. Nhấp vào pod config-server
2. Nhấp nút **"Logs"**
3. Xem tất cả logs ứng dụng Spring Boot
4. Sử dụng logs để debug bất kỳ vấn đề nào với container của bạn

Đây là nơi chính để kiểm tra khi khắc phục sự cố với container.

### 4. Kiểm Tra Replica Sets

Điều hướng đến phần **Replica Sets**:

- Xem replica set cho config-server-deployment
- Xem trạng thái running so với desired
- Kiểm tra pods nào đang chạy container
- Giám sát sức khỏe và trạng thái của pod

## Phần 5: Kiểm Tra Config Server

Sau khi triển khai, hãy kiểm tra kỹ lưỡng Config Server bằng cách truy cập các endpoint cấu hình của nó.

### Kiểm Tra 1: Cấu Hình Accounts Microservice (Production Profile)

Truy cập cấu hình accounts service cho production profile:

```
URL: http://localhost:8071/accounts/prod
```

**Kết Quả Mong Đợi:** 
- Trả về các thuộc tính cấu hình cho accounts microservice
- Bao gồm các thuộc tính từ cả production profile và default profile
- Các thuộc tính được merge và trả về ở định dạng JSON

### Kiểm Tra 2: Cấu Hình Loans Microservice

Truy cập cấu hình loans service:

```
URL: http://localhost:8071/loans/default
```

**Kết Quả Mong Đợi:**
- Trả về các thuộc tính cấu hình cho loans microservice
- Hiển thị các thuộc tính từ default profile

### Kiểm Tra 3: Cấu Hình Eureka Server

Truy cập cấu hình Eureka Server:

```
URL: http://localhost:8071/eureka/default
```

**Kết Quả Mong Đợi:**
- Trả về các thuộc tính cấu hình Eureka Server
- Tất cả thuộc tính đến từ default profile

**Lưu Ý Quan Trọng:** Eureka Server không có các thuộc tính riêng cho profile. Tất cả thuộc tính Eureka đều có sẵn trong default profile, đó là lý do tại sao chúng ta truy cập nó với `/default`.

### Xác Nhận Kiểm Tra Thành Công

Nếu cả ba endpoint đều trả về các thuộc tính cấu hình như mong đợi, điều này xác nhận rằng:
- Config Server đã được triển khai thành công lên Kubernetes cluster
- Service có thể truy cập được tại `localhost:8071`
- Việc lấy cấu hình đang hoạt động chính xác
- Tất cả microservices sẽ có thể lấy cấu hình của chúng

## Phần 6: Hiểu về Các Loại Service trong Kubernetes

Config Server được expose bằng loại service **LoadBalancer**. Hãy hiểu điều này có nghĩa là gì:

### Các Thành Phần Service

1. **ClusterIP**: 
   - Địa chỉ IP nội bộ trong cluster
   - Chỉ truy cập được từ bên trong Kubernetes cluster
   - Mọi service đều nhận một ClusterIP mặc định

2. **NodePort**: 
   - Port `30153` trong ví dụ của chúng ta
   - Tự động gán bởi Kubernetes
   - Cho phép truy cập service qua IP của bất kỳ node nào
   - Phạm vi port: 30000-32767

3. **LoadBalancer**: 
   - Cung cấp truy cập bên ngoài đến service
   - Trong môi trường cục bộ: Sử dụng `localhost`
   - Trong môi trường cloud: Cung cấp load balancer thực với IP công khai
   - Expose service tại port `8071`

### Môi Trường Cục Bộ vs Cloud

**Môi Trường Cục Bộ:**
- External IP: `localhost`
- Phù hợp cho phát triển và kiểm thử
- Không cần load balancing thực sự

**Môi Trường Cloud (AWS, Azure, GCP):**
- External IP: Địa chỉ IP công khai thực (ví dụ: 52.123.45.67)
- Cung cấp load balancer của nhà cung cấp cloud
- Phân phối traffic tự động
- Tính khả dụng cao và khả năng mở rộng

## Phần 7: Hướng Dẫn Khắc Phục Sự Cố

### Xem Logs Sử Dụng kubectl

Nếu bạn gặp vấn đề, hãy kiểm tra logs của pod:

```bash
# Lấy tên pod trước
kubectl get pods

# Xem logs (thay thế <pod-name> bằng tên pod thực tế)
kubectl logs <pod-name>

# Theo dõi logs theo thời gian thực
kubectl logs -f <pod-name>

# Xem logs từ instance container trước đó (nếu container restart)
kubectl logs <pod-name> --previous
```

### Xem Logs Sử Dụng Kubernetes Dashboard

1. Điều hướng đến **Pods**
2. Nhấp vào pod config-server
3. Nhấp nút **"Logs"**
4. Xem logs ứng dụng Spring Boot
5. Sử dụng tính năng tìm kiếm và lọc để tìm lỗi cụ thể

### Các Vấn Đề Thường Gặp và Giải Pháp

#### Vấn Đề 1: Pod Không Khởi Động

**Triệu Chứng:** Trạng thái pod hiển thị `Error`, `CrashLoopBackOff`, hoặc `ImagePullBackOff`

**Giải Pháp:**
- Kiểm tra logs để tìm lỗi ứng dụng
- Xác minh Docker image tồn tại và có thể truy cập được
- Kiểm tra image pull secrets nếu sử dụng private registry
- Xác minh giới hạn tài nguyên không quá hạn chế

#### Vấn Đề 2: Service Không Truy Cập Được

**Triệu Chứng:** Không thể truy cập service tại `localhost:8071`

**Giải Pháp:**
- Xác minh loại service là LoadBalancer
- Kiểm tra cấu hình port trong file manifest
- Đảm bảo pod đang ở trạng thái `Running`
- Xác minh không có xung đột port trên máy cục bộ của bạn

#### Vấn Đề 3: Connection Refused

**Triệu Chứng:** Endpoint service trả về "connection refused"

**Giải Pháp:**
- Đảm bảo container port khớp với target port của service
- Xác minh ứng dụng đang lắng nghe trên port chính xác (8071)
- Kiểm tra xem ứng dụng đã khởi động thành công trong logs chưa
- Xác minh các quy tắc firewall không chặn port

#### Vấn Đề 4: Cấu Hình Không Load

**Triệu Chứng:** Các endpoint trả về lỗi hoặc phản hồi trống

**Giải Pháp:**
- Xác minh Config Server được kết nối với configuration repository
- Kiểm tra thông tin xác thực và quyền truy cập Git repository
- Đảm bảo các file cấu hình tồn tại trong repository
- Xem lại logs Config Server để tìm lỗi kết nối

### Kubernetes Self-Healing (Tự Phục Hồi)

Hãy nhớ rằng Kubernetes có khả năng tự phục hồi:

- Nếu container bị crash, Kubernetes tự động restart nó
- Nếu desired replicas không khớp với current replicas, Kubernetes tạo hoặc xóa pods
- Health checks đảm bảo chỉ pods khỏe mạnh nhận traffic
- Các node bị lỗi kích hoạt việc lên lịch lại pod sang các node khỏe mạnh

## Phần 8: Tóm Tắt Triển Khai

### Những Gì Chúng Ta Đã Triển Khai

✅ **Config Server Deployment:**
- 1 replica (pod) chạy Config Server container
- Chính sách restart tự động
- Phân bổ và giới hạn tài nguyên
- Cấu hình health check

✅ **Config Server Service:**
- Loại: LoadBalancer
- Truy cập bên ngoài qua `localhost:8071`
- ClusterIP nội bộ cho giao tiếp trong cluster
- NodePort `30153` cho truy cập cấp node

### Lợi Ích Chính

1. **Quản Lý Cấu Hình Tập Trung**: Tất cả microservices có thể lấy cấu hình từ một vị trí trung tâm
2. **Tự Phục Hồi**: Kubernetes tự động phục hồi từ lỗi
3. **Khả Năng Mở Rộng**: Dễ dàng mở rộng bằng cách điều chỉnh số lượng replica
4. **Service Discovery**: Các service khác có thể khám phá Config Server qua Kubernetes DNS
5. **Load Balancing**: Load balancing tích hợp sẵn cho traffic bên ngoài

### Danh Sách Kiểm Tra Xác Minh Triển Khai

Trước khi tiến hành triển khai các microservices khác, hãy đảm bảo:

- [ ] Deployment hiển thị `1/1` ready
- [ ] Service có loại LoadBalancer và external endpoint
- [ ] Trạng thái pod là `Running`
- [ ] Replica set hiển thị desired = current = 1
- [ ] Tất cả test endpoints trả về cấu hình như mong đợi
- [ ] Logs hiển thị Spring Boot khởi động thành công
- [ ] Không có lỗi trong Kubernetes Dashboard

## Tài Nguyên Bổ Sung

### Tham Chiếu Lệnh

Tất cả các lệnh được sử dụng trong hướng dẫn này:

```bash
# Lệnh xác minh
kubectl get deployments
kubectl get services
kubectl get replicaset
kubectl get pods

# Lệnh triển khai
kubectl apply -f config-server.yaml

# Lệnh logging
kubectl logs <pod-name>
kubectl logs -f <pod-name>

# Mô tả tài nguyên để biết thông tin chi tiết
kubectl describe deployment config-server-deployment
kubectl describe service config-server
kubectl describe pod <pod-name>
```

### Liên Kết Tài Liệu

- Các file manifest đầy đủ có sẵn trong kho GitHub
- Tất cả lệnh được ghi lại để tham khảo trong tương lai
- Ví dụ cấu hình cho các profile khác nhau
- Hướng dẫn khắc phục sự cố với các kịch bản thường gặp

## Kết Luận

Chúc mừng! Bạn đã thành công:

1. ✅ Xác minh trạng thái ban đầu của Kubernetes cluster
2. ✅ Triển khai Config Server lên Kubernetes bằng file manifest
3. ✅ Xác minh triển khai qua nhiều phương pháp (kubectl và Dashboard)
4. ✅ Kiểm tra tất cả các endpoint cấu hình thành công
5. ✅ Hiểu về các loại service và networking trong Kubernetes

Config Server của bạn hiện đang chạy trong Kubernetes và sẵn sàng phục vụ cấu hình cho các microservices khác. Đây là bước đầu tiên quan trọng trong việc xây dựng kiến trúc microservices trên Kubernetes.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- Triển khai các microservices bổ sung (Accounts, Loans, Cards)
- Cấu hình giao tiếp giữa các service
- Thiết lập service discovery với Eureka
- Triển khai API Gateway trong Kubernetes
- Quản lý cấu hình theo môi trường cụ thể

Cảm ơn và hẹn gặp lại bạn trong bài giảng tiếp theo!




FILE: 44-deploying-microservices-configmaps-kubernetes.md


# Triển khai Microservices với ConfigMaps trong Kubernetes

## Tổng quan

Hướng dẫn này giải thích cách tạo và sử dụng ConfigMaps trong Kubernetes để quản lý các biến môi trường cho việc triển khai microservices. ConfigMaps cho phép bạn lưu trữ dữ liệu cấu hình không bảo mật dưới dạng các cặp key-value có thể được container sử dụng như biến môi trường, tham số dòng lệnh, hoặc file cấu hình.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster đang chạy
- kubectl CLI đã được cấu hình
- Các file Docker compose với cấu hình biến môi trường
- Hiểu biết cơ bản về các đối tượng Kubernetes

## Sự khác biệt giữa ConfigMaps và Secrets

### ConfigMaps
- Được sử dụng để lưu trữ dữ liệu **không bảo mật** dưới dạng cặp key-value
- Container có thể sử dụng ConfigMaps như:
  - Biến môi trường
  - Tham số dòng lệnh
  - File cấu hình trong volume
- Dữ liệu hiển thị dưới dạng văn bản thuần trong Kubernetes Dashboard

### Secrets
- Được sử dụng để lưu trữ dữ liệu **bảo mật**
- Dữ liệu được mã hóa base64 theo mặc định
- Ẩn khỏi chế độ xem trực tiếp trong Kubernetes Dashboard
- **Lưu ý**: "Secrets trong Kubernetes không thực sự là bí mật" - có những cách tốt hơn để lưu trữ secrets trong môi trường cloud, thường được quản lý bởi team Platform/DevOps

## Các biến môi trường cần thiết

Để triển khai microservices, chúng ta cần các biến môi trường sau:

- **Activated profile**: Profile Spring nào sẽ được sử dụng
- **Spring config import URL**: Vị trí của configuration server
- **Eureka server URL**: Vị trí của service discovery server
- **Tên ứng dụng**: Cho config server, Eureka server, accounts, loans, cards, gateway
- **Cấu hình Keycloak**:
  - Tên người dùng admin
  - Mật khẩu admin
  - URL Keycloak để resource server lấy certificate

## Tạo file Manifest ConfigMap

### Bước 1: Tạo file YAML

Tạo file mới có tên `configmaps.yml` trong thư mục Kubernetes của bạn.

### Bước 2: Định nghĩa cấu trúc ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: easybank-configmap
data:
  SPRING_PROFILE: "default"
  SPRING_CONFIG_IMPORT: "configserver:http://configserver:8071/"
  EUREKA_SERVER_URL: "http://eurekaserver:8070/eureka/"
  CONFIG_SERVER_APP_NAME: "configserver"
  EUREKA_SERVER_APP_NAME: "eurekaserver"
  ACCOUNTS_APP_NAME: "accounts"
  LOANS_APP_NAME: "loans"
  CARDS_APP_NAME: "cards"
  GATEWAY_APP_NAME: "gateway"
  KEYCLOAK_ADMIN_USERNAME: "admin"
  KEYCLOAK_ADMIN_PASSWORD: "admin"
  KEYCLOAK_SERVER_URL: "http://keycloak:7080"
```

### Các điểm chính:

1. **apiVersion**: Đặt là `v1` cho ConfigMaps
2. **kind**: Phải là `ConfigMap`
3. **metadata.name**: Chọn tên mô tả rõ ràng (ví dụ: `easybank-configmap`)
4. **data**: Chứa tất cả các thuộc tính môi trường dưới dạng cặp key-value

### Cấu hình tên Service

Các hostname trong biến môi trường phải khớp với tên Kubernetes service của bạn:
- Tên service Config Server: `configserver`
- Tên service Eureka Server: `eurekaserver`
- Tên service Keycloak: `keycloak` (expose trên cổng 7080)

## Triển khai ConfigMap lên Kubernetes

### Áp dụng ConfigMap

Chạy lệnh kubectl sau:

```bash
kubectl apply -f configmaps.yaml
```

Kết quả mong đợi:
```
configmap/easybank-configmap created
```

### Xác minh việc tạo ConfigMap

#### Sử dụng kubectl:
```bash
kubectl get configmaps
kubectl describe configmap easybank-configmap
```

#### Sử dụng Kubernetes Dashboard:

1. Truy cập Kubernetes Dashboard
2. Lấy authentication token (nếu phiên đã hết hạn)
3. Chọn namespace `default`
4. Điều hướng đến mục **Config Maps**
5. Click vào ConfigMap của bạn để xem tất cả các biến môi trường

## Lưu ý quan trọng

### Các thành phần không được bao gồm

ConfigMap này không bao gồm các thuộc tính cho:
- Kafka
- RabbitMQ
- OpenTelemetry
- Grafana

**Lý do**: Các thành phần tiêu chuẩn công nghiệp này sẽ được triển khai bằng Helm Charts trong các bài giảng sau, điều này dễ dàng hơn và ít phức tạp hơn so với việc viết file manifest Kubernetes thủ công.

### Yêu cầu về Keycloak

Việc triển khai Keycloak là **bắt buộc** vì:
- Gateway server được bảo mật bằng OAuth2
- Không có Keycloak server, bạn không thể truy cập bất kỳ API nào
- Cần thiết để tạo dữ liệu bên trong microservices

## Các bước tiếp theo

Với ConfigMap đã được tạo thành công, bây giờ bạn có thể:
1. Triển khai các microservices còn lại lên Kubernetes cluster
2. Tham chiếu các biến môi trường này trong deployment manifest của bạn
3. Tiến hành thiết lập Keycloak cho xác thực và phân quyền

## ConfigMap vs Secrets: Xem dữ liệu

### Khả năng hiển thị dữ liệu ConfigMap
- Dữ liệu hiển thị trực tiếp trong Kubernetes Dashboard
- Định dạng văn bản thuần
- Phù hợp cho cấu hình không nhạy cảm

### Khả năng hiển thị dữ liệu Secrets
- Dữ liệu bị ẩn theo mặc định trong Kubernetes Dashboard
- Được mã hóa Base64 (không phải mã hóa thực sự)
- Click vào tùy chọn "View" để xem giá trị token
- **Lưu ý bảo mật**: Không phải là cách hoàn hảo để bảo mật secrets; môi trường cloud cung cấp các giải pháp quản lý secret tốt hơn

## Kết luận

ConfigMaps cung cấp một cách hiệu quả để quản lý các biến môi trường trong Kubernetes clusters. Bằng cách tập trung hóa dữ liệu cấu hình, bạn có thể dễ dàng inject các biến giống nhau vào nhiều triển khai microservices, làm cho cơ sở hạ tầng của bạn dễ bảo trì và mở rộng hơn.




FILE: 45-deploying-remaining-microservices-to-kubernetes-cluster.md


# Triển Khai Các Microservices Còn Lại Lên Kubernetes Cluster

## Tổng Quan

Hướng dẫn này giải thích quy trình triển khai tất cả các microservices còn lại vào Kubernetes cluster. Chúng ta sẽ tìm hiểu cách chuẩn bị các file manifest Kubernetes và thứ tự triển khai phù hợp để đảm bảo tất cả services hoạt động ăn khớp với nhau.

## Yêu Cầu Trước Khi Bắt Đầu

- Kubernetes cluster đã được cài đặt (Docker Desktop hoặc tương tự)
- Hiểu biết cơ bản về các khái niệm Kubernetes (Deployments, Services, ConfigMaps)
- Các microservices đã được build và có sẵn dưới dạng Docker images

## Thứ Tự Triển Khai

Để triển khai microservices vào một cluster mới, hãy tuân theo thứ tự cụ thể sau:

1. **Keycloak** (Authentication Server - Máy chủ xác thực)
2. **ConfigMap** (Lưu trữ cấu hình)
3. **Config Server** (Cấu hình tập trung)
4. **Eureka Server** (Service discovery - Phát hiện dịch vụ)
5. **Accounts Microservice** (Microservice tài khoản)
6. **Loans Microservice** (Microservice khoản vay)
7. **Cards Microservice** (Microservice thẻ)
8. **Gateway Server** (API Gateway - Cổng API)

## Cấu Trúc File Manifest Kubernetes

Tất cả các file manifest được tổ chức với tiền tố số (1, 2, 3, 4, 5, 6, 7, 8) để chỉ ra thứ tự triển khai. Quy ước đặt tên này giúp dễ dàng triển khai các services theo đúng trình tự.

## Triển Khai Keycloak

### Cấu Hình Deployment

Deployment của Keycloak bao gồm:

- **Label**: `keycloak`
- **Replicas**: 1
- **Container Image**: Keycloak image chính thức
- **Chế độ khởi động**: Development mode (`start-dev`)

### Biến Môi Trường

Keycloak yêu cầu hai biến môi trường quan trọng được inject từ ConfigMap:

```yaml
env:
  - name: KEYCLOAK_ADMIN
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: KEYCLOAK_ADMIN
  - name: KEYCLOAK_ADMIN_PASSWORD
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: KEYCLOAK_ADMIN_PASSWORD
```

### Cấu Hình Service

- **Loại**: LoadBalancer
- **Cổng External**: 7080
- **Target Port**: 8080 (cổng container)

## Triển Khai Eureka Server

### Điểm Chính

- **Image Tag**: `s12` (phiên bản Section 12)
- Sử dụng tag Section 12 để tránh phụ thuộc vào Kafka/RabbitMQ từ Sections 13-14
- Đơn giản hóa việc triển khai bằng cách tập trung vào các microservices cốt lõi

### Biến Môi Trường

```yaml
env:
  - name: SPRING_APPLICATION_NAME
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: EUREKA_APPLICATION_NAME
  - name: SPRING_CONFIG_IMPORT
    valueFrom:
      configMapKeyRef:
        name: easybank-configmap
        key: SPRING_CONFIG_IMPORT
```

- **Application Name**: Lấy từ ConfigMap dưới key `EUREKA_APPLICATION_NAME`
- **Config Server URL**: Trỏ đến `config-server:8071`

### Cấu Hình Service

- **Loại**: LoadBalancer
- Cho phép truy cập từ bên ngoài để giám sát service registry

## Triển Khai Accounts Microservice

### Cấu Hình

- **Image Tag**: `s12`
- Bao gồm tất cả các thông số deployment tiêu chuẩn

### Biến Môi Trường

Biến môi trường quan trọng cho service discovery:

```yaml
- name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
  valueFrom:
    configMapKeyRef:
      name: easybank-configmap
      key: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
```

Điều này cho phép Accounts microservice đăng ký với Eureka Server.

### Cấu Hình Service

- **Loại**: LoadBalancer
- Expose microservice để truy cập từ bên ngoài

## Loans và Cards Microservices

Cả hai đều tuân theo cùng pattern như Accounts microservice:

- Sử dụng image tag `s12`
- Inject biến môi trường từ ConfigMap
- Đăng ký với Eureka Server
- Expose dưới dạng LoadBalancer services

## Triển Khai Gateway Server

### Cấu Hình Đặc Biệt

Gateway Server yêu cầu thêm một biến môi trường cho tích hợp OAuth2:

```yaml
- name: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
  valueFrom:
    configMapKeyRef:
      name: easybank-configmap
      key: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
```

URL này trỏ đến certificate endpoint của Keycloak để xác thực JWT.

### Image Tag

- Sử dụng phiên bản `s12` để nhất quán với các microservices khác

## Best Practices Cho ConfigMap

### Quy Ước Đặt Tên Key

- Sử dụng tên key mô tả rõ ràng trong ConfigMap (ví dụ: `EUREKA_APPLICATION_NAME`)
- Tên biến môi trường trong deployment phải khớp với yêu cầu của Spring Boot
- Key trong ConfigMap có thể sử dụng tên tùy chỉnh để tổ chức tốt hơn

### Cấu Trúc Ví Dụ

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: easybank-configmap
data:
  KEYCLOAK_ADMIN: "admin"
  KEYCLOAK_ADMIN_PASSWORD: "admin"
  EUREKA_APPLICATION_NAME: "eurekaserver"
  SPRING_CONFIG_IMPORT: "configserver:http://config-server:8071/"
  EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: "http://eureka-server:8070/eureka/"
```

## Pattern Triển Khai Chung

Tất cả microservices tuân theo pattern tiêu chuẩn này:

1. **Deployment Object**
   - Định nghĩa metadata với labels
   - Đặt số lượng replica
   - Chỉ định selector khớp với labels
   - Cấu hình thông số container
   - Inject biến môi trường từ ConfigMap
   - Định nghĩa các container ports

2. **Service Object**
   - Khớp deployment labels với service selector
   - Đặt loại service (LoadBalancer)
   - Map external port với target port (container port)

## Cấu Hình Port

### Lưu Ý Quan Trọng

- **Container Port**: Cổng mà ứng dụng chạy bên trong container
- **Target Port**: Phải khớp với container port
- **External Port**: Cổng được expose cho clients bên ngoài qua LoadBalancer

### Ví Dụ

```yaml
ports:
  - containerPort: 8080  # Cổng container nội bộ
---
ports:
  - port: 7080           # Cổng external
    targetPort: 8080     # Phải khớp với containerPort
```

## Các Lệnh Triển Khai

Apply các manifest files theo thứ tự:

```bash
kubectl apply -f 1-keycloak.yaml
kubectl apply -f 2-configmaps.yaml
kubectl apply -f 3-configserver.yaml
kubectl apply -f 4-eurekaserver.yaml
kubectl apply -f 5-accounts.yaml
kubectl apply -f 6-loans.yaml
kubectl apply -f 7-cards.yaml
kubectl apply -f 8-gateway.yaml
```

## Các Bước Xác Thực

Sau khi triển khai, xác thực từng service:

```bash
# Kiểm tra deployments
kubectl get deployments

# Kiểm tra services
kubectl get services

# Kiểm tra pods
kubectl get pods

# Xem logs
kubectl logs <pod-name>
```

## Tại Sao Sử Dụng Images Section 12?

Quyết định sử dụng image tags `s12` thay vì `s14`:

- **Section 13-14**: Bao gồm kiến trúc event-driven với RabbitMQ/Kafka
- **Section 15**: Tập trung vào triển khai microservices cơ bản
- **Đơn giản hóa**: Tránh độ phức tạp bổ sung của message broker setup
- **Cải tiến tương lai**: Helm charts (các sections sắp tới) sẽ đơn giản hóa setup event-driven

## Tóm Tắt

Chiến lược triển khai này đảm bảo:

- **Trình tự đúng đắn**: Services triển khai theo thứ tự phụ thuộc
- **Quản lý cấu hình**: Tập trung qua ConfigMap
- **Service Discovery**: Tất cả microservices đăng ký với Eureka
- **Bảo mật**: Tích hợp OAuth2 với Keycloak
- **Khả năng mở rộng**: LoadBalancer services cho phép truy cập từ bên ngoài

Bằng cách tuân theo phương pháp có cấu trúc này, bạn có thể triển khai đáng tin cậy toàn bộ kiến trúc microservices lên bất kỳ Kubernetes cluster nào.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- Apply tất cả manifest files vào Kubernetes cluster
- Xác thực deployments và service registrations
- Kiểm tra end-to-end communication giữa các microservices
- Xác minh tích hợp bảo mật OAuth2

---

**Lưu ý**: Hướng dẫn này là một phần của khóa học toàn diện về Spring Boot microservices bao gồm các pattern triển khai Kubernetes.




FILE: 46-deploying-microservices-to-kubernetes-with-keycloak-security.md


# Triển khai Microservices lên Kubernetes với Bảo mật Keycloak

## Tổng quan

Hướng dẫn này bao gồm quy trình đầy đủ để triển khai các microservices Spring Boot lên Kubernetes cluster với bảo mật OAuth2 sử dụng Keycloak làm máy chủ xác thực. Bạn sẽ học cách triển khai nhiều microservices theo đúng thứ tự, cấu hình bảo mật và kiểm tra toàn bộ hệ thống.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster đã được thiết lập (Docker Desktop hoặc tương tự)
- kubectl CLI đã được cấu hình
- Các file Kubernetes manifest đã chuẩn bị sẵn
- Hiểu biết cơ bản về kiến trúc microservices

## Kiến trúc Triển khai

Triển khai bao gồm các thành phần sau:
- **Keycloak** - Máy chủ xác thực
- **Config Server** - Quản lý cấu hình tập trung
- **Eureka Server** - Service discovery (phát hiện dịch vụ)
- **Gateway Server** - API gateway với bảo mật OAuth2
- **Business Microservices** - Các dịch vụ Accounts, Loans và Cards

## Quy trình Triển khai từng bước

### 1. Triển khai Keycloak Authorization Server

Bắt đầu bằng cách triển khai dịch vụ Keycloak:

```bash
kubectl apply -f 1_keycloak.yaml
```

Lệnh này tạo dịch vụ Keycloak để xử lý xác thực và phân quyền cho tất cả microservices.

### 2. Triển khai ConfigMaps

Áp dụng các configuration maps:

```bash
kubectl apply -f 2_configmaps.yaml
```

**Lưu ý quan trọng**: Kubernetes đủ thông minh để phát hiện nếu không có thay đổi nào. Nếu bạn áp dụng cùng một cấu hình lần nữa, nó sẽ trả về trạng thái "unchanged" (không thay đổi), cho biết không cần thực hiện hành động nào. Đây là một trong những tính năng mạnh mẽ của cách tiếp cận declarative của Kubernetes.

### 3. Triển khai Config Server

Triển khai Config Server với image đã cập nhật:

```bash
kubectl apply -f 3_configserver.yaml
```

**Thay đổi chính**: Phiên bản image đã được cập nhật từ S14 sang S12. Khi bạn thực thi lệnh này:
- **Deployment** sẽ được cấu hình lại với image mới
- **Service** giữ nguyên không đổi (không phát hiện thay đổi)

**Xác minh**: 
- Truy cập Kubernetes dashboard
- Điều hướng đến namespace mặc định
- Kiểm tra pods và xem logs của Config Server
- Đảm bảo bạn thấy thông báo "Successfully started Config Server"

⚠️ **Quan trọng**: Luôn đợi Config Server triển khai hoàn tất thành công trước khi tiếp tục bước tiếp theo.

### 4. Triển khai Eureka Server

Sau khi Config Server đang chạy:

```bash
kubectl apply -f 4_eurekaserver.yaml
```

**Xác minh**:
- Kiểm tra trạng thái pod trong Kubernetes dashboard
- Xem logs để xác nhận "Eureka Server successfully started"
- Đợi khởi động hoàn toàn trước khi tiếp tục

### 5. Triển khai các Business Microservices

Triển khai ba business microservices:

```bash
kubectl apply -f 5_accounts.yaml
kubectl apply -f 6_loans.yaml
kubectl apply -f 7_cards.yaml
```

**Quản lý Dependencies quan trọng**:
- Không giống Docker Compose, Kubernetes không có chức năng `depends_on` tích hợp sẵn
- Bạn phải đảm bảo thủ công các dịch vụ phụ thuộc đã khởi động hoàn toàn trước khi triển khai các dịch vụ phụ thuộc vào chúng
- Đợi cả ba microservices (Accounts, Loans, Cards) khởi động hoàn toàn trước khi triển khai Gateway

**Tại sao điều này quan trọng**:
- Nếu dependencies chưa sẵn sàng, containers sẽ khởi động lại nhiều lần
- Cuối cùng, deployment sẽ thành công, nhưng gây ra khởi động lại không cần thiết
- Trong môi trường production, các đội DevOps sử dụng công cụ orchestration nâng cao để quản lý thứ tự triển khai

**Xác minh**:
- Truy cập Eureka dashboard
- Xác nhận cả ba microservices đã được đăng ký
- Kiểm tra trạng thái đăng ký trước khi tiếp tục

### 6. Triển khai Gateway Server

Cuối cùng, triển khai API Gateway:

```bash
kubectl apply -f 8_gatewayserver.yaml
```

**Xác minh**:
- Làm mới Eureka dashboard
- Xác nhận Gateway Server đã đăng ký thành công

## Cấu hình Bảo mật Keycloak

### Truy cập Keycloak Admin Console

1. Điều hướng đến `http://localhost:7080`
2. Click "Administration Console"
3. Thông tin đăng nhập:
   - Username: `admin`
   - Password: `admin`

### Tạo Client Application

1. Vào phần **Clients**
2. Click **Create Client**
3. Cấu hình client:
   - **Client ID**: `easybank-callcenter-cc`
   - Click **Next**
4. Bật **Client Authentication**
5. Tắt **Standard Flow** và **Direct Access Grants**
6. Bật **Service Account Roles**
7. Click **Next** → **Next** → **Save**
8. Sao chép **Client Secret** từ tab Credentials (cần cho việc test API)

### Tạo Client Roles

Tạo ba roles cho client:

1. Điều hướng đến **Roles** (cho client của bạn)
2. Click **Create Role**
3. Tạo các roles sau:
   - `accounts`
   - `cards`
   - `loans`

### Gán Roles cho Client

1. Quay lại **Clients** → Chọn `easybank-callcenter-cc`
2. Click **Service Account Roles**
3. Click **Assign Role**
4. Chọn cả ba roles (accounts, cards, loans)
5. Click **Assign**

## Kiểm tra Triển khai

### Thiết lập Postman

Đối với tất cả các API requests, bạn cần lấy access token sử dụng OAuth2 Client Credentials flow.

**Cấu hình Token**:
- Grant Type: Client Credentials
- Access Token URL: `http://localhost:7080/realms/master/protocol/openid-connect/token`
- Client ID: `easybank-callcenter-cc`
- Client Secret: [Secret bạn đã sao chép]

### Test 1: Tạo Account

**Endpoint**: `POST /api/accounts`
**Số điện thoại**: `688`

1. Click **Get New Access Token**
2. Sử dụng token trong request
3. Click **Send**
4. Kết quả mong đợi: "Account details successfully created"

### Test 2: Tạo Cards

**Endpoint**: `POST /api/cards`
**Số điện thoại**: `688`

1. Cập nhật client secret trong request (giống như trên)
2. Lấy access token mới
3. Click **Send**
4. Kết quả mong đợi: "Cards details created successfully"

### Test 3: Tạo Loans

**Endpoint**: `POST /api/loans`
**Số điện thoại**: `688`

1. Cập nhật client secret trong request
2. Lấy access token mới
3. Click **Send**
4. Kết quả mong đợi: "Loans details created successfully"

### Test 4: Lấy Customer Details

**Endpoint**: `GET /api/accounts/fetchCustomerDetails?mobileNumber=688`

Đây là thao tác GET để lấy thông tin khách hàng đầy đủ bao gồm accounts, loans và cards.

1. Không cần xác thực cho GET (nếu được cấu hình)
2. Cập nhật số điện thoại thành `688`
3. Click **Send**
4. Kết quả mong đợi: Thông tin khách hàng đầy đủ với accounts, loans và cards

**Xử lý sự cố**:
- Nếu nhận được "Customer not found" → Xác minh số điện thoại khớp với số bạn đã sử dụng khi tạo
- Nếu nhận được "Unauthorized" → Lấy access token mới
- Đảm bảo tất cả các thao tác tạo đã sử dụng cùng một số điện thoại

## Hiểu về Kubernetes Manifest Files

### Định nghĩa ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: [configmap-name]
data:
  key1: value1
  key2: value2
```

ConfigMaps lưu trữ dữ liệu cấu hình dưới dạng các cặp key-value có thể được sử dụng bởi pods.

### Định nghĩa Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: [deployment-name]
  labels:
    app: [app-name]
spec:
  replicas: 1
  selector:
    matchLabels:
      app: [app-name]
  template:
    metadata:
      labels:
        app: [app-name]
    spec:
      containers:
      - name: [container-name]
        image: [image:tag]
        ports:
        - containerPort: [port]
```

**Các thành phần chính**:
- **replicas**: Số lượng pod instances
- **selector**: Khớp với pods để quản lý
- **template**: Đặc tả pod bao gồm chi tiết container

### Định nghĩa Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: [service-name]
spec:
  selector:
    app: [app-name]
  type: ClusterIP
  ports:
  - protocol: TCP
    port: [external-port]
    targetPort: [container-port]
```

**Các loại Service**:
- **ClusterIP**: Chỉ truy cập nội bộ cluster (mặc định)
- **LoadBalancer**: Truy cập từ bên ngoài với load balancing
- **NodePort**: Expose service trên IP của mỗi node

### Liên kết Deployments và Services

Kết nối giữa Deployment và Service được thiết lập thông qua **labels**:

```yaml
# Trong Deployment metadata
labels:
  app: accounts

# Trong Service selector
selector:
  app: accounts
```

Cả hai phải sử dụng cùng giá trị label để thiết lập liên kết. Service định tuyến traffic đến các pods khớp với selector labels.

## Những điểm quan trọng cần nhớ

1. **Kubernetes Intelligence**: Kubernetes phát hiện thay đổi cấu hình và chỉ áp dụng những gì khác biệt
2. **Thứ tự Triển khai quan trọng**: Đảm bảo dependencies đã khởi động hoàn toàn trước khi triển khai các dịch vụ phụ thuộc
3. **Không có Dependencies tự động**: Không giống Docker Compose, Kubernetes không có quản lý dependency tích hợp sẵn
4. **Thực hành Production**: Các đội DevOps sử dụng công cụ nâng cao cho triển khai tự động, có thứ tự
5. **Label Binding**: Services tìm pods thông qua label selectors khớp
6. **Service Types**: Chọn ClusterIP cho dịch vụ nội bộ, LoadBalancer cho expose ra ngoài

## Tiếp theo là gì?

Triển khai này minh họa các khái niệm cơ bản về chạy microservices trong Kubernetes. Tuy nhiên, Kubernetes cung cấp nhiều tính năng mạnh mẽ hơn:
- Auto-scaling dựa trên tải
- Khả năng tự phục hồi (self-healing)
- Rolling updates và rollbacks
- Networking và ingress nâng cao
- Quản lý ConfigMap và Secret
- Resource limits và quotas

Những chủ đề nâng cao này sẽ được đề cập trong các bài giảng sắp tới, nơi bạn sẽ khám phá sức mạnh và "phép màu" thực sự của Kubernetes.

## Trách nhiệm của Developer vs. DevOps

**Là một Developer**:
- Hiểu các manifest files được cung cấp bởi đội DevOps
- Debug các vấn đề production trong mạng microservice
- Biết các khái niệm và lệnh Kubernetes cơ bản

**Bạn không cần**:
- Thành thạo viết các Kubernetes manifests phức tạp từ đầu
- Xử lý orchestration triển khai nâng cao
- Quản lý các Kubernetes clusters production

Tập trung vào việc xây dựng các microservices tuyệt vời, và làm việc cộng tác với đội DevOps của bạn cho các chiến lược triển khai.

## Kết luận

Bạn đã triển khai thành công một kiến trúc microservices hoàn chỉnh lên Kubernetes với bảo mật OAuth2 sử dụng Keycloak. Hệ thống bao gồm service discovery, cấu hình tập trung, API gateway, và nhiều business services - tất cả đều được bảo mật và giao tiếp trong Kubernetes cluster.

Nền tảng này chuẩn bị cho bạn khám phá các tính năng Kubernetes nâng cao hơn trong các bài giảng tiếp theo!




FILE: 47-kubernetes-self-healing-and-replica-management.md


# Kubernetes Self-Healing và Quản Lý Replica

## Tổng Quan

Hướng dẫn này trình bày khả năng tự phục hồi (self-healing) của Kubernetes và cách quản lý replica cho các microservices được triển khai trong Kubernetes cluster. Chúng ta sẽ khám phá cách Kubernetes tự động duy trì trạng thái mong muốn của containers bằng cách tạo lại chúng khi bị lỗi hoặc bị xóa.

## Yêu Cầu Tiên Quyết

- Tất cả microservices đã được triển khai lên Kubernetes cluster
- Đã cài đặt và cấu hình kubectl CLI tool
- Hiểu biết cơ bản về Kubernetes deployments và pods

## Hiểu về Kubernetes Self-Healing

Kubernetes cung cấp khả năng tự phục hồi mà Docker hoặc Docker Compose truyền thống không thể đạt được. Khi Kubernetes phát hiện một container không hoạt động đúng cách hoặc đã hoàn toàn dừng lại, nó sẽ tự động tạo lại một container mới để thay thế container bị lỗi.

Khả năng này đảm bảo tính khả dụng cao và độ tin cậy cho microservices của bạn mà không cần can thiệp thủ công.

## Kiểm Tra Replica Sets

### Xem Replica Sets Hiện Tại

Đầu tiên, hãy kiểm tra các replica sets hiện tại cho tất cả deployments:

```bash
kubectl get replicaset
```

Lệnh này hiển thị:
- **Desired state**: Số lượng replicas được chỉ định trong deployment của bạn
- **Current state**: Số lượng replicas hiện đang chạy
- **Ready**: Số lượng containers sẵn sàng phục vụ các ứng dụng client

Bạn sẽ thấy replica sets cho tất cả deployments:
- accounts
- cards
- config-server
- eureka-server
- gateway-server
- keycloak
- loans

### Xem Các Pods Đang Chạy

Để xem tất cả các pods đang chạy:

```bash
kubectl get pods
```

Ban đầu, bạn sẽ thấy một pod duy nhất cho mỗi deployment vì số lượng replica được đặt là 1.

## Mở Rộng Replicas

### Cập Nhật Số Lượng Replica

Hãy tăng số lượng replicas cho accounts microservice:

1. Mở file deployment `accounts.yaml`
2. Thay đổi giá trị `replicas` từ `1` thành `2`
3. Lưu file

### Áp Dụng Các Thay Đổi

```bash
kubectl apply -f 5_accounts.yaml
```

Kubernetes thông minh phát hiện các thay đổi và cập nhật deployment tương ứng.

### Xác Minh Việc Mở Rộng

Kiểm tra lại replica set:

```bash
kubectl get replicaset
```

Đối với accounts deployment, bạn sẽ thấy:
- Desired: 2
- Current: 2
- Ready: 2

Xác nhận bằng:

```bash
kubectl get pods
```

Bạn sẽ thấy hai pods cho accounts microservice:
- Pod gốc (được tạo trước đó)
- Pod mới (vừa được tạo để khớp với trạng thái mong muốn)

## Thực Hành Self-Healing

### Xóa Pod Thủ Công

Để minh họa khả năng tự phục hồi, hãy xóa thủ công một trong các pods của accounts microservice:

```bash
kubectl delete pod <tên-pod>
```

Thay thế `<tên-pod>` bằng tên thực tế của một trong các pods accounts của bạn.

### Quan Sát Khôi Phục Tự Động

Ngay lập tức kiểm tra replica set:

```bash
kubectl get replicaset
```

Giá trị current nên vẫn là 2 vì Kubernetes đã đang làm việc để khôi phục trạng thái mong muốn.

Kiểm tra các pods:

```bash
kubectl get pods
```

Bạn sẽ nhận thấy:
- Pod bị xóa đã biến mất
- Một pod mới đã được tự động tạo ra (tuổi: vài giây)
- Trạng thái mong muốn khớp với trạng thái hiện tại

### Xem Các Sự Kiện Kubernetes

Để xem những gì đã xảy ra đằng sau hậu trường:

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

Lệnh này hiển thị tất cả các sự kiện được sắp xếp theo thời gian tạo. Bạn sẽ thấy:
1. **Killing event**: Khi bạn xóa pod thủ công
2. **Create event**: Khi Kubernetes tự động tạo pod thay thế

Ví dụ về các thông báo đầu ra:
- "Killing pod..."
- "Successfully created pod..."
- "Created pod accounts-deployment-..."

## Những Điểm Chính

1. **Self-Healing**: Kubernetes liên tục giám sát các containers và tự động thay thế những containers không khỏe mạnh hoặc bị tắt
2. **Quản Lý Trạng Thái Mong Muốn**: Kubernetes luôn làm việc để khớp trạng thái hiện tại với trạng thái mong muốn được định nghĩa trong các deployment files
3. **Tính Khả Dụng Cao**: Việc khôi phục tự động này đảm bảo microservices của bạn vẫn khả dụng mà không cần can thiệp thủ công
4. **Vượt Trội hơn Docker Compose**: Những khả năng này không có sẵn trong Docker độc lập hoặc Docker Compose, làm cho Kubernetes trở nên thiết yếu cho môi trường production

## Thực Tiễn Tốt Nhất

- Định nghĩa số lượng replica phù hợp dựa trên yêu cầu tải của ứng dụng
- Giám sát các sự kiện Kubernetes thường xuyên để hiểu hành vi của cluster
- Sử dụng health checks và readiness probes để giúp Kubernetes đưa ra quyết định có căn cứ
- Test khả năng tự phục hồi trong môi trường non-production trước

## Kết Luận

Khả năng tự phục hồi của Kubernetes là một trong những tính năng mạnh mẽ nhất để chạy microservices trong môi trường production. Bằng cách tự động duy trì trạng thái mong muốn, Kubernetes đảm bảo tính khả dụng cao và giảm gánh nặng vận hành cho các nhóm phát triển. Các nền tảng điều phối container như Kubernetes là thiết yếu để quản lý các kiến trúc microservice phức tạp ở quy mô lớn.

---

*Hướng dẫn này là một phần của loạt bài toàn diện về microservices bao gồm Spring Boot, Kubernetes và kiến trúc cloud-native.*




FILE: 48-kubernetes-rolling-updates-and-rollbacks.md


# Kubernetes Rolling Updates và Rollbacks

## Tổng Quan

Hướng dẫn này trình bày cách triển khai các thay đổi mới vào Kubernetes cluster mà không gây gián đoạn dịch vụ, đồng thời cách rollback về phiên bản trước khi gặp sự cố. Chúng ta sẽ khám phá các chiến lược triển khai tích hợp sẵn của Kubernetes thông qua ví dụ về microservices Spring Boot.

## Yêu Cầu Trước

- Kubernetes cluster đang chạy
- Công cụ kubectl CLI đã được cấu hình
- Docker images đã được push lên registry
- Hiểu biết cơ bản về Kubernetes deployments

## Scaling Deployments (Mở Rộng Triển Khai)

### Phương Pháp 1: Sử Dụng Lệnh kubectl scale

Bạn có thể scale deployments trực tiếp từ dòng lệnh:

```bash
kubectl scale deployment accounts-deployment --replicas=1
```

Lệnh này scale `accounts-deployment` xuống còn 1 replica.

### Phương Pháp 2: Cập Nhật File YAML Manifest

Hoặc bạn có thể cập nhật trường `replicas` trong file Kubernetes manifest và apply các thay đổi:

```yaml
spec:
  replicas: 1
```

**Best Practice (Thực Hành Tốt Nhất):** Luôn cập nhật các file YAML manifest ngay cả khi sử dụng lệnh kubectl để đảm bảo tính nhất quán cho các lần triển khai sau.

### Kiểm Tra Deployments Đã Scale

Kiểm tra trạng thái pod hiện tại:

```bash
kubectl get pods
kubectl get replicaset
```

Output sẽ hiển thị số lượng replicas mong muốn và thực tế cho mỗi deployment.

## Rolling Updates (Cập Nhật Luân Chuyển)

### Hiểu Về Triển Khai Không Gián Đoạn

Kubernetes thực hiện rolling updates bằng cách:
1. Tạo pods mới với image đã cập nhật
2. Đợi pods mới sẵn sàng
3. Ngừng các pods cũ từng bước một
4. Không bao giờ kill tất cả instances cùng lúc

### Cập Nhật Container Images

#### Phương Pháp 1: Sử Dụng Lệnh kubectl set image

```bash
kubectl set image deployment/gatewayserver-deployment gatewayserver=eazybytes/gatewayserver:s11 --record
```

**Giải Thích Lệnh:**
- `deployment/gatewayserver-deployment` - Tên deployment đích
- `gatewayserver` - Tên container trong deployment
- `eazybytes/gatewayserver:s11` - Docker image mới với tag
- `--record` - Ghi lại lý do triển khai (đã deprecated nhưng vẫn hữu ích)

**Lưu Ý:** Flag `--record` đã bị deprecated và có thể bị loại bỏ trong các phiên bản Kubernetes tương lai. Nếu gặp lỗi, hãy xóa flag này.

#### Phương Pháp 2: Cập Nhật File YAML Manifest

Cập nhật image tag trong file deployment YAML và apply:

```yaml
spec:
  containers:
  - name: gatewayserver
    image: eazybytes/gatewayserver:s11
```

```bash
kubectl apply -f gateway.yaml
```

### Giám Sát Rolling Updates

Theo dõi quá trình triển khai:

```bash
kubectl get pods
```

Bạn sẽ quan sát thấy:
- Pods mới được tạo với trạng thái "ContainerCreating"
- Pods mới chuyển sang trạng thái "Running"
- Pods cũ chỉ bị terminate sau khi pods mới hoạt động ổn định

### Xử Lý Triển Khai Thất Bại

Nếu bạn chỉ định tag image không hợp lệ, Kubernetes sẽ:
1. Cố gắng pull image
2. Hiển thị trạng thái "ImagePullBackOff" hoặc "ErrImagePull"
3. **Giữ các pods hiện tại đang chạy** - Không có downtime!
4. Không terminate các pods đang hoạt động cho đến khi pods mới được tạo thành công

Ví dụ với image không hợp lệ:

```bash
kubectl set image deployment/gatewayserver-deployment gatewayserver=eazybytes/gatewayserver:s111
```

Kết quả: Các pods cũ tiếp tục phục vụ traffic trong khi pods mới không khởi động được.

### Xem Các Events Của Deployment

Kiểm tra events chi tiết để hiểu điều gì đã xảy ra:

```bash
kubectl get events
```

Events hiển thị:
- Các thao tác pull image
- Lên lịch pods
- Tạo containers
- Khởi động pods
- Terminate pods cũ

### Xác Minh Triển Khai

Kiểm tra phiên bản image hiện tại:

```bash
kubectl describe pod <pod-name>
```

Tìm trường `Image:` trong output để xác nhận phiên bản đã triển khai.

## Rollback Operations (Thao Tác Rollback)

### Xem Lịch Sử Rollout

Xem tất cả các revisions của deployment:

```bash
kubectl rollout history deployment/gatewayserver-deployment
```

Output hiển thị:
- Số revision
- Nguyên nhân thay đổi (nếu dùng --record)
- Cấu hình deployment

### Rollback Về Phiên Bản Trước

#### Rollback Về Revision Ngay Trước Đó

```bash
kubectl rollout undo deployment/gatewayserver-deployment
```

#### Rollback Về Revision Cụ Thể

```bash
kubectl rollout undo deployment/gatewayserver-deployment --to-revision=1
```

Lệnh này rollback về revision 1, khôi phục trạng thái hoạt động trước đó.

### Xác Minh Rollback

1. Kiểm tra trạng thái pod:
```bash
kubectl get pods
```

2. Xác minh phiên bản image:
```bash
kubectl describe pod <new-pod-name>
```

Image tag phải phản ánh revision trước đó.

## Hiểu Kiến Trúc Deployment Của Kubernetes

### Hệ Thống Phân Cấp Deployment

```
Deployment (Chỉ thị/Thông số kỹ thuật)
    ↓
ReplicaSet (Quản lý số lượng replicas mong muốn)
    ↓
Pods (Được tạo dựa trên số lượng replicas)
    ↓
Containers (Instances microservice thực tế)
```

**Biểu Diễn Trực Quan:**
- **Deployment**: Định nghĩa trạng thái mong muốn và thông số kỹ thuật
- **ReplicaSet**: Tạo và quản lý pods dựa trên số lượng replicas
- **Pods**: Lưu trữ các containers thực tế
- **Containers**: Chạy ứng dụng microservice

Nếu chỉ định `replicas: 2`, ReplicaSet sẽ tạo 2 pods, mỗi pod chứa container microservice.

## Auto-Scaling (Mở Rộng Tự Động - Nâng Cao)

Kubernetes hỗ trợ **Horizontal Pod Autoscaler (HPA)** cho việc scale tự động dựa trên:
- Sử dụng CPU
- Sử dụng Memory
- Custom metrics

Ví dụ cấu hình HPA:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gatewayserver-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gatewayserver-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

**Lưu Ý:** Auto-scaling thường được quản lý bởi Kubernetes administrators trong môi trường production. Để biết thông tin chi tiết, tham khảo [tài liệu chính thức của Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

## Best Practices (Thực Hành Tốt Nhất)

1. **Luôn test trong môi trường development** trước khi deploy lên production
2. **Giữ các file YAML manifests được cập nhật** để phản ánh trạng thái hiện tại
3. **Sử dụng image tags có ý nghĩa** (tránh `latest` trong production)
4. **Giám sát tiến trình rollout** với `kubectl get pods -w`
5. **Duy trì lịch sử rollout** để dễ dàng rollback
6. **Đặt resource limits phù hợp** để tránh vấn đề về memory/CPU
7. **Sử dụng health checks** (liveness và readiness probes)
8. **Ghi chép các thay đổi** trong deployment annotations

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

1. **ImagePullBackOff**: Tên hoặc tag image không hợp lệ
   - Giải pháp: Xác minh image tồn tại trong registry

2. **CrashLoopBackOff**: Container khởi động nhưng ngay lập tức crash
   - Giải pháp: Kiểm tra logs ứng dụng với `kubectl logs <pod-name>`

3. **Insufficient Memory**: Pods không thể được scheduled
   - Giải pháp: Giảm số lượng replicas hoặc tăng tài nguyên node

4. **Pending Pods**: Không có tài nguyên khả dụng
   - Giải pháp: Scale cluster hoặc giảm resource requests

## Tóm Tắt

Kubernetes cung cấp các công cụ mạnh mẽ cho triển khai không gián đoạn:

- **Rolling Updates**: Triển khai thay đổi từng bước mà không làm gián đoạn dịch vụ
- **Rollbacks**: Nhanh chóng quay về phiên bản hoạt động trước đó
- **Scaling**: Điều chỉnh số lượng replicas một cách linh hoạt
- **Auto-scaling**: Tự động scale dựa trên nhu cầu (nâng cao)

Với những tính năng này, Kubernetes đảm bảo tính khả dụng cao và độ tin cậy cho kiến trúc microservices của bạn.

## Tài Liệu Tham Khảo

- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)




FILE: 49-kubernetes-service-types-for-microservices.md


# Các Loại Service trong Kubernetes cho Microservices

## Tổng Quan

Khi triển khai microservices lên Kubernetes, việc hiểu rõ các loại service là vô cùng quan trọng để expose ứng dụng một cách đúng đắn. Hướng dẫn này đề cập đến ba loại service chính trong Kubernetes: ClusterIP, NodePort và LoadBalancer, kèm theo các ví dụ thực tế cho Spring Boot microservices.

## Vấn Đề Khi Expose Tất Cả Services

Ban đầu, bạn có thể triển khai tất cả microservices với service type là LoadBalancer, expose chúng ra thế giới bên ngoài:
- Loans microservice
- Cards microservice
- Gateway server
- Eureka server
- Keycloak
- Config server

**Tuy nhiên, đây KHÔNG phải là cách tiếp cận đúng!**

Chỉ có **Gateway server** nên được expose ra bên ngoài vì nó đóng vai trò là edge server. Tất cả các client communications nên được định tuyến qua gateway, không phải trực tiếp đến từng microservice riêng lẻ.

## Ba Loại Service Chính

### 1. ClusterIP Service

**Service type mặc định** - Được sử dụng cho giao tiếp nội bộ trong Kubernetes cluster.

#### Đặc điểm:
- Tạo một địa chỉ IP nội bộ cho giao tiếp trong cluster
- **KHÔNG thể truy cập** từ bên ngoài cluster
- Service type mặc định nếu không chỉ định
- Tốt nhất cho việc bảo mật microservices khỏi traffic bên ngoài

#### Use Case:
Hoàn hảo cho các backend microservices (accounts, loans, cards) chỉ nên giao tiếp nội bộ.

#### Cấu Hình Ví Dụ:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: accounts
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: accounts
```

#### Cách Hoạt Động:

1. **Container Port**: Microservice chạy trên port 8080 bên trong pod
2. **Service Port**: Được expose cho các services khác tại port 80 thông qua ClusterIP
3. **Phương Thức Truy Cập**: Các services khác sử dụng:
   - Địa chỉ ClusterIP
   - Tên service (ví dụ: `http://accounts:80`)

#### Load Balancing:
Kubernetes tự động cân bằng tải các requests giữa nhiều pod replicas. Nếu bạn có 2 replicas trên các worker nodes khác nhau, Kubernetes phân phối traffic một cách thông minh mà client không cần biết vị trí của pods.

**Ví Dụ Setup:**
- Worker Node 1: Accounts pod (port 8080)
- Worker Node 2: Accounts pod (port 8080)
- ClusterIP Service: Expose cả hai tại port 80

Các services khác chỉ cần gọi `http://accounts:80` và Kubernetes sẽ xử lý routing!

---

### 2. NodePort Service

Expose service trên IP của mỗi worker node tại một port cố định.

#### Đặc điểm:
- Tự động gán một port trong khoảng: **30000-32767**
- Có thể truy cập từ bên ngoài cluster
- Yêu cầu biết địa chỉ IP của worker nodes
- Được xây dựng trên ClusterIP

#### Cấu Hình Ví Dụ:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: accounts
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 32593  # Tùy chọn - tự động tạo nếu không chỉ định
  selector:
    app: accounts
```

#### Luồng Traffic:

1. Client bên ngoài gửi request đến: `http://<worker-node-ip>:32593`
2. Request đến NodePort (32593)
3. Chuyển tiếp đến ClusterIP service (port 80)
4. Cân bằng tải đến pod phù hợp (port 8080)

#### Nhược Điểm:

❌ **Vấn Đề IP Động**: Nếu worker node bị lỗi và được thay thế, địa chỉ IP của nó sẽ thay đổi
❌ **Phụ Thuộc Client**: Clients bên ngoài phải theo dõi và cập nhật địa chỉ IP của worker nodes
❌ **Không Sẵn Sàng Production**: Khó quản lý trong môi trường production

---

### 3. LoadBalancer Service

Cung cấp một external load balancer với địa chỉ IP public tĩnh.

#### Đặc điểm:
- Tạo một external load balancer (được cung cấp bởi cloud provider)
- Gán một **địa chỉ IP public tĩnh**
- Được xây dựng trên NodePort và ClusterIP
- Sẵn sàng production cho external traffic

#### Cấu Hình Ví Dụ:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: gateway
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: gateway
```

#### Luồng Traffic:

1. Client bên ngoài gửi request đến: `http://<public-ip-or-domain>`
2. Load Balancer nhận traffic (IP public tĩnh)
3. Chuyển tiếp đến NodePort của worker node phù hợp
4. NodePort chuyển tiếp đến ClusterIP service
5. Cân bằng tải đến pod container phù hợp

#### Ưu Điểm:

✅ **IP Public Tĩnh**: Không bao giờ thay đổi trừ khi admin thay đổi thủ công
✅ **Ánh Xạ DNS**: Có thể ánh xạ tới tên miền (ví dụ: `api.mycompany.com`)
✅ **Đơn Giản Cho Client**: Clients sử dụng một endpoint duy nhất bất kể cluster thay đổi
✅ **Tự Động Theo Dõi**: Load balancer tự động theo dõi thay đổi của worker nodes
✅ **Mở Rộng Động**: Xử lý việc scaling replicas tự động (2 → 3 replicas)

---

## Best Practices cho Microservices

### Chiến Lược Service Type Được Khuyến Nghị:

| Microservice | Service Type | Lý Do |
|-------------|-------------|-------|
| Gateway Server | LoadBalancer | Điểm vào cho tất cả external traffic |
| Eureka Server | ClusterIP | Chỉ service discovery nội bộ |
| Config Server | ClusterIP | Quản lý cấu hình nội bộ |
| Accounts Service | ClusterIP | Backend service - không cần truy cập bên ngoài |
| Loans Service | ClusterIP | Backend service - không cần truy cập bên ngoài |
| Cards Service | ClusterIP | Backend service - không cần truy cập bên ngoài |
| Keycloak | LoadBalancer (tùy chọn) | Có thể cần truy cập bên ngoài cho OAuth flows |

### Lợi Ích Bảo Mật:

Sử dụng ClusterIP cho backend services mang lại:
- Bảo vệ khỏi truy cập bên ngoài không được ủy quyền
- Ngăn chặn việc expose trực tiếp microservices
- Thực thi gateway pattern (điểm vào duy nhất)
- Giảm bề mặt tấn công

---

## Tóm Tắt

Hiểu rõ các loại service trong Kubernetes là **thiết yếu** cho các nhà phát triển microservice:

- **ClusterIP**: Giao tiếp nội bộ, lựa chọn mặc định cho backend services
- **NodePort**: Truy cập bên ngoài qua node IP, phù hợp cho testing/development
- **LoadBalancer**: Sẵn sàng production cho truy cập bên ngoài với IP tĩnh

**Điểm Chính**: Chỉ expose Gateway server của bạn với LoadBalancer. Giữ tất cả các microservices khác ở chế độ internal bằng ClusterIP để có bảo mật và kiến trúc tốt hơn.

---

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ xem một demo thực tế về cấu hình các loại service này trong một deployment Spring Boot microservices thực tế.

**Chúc Bạn Học Tốt!** 🚀




FILE: 5-obtaining-access-token-from-keycloak-auth-server.md


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




FILE: 50-kubernetes-service-types-demo-and-implementation.md


# Demo và Triển Khai Các Loại Dịch Vụ Kubernetes

## Tổng Quan

Hướng dẫn này trình bày ba loại dịch vụ Kubernetes chính (LoadBalancer, ClusterIP và NodePort) và cách chúng hoạt động khi expose microservices trong Kubernetes cluster.

## Hiểu Về Triển Khai Dịch Vụ Hiện Tại

### Kiểm Tra Các Dịch Vụ Đã Triển Khai

Để xem tất cả các dịch vụ trong Kubernetes cluster, chạy lệnh:

```bash
kubectl get services
```

Lệnh này hiển thị:
- Tên dịch vụ
- Loại dịch vụ
- IP bên ngoài (nếu có)
- Cổng và node port

### Loại Dịch Vụ: LoadBalancer

Microservice accounts ban đầu được triển khai với loại LoadBalancer:

**Đặc điểm:**
- **External IP**: `localhost` (trong cluster local) hoặc public IP (trong môi trường cloud)
- **Port**: 8080
- **NodePort**: Được tạo ngẫu nhiên (ví dụ: 30175)

**Luồng Request:**
1. Request từ bên ngoài → LoadBalancer (External IP)
2. LoadBalancer → NodePort
3. NodePort → ClusterIP
4. ClusterIP → Container microservice

**Kiểm Tra LoadBalancer:**
```
http://localhost:8080/api/contact-info
```

### Những Cân Nhắc Quan Trọng Với LoadBalancer

**Tại Sao Nên Tránh LoadBalancer Trong Production:**

1. **Vấn Đề Bảo Mật**: Microservices không nên được truy cập trực tiếp từ client bên ngoài. Traffic nên đi qua edge server/API gateway.

2. **Chi Phí**: Trong môi trường cloud:
   - Địa chỉ IP công khai không miễn phí
   - Mỗi LoadBalancer cần một public IP riêng
   - 100 microservices = 100 public IP = hóa đơn cloud đáng kể

## Triển Khai Loại Dịch Vụ ClusterIP

### Cấu Hình

Chỉnh sửa file Kubernetes manifest cho microservice accounts:

```yaml
type: ClusterIP
```

**Lưu ý**: "IP" phải viết hoa.

### Áp Dụng Cấu Hình

```bash
kubectl apply -f accounts-microservice.yaml
kubectl get services
```

### Hoạt Động Của ClusterIP

**Đặc điểm:**
- **External IP**: Không có
- **Cluster IP**: Chỉ có IP nội bộ
- **Port**: 8080
- **Khả năng truy cập**: Chỉ từ bên trong Kubernetes cluster

**Kết quả**: Các request từ trình duyệt bên ngoài tới API sẽ thất bại với lỗi "site cannot be reached", vì traffic từ bên ngoài cluster bị chặn.

**Giao Tiếp Nội Bộ**: Các ứng dụng khác trong cluster có thể giao tiếp sử dụng:
- Tên dịch vụ: `accounts`
- Địa chỉ Cluster IP
- Port: 8080

## Triển Khai Loại Dịch Vụ NodePort

### Cấu Hình

Chỉnh sửa file Kubernetes manifest:

```yaml
type: NodePort
```

Không cần chỉ định giá trị NodePort cụ thể; Kubernetes sẽ tạo ngẫu nhiên.

### Áp Dụng Cấu Hình

```bash
kubectl apply -f accounts-microservice.yaml
kubectl get services
```

### Hoạt Động Của NodePort

**Ví dụ Output:**
- **Service Type**: NodePort
- **NodePort**: 31182 (được tạo ngẫu nhiên)

**Truy Cập Microservice:**

❌ **Thất bại** - Sử dụng service port:
```
http://localhost:8080/api/contact-info
```

✅ **Thành công** - Sử dụng NodePort:
```
http://localhost:31182/api/contact-info
```

### Hạn Chế Của NodePort

- Cần sử dụng NodePort cụ thể để truy cập từ bên ngoài
- Nếu microservice được triển khai vào worker node khác, địa chỉ IP sẽ thay đổi
- Có thể gây vấn đề về khả năng truy cập trong production

## Thực Hành Tốt Nhất và Khuyến Nghị

### Lựa Chọn Loại Dịch Vụ

| Loại Dịch Vụ | Trường Hợp Sử Dụng | Khả Năng Truy Cập |
|--------------|-------------------|-------------------|
| **ClusterIP** | Microservices nội bộ | Chỉ trong cluster |
| **NodePort** | Phát triển/kiểm thử | Bên ngoài qua NodePort |
| **LoadBalancer** | Dịch vụ công khai | Bên ngoài qua public IP |

### Khuyến Nghị Cho Production

1. **Gateway Server**: Chỉ sử dụng LoadBalancer cho API Gateway/Edge Server
2. **Microservices Nội Bộ**: Sử dụng ClusterIP cho tất cả microservices khác
3. **Bảo Mật**: Định tuyến tất cả traffic bên ngoài qua gateway server
4. **Tối Ưu Chi Phí**: Giảm thiểu việc sử dụng LoadBalancer để giảm chi phí cloud

### Chiến Lược Triển Khai Tương Lai

Trong các phần tiếp theo về Kafka, Grafana và các thành phần khác:
- Thay đổi tất cả microservices sang loại **ClusterIP**
- **Ngoại lệ**: Giữ Gateway Server là **LoadBalancer**
- Điều này đảm bảo bảo mật và quản lý chi phí hợp lý

## Khôi Phục Thay Đổi

Cho mục đích học tập trong giai đoạn triển khai Kubernetes ban đầu, microservice accounts vẫn giữ là LoadBalancer:

```yaml
type: LoadBalancer
```

Điều này giúp dễ hiểu và kiểm thử hơn khi bạn làm việc qua các khái niệm triển khai Kubernetes.

## Tóm Tắt

- **LoadBalancer**: Expose dịch vụ ra bên ngoài với public IP (tốn kém, sử dụng hạn chế)
- **ClusterIP**: Chỉ truy cập nội bộ (được khuyến nghị cho hầu hết microservices)
- **NodePort**: Truy cập bên ngoài qua node port (phù hợp cho phát triển)

Hiểu các loại dịch vụ này rất quan trọng cho kiến trúc microservice Kubernetes và chiến lược triển khai phù hợp.

---

**Bước Tiếp Theo**: Trong các bài giảng tiếp theo, chúng ta sẽ khám phá việc bảo mật microservices và triển khai các mẫu gateway phù hợp với các loại dịch vụ Kubernetes.




FILE: 51-kubernetes-helm-introduction-and-deployment-challenges.md


# Các Thách Thức Triển Khai Kubernetes và Giới Thiệu Helm

## Tổng Quan

Tài liệu này thảo luận về các thách thức khi triển khai microservices lên Kubernetes sử dụng các file manifest cơ bản và giới thiệu Helm như một giải pháp cho những vấn đề này.

## Phương Pháp Triển Khai Hiện Tại

Hiện tại, tất cả các microservices đã được triển khai thành công vào Kubernetes cluster bằng cách sử dụng các file manifest của Kubernetes. Phương pháp này hoạt động tốt cho các dự án nhỏ, nhưng gặp nhiều thách thức khi mở rộng lên môi trường production thực tế.

### Thiết Lập Hiện Có

- Tất cả các file manifest Kubernetes được duy trì trong thư mục `Section15/Kubernetes`
- Hiện đang quản lý 8 file manifest Kubernetes khác nhau
- Các file này xử lý:
  - Tạo ConfigMap
  - Triển khai microservice
  - Expose các microservice

## Các Thách Thức Chính với Triển Khai Kubernetes Cơ Bản

### 1. Quản Lý Số Lượng Lớn File Manifest

**Vấn đề**: Với chỉ 6-7 microservices, việc quản lý các file manifest tương đối đơn giản. Tuy nhiên, trong các dự án thực tế với hàng trăm microservices, việc tạo và duy trì các file manifest riêng lẻ trở thành cơn ác mộng.

**Tác động**: 
- Số lượng file tăng theo cấp số nhân
- Khó duy trì tính nhất quán
- Mất thời gian cho việc cập nhật và sửa đổi

### 2. Áp Dụng File Manifest Thủ Công

**Vấn đề**: Mỗi file manifest phải được áp dụng riêng lẻ bằng các lệnh như:

```bash
kubectl apply -f <manifest-file>
```

**Tác động**:
- Với 100 microservices, lệnh này phải chạy 100 lần
- Dễ xảy ra lỗi do con người
- Quá trình triển khai mất thời gian
- Không có cách hiệu quả để triển khai tất cả services cùng lúc

### 3. Quản Lý Nhiều Môi Trường

**Vấn đề**: Các tổ chức thường có nhiều môi trường (Development, QA, Production), mỗi môi trường có yêu cầu khác nhau:

- **Development**: 1 replica cho mỗi microservice
- **QA**: 3 replicas cho mỗi microservice
- **Production**: 5-10 replicas dựa trên traffic

**Tác động**:
- Cần duy trì các file manifest riêng cho từng môi trường
- Hàng trăm file manifest nhân với số lượng môi trường
- Gấp đôi hoặc gấp ba tổng số file cần quản lý
- Khó theo dõi cấu hình đặc thù cho từng môi trường

### 4. Quy Trình Gỡ Cài Đặt Phức Tạp

**Vấn đề**: Gỡ cài đặt microservices yêu cầu chạy lệnh delete cho từng service riêng lẻ:

```bash
kubectl delete -f <manifest-file>
```

**Minh họa quy trình xóa**:
1. Xóa Gateway Server
2. Xóa Cards microservice
3. Xóa Loans microservice
4. Xóa Accounts microservice
5. Xóa Eureka Server
6. Xóa Config Server
7. Xóa ConfigMap
8. Xóa Keycloak

**Tác động**:
- Cực kỳ tẻ nhạt với các deployment lớn
- Nguy cơ cao bỏ sót services trong quá trình dọn dẹp
- Không có cách hiệu quả để xóa tất cả services cùng lúc

## Giải Pháp: Helm

### Helm là gì?

**Helm là package manager cho Kubernetes** giải quyết tất cả các thách thức đã đề cập ở trên.

### Lợi Ích Chính

- Đơn giản hóa việc triển khai và quản lý microservice
- Xử lý nhiều file manifest như một package duy nhất
- Hỗ trợ cấu hình đặc thù cho từng môi trường
- Cung cấp khả năng cài đặt và gỡ cài đặt dễ dàng
- Làm cho cuộc sống DevOps "cực kỳ, cực kỳ dễ dàng"

### Tiếp Theo Là Gì?

Phần tiếp theo sẽ tập trung vào:
- Thiết lập Helm
- Cấu hình microservices với Helm
- Các minh họa thực tế
- Best practices khi sử dụng Helm

## Code Repository

Tất cả các file manifest Kubernetes từ Section 15 có sẵn trong GitHub repository để tham khảo. Lưu ý rằng không có thay đổi code microservice nào được thực hiện trong phần này - trọng tâm hoàn toàn là các khái niệm triển khai Kubernetes.

## Tóm Tắt

Mặc dù các file manifest Kubernetes cơ bản hoạt động tốt cho các deployment nhỏ, chúng đưa ra những thách thức đáng kể khi mở rộng quy mô:
- Khó quản lý hàng trăm files
- Quy trình triển khai thủ công, lặp đi lặp lại
- Cấu hình phức tạp cho nhiều môi trường
- Thủ tục gỡ cài đặt tẻ nhạt

Helm giải quyết tất cả các thách thức này bằng cách cung cấp phương pháp package manager cho Kubernetes deployments, đơn giản hóa đáng kể quy trình làm việc DevOps cho kiến trúc microservices.

---

**Ghi nhớ**: Dành thời gian để hiểu những thách thức này trước khi chuyển sang Helm, vì nó sẽ giúp bạn đánh giá cao giá trị mà Helm mang lại cho các deployment Kubernetes.




FILE: 52-kubernetes-helm-introduction-and-benefits.md


# Kubernetes Helm: Giới Thiệu và Lợi Ích

## Tổng Quan

Trong bài giảng này, chúng ta sẽ tìm hiểu chi tiết về Helm - tìm hiểu Helm là gì, cách hoạt động và cách nó giải quyết các thách thức quan trọng trong việc triển khai Kubernetes cho các ứng dụng microservices.

## Helm là gì?

**Helm là trình quản lý gói (package manager) cho Kubernetes.** Mục tiêu chính của Helm là giúp các nhà phát triển và thành viên nhóm DevOps quản lý các dự án và triển khai Kubernetes bằng cách cung cấp phương pháp hiệu quả hơn trong việc xử lý các tệp manifest của Kubernetes.

Bất kể bạn có bao nhiêu microservices trong mạng lưới microservice của mình, Helm sẽ giúp cuộc sống của bạn dễ dàng hơn.

## Vấn Đề Khi Không Sử Dụng Helm

Khi không có Helm, các nhóm phải đối mặt với một số thách thức:

1. **Nhiều Tệp Manifest**: Bạn cần duy trì nhiều tệp manifest Kubernetes (deployment, service, config map) cho mỗi microservice bạn triển khai
2. **Thao Tác Thủ Công**: Các thành viên nhóm DevOps phải áp dụng hoặc xóa thủ công các tệp manifest Kubernetes này bằng các lệnh kubectl
3. **Vấn Đề Khả Năng Mở Rộng**: Khi mạng lưới microservice của bạn phát triển, việc quản lý các tệp riêng lẻ trở nên ngày càng phức tạp

## Cách Helm Giải Quyết Các Thách Thức Này

### Helm Charts

Helm sử dụng định dạng đóng gói gọi là **Charts**. Một chart là tập hợp các tệp mô tả một nhóm tài nguyên Kubernetes có liên quan.

**Tính Năng Chính:**
- Gộp tất cả các tệp manifest của microservices vào một thành phần duy nhất gọi là Chart
- Triển khai các ứng dụng đơn giản hoặc phức tạp (HTTP servers, REST APIs, databases, các thành phần cache)
- Hỗ trợ child charts và dependent charts (tương tự như lớp cha/lớp con trong Java)
- Cài đặt toàn bộ cây phụ thuộc chỉ với một lệnh duy nhất

### Ví Dụ: Các Tệp Service Manifest

**Không có Helm**, bạn cần các tệp manifest riêng biệt:
- `account-service.yaml`
- `loan-service.yaml`
- `card-service.yaml`

Các tệp này chia sẻ cùng một khung với chỉ một vài giá trị động:
- **Giá trị tĩnh**: API version (v1), kind (Service), protocol (TCP)
- **Giá trị động**: metadata name, app selector, service type, ports

**Với Helm**, bạn tạo:
1. **template.yaml duy nhất** - Chứa cấu trúc tĩnh với các placeholder cho giá trị động
2. **Nhiều values.yaml** - Một tệp cho mỗi microservice với cấu hình cụ thể

```yaml
# Ví dụ Helm Service Template
metadata:
  name: {{ .Values.deploymentLabel }}
spec:
  selector:
    app: {{ .Values.deploymentLabel }}
  type: {{ .Values.serviceType }}
```

```yaml
# values.yaml cho Accounts Microservice
deploymentLabel: accounts
serviceType: LoadBalancer
port: 8080
```

Tại thời điểm chạy, Helm tự động tạo các tệp manifest Kubernetes bằng cách kết hợp template với các giá trị.

## Helm như một Trình Quản Lý Gói

**Trình quản lý gói (package manager)** giúp bạn cài đặt, gỡ cài đặt hoặc nâng cấp các gói phần mềm. Các ví dụ phổ biến bao gồm:

- **Pip** - Trình quản lý gói Python
- **NPM** - Trình quản lý gói JavaScript (cho Angular, React, v.v.)
- **Helm** - Trình quản lý gói Kubernetes

Helm là cách tốt nhất để tìm kiếm, chia sẻ và sử dụng phần mềm được xây dựng cho Kubernetes.

## Lợi Ích Chính của Helm

### 1. Hỗ Trợ Đóng Gói
- Gói các tệp manifest Kubernetes vào một Helm chart duy nhất
- Phân phối charts đến các kho lưu trữ công khai hoặc riêng tư
- Chia sẻ charts với các nhóm khác (tương tự như chia sẻ mã Java)

### 2. Cài Đặt Dễ Dàng Hơn
- Triển khai, nâng cấp, rollback hoặc gỡ cài đặt toàn bộ ứng dụng microservice chỉ với một lệnh duy nhất
- Không cần chạy các lệnh kubectl thủ công
- Quy trình triển khai được đơn giản hóa

### 3. Quản Lý Phát Hành và Phiên Bản
- Rollback toàn bộ Kubernetes cluster về trạng thái hoạt động trước đó chỉ với một lệnh duy nhất
- Không giống như các tệp manifest Kubernetes tiêu chuẩn (chỉ hỗ trợ rollback từng microservices riêng lẻ)
- Kiểm soát phiên bản ở cấp độ cluster hoàn chỉnh

## Tóm Tắt

Helm là một trình quản lý gói mạnh mẽ cho Kubernetes với các đặc điểm:
- Đơn giản hóa việc quản lý các tệp manifest Kubernetes thông qua Charts
- Giảm các thao tác thủ công với triển khai một lệnh duy nhất
- Hỗ trợ mạng lưới microservice phức tạp với dependent charts
- Cung cấp khả năng kiểm soát phiên bản và rollback mạnh mẽ

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu hơn vào Helm charts và khám phá các minh họa thực tế về các tính năng này.

## Các Bước Tiếp Theo

Chúng ta sẽ tiếp tục khám phá Helm charts một cách chi tiết, làm cho các khái niệm trở nên rõ ràng hơn thông qua các ví dụ thực tế và minh họa.

---

**Cảm ơn bạn, và tôi sẽ gặp bạn trong bài giảng tiếp theo!**




FILE: 53-kubernetes-helm-installation-guide.md


# Hướng Dẫn Cài Đặt Kubernetes Helm

## Giới Thiệu

Hướng dẫn này sẽ hướng dẫn bạn qua quy trình cài đặt Helm, trình quản lý gói cho Kubernetes, trên các hệ điều hành khác nhau bao gồm macOS, Windows và Linux.

## Yêu Cầu Trước Khi Cài Đặt

Trước khi cài đặt Helm, hãy đảm bảo bạn đáp ứng các yêu cầu sau:

1. **Kubernetes Cluster**: Bạn cần có một Kubernetes cluster đang chạy trong hệ thống cục bộ hoặc trên bất kỳ môi trường đám mây nào.
2. **Cấu Hình Bảo Mật** (Tùy chọn): Quyết định về các cấu hình bảo mật liên quan đến quá trình cài đặt của bạn, nếu có.
3. **Cài Đặt Helm**: Cài đặt và cấu hình Helm trong hệ thống cục bộ của bạn (được đề cập trong hướng dẫn này).

## Bắt Đầu

Để bắt đầu cài đặt Helm:

1. Truy cập trang web chính thức của Helm: [helm.sh](https://helm.sh)
2. Nhấp vào nút **Get Started** ở góc trên bên phải
3. Bạn sẽ được chuyển đến trang yêu cầu cài đặt
4. Nhấp vào **Installing Helm** để truy cập hướng dẫn cài đặt

## Phương Pháp Cài Đặt

Có nhiều cách để cài đặt Helm:
- Từ bản phát hành nhị phân
- Từ các script
- **Từ trình quản lý gói** (Được khuyến nghị)

Hướng dẫn này tập trung vào việc cài đặt Helm bằng trình quản lý gói, vì đây là cách tiếp cận đơn giản nhất.

## Cài Đặt Helm trên macOS

### Sử Dụng Homebrew

Homebrew là trình quản lý gói mặc định cho macOS.

1. Mở terminal của bạn
2. Chạy lệnh sau:

```bash
brew install helm
```

3. Đợi quá trình cài đặt hoàn tất
4. Xác minh cài đặt bằng cách kiểm tra phiên bản:

```bash
helm version
```

Bạn sẽ thấy đầu ra hiển thị phiên bản Helm của bạn (ví dụ: Helm 3.2.3).

## Cài Đặt Helm trên Windows

### Sử Dụng Chocolatey

Chocolatey là trình quản lý gói phổ biến cho Hệ điều hành Windows.

### Bước 1: Cài Đặt Chocolatey

1. Truy cập trang web Chocolatey: [chocolatey.org](https://chocolatey.org)
2. Nhấp vào **Install** ở góc trên bên phải
3. Chọn tùy chọn **Individual** (để thiết lập hệ thống cục bộ cá nhân)

### Bước 2: Chuẩn Bị PowerShell

1. Mở **PowerShell** với quyền quản trị viên:
   - Đi đến hộp tìm kiếm Windows
   - Tìm kiếm "PowerShell"
   - Nhấp chuột phải và chọn "Run as Administrator" (Chạy với quyền quản trị)

2. Kiểm tra chính sách thực thi hiện tại:

```powershell
Get-ExecutionPolicy
```

3. Nếu đầu ra hiển thị "Restricted" (Bị hạn chế), bạn cần thay đổi nó:

```powershell
Set-ExecutionPolicy AllSigned
```

4. Xác minh thay đổi:

```powershell
Get-ExecutionPolicy
```

Đầu ra bây giờ sẽ hiển thị "AllSigned" thay vì "Restricted".

### Bước 3: Cài Đặt Chocolatey

1. Sao chép và thực thi lệnh cài đặt từ trang web Chocolatey trong PowerShell của bạn
2. Xác minh cài đặt Chocolatey:

```powershell
choco
```

hoặc

```powershell
choco -?
```

Lệnh này sẽ hiển thị phiên bản Chocolatey đã cài đặt.

### Bước 4: Cài Đặt Helm

Sau khi Chocolatey được cài đặt, chạy lệnh sau:

```powershell
choco install kubernetes-helm
```

### Bước 5: Xác Minh Cài Đặt Helm

```powershell
helm version
```

## Cài Đặt Helm trên Linux/Ubuntu

Đối với người dùng Linux và Ubuntu, vui lòng tham khảo trang cài đặt Helm chính thức tại [helm.sh](https://helm.sh) để biết hướng dẫn cài đặt cụ thể cho bản phân phối của bạn.

## Khắc Phục Sự Cố

Nếu bạn gặp bất kỳ sự cố nào trong quá trình cài đặt:

1. Xem lại tài liệu cài đặt Helm chính thức
2. Kiểm tra các yêu cầu tiên quyết đã được đáp ứng
3. Đảm bảo bạn có quyền quản trị viên/sudo phù hợp
4. Xác minh kết nối internet của bạn để tải xuống các gói

## Kết Luận

Bây giờ bạn đã cài đặt thành công Helm trên hệ thống cục bộ của mình. Bạn có thể xác minh điều này bằng cách chạy lệnh `helm version` trong terminal hoặc command prompt. Với Helm đã được cài đặt, bạn đã sẵn sàng để bắt đầu quản lý các ứng dụng Kubernetes bằng cách sử dụng Helm charts.

## Tài Nguyên Bổ Sung

- Tài liệu Helm chính thức: [helm.sh/docs](https://helm.sh/docs)
- Kho lưu trữ Helm trên GitHub: [github.com/helm/helm](https://github.com/helm/helm)
- Tài liệu Kubernetes: [kubernetes.io](https://kubernetes.io)




FILE: 54-bitnami-helm-charts-important-update.md


# Cập Nhật Quan Trọng Về Bitnami Images & Helm Charts

## Tổng Quan

Tài liệu này cung cấp thông tin quan trọng về những thay đổi trong mô hình cấp phép của Bitnami và cách nó ảnh hưởng đến việc triển khai các thành phần microservices sử dụng Helm Charts trong môi trường Kubernetes.

## Cập Nhật Quan Trọng: Bitnami Không Còn Là Mã Nguồn Mở

Trong các bài giảng sắp tới, chúng ta sẽ sử dụng Helm Charts để triển khai một số thành phần như:
- Kafka
- Keycloak
- Prometheus
- Loki
- Alloy
- Tempo
- Grafana

### Điều Gì Đã Thay Đổi?

Trước đây, các charts và images này được cung cấp bởi **Bitnami**, vốn là mã nguồn mở và miễn phí cho tất cả mọi người. Tuy nhiên, Bitnami hiện đã chuyển đổi thành một **sản phẩm thương mại**, và các tổ chức doanh nghiệp phải trả hàng nghìn đô la mỗi tháng để sử dụng các images và Helm Charts cấp độ production của họ.

**Thông Báo Chính Thức:**  
👉 [Cách Chuẩn Bị Cho Những Thay Đổi Của Bitnami Sắp Tới](https://docs.bitnami.com/tutorials/prepare-for-bitnami-changes/)

## Chúng Ta Sẽ Sử Dụng Gì Thay Thế

Để đảm bảo bạn có thể tiếp tục học tập một cách liền mạch, các Helm Charts tùy chỉnh đã được chuẩn bị sẵn với mục đích tương tự như Bitnami — và chúng đã sẵn sàng để sử dụng cho tất cả các bài thực hành trong khóa học này.

### GitHub Repository

Bạn có thể tìm thấy các Helm Charts tùy chỉnh trong repository GitHub dưới thư mục `helm-new`:

🔗 **Link Repository:** [https://github.com/eazybytes/microservices/tree/3.4.1/section_16/helm-new](https://github.com/eazybytes/microservices/tree/3.4.1/section_16/helm-new)

**Lưu Ý:** Không cần phải sửa đổi bất cứ điều gì bên trong các charts này — chúng đã được cấu hình đầy đủ cho các bài tập thực hành.

## Thứ Tự Triển Khai

Vui lòng cài đặt các Helm charts theo thứ tự sau, chờ **1–2 phút** giữa mỗi lần triển khai:

1. **Keycloak**
2. **Kafka**
3. **Prometheus**
4. **Loki**
5. **Alloy**
6. **Tempo**
7. **Grafana**
8. **EazyBank**

### Tại Sao Thứ Tự Này Quan Trọng

Chuỗi triển khai đảm bảo rằng các phụ thuộc được thiết lập đúng cách trước khi các dịch vụ phụ thuộc được triển khai. Việc chờ đợi giữa các lần triển khai cho phép Kubernetes khởi tạo các pods và services một cách hợp lý.

## Về Demo Charts

Các charts mà chúng ta sẽ sử dụng là **phiên bản đơn giản hóa**, nhưng các khái niệm và quy trình làm việc vẫn hoàn toàn giống như bạn sẽ trải nghiệm với các Bitnami charts cấp độ production. Điều này đảm bảo rằng:

- Bạn học được các khái niệm cơ bản giống nhau
- Kiến thức có thể chuyển đổi sang môi trường production
- Trải nghiệm học tập vẫn thực tế và thực hành

## Lưu Ý Quan Trọng

⚠️ Demo/sample Helm chart được thảo luận trong bài giảng tiếp theo dựa trên Bitnami, vốn không còn là mã nguồn mở nữa.

**Vui lòng không cài đặt hoặc chạy chart đó** — chỉ cần xem bài giảng để hiểu các khái niệm và cấu trúc của Helm chart.

## Kết Luận

Hãy tiếp tục hành trình học tập thực hành của chúng ta — chúc bạn vui vẻ khám phá Helm và Kubernetes! 🚀

---

*– Madan*

## Tài Nguyên Bổ Sung

- [Tài Liệu Chính Thức Kubernetes](https://kubernetes.io/docs/)
- [Tài Liệu Chính Thức Helm](https://helm.sh/docs/)
- [Best Practices cho Spring Boot Microservices](https://spring.io/microservices)

## Chủ Đề Liên Quan

- Container Orchestration với Kubernetes
- Cấu Trúc và Quản Lý Helm Charts
- Kiến Trúc Microservices với Spring Boot
- DevOps Best Practices cho Ứng Dụng Java




FILE: 55-helm-chart-installation-and-wordpress-deployment.md


# Hướng Dẫn Cài Đặt Helm Chart và Triển Khai WordPress

## Giới Thiệu

Hướng dẫn này minh họa sức mạnh của Helm thông qua việc cài đặt một chart mẫu từ tài liệu chính thức. Chúng ta sẽ triển khai một website WordPress trên Kubernetes cluster cục bộ sử dụng Helm charts.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu, hãy đảm bảo Kubernetes cluster cục bộ của bạn đang hoạt động.

### Kiểm Tra Trạng Thái Kubernetes Cluster

1. **Sử dụng Docker Dashboard:**
   - Mở Docker Dashboard
   - Xác nhận thông báo: "Kubernetes is running"

2. **Sử dụng lệnh kubectl:**
   ```bash
   kubectl get services
   ```
   Lệnh này liệt kê tất cả các services trong Kubernetes cluster cục bộ. Ban đầu, bạn chỉ thấy service mặc định của Kubernetes.

### Kiểm Tra Helm

Kiểm tra các cài đặt Helm hiện có trong cluster:

```bash
helm ls
```

Nếu chưa cài đặt chart nào, lệnh này sẽ trả về danh sách rỗng.

## Helm Kết Nối Với Kubernetes Như Thế Nào

Helm tự động kết nối với Kubernetes cluster bằng cách đọc thông tin cấu hình được lưu trữ cục bộ trên hệ thống của bạn.

### Vị Trí File Cấu Hình Kubernetes

- **Windows:** `C:\Users\<username>\.kube\config`
- **Linux/Mac:** `~/.kube/config`

File config này chứa tất cả thông tin kết nối mà cả `kubectl` và `helm` sử dụng để tương tác với Kubernetes cluster. Cấu hình thường bao gồm chi tiết về Docker Desktop cluster hoặc các Kubernetes cluster khác mà bạn đã kết nối.

## Tìm Kiếm Helm Charts

Helm cung cấp chức năng tìm kiếm mạnh mẽ để tìm các chart từ các repository công khai.

### Sử Dụng Helm Search Hub

Để tìm kiếm các chart WordPress:

```bash
helm search hub wordpress
```

Lệnh này tìm kiếm trên Artifact Hub tất cả các chart WordPress có sẵn từ nhiều repository khác nhau. Bạn sẽ thấy kết quả từ nhiều nguồn, bao gồm Bitnami - một repository nổi tiếng với các Helm chart sẵn sàng cho production.

## Thêm Repository Bitnami

Trước khi cài đặt chart từ Bitnami, bạn cần thêm repository vào cấu hình Helm cục bộ.

### Thêm Repository Bitnami

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Nếu repository đã tồn tại, bạn sẽ nhận được thông báo cho biết nó đã được cấu hình. Nếu chưa, nó sẽ được thêm thành công.

## Cài Đặt WordPress Sử Dụng Helm

Bây giờ bạn có thể cài đặt Helm chart WordPress từ repository Bitnami.

### Lệnh Cài Đặt

```bash
helm install happy-panda bitnami/wordpress
```

**Giải Thích Lệnh:**
- `helm install` - Lệnh cài đặt
- `happy-panda` - Tên release (bạn có thể chọn tên bất kỳ)
- `bitnami/wordpress` - Tên repository và tên chart

### Sau Khi Cài Đặt

Sau khi chạy lệnh, Helm sẽ:
1. Triển khai tất cả các Kubernetes resources cần thiết
2. Cung cấp hướng dẫn truy cập trang WordPress
3. Hiển thị các lệnh để lấy URL và thông tin đăng nhập WordPress

**Lưu ý:** Có thể mất 1-2 phút để LoadBalancer IP khả dụng.

## Truy Cập WordPress

### Lấy URL WordPress

Chạy các lệnh được cung cấp trong output cài đặt để lấy URL:

```bash
# Các lệnh cụ thể sẽ được hiển thị trong terminal output của bạn
```

Thông thường, bạn sẽ truy cập:
- **Trang Công Khai:** `http://localhost`
- **Trang Quản Trị:** `http://localhost/admin`

### Lấy Thông Tin Đăng Nhập Admin

Lấy username:
```bash
echo Username: user
```

Lấy password:
```bash
# Lệnh sẽ được cung cấp trong installation output
```

## Helm Đã Triển Khai Gì Đằng Sau

Lệnh `helm install` duy nhất đã tạo ra nhiều Kubernetes resources:

### Deployments
- WordPress application deployment
- MariaDB database deployment

### Pods
- WordPress pod(s)
- MariaDB pod(s)

### ReplicaSets
- Đảm bảo số lượng pod replicas mong muốn

### Services
- **WordPress:** LoadBalancer service type (có thể truy cập từ bên ngoài cluster)
- **MariaDB:** ClusterIP service type (chỉ truy cập nội bộ)

### ConfigMaps
- Chứa các thuộc tính môi trường và cài đặt cấu hình

### Secrets
- `happy-panda-wordpress` - Thông tin đăng nhập WordPress
- Thông tin đăng nhập database MariaDB

Tất cả các resources này làm việc cùng nhau để tạo ra một website WordPress sẵn sàng cho production.

## Khám Phá Các File Helm Chart

### Xác Định Vị Trí Cache Helm Chart

Tìm nơi Helm lưu trữ các chart đã tải xuống:

```bash
helm env
```

Tìm biến `HELM_CACHE_HOME`, thường là:
- **Windows:** `C:\Users\<username>\Library\Caches\Helm`
- **Linux/Mac:** `~/.cache/helm`

### Cấu Trúc Chart

Điều hướng đến thư mục cache:
```
<HELM_CACHE_HOME>/repository/wordpress
```

Giải nén file chart đã nén để xem cấu trúc. Chart chứa:
- Các file manifest Kubernetes (YAML)
- Templates
- File values
- Metadata của chart
- Dependencies

Các file này định nghĩa tất cả các Kubernetes resources đã được triển khai.

## Lợi Ích Của Việc Sử Dụng Helm

1. **Triển Khai Đơn Giản:** Triển khai ứng dụng phức tạp chỉ với một lệnh
2. **Sẵn Sàng Production:** Sử dụng các chart được cộng đồng duy trì với best practices
3. **Cấu Hình Nhất Quán:** Quản lý nhiều deployment dễ dàng
4. **Kiểm Soát Phiên Bản:** Theo dõi và quản lý các phiên bản ứng dụng
5. **Cập Nhật Dễ Dàng:** Nâng cấp ứng dụng với các lệnh đơn giản
6. **Khả Năng Rollback:** Quay lại phiên bản trước nếu cần

## Xác Minh Triển Khai

### Sử Dụng Docker Dashboard

Kiểm tra các phần sau:
- **Deployments:** Xem các deployment WordPress và MariaDB
- **Pods:** Xác minh các pod đang chạy
- **Services:** Kiểm tra các LoadBalancer và ClusterIP services
- **ConfigMaps:** Xem lại dữ liệu cấu hình
- **Secrets:** Xem thông tin đăng nhập được lưu trữ (đã mã hóa)

### Sử Dụng Các Lệnh kubectl

```bash
# Liệt kê deployments
kubectl get deployments

# Liệt kê pods
kubectl get pods

# Liệt kê services
kubectl get services

# Liệt kê configmaps
kubectl get configmaps

# Liệt kê secrets
kubectl get secrets
```

## Kết Luận

Helm charts đơn giản hóa đáng kể việc triển khai các ứng dụng phức tạp trên Kubernetes. Chỉ với một lệnh `helm install`, bạn đã triển khai một website WordPress đầy đủ chức năng với database backend, networking phù hợp, quản lý cấu hình và bảo mật - tất cả tuân theo các tiêu chuẩn sẵn sàng cho production.

Điều này chứng minh sức mạnh và hiệu quả của việc sử dụng Helm cho các triển khai Kubernetes, đặc biệt khi làm việc với kiến trúc microservices trong các ứng dụng Spring Boot hoặc bất kỳ ứng dụng container hóa nào khác.

## Các Bước Tiếp Theo

- Khám phá cấu trúc helm chart chi tiết
- Học cách tùy chỉnh Helm values
- Hiểu về Helm chart templating
- Thực hành tạo Helm charts của riêng bạn




FILE: 56-helm-chart-structure-and-management.md


# Cấu Trúc và Quản Lý Helm Chart

## Tổng Quan

Hướng dẫn này giải thích cấu trúc chuẩn của Helm chart và trình bày cách quản lý các bản cài đặt Helm trong Kubernetes, sử dụng WordPress làm ví dụ trước khi chuyển sang triển khai microservices.

## Cấu Trúc Helm Chart

Bất kỳ Helm chart nào cũng tuân theo một cấu trúc được định nghĩa trước, dù bạn tự tạo hay sử dụng chart của bên thứ ba.

### Cấu Trúc Thư Mục

```
wordpress/                    # Thư mục cha (tên chart)
├── Chart.yaml               # Metadata của chart
├── values.yaml              # Cấu hình giá trị động
├── charts/                  # Các chart phụ thuộc
└── templates/               # Template manifest Kubernetes
```

### Các Thành Phần Chính

#### 1. Chart.yaml
File này chứa thông tin metadata về Helm chart:
- Phiên bản chart
- Phiên bản API
- Phiên bản ứng dụng
- Các phụ thuộc vào chart khác
- Mô tả
- Thông tin người duy trì
- Repository nguồn

**Ví dụ từ WordPress chart:**
```yaml
apiVersion: v2
appVersion: "6.3.1"
dependencies:
  - name: memcached
  - name: mariadb
  - name: common
description: "WordPress là nền tảng blog và quản lý nội dung phổ biến nhất thế giới"
version: 17.1.4
```

#### 2. values.yaml
Chứa tất cả các giá trị động sẽ được inject vào các file template tại runtime. Đây là các cặp key-value để cấu hình:
- Chi tiết Docker image
- Giới hạn tài nguyên
- Cấu hình service
- Cài đặt theo môi trường cụ thể

Tất cả các giá trị được định nghĩa ở đây sẽ được Helm chart sử dụng tại runtime để chuẩn bị các file manifest Kubernetes dựa trên các template.

#### 3. Thư Mục charts/
Chứa các Helm chart khác mà chart hiện tại phụ thuộc vào. Mỗi phụ thuộc tự nó là một Helm chart hoàn chỉnh với cấu trúc riêng.

**Ví dụ:** WordPress chart phụ thuộc vào:
- `common` - Tiện ích chung
- `mariadb` - Cơ sở dữ liệu
- `memcached` - Lớp caching

#### 4. Thư Mục templates/
Chứa các file template manifest Kubernetes:
- `deployment.yaml` - Cấu hình Deployment
- `service.yaml` - Định nghĩa Service
- `configmap.yaml` - Template ConfigMap
- `secret.yaml` - Template Secret
- Và nhiều hơn nữa...

Các template này tuân theo cú pháp manifest Kubernetes chuẩn nhưng bao gồm việc inject giá trị động từ `values.yaml`.

**Ví dụ cấu trúc deployment.yaml:**
- Sử dụng cú pháp deployment Kubernetes chuẩn
- Inject các giá trị runtime từ `values.yaml`
- Hỗ trợ tất cả các file template, không chỉ deployment

### Các File Bổ Sung
- `.helmignore` - File cần bỏ qua (do Helm quản lý)
- `Chart.lock` - File khóa phụ thuộc (do Helm quản lý)
- `values.schema.json` - Schema xác thực values (tùy chọn)

## Quản Lý Helm Release

### Liệt Kê Các Release Đã Cài Đặt

```bash
helm ls
```

**Kết quả bao gồm:**
- Tên release
- Namespace
- Số revision
- Trạng thái (deployed, failed, v.v.)
- Tên và phiên bản chart
- Phiên bản ứng dụng

**Ví dụ kết quả:**
```
NAME         NAMESPACE   REVISION   STATUS     CHART              APP VERSION
happy-panda  default     1          deployed   wordpress-17.1.4   6.3.1
```

**Lưu ý:** Phiên bản chart (17.1.4) đề cập đến chính Helm chart, trong khi phiên bản app (6.3.1) đề cập đến ứng dụng WordPress được triển khai.

### Gỡ Cài Đặt Release

```bash
helm uninstall <tên-release>
```

**Ví dụ:**
```bash
helm uninstall happy-panda
```

Lệnh đơn giản này sẽ xóa:
- Tất cả deployment
- Tất cả pod
- Tất cả replica set
- Tất cả service
- Tất cả config map
- Tất cả secret
- Tất cả tài nguyên khác được tạo bởi chart

### Xác Minh

Sau khi gỡ cài đặt, xác minh thông qua Kubernetes dashboard:
- Không có workload nào được hiển thị
- Không có deployment
- Không có pod
- Không có replica set
- Service đã bị xóa
- Config map đã bị xóa
- Secret đã bị xóa

## Tạo Helm Chart Tùy Chỉnh Cho Microservices

### Tại Sao Cần Tạo Chart Tùy Chỉnh?

Các Helm chart của bên thứ ba như WordPress sẵn có, nhưng đối với microservices tùy chỉnh:
- Không có chart được xây dựng sẵn
- Yêu cầu kinh doanh là duy nhất
- Cần các file manifest Kubernetes tùy chỉnh

### Lợi Ích của Helm Chart Tùy Chỉnh

1. **Triển Khai Bằng Lệnh Đơn** - Triển khai tất cả microservices với một lệnh
2. **Quản Lý Môi Trường** - Duy trì các file `values.yaml` riêng cho các môi trường khác nhau
3. **Kiểm Soát Phiên Bản** - Theo dõi phiên bản chart cùng với code
4. **Tái Sử Dụng** - Sử dụng cùng cấu trúc chart cho nhiều triển khai

### Các Bước Tiếp Theo

Cho Eazy Bytes Microservices:
1. Tạo cấu trúc Helm chart tùy chỉnh
2. Định nghĩa các template phù hợp cho tất cả microservices
3. Cấu hình `values.yaml` cho các môi trường khác nhau
4. Triển khai sử dụng lệnh Helm

## Tóm Tắt

Helm chart cung cấp một cách mạnh mẽ để quản lý triển khai Kubernetes:
- **Cấu trúc chuẩn hóa** làm cho chart dễ dự đoán và bảo trì
- **Inject giá trị động** cho phép cấu hình theo môi trường cụ thể
- **Lệnh đơn giản** để cài đặt và gỡ cài đặt
- **Quản lý phụ thuộc** xử lý các stack ứng dụng phức tạp

Sức mạnh của Helm nằm ở khả năng quản lý toàn bộ stack ứng dụng bằng các lệnh đơn giản, làm cho nó lý tưởng cho kiến trúc microservices.

---

*Hướng dẫn này là một phần của loạt bài về triển khai microservices với Kubernetes và Helm.*




FILE: 57-building-custom-helm-charts-for-microservices.md


# Xây Dựng Helm Charts Tùy Chỉnh Cho Microservices

## Giới Thiệu

Trong các dự án thực tế và tổ chức doanh nghiệp, các nhóm cần xây dựng Helm charts riêng dựa trên yêu cầu cụ thể của microservices. Hướng dẫn này sẽ giúp bạn tạo một Helm chart tùy chỉnh có thể triển khai tất cả microservices lên Kubernetes cluster chỉ với một lệnh duy nhất.

## Bắt Đầu

### Tạo Cấu Trúc Dự Án

1. Tạo cấu trúc thư mục mới:
   - Tạo thư mục có tên `Section_16`
   - Bên trong, tạo thư mục con có tên `Helm`

2. Điều hướng đến thư mục Helm trong terminal:
   ```bash
   cd Section_16/Helm
   ```

### Tạo Helm Chart Cơ Bản

Tạo một Helm chart chung sẽ đóng vai trò là template cho tất cả microservices:

```bash
helm create eazybank-common
```

Lệnh này tạo một Helm chart với các tệp và thư mục được định nghĩa sẵn.

## Dọn Dẹp Chart Mặc Định

Helm chart mặc định chứa các template triển khai website NGINX. Vì chúng ta đang xây dựng nội dung riêng:

1. **Xóa tất cả các tệp template** trong thư mục `templates`
2. **Xóa nội dung tệp `values.yaml`** - loại bỏ tất cả giá trị liên quan đến NGINX
3. **Xác minh không có dependencies** trong thư mục `charts`

## Cấu Hình Chart.yaml

Cập nhật tệp `Chart.yaml` với thông tin cụ thể của bạn:

```yaml
apiVersion: v2
name: eazybank-common
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.0.0"
```

Các trường quan trọng:
- **version**: Phiên bản của Helm chart (0.1.0)
- **appVersion**: Phiên bản của ứng dụng (1.0.0)

## Tạo Các Tệp Template

Để triển khai microservices lên Kubernetes, chúng ta cần ba tệp manifest chính:
1. Deployment manifest
2. Service manifest
3. ConfigMap

### 1. Service Template (service.yaml)

```yaml
{{- define "common.service" -}}
apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.serviceName }}
spec:
  selector:
    app: {{ .Values.appLabel }}
  type: {{ .Values.service.type }}
  ports:
    - name: http
      protocol: TCP
      port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
{{- end }}
```

**Tính Năng Chính:**
- Sử dụng `define` để tạo template có thể tái sử dụng với tên `common.service`
- Các giá trị động được inject từ `values.yaml`:
  - `serviceName`: Tên của service
  - `appLabel`: Nhãn ứng dụng cho selector
  - `service.type`: Loại service (ClusterIP, NodePort, LoadBalancer)
  - `service.port`: Cổng service
  - `service.targetPort`: Cổng đích

### 2. Deployment Template (deployment.yaml)

```yaml
{{- define "common.deployment" -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.appLabel }}
  labels:
    app: {{ .Values.appLabel }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Values.appLabel }}
  template:
    metadata:
      labels:
        app: {{ .Values.appLabel }}
    spec:
      containers:
      - name: {{ .Values.appLabel }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        ports:
        - containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        env:
        {{- if .Values.appname_enabled }}
        - name: SPRING_APPLICATION_NAME
          value: {{ .Values.appName }}
        {{- end }}
        {{- if .Values.profile_enabled }}
        - name: SPRING_PROFILES_ACTIVE
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_PROFILES_ACTIVE
        {{- end }}
        {{- if .Values.config_enabled }}
        - name: SPRING_CONFIG_IMPORT
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_CONFIG_IMPORT
        {{- end }}
        {{- if .Values.eureka_enabled }}
        - name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
        {{- end }}
        {{- if .Values.resourceserver_enabled }}
        - name: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI
        {{- end }}
        {{- if .Values.otel_enabled }}
        - name: JAVA_TOOL_OPTIONS
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: JAVA_TOOL_OPTIONS
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: {{ .Values.otel.endpoint }}
        - name: OTEL_METRICS_EXPORTER
          value: {{ .Values.otel.metricsExporter }}
        - name: OTEL_SERVICE_NAME
          value: {{ .Values.appName }}
        {{- end }}
        {{- if .Values.kafka_enabled }}
        - name: SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS
          valueFrom:
            configMapKeyRef:
              name: {{ .Values.global.configMapName }}
              key: SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS
        {{- end }}
{{- end }}
```

**Tính Năng Chính:**
- Số lượng replica động
- Cấu hình container image
- Biến môi trường có điều kiện sử dụng câu lệnh `if`:
  - **appname_enabled**: Tên ứng dụng Spring
  - **profile_enabled**: Spring profiles (dev, QA, prod)
  - **config_enabled**: Spring config import
  - **eureka_enabled**: URL dịch vụ Eureka
  - **resourceserver_enabled**: Cấu hình OAuth2 resource server (cho Gateway)
  - **otel_enabled**: Cấu hình OpenTelemetry cho observability
  - **kafka_enabled**: Cấu hình Kafka broker cho event-driven microservices

### 3. ConfigMap Template (configmap.yaml)

```yaml
{{- define "common.configmap" -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.global.configMapName }}
data:
  SPRING_PROFILES_ACTIVE: {{ .Values.global.activeProfile }}
  SPRING_CONFIG_IMPORT: {{ .Values.global.configImport }}
  EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: {{ .Values.global.eurekaServiceURL }}
  SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI: {{ .Values.global.keycloakURL }}
  JAVA_TOOL_OPTIONS: {{ .Values.global.javaToolOptions }}
{{- end }}
```

**Tính Năng Chính:**
- Sử dụng tiền tố `global` cho các giá trị chung cho tất cả microservices
- Cấu hình cụ thể theo môi trường (dev, QA, prod)
- Quản lý cấu hình tập trung

## Hiểu Cấu Trúc Template

### Ngôn Ngữ Template Helm

Helm sử dụng **ngôn ngữ template Go** và **ngôn ngữ template Sprig**. Các khái niệm chính:

- **`{{ .Values }}`**: Object chứa các giá trị từ `values.yaml`
- **`{{- -}}`**: Dấu gạch ngang loại bỏ khoảng trắng trước/sau câu lệnh
- **`{{- define "name" -}}`**: Định nghĩa một template có tên
- **`{{- end }}`**: Đóng khối define hoặc if
- **`{{- if .Values.property }}`**: Rendering có điều kiện

### Giá Trị Global vs. Giá Trị Cụ Thể Của Microservice

- **Giá trị Global**: Chung cho tất cả microservices (ví dụ: tên ConfigMap, URL Eureka)
- **Giá trị cụ thể của Microservice**: Riêng cho từng service (ví dụ: tên service, số lượng replica)

## Cấu Hình Values.yaml

Chart `eazybank-common` giữ `values.yaml` của nó **trống** vì:
- Đây là một common/library chart được sử dụng bởi các Helm charts khác
- Mỗi Helm chart của microservice cung cấp `values.yaml` riêng
- Templates có thể tái sử dụng, nhưng giá trị cụ thể cho từng microservice

## Lợi Ích Của Phương Pháp Này

1. **Triển Khai Bằng Một Lệnh**: Triển khai tất cả microservices chỉ với một lệnh
2. **Gỡ Cài Đặt Bằng Một Lệnh**: Xóa tất cả microservices chỉ với một lệnh
3. **Bảo Trì Dễ Dàng**: Quản lý bất kỳ số lượng Kubernetes manifests nào cho nhiều microservices
4. **Tái Sử Dụng**: Templates chung được chia sẻ cho tất cả microservices
5. **Linh Hoạt Môi Trường**: Các giá trị khác nhau cho môi trường dev, QA và prod

## Các Bước Tiếp Theo

Bước tiếp theo là tạo các Helm charts riêng cho từng microservice (accounts, loans, cards, v.v.) sẽ:
- Tận dụng chart `eazybank-common` như một dependency
- Cung cấp `values.yaml` riêng với cấu hình cụ thể cho microservice

## Tóm Tắt

Phương pháp Helm chart tùy chỉnh này cung cấp:
- Template chung cho service, deployment và ConfigMap
- Inject biến môi trường có điều kiện
- Hỗ trợ Spring Boot, Eureka, OAuth2, OpenTelemetry và Kafka
- Quản lý cấu hình linh hoạt qua các môi trường
- Đơn giản hóa việc triển khai microservices lên Kubernetes

Bằng cách tạo nền tảng này, các nhóm có thể quản lý hiệu quả kiến trúc microservice phức tạp trong Kubernetes với chi phí vận hành tối thiểu.




FILE: 58-creating-helm-chart-for-accounts-microservice.md


# Tạo Helm Chart cho Microservice Accounts

## Tổng quan

Hướng dẫn này trình bày cách tạo Helm chart cho microservice accounts bằng cách tận dụng Helm chart `easybank-common`, nơi chứa tất cả các file template Kubernetes manifest cần thiết.

## Yêu cầu trước

- Helm chart `easybank-common` với các template đã được định nghĩa sẵn
- Hiểu biết cơ bản về Helm charts và Kubernetes
- Microservice accounts đã sẵn sàng để triển khai

## Bước 1: Tạo cấu trúc dự án

Đầu tiên, tạo một thư mục mới có tên `easybank-services` để tổ chức tất cả các Helm chart của microservices:

```bash
mkdir easybank-services
cd easybank-services
```

## Bước 2: Tạo Helm Chart

Tạo một Helm chart mới cho microservice accounts:

```bash
helm create accounts
```

Lệnh này tạo một thư mục có tên `accounts` với cấu trúc Helm chart mặc định.

## Bước 3: Dọn dẹp các file mặc định

Xóa các file template mặc định và xóa nội dung của `values.yaml`, vì chúng ta sẽ định nghĩa riêng:

1. Xóa tất cả các file trong thư mục `templates/`
2. Xóa nội dung của file `values.yaml`

## Bước 4: Cấu hình Chart.yaml

Mở file `chart.yaml` và cập nhật với cấu hình sau:

```yaml
apiVersion: v2
name: accounts
description: Helm chart cho accounts microservice
version: 1.0.0
appVersion: "1.0.0"

dependencies:
  - name: easybank-common
    version: 0.1.0
    repository: file://../../easybank-common
```

### Các điểm chính:

- **name**: Tên của chart (accounts)
- **version**: Cập nhật lên 1.0.0
- **dependencies**: Định nghĩa phụ thuộc vào chart `easybank-common`
- **repository**: Sử dụng giao thức `file://` với đường dẫn tương đối (`../../`) để tham chiếu đến common chart cục bộ

Ký hiệu `../../` điều hướng lên hai thư mục từ vị trí hiện tại để tìm chart `easybank-common`.

## Bước 5: Thêm các file Template

Tạo hai file template trong thư mục `templates/`:

### deployment.yaml

```yaml
{{ include "common.deployment" . }}
```

### service.yaml

```yaml
{{ include "common.service" . }}
```

Các template này tham chiếu đến các template chung được định nghĩa trong chart `easybank-common`:
- `common.deployment` - Template cho Kubernetes Deployment
- `common.service` - Template cho Kubernetes Service

Cách tiếp cận này cho phép tái sử dụng cấu hình chung trên nhiều microservices.

## Bước 6: Cấu hình values.yaml

Điền vào `values.yaml` với cấu hình sau:

```yaml
deploymentName: accounts-deployment
serviceName: accounts-service
appLabel: accounts
appName: accounts
replicaCount: 1

image:
  repository: eazybank/accounts
  tag: s14

containerPort: 8080

service:
  type: ClusterIP
  port: 8080
  targetPort: 8080

# Các cờ biến môi trường
appNameEnabled: true
profileEnabled: true
configEnabled: true
eurekaEnabled: true
resourceServerEnabled: false
otelEnabled: true
kafkaEnabled: true
```

### Chi tiết cấu hình:

#### Cài đặt cơ bản
- **deploymentName**: Tên cho Kubernetes Deployment
- **serviceName**: Tên cho Kubernetes Service
- **appLabel**: Label được sử dụng để xác định ứng dụng
- **appName**: Tên ứng dụng (được sử dụng làm `spring.application.name`)
- **replicaCount**: Số lượng pod replica

#### Cấu hình Image
- **image.repository**: Repository của Docker image
- **image.tag**: Tag của image (s14 đề cập đến section 14 với implementation Kafka)

#### Cấu hình Port
- **containerPort**: Port mà container lắng nghe (8080)
- **service.type**: ClusterIP (chỉ truy cập nội bộ, không expose ra bên ngoài)
- **service.port**: Port của Service
- **service.targetPort**: Port đích trên pod

#### Các cờ biến môi trường

Các cờ boolean này kiểm soát biến môi trường nào được inject:

- **appNameEnabled**: Inject biến môi trường `SPRING_APPLICATION_NAME`
- **profileEnabled**: Kích hoạt cấu hình Spring profiles
- **configEnabled**: Kích hoạt kết nối đến Config Server
- **eurekaEnabled**: Kích hoạt service discovery của Eureka
- **resourceServerEnabled**: Đặt thành `false` vì chỉ Gateway đóng vai trò là OAuth2 resource server
- **otelEnabled**: Kích hoạt OpenTelemetry cho logging đến Grafana và distributed tracing đến Grafana Tempo
- **kafkaEnabled**: Kích hoạt kết nối Kafka cho giao tiếp event-driven với message microservice

## Bước 7: Build Helm Dependencies

Biên dịch Helm chart và tải về các dependencies:

```bash
cd accounts
helm dependency build
```

Lệnh này thực hiện:
1. Biên dịch Helm chart accounts
2. Tải về và đóng gói các chart phụ thuộc (easybank-common)
3. Đặt dependency đã nén vào thư mục `charts/`

Sau khi thực thi, bạn sẽ thấy một file nén như `easybank-common-0.1.0.tgz` trong thư mục `charts/`.

## Các lưu ý quan trọng

### Tại sao cần các file Template

Mặc dù các template đã được định nghĩa trong `easybank-common`, chúng ta vẫn cần các file template trong chart accounts. Các file này hoạt động như các tham chiếu để include các template chung:

```yaml
{{ include "common.deployment" . }}
```

Cú pháp này import template từ dependency chart.

### Service Type: ClusterIP

Service type được đặt thành ClusterIP vì:
- Microservice accounts không nên được expose ra bên ngoài
- Chỉ Gateway server cần truy cập từ bên ngoài
- Các microservice nội bộ giao tiếp trong cluster

### Helm Dependency Build

Lệnh `helm dependency build` phải được chạy cho bất kỳ chart nào có dependencies. Chart `easybank-common` không yêu cầu lệnh này vì nó không có dependencies.

## Xác minh

Sau khi build, xác minh cấu trúc:

```
accounts/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   └── service.yaml
└── charts/
    └── easybank-common-0.1.0.tgz
```

## Các bước tiếp theo

Lặp lại quy trình này cho tất cả các microservices còn lại trong kiến trúc của bạn, tùy chỉnh `values.yaml` cho các yêu cầu cụ thể của từng service.

## Tóm tắt

Bạn đã tạo thành công một Helm chart cho microservice accounts với:
- Tận dụng các template được chia sẻ từ easybank-common
- Định nghĩa các cấu hình cụ thể cho service
- Duy trì dependencies đúng cách
- Sẵn sàng để triển khai Kubernetes

Mẫu này có thể được nhân rộng cho tất cả các microservices trong hệ thống, đảm bảo tính nhất quán và khả năng tái sử dụng trong toàn bộ cơ sở hạ tầng triển khai của bạn.




FILE: 59-creating-helm-charts-for-remaining-microservices.md


# Tạo Helm Charts cho các Microservices còn lại

## Tổng quan

Trong hướng dẫn này, chúng ta sẽ tạo Helm charts cho tất cả các microservices còn lại trong ứng dụng Spring Boot. Sau khi đã tạo Helm chart cho Accounts microservice, chúng ta sẽ sao chép và tùy chỉnh nó cho Cards, Config Server, Eureka Server, Gateway Server, Loans và Message microservices.

## Tạo Helm Charts bằng cách Sao chép

Thay vì tạo từng Helm chart từ đầu, chúng ta có thể tận dụng Helm chart của Accounts hiện có:

1. **Sao chép Helm chart của Accounts** vào cùng thư mục
2. **Đổi tên** nó thành microservice đích (ví dụ: "cards")
3. **Tùy chỉnh** các file cấu hình

### Quy trình từng bước

#### 1. Chỉnh sửa Chart.yaml

Mở file `Chart.yaml` và cập nhật tên:

```yaml
name: cards  # Đổi từ 'accounts'
```

Không cần thay đổi gì khác trong file này.

#### 2. Hiểu về Cấu trúc Thư mục

- **templates/**: Chứa các templates chung - không cần thay đổi
- **charts/**: Chứa các dependencies đã biên dịch (EasyBank Common) - không cần thay đổi
- **Chart.lock**: Được tạo bởi Helm trong quá trình biên dịch
- **values.yaml**: Cần tùy chỉnh cho từng microservice

> **Lưu ý**: Nếu gặp vấn đề khi biên dịch, bạn có thể xóa `Chart.lock` và biên dịch lại.

#### 3. Tùy chỉnh values.yaml

Cập nhật file `values.yaml` với các giá trị cụ thể cho từng microservice:

```yaml
deploymentName: cards-deployment
serviceName: cards-service
appLabel: cards
appName: cards
replicaCount: 1
image:
  name: easybytes/cards
  tag: latest
containerPort: 9000
port: 9000
targetPort: 9000
serviceType: ClusterIP
```

## Cấu hình cho từng Microservice

### Cards Microservice

**Cấu hình chính:**
- Container Port: `9000`
- Service Type: `ClusterIP`
- Kafka Enabled: `false` (Cards không kết nối với Kafka)

### Config Server

**Cấu hình values.yaml:**

```yaml
deploymentName: configserver-deployment
serviceName: configserver-service
appLabel: configserver
appName: configserver
image:
  name: easybytes/configserver
containerPort: 8071
serviceType: ClusterIP
```

**Các giá trị Boolean:**
- `profileEnabled: false` - Config server tải properties của tất cả profiles
- `configEnabled: false` - Config server không cần URL config của chính nó
- `eurekaEnabled: false`
- `resourceServerEnabled: false`
- `otelEnabled: true`
- `kafkaEnabled: false`

> **Tại sao profile bị vô hiệu hóa**: Config server quản lý properties cho tất cả profiles. Các microservices riêng lẻ cần thuộc tính profile để lấy cấu hình cụ thể từ Spring Cloud Config Server.

### Eureka Server

**Cấu hình chính:**
- Container Port: `8070`

**Các giá trị Boolean:**
- `appNameEnabled: true`
- `profileEnabled: false`
- `configEnabled: true`
- `eurekaEnabled: false`
- `resourceServerEnabled: false`
- `otelEnabled: true`
- `kafkaEnabled: false`

### Gateway Server

**Cấu hình chính:**
- Service Type: `LoadBalancer` (được expose ra ngoài cho các client)

**Các giá trị Boolean:**
- `resourceServerEnabled: true` - Gateway hoạt động như OAuth2 resource server

> **Quan trọng**: Gateway là microservice duy nhất được cấu hình làm resource server trong kiến trúc này.

### Loans Microservice

**Cấu hình chính:**
- Container Port: `8090`
- Image: `easybytes/loans`

Cấu hình tương tự như Cards và Accounts microservices, với số port và tên image là điểm khác biệt chính.

### Message Microservice

**Cấu hình chính:**
- Container Port: `9010`
- Được xây dựng với Spring Cloud Functions và Spring Cloud Stream

**Các giá trị Boolean:**
- `profileEnabled: false`
- `configEnabled: false`
- `eurekaEnabled: false`
- `otelEnabled: false`
- `kafkaEnabled: true` - Message microservice sử dụng Kafka

## Biên dịch lại Helm Charts

### Khi nào cần Biên dịch lại

Bạn không cần biên dịch lại nếu:
- Các dependent charts đã có sẵn ở dạng nén
- Bạn đang sử dụng cùng một EasyBank Common Helm chart

### Cách Biên dịch lại

Nếu cần, chạy lệnh sau trong thư mục Helm chart của microservice:

```bash
helm dependency build
```

Lệnh này sẽ:
- Xóa các charts cũ
- Thay thế bằng các phiên bản mới được biên dịch

**Lưu ý**: Cùng một EasyBank Common Helm chart đã nén từ Accounts microservice sẽ được sử dụng cho tất cả các microservices.

## Helm Chart theo Môi trường

### Thách thức

Việc cài đặt từng Helm chart theo cách thủ công (accounts, cards, config server, v.v.) rất tẻ nhạt và dễ xảy ra lỗi.

### Giải pháp

Tạo một **Helm chart theo môi trường** để:
1. Định nghĩa tất cả các giá trị liên quan đến ConfigMap
2. Khai báo dependencies trên tất cả các Helm charts của microservices
3. Cho phép triển khai bằng một lệnh duy nhất

Cách tiếp cận này sẽ làm cho hệ sinh thái Helm dễ quản lý hơn nhiều sau khi thiết lập ban đầu.

## Điểm chính cần nhớ

- **Thiết lập một lần**: Tạo Helm charts là hoạt động một lần giúp đơn giản hóa các lần triển khai sau
- **Tái sử dụng**: Templates và dependency charts có thể được tái sử dụng cho các microservices
- **Tùy chỉnh**: Chỉ có `values.yaml` cần sửa đổi cho từng microservice
- **Tự động hóa**: Helm charts theo môi trường cho phép triển khai bằng một lệnh
- **Nhất quán**: Sử dụng một common Helm chart đảm bảo tính nhất quán giữa tất cả microservices

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- Tạo Helm charts theo môi trường
- Liên kết tất cả các Helm charts của microservices lại với nhau
- Demo quy trình triển khai hoàn chỉnh

---

**Lưu ý**: Thiết lập ban đầu đòi hỏi công sức thủ công, nhưng một khi đã cấu hình xong, hệ sinh thái Helm sẽ đơn giản hóa đáng kể việc triển khai và quản lý microservices.




FILE: 6-configuring-gateway-as-oauth2-resource-server.md


# Cấu Hình Gateway Server Như OAuth2 Resource Server

## Tổng Quan

Hướng dẫn này trình bày cách chuyển đổi Spring Cloud Gateway server thành OAuth2 resource server, cho phép nó xác thực JWT access token được cấp bởi Keycloak authorization server.

## Yêu Cầu Trước

- Keycloak authorization server đã được thiết lập và đang chạy
- Thông tin client credentials đã được cấu hình trong auth server
- Ứng dụng Spring Cloud Gateway (từ Section 11)

## Các Bước Thực Hiện

### 1. Thiết Lập Dự Án

Tạo folder section mới bằng cách sao chép implementation trước đó:

```bash
# Sao chép Section 11 sang Section 12
# Xóa các file ẩn (.idea, etc.)
```

Mở project trong IntelliJ IDEA và bật annotation processing khi được nhắc.

### 2. Thêm Maven Dependencies

Thêm ba dependencies liên quan đến security vào file `pom.xml` của Gateway server:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-resource-server</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-jose</artifactId>
</dependency>
```

**Mục Đích Của Các Dependencies:**
- `spring-boot-starter-security`: Thêm Spring Security framework
- `spring-security-oauth2-resource-server`: Chuyển đổi gateway thành OAuth2 resource server
- `spring-security-oauth2-jose`: Cung cấp hỗ trợ xử lý JWT token

Tải lại Maven changes để download tất cả các thư viện cần thiết.

### 3. Tạo Cấu Hình Security

Tạo package mới: `com.eazybytes.gatewayserver.config`

Tạo class mới `SecurityConfig.java`:

```java
package com.eazybytes.gatewayserver.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity serverHttpSecurity) {
        serverHttpSecurity
            .authorizeExchange(exchanges -> exchanges
                .pathMatchers(HttpMethod.GET).permitAll()
                .pathMatchers("/easybank/accounts/**").authenticated()
                .pathMatchers("/easybank/cards/**").authenticated()
                .pathMatchers("/easybank/loans/**").authenticated()
            )
            .oauth2ResourceServer(oAuth2ResourceServerSpec -> 
                oAuth2ResourceServerSpec.jwt(Customizer.withDefaults())
            )
            .csrf(csrfSpec -> csrfSpec.disable());
        
        return serverHttpSecurity.build();
    }
}
```

**Các Điểm Chính:**

- **@Configuration**: Báo cho Spring tạo các bean từ class này trong quá trình khởi động
- **@EnableWebFluxSecurity**: Bắt buộc cho Spring Cloud Gateway (reactive framework). Sử dụng `@EnableWebSecurity` cho ứng dụng Spring Boot web thông thường
- **authorizeExchange()**: Cấu hình các quy tắc phân quyền request
- **pathMatchers()**: Định nghĩa các quy tắc security cho các API path cụ thể
- **permitAll()**: Cho phép truy cập không cần xác thực (cho các phương thức GET)
- **authenticated()**: Yêu cầu xác thực cho các path được chỉ định
- **oauth2ResourceServer()**: Chuyển đổi gateway thành OAuth2 resource server
- **jwt()**: Kích hoạt xác thực JWT token với cài đặt mặc định
- **csrf().disable()**: Vô hiệu hóa bảo vệ CSRF (không cần thiết khi không có browser tham gia)

### 4. Cấu Hình Resource Server Properties

Thêm cấu hình sau vào file `application.yml`:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: http://localhost:7080/realms/master/protocol/openid-connect/certs
```

**Mục Đích:**
- Resource server tải xuống public certificate từ Keycloak trong quá trình khởi động
- Public certificate này được sử dụng để xác thực JWT access token
- Resource server có thể xác minh xem token có được Keycloak cấp hợp lệ hay không
- Public certificate chỉ có thể xác thực token nhưng không thể tạo token mới (chỉ private certificate của Keycloak mới có thể tạo token)

## Giải Thích Các Quy Tắc Security

Cấu hình triển khai mô hình security như sau:

1. **Tất cả GET requests**: Được phép không cần xác thực (truy cập chỉ đọc)
2. **POST/PUT/DELETE requests** đến `/easybank/accounts/**`, `/easybank/cards/**`, `/easybank/loans/**`: Yêu cầu xác thực

**Độ Ưu Tiên**: Các cấu hình được đánh giá từ trên xuống dưới, do đó GET request có độ ưu tiên đầu tiên và luôn được cho phép, ngay cả trên các path yêu cầu xác thực.

## Cách Hoạt Động Của Token Validation

1. Client gửi access token trong request đến Gateway
2. Gateway (resource server) xác thực token sử dụng public certificate từ Keycloak
3. Nếu hợp lệ, request được xử lý; nếu không hợp lệ, request bị từ chối
4. Public certificate được tải xuống lúc khởi động từ endpoint `jwk-set-uri`

## Tóm Tắt

Ba thay đổi chính đã được thực hiện:
1. Thêm ba Maven dependencies cho OAuth2 và hỗ trợ JWT
2. Tạo class `SecurityConfig` với các quy tắc security
3. Cấu hình `jwk-set-uri` trong `application.yml` để xác thực token

Gateway server hiện hoạt động như OAuth2 resource server trong luồng client credentials grant flow.

## Các Bước Tiếp Theo

- Build project
- Test cấu hình security
- Xác minh token validation hoạt động như mong đợi

## Tài Nguyên Bổ Sung

- Để biết thêm chi tiết về bảo vệ CSRF, tham khảo tài liệu Spring Security
- Cân nhắc tham gia khóa học Spring Security toàn diện để hiểu sâu hơn




FILE: 60-creating-environment-specific-helm-charts-for-microservices.md


# Tạo Helm Charts Cho Từng Môi Trường Triển Khai Microservices

## Tổng Quan

Hướng dẫn này trình bày cách tạo các Helm chart riêng biệt cho từng môi trường, cho phép bạn triển khai tất cả microservices chỉ với một lệnh duy nhất. Thay vì quản lý việc triển khai từng microservice riêng lẻ, bạn sẽ tạo các Helm chart thống nhất cho các môi trường khác nhau (Dev, QA, Production).

## Yêu Cầu Trước Khi Bắt Đầu

- Đã có các Helm chart cho microservices (Eazy Bank Command và Eazy Bank Services)
- Hiểu biết cơ bản về Helm charts
- Có quyền truy cập vào Kubernetes cluster
- Đã cài đặt Helm trên hệ thống

## Tạo Cấu Trúc Thư Mục Môi Trường

### Bước 1: Thiết Lập Thư Mục Environments

Tạo một thư mục mới có tên `Environments` trong cùng thư mục với `Eazy Bank Command` và `Eazy Bank Services`.

```bash
mkdir Environments
cd Environments
```

## Tạo Helm Chart Cho Môi Trường Dev

### Bước 2: Khởi Tạo Helm Chart Cơ Bản

Tạo một Helm chart mới cho môi trường development:

```bash
helm create dev-ENV
```

Lệnh này tạo ra cấu trúc Helm chart cơ bản với tên `dev-ENV`.

### Bước 3: Dọn Dẹp Templates Mặc Định

1. Điều hướng đến thư mục `templates` bên trong `dev-ENV`
2. Xóa tất cả các file template mặc định
3. Mở file `values.yaml` và xóa tất cả các giá trị mặc định

### Bước 4: Cấu Hình Chart.yaml

Mở file `chart.yaml` và cập nhật `appVersion`:

```yaml
apiVersion: v2
name: dev-ENV
description: Helm chart cho môi trường Dev
type: application
version: 0.1.0
appVersion: "1.0.0"
```

### Bước 5: Định Nghĩa Dependencies

Thêm tất cả các microservice phụ thuộc vào `chart.yaml`:

```yaml
dependencies:
  - name: eazybank-command
    version: "1.0.0"
    repository: "file://../eazybank-command"
  - name: configserver
    version: "1.0.0"
    repository: "file://../configserver"
  - name: eurekaserver
    version: "1.0.0"
    repository: "file://../eurekaserver"
  - name: accounts
    version: "1.0.0"
    repository: "file://../accounts"
  - name: cards
    version: "1.0.0"
    repository: "file://../cards"
  - name: loans
    version: "1.0.0"
    repository: "file://../loans"
  - name: gatewayserver
    version: "1.0.0"
    repository: "file://../gatewayserver"
  - name: message
    version: "1.0.0"
    repository: "file://../message"
```

## Thiết Lập ConfigMap Template

### Bước 6: Tạo ConfigMap Template

Trong thư mục `templates`, tạo file `configmap.yaml`. Thay vì định nghĩa một ConfigMap template mới, hãy tham chiếu đến ConfigMap template chung:

```yaml
{{- include "common.configmap" . }}
```

Cách này import và sử dụng ConfigMap template từ Eazy Bank Common Helm chart (`common.configmap`).

### Tại Sao Chỉ Cần ConfigMap Templates?

- **Deployment và Service manifests** KHÔNG cần thiết trong environment charts
- Chúng đã có sẵn trong các Helm chart của từng microservice
- **ConfigMap được chia sẻ** giữa tất cả microservices, rất phù hợp cho cấu hình cấp môi trường

## Cấu Hình Values Cho Môi Trường Dev

### Bước 7: Điền Thông Tin vào values.yaml

Thêm các giá trị sau vào `values.yaml`:

```yaml
global:
  configMapName: "eazybank-dev-configmap"
  activeProfile: "default"
  configServerUrl: "http://configserver:8071"
  eurekaServerUrl: "http://eurekaserver:8070/eureka/"
  keycloakUrl: "http://keycloak.default.svc.cluster.local:80"
  otelJarPath: "/app/libs/opentelemetry-javaagent.jar"
  tempoUrl: "http://tempo.default.svc.cluster.local:4317"
  otelMetricsExporter: "none"
  kafkaBrokerUrl: "kafka.default.svc.cluster.local:9092"
```

### Hiểu Về Các Giá Trị Cấu Hình

#### Tiền Tố Global
- Tiền tố `global` cho biết các giá trị này áp dụng cho tất cả microservices
- Đây là quy ước tùy chỉnh để tổ chức (không phải chuẩn Helm)

#### Các Tham Số Cấu Hình Chính

1. **configMapName**: Tên của ConfigMap resource (`eazybank-dev-configmap`)

2. **activeProfile**: Spring Boot profile sử dụng (`default` cho môi trường Dev)

3. **configServerUrl**: URL service của Config Server
   - Hostname khớp với tên service định nghĩa trong `service.yaml`

4. **eurekaServerUrl**: URL service của Eureka Server
   - Định dạng: `http://servicename:port/eureka/`

5. **keycloakUrl**: URL service xác thực Keycloak
   - Sử dụng DNS nội bộ Kubernetes: `servicename.namespace.svc.cluster.local`
   - Port 80 (chuẩn cho triển khai Helm chart production)

6. **otelJarPath**: Đường dẫn đến file JAR OpenTelemetry Java agent

7. **tempoUrl**: URL service Grafana Tempo cho distributed tracing
   - Tuân theo quy ước đặt tên service Kubernetes

8. **otelMetricsExporter**: Cấu hình OpenTelemetry metrics exporter

9. **kafkaBrokerUrl**: URL service Kafka broker
   - Sử dụng định dạng DNS nội bộ Kubernetes

### Bước 8: Build Dependencies

Biên dịch Helm chart và tải về tất cả dependencies:

```bash
cd dev-ENV
helm dependency build
```

Lệnh này:
- Biên dịch tất cả các Helm chart phụ thuộc
- Tải về và đóng gói chúng vào thư mục `charts`
- Tạo phiên bản nén/đóng gói của mỗi dependency

## Tạo Helm Chart Cho Môi Trường QA

### Bước 9: Thiết Lập Môi Trường QA

1. Sao chép thư mục `dev-ENV` và đổi tên thành `qa-ENV`

2. Cập nhật `chart.yaml`:
```yaml
name: qa-ENV
```

3. Cập nhật `values.yaml`:
```yaml
global:
  configMapName: "eazybank-qa-configmap"
  activeProfile: "qa"
  # Giữ nguyên các giá trị khác hoặc cập nhật theo nhu cầu QA
  configServerUrl: "http://configserver:8071"
  eurekaServerUrl: "http://eurekaserver:8070/eureka/"
  # ... phần còn lại của cấu hình
```

**Thay Đổi Chính:**
- `activeProfile` đổi thành `"qa"`
- `configMapName` đổi thành `"eazybank-qa-configmap"`
- Các giá trị khác có thể tùy chỉnh nếu môi trường QA có hostname/service name khác

## Tạo Helm Chart Cho Môi Trường Production

### Bước 10: Thiết Lập Môi Trường Production

1. Sao chép thư mục `qa-ENV` và đổi tên thành `prod-ENV`

2. Cập nhật `chart.yaml`:
```yaml
name: prod-ENV
```

3. Cập nhật `values.yaml`:
```yaml
global:
  configMapName: "eazybank-prod-configmap"
  activeProfile: "prod"
  # Giữ nguyên các giá trị khác hoặc cập nhật theo nhu cầu Production
  configServerUrl: "http://configserver:8071"
  eurekaServerUrl: "http://eurekaserver:8070/eureka/"
  # ... phần còn lại của cấu hình
```

**Thay Đổi Chính:**
- `activeProfile` đổi thành `"prod"`
- `configMapName` đổi thành `"eazybank-prod-configmap"`

## Triển Khai

### Cách Triển Khai

Để triển khai tất cả microservices cho một môi trường cụ thể, chỉ cần cài đặt Helm chart tương ứng:

**Môi Trường Dev:**
```bash
helm install eazybank-dev ./dev-ENV
```

**Môi Trường QA:**
```bash
helm install eazybank-qa ./qa-ENV
```

**Môi Trường Production:**
```bash
helm install eazybank-prod ./prod-ENV
```

### Điều Gì Xảy Ra Đằng Sau

Khi bạn cài đặt một environment-specific Helm chart:

1. **Tất cả microservices phụ thuộc** được tự động cài đặt
2. **ConfigMap được tạo** với các giá trị riêng của môi trường
3. **Tất cả microservices đọc** cấu hình từ ConfigMap dùng chung tại runtime
4. **Service discovery** và **configuration management** hoạt động liền mạch

## Lợi Ích Của Phương Pháp Này

1. **Triển Khai Một Lệnh**: Triển khai toàn bộ kiến trúc microservice với một lệnh
2. **Cô Lập Môi Trường**: Cấu hình riêng biệt cho Dev, QA và Production
3. **Cấu Hình Tập Trung**: ConfigMap cung cấp cấu hình dùng chung cho tất cả services
4. **Tính Nhất Quán**: Quy trình triển khai giống nhau trên tất cả môi trường
5. **Dễ Cập Nhật**: Chỉnh sửa giá trị môi trường ở một nơi duy nhất
6. **Kiểm Soát Phiên Bản**: Theo dõi cấu hình môi trường trong Git

## So Sánh Với Docker Compose

Các giá trị cấu hình trong Helm charts tương tự như các biến môi trường bạn sẽ inject trong Docker Compose files. Cả hai phương pháp đều đạt được mục tiêu cung cấp cấu hình runtime cho microservices, nhưng Helm được thiết kế cho orchestration trên Kubernetes.

## Thực Hành Tốt Nhất

1. **Sử dụng Kubernetes Internal DNS** cho giao tiếp service-to-service
2. **Tuân theo quy ước đặt tên** cho ConfigMaps (tên riêng cho từng môi trường)
3. **Tách secrets riêng** khỏi ConfigMaps (sử dụng Kubernetes Secrets)
4. **Ghi chú sự khác biệt giữa các môi trường** trong comment của values.yaml
5. **Kiểm tra từng environment chart** trước khi triển khai production
6. **Quản lý phiên bản** tất cả Helm charts và values files

## Xử Lý Sự Cố

### Các Vấn Đề Thường Gặp

1. **Dependency Build Thất Bại**: Đảm bảo tất cả charts được tham chiếu tồn tại tại đường dẫn đã chỉ định
2. **Không Tìm Thấy Service**: Kiểm tra tên service khớp với tên trong file service.yaml
3. **ConfigMap Không Được Áp Dụng**: Kiểm tra template common.configmap được import đúng cách

## Kết Luận

Bạn đã tạo thành công các Helm chart riêng cho từng môi trường, giúp đơn giản hóa việc triển khai microservice. Phương pháp này cung cấp giải pháp production-ready để quản lý nhiều môi trường với chi phí tối thiểu và tính nhất quán tối đa.




FILE: 61-creating-environment-specific-helm-charts-for-microservices-from-transcript.md


# Tạo Helm Charts Riêng Cho Từng Môi Trường Microservices

## Tổng Quan

Hướng dẫn này sẽ giúp bạn tạo các Helm charts riêng cho từng môi trường, cho phép triển khai toàn bộ microservices với một lệnh Helm duy nhất. Phương pháp này đơn giản hóa việc triển khai trên các môi trường khác nhau (dev, QA, production) trong khi vẫn duy trì cấu hình riêng cho từng môi trường.

## Yêu Cầu Tiên Quyết

- Đã có sẵn Eazy Bank Common và Eazy Bank Services Helm charts
- Hiểu biết cơ bản về Helm và Kubernetes
- Có quyền truy cập terminal với Helm CLI đã cài đặt

## Tạo Cấu Trúc Thư Mục Environments

Đầu tiên, tạo một thư mục mới có tên `Environments` trong cùng thư mục chứa `Eazy Bank Command` và `Eazy Bank Services`.

```bash
mkdir Environments
cd Environments
```

## Tạo Helm Chart Cho Môi Trường Development

### Bước 1: Tạo Helm Chart

Tạo một Helm chart mới cho môi trường development:

```bash
helm create dev-env
```

### Bước 2: Dọn Dẹp Templates Mặc Định

Di chuyển vào thư mục `dev-env` vừa tạo và:
1. Xóa tất cả các file trong thư mục `templates`
2. Xóa tất cả các giá trị trong file `values.yaml`

### Bước 3: Cấu Hình Chart.yaml

Mở file `chart.yaml` và cập nhật `appVersion` để đảm bảo tính nhất quán:

```yaml
apiVersion: v2
name: dev-env
description: A Helm chart for development environment
appVersion: "1.0.0"
```

### Bước 4: Định Nghĩa Dependencies

Thêm phần dependencies vào `chart.yaml`:

```yaml
dependencies:
  - name: easybank-common
  - name: configserver
  - name: eurekaserver
  - name: accounts
  - name: cards
  - name: loans
  - name: gatewayserver
  - name: message
```

## Hiểu Về Templates Riêng Cho Môi Trường

**Lưu Ý Quan Trọng:** Helm charts cho môi trường không cần các file manifest deployment và service vì những file này đã có sẵn trong các Helm charts riêng của từng microservice. Charts cho môi trường chỉ cần template ConfigMap vì cấu hình ConfigMap được chia sẻ cho tất cả microservices.

### Bước 5: Tạo ConfigMap Template

Tạo file `config.yaml` trong thư mục `templates` để import template ConfigMap chung:

```yaml
{{- template "common.configmap" . }}
```

Dòng này import template ConfigMap đã được định nghĩa trong Eazy Bank Common Helm chart.

## Cấu Hình Values Cho Môi Trường Development

### Bước 6: Điền Thông Tin values.yaml

Thêm cấu hình sau vào `values.yaml`:

```yaml
global:
  configMapName: easybank-dev-configmap
  activeProfile: default
  configServerUrl: http://configserver:8071
  eurekaServerUrl: http://eurekaserver:8070/eureka
  keycloakUrl: http://keycloak.default.svc.cluster.local:80
  openTelemetryJarPath: /path/to/opentelemetry.jar
  tempoUrl: http://tempo.default.svc.cluster.local:9411
  otelMetricsExporter: none
  kafkaBrokerUrl: kafka-service:9092
```

### Giải Thích Các Cấu Hình Chính

- **global prefix**: Dùng để chỉ ra các giá trị này áp dụng cho tất cả microservices
- **activeProfile**: Đặt là "default" cho môi trường development
- **Service URLs**: Sử dụng tên service trong Kubernetes (phải khớp với tên service được định nghĩa trong các file service.yaml)
- **Keycloak/Kafka URLs**: Tuân theo định dạng `servicename.namespace.svc.cluster.local` cho triển khai theo tiêu chuẩn production

## Build Helm Chart

### Bước 7: Compile Dependencies

Di chuyển vào thư mục `dev-env` và chạy lệnh:

```bash
helm dependencies build
```

Lệnh này sẽ compile tất cả các dependent Helm charts và lưu trữ chúng trong thư mục `charts` ở dạng nén.

## Tạo Các Môi Trường Bổ Sung

### Tạo Môi Trường QA

1. Copy thư mục `dev-env` và đổi tên thành `qa-env`
2. Cập nhật `chart.yaml`:
   ```yaml
   name: qa-env
   ```
3. Cập nhật `values.yaml`:
   ```yaml
   global:
     configMapName: easybank-qa-configmap
     activeProfile: qa
     # Giữ nguyên các giá trị khác hoặc tùy chỉnh theo nhu cầu
   ```
4. Build dependencies:
   ```bash
   cd qa-env
   helm dependencies build
   ```

### Tạo Môi Trường Production

1. Copy thư mục `qa-env` và đổi tên thành `prod-env`
2. Cập nhật `chart.yaml`:
   ```yaml
   name: prod-env
   ```
3. Cập nhật `values.yaml`:
   ```yaml
   global:
     configMapName: easybank-prod-configmap
     activeProfile: prod
     # Giữ nguyên các giá trị khác hoặc tùy chỉnh theo nhu cầu
   ```
4. Build dependencies:
   ```bash
   cd prod-env
   helm dependencies build
   ```

## Chiến Lược Triển Khai

Sau khi tạo xong các Helm charts riêng cho từng môi trường, bạn có thể triển khai toàn bộ microservices vào một môi trường cụ thể chỉ với một lệnh duy nhất:

```bash
# Cho môi trường development
helm install dev-deployment ./dev-env

# Cho môi trường QA
helm install qa-deployment ./qa-env

# Cho môi trường production
helm install prod-deployment ./prod-env
```

Đằng sau hậu trường, lệnh duy nhất này sẽ:
- Cài đặt tất cả các microservices phụ thuộc (config server, Eureka server, accounts, cards, loans, gateway, message)
- Tạo ConfigMap riêng cho môi trường
- Cấu hình tất cả services với các thiết lập môi trường phù hợp

## Sử Dụng ConfigMap

ConfigMap được tạo bởi các Helm charts này chứa các thuộc tính cấu hình mà tất cả microservices có thể đọc tại runtime. Điều này tương tự như cách Docker Compose inject các thuộc tính vào microservices, nhưng được triển khai theo cách native của Kubernetes.

## Các Bước Tiếp Theo

Trước khi triển khai microservices vào Kubernetes cluster, bạn cần thiết lập các thành phần bổ sung:
- Keycloak (cho xác thực và phân quyền)
- Apache Kafka (cho event streaming)
- Grafana (cho giám sát)

Các thành phần này có sẵn Helm charts được xây dựng trước từ cộng đồng open-source, sẽ được đề cập trong các bài giảng tiếp theo.

## Tóm Tắt

Phương pháp này cung cấp:
- **Triển khai với một lệnh duy nhất**: Triển khai toàn bộ kiến trúc microservice với một lệnh
- **Cách ly môi trường**: Cấu hình riêng biệt cho dev, QA, và production
- **Cấu hình tập trung**: ConfigMap được chia sẻ cho tất cả microservices
- **Dễ bảo trì**: Dễ dàng cập nhật và kiểm soát phiên bản cho các thiết lập riêng của môi trường
- **Sẵn sàng cho production**: Tuân theo các best practices của Kubernetes cho việc đặt tên và khám phá service

## Best Practices (Thực Hành Tốt Nhất)

1. Luôn compile các dependent charts sau khi thay đổi common charts
2. Validate Helm templates trước khi cài đặt bằng lệnh `helm template .`
3. Sử dụng quy ước đặt tên nhất quán giữa các môi trường
4. Lưu trữ dữ liệu nhạy cảm trong Kubernetes Secrets, không phải ConfigMaps
5. Kiểm soát phiên bản cho tất cả các thay đổi Helm chart
6. Test ở môi trường thấp hơn trước khi đưa lên production

## Các Lỗi Thường Gặp và Cách Khắc Phục

### Lỗi Template

Nếu gặp lỗi khi chạy `helm template .`, kiểm tra:
- Tên biến trong template có đúng không
- Cú pháp trong các file YAML có hợp lệ không
- Các dependencies đã được build chưa

### Lỗi Dependencies

Nếu không thể build dependencies:
- Đảm bảo đường dẫn đến các charts phụ thuộc là chính xác
- Kiểm tra kết nối mạng nếu pull từ remote repository
- Xác nhận rằng tất cả các charts phụ thuộc tồn tại và có phiên bản phù hợp

## Kết Luận

Việc tạo các Helm charts riêng cho từng môi trường là một phương pháp mạnh mẽ để quản lý triển khai microservices qua nhiều môi trường khác nhau. Nó cung cấp sự linh hoạt, dễ bảo trì và tuân theo các best practices của Kubernetes. Với cách tiếp cận này, bạn có thể dễ dàng mở rộng và quản lý hệ thống microservices phức tạp một cách hiệu quả.




FILE: 62-validating-and-deploying-helm-charts-for-microservices.md


# Xác Thực và Triển Khai Helm Charts cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách xác thực Helm charts trước khi triển khai bằng lệnh `helm template`, khắc phục các lỗi thường gặp và chuẩn bị triển khai microservices lên Kubernetes cluster.

## Yêu Cầu Tiên Quyết

- Đã cài đặt và cấu hình Helm
- Các Helm charts tùy chỉnh cho microservices EasyBank
- Quyền truy cập Terminal vào thư mục dự án

## Xác Thực Helm Charts với helm template

### Mục Đích

Trước khi cài đặt Helm charts vào Kubernetes cluster, việc xác thực các file manifest Kubernetes sẽ được tạo ra là rất quan trọng. Lệnh `helm template` cho phép bạn xem trước các file này mà không thực sự triển khai chúng.

### Sử Dụng Lệnh helm template

1. **Di chuyển đến thư mục Helm chart**
   ```bash
   cd dev-env
   ```

2. **Chạy lệnh template**
   ```bash
   helm template .
   ```
   
   Dấu chấm (`.`) cho Helm biết rằng template nằm trong thư mục hiện tại.

### Kết Quả Mong Đợi

Lệnh này tạo ra tất cả các file manifest Kubernetes mà Helm sẽ tạo, bao gồm:
- Cấu hình Deployment
- Định nghĩa Service
- ConfigMaps
- Biến môi trường

## Khắc Phục Các Lỗi Thường Gặp

### Lỗi Cấu Hình Service Port

**Vấn đề:** Lỗi trong file template `common.service` nằm trong chart `easybank-common`.

**Triệu chứng:** Tên biến cho port chứa ký tự đặc biệt: `value.special_character.port`

**Giải pháp:**
1. Di chuyển đến templates của chart:
   ```
   easybank-common/templates/service.yaml
   ```

2. Sửa biến port từ:
   ```yaml
   port: {{ .Values.special_character.port }}
   ```
   
   Thành:
   ```yaml
   port: {{ .Values.service.port }}
   ```

## Biên Dịch Lại Helm Charts Sau Khi Thay Đổi

Khi bạn thay đổi common chart (`easybank-common`), tất cả các charts phụ thuộc phải được biên dịch lại.

### Biên Dịch Lại Charts của Từng Microservice

Di chuyển đến thư mục Helm chart của mỗi microservice và chạy:

```bash
cd easybank-services/accounts
helm dependency build
```

Lặp lại quy trình này cho tất cả các microservices phụ thuộc vào `easybank-common`.

### Biên Dịch Lại Environment Charts

Sau khi cập nhật microservice charts, biên dịch lại các charts theo môi trường:

**Môi Trường Development:**
```bash
cd environments/dev-env
helm dependency build
```

**Môi Trường QA:**
```bash
cd environments/qa-env
helm dependency build
```

**Môi Trường Production:**
```bash
cd environments/prod-env
helm dependency build
```

## Xác Thực Manifests Được Tạo Ra

### Ví dụ: Message Microservice

Sau khi chạy `helm template`, bạn có thể xem xét deployment được tạo:

```yaml
metadata:
  name: message-deployment
spec:
  replicas: 1
  # Các biến môi trường và cấu hình khác
```

### Xác Thực Theo Môi Trường

Các môi trường khác nhau sẽ tạo ra tên tài nguyên khác nhau:

**Môi Trường Production:**
```bash
cd prod-env
helm template .
```
Kết quả bao gồm: `easybank-prod-configmap`

**Môi Trường Development:**
```bash
cd dev-env
helm template .
```
Kết quả bao gồm: `easybank-dev-configmap`

## Yêu Cầu Trước Khi Triển Khai

Trước khi triển khai microservices lên Kubernetes, đảm bảo các thành phần sau đã được thiết lập:

### Các Thành Phần Hạ Tầng Cần Thiết

1. **Keycloak** - Quản lý định danh và truy cập
2. **Apache Kafka** - Nền tảng streaming sự kiện
3. **Grafana** - Giám sát và quan sát

### Sử Dụng Helm Charts Có Sẵn

Bạn không cần tạo Helm charts thủ công cho các thành phần này. Chúng được sử dụng rộng rãi trong ngành, và các cộng đồng mã nguồn mở đã xây dựng Helm charts cho:
- Kafka
- Keycloak
- Grafana

Các charts này có thể được cài đặt trực tiếp từ các Helm repositories.

## Các Bước Tiếp Theo

1. Thiết lập các thành phần hạ tầng (Keycloak, Kafka, Grafana) sử dụng Helm charts có sẵn
2. Triển khai môi trường bạn chọn (dev, qa, hoặc prod) bằng cách cài đặt environment Helm chart tương ứng
3. Xác minh tất cả microservices đang chạy chính xác
4. Giám sát việc triển khai sử dụng Grafana dashboards

## Thực Hành Tốt

- Luôn xác thực Helm charts bằng `helm template` trước khi cài đặt
- Biên dịch lại tất cả charts phụ thuộc sau khi sửa đổi common charts
- Kiểm tra triển khai trong môi trường development trước khi đưa lên QA và production
- Giữ các cấu hình theo môi trường riêng biệt
- Sử dụng version control cho tất cả thay đổi Helm chart

## Tóm Tắt

Lệnh `helm template` là công cụ xác thực quan trọng cho phép bạn xem trước các file manifest Kubernetes trước khi triển khai. Bằng cách phát hiện lỗi sớm và xác thực cấu hình trên các môi trường khác nhau, bạn có thể đảm bảo việc triển khai kiến trúc microservices của mình diễn ra suôn sẻ.




FILE: 63-deploying-keycloak-with-bitnami-helm-charts.md


# Triển khai Keycloak với Bitnami Helm Charts

## Giới thiệu

Một trong những ưu điểm lớn của Helm là có một cộng đồng hỗ trợ rất tốt. Điều này giúp bạn dễ dàng tìm thấy các Helm chart để cài đặt bất kỳ sản phẩm nào trong ngành công nghiệp phần mềm. Ví dụ, nếu bạn muốn cài đặt Kafka trong Kubernetes cluster của mình, bạn không cần phải chuẩn bị các tệp manifest Kubernetes thủ công. Thay vào đó, bạn có thể dựa vào các Helm chart có sẵn trên web.

## Bitnami Helm Charts

Bitnami là một công ty/cộng đồng duy trì các Helm chart với tiêu chuẩn sản xuất tuyệt vời. Bitnami giúp bạn dễ dàng chạy các phần mềm nguồn mở yêu thích trên bất kỳ nền tảng nào, bao gồm laptop, Kubernetes hoặc tất cả các đám mây lớn. Bitnami được hỗ trợ bởi VMware.

### Truy cập Bitnami Helm Charts

1. Tìm kiếm "bitnami helm charts github" trên Google
2. Điều hướng đến kho lưu trữ GitHub của Bitnami Helm charts
3. Mở thư mục Bitnami để xác định các Helm chart cho nhiều sản phẩm khác nhau

**Các sản phẩm có sẵn bao gồm:**
- Argo CD
- Cassandra
- Console
- Drupal
- Elasticsearch
- Grafana (bao gồm Grafana Loki, Grafana Tempo)
- Kafka
- Keycloak
- Kibana
- Kube Prometheus
- MongoDB
- Logstash
- MariaDB
- MySQL
- Nginx
- PostgreSQL
- RabbitMQ
- Redis

## Cài đặt Keycloak với Helm

### Bước 1: Tải xuống Bitnami Helm Charts

1. Điều hướng đến thư mục charts trong kho lưu trữ GitHub của Bitnami
2. Nhấp vào "Download Zip" để tải xuống tất cả Helm charts
3. Giải nén tệp zip đã tải xuống vào hệ thống cục bộ của bạn
4. Tìm thư mục Keycloak Helm chart
5. Sao chép thư mục Keycloak vào vị trí Helm charts của bạn

### Bước 2: Cấu hình Keycloak Helm Chart

Keycloak Helm chart chứa:
- `chart.yaml`
- Thư mục `templates`
- `values.yaml`

**Chỉnh sửa values.yaml:**

1. **Thay đổi loại Service:**
   - Tìm kiếm `cluster IP` trong tệp values.yaml
   - Thay thế `ClusterIP` bằng `LoadBalancer` để expose Keycloak ra bên ngoài

2. **Đặt mật khẩu Admin:**
   - Tìm kiếm biến `admin password`
   - Mặc định, admin user là `user` và password để trống (tạo mật khẩu ngẫu nhiên)
   - Đặt mật khẩu tùy chỉnh (ví dụ: `password`) để dễ dàng truy cập hơn

### Bước 3: Build Dependencies

Trước khi cài đặt, hãy build các dependencies của Helm chart:

```bash
cd keycloak
helm dependency build
```

Lệnh này biên dịch tất cả các dependencies và đóng gói chúng trong Keycloak Helm chart. Keycloak có dependency vào cơ sở dữ liệu PostgreSQL, sẽ được bao gồm.

### Bước 4: Cài đặt Keycloak

Điều hướng đến thư mục cha chứa Keycloak chart và chạy:

```bash
helm install keycloak keycloak
```

Trong đó:
- `keycloak` đầu tiên là tên release
- `keycloak` thứ hai là tên chart/thư mục

**Lưu ý:** Quá trình cài đặt sẽ xuất ra các hướng dẫn để truy cập Keycloak.

### Bước 5: Truy cập Keycloak

Đợi 1-2 phút để LoadBalancer được tạo. Sau đó truy cập Keycloak tại:
- URL: `http://localhost:80`
- Username: `user`
- Password: `password` (như đã cấu hình trong values.yaml)

## Cấu hình Keycloak cho Microservices

### Tạo Client

1. Điều hướng đến Administration Console
2. Nhấp vào "Clients"
3. Tạo một client mới với ID: `easybank-callcenter-cc`
4. Bật **Client Authentication**
5. Tắt **Standard Flow** và **Direct Access Grants**
6. Bật **Service Account Roles**
7. Lưu cấu hình
8. Vào tab "Credentials" và sao chép giá trị secret

### Tạo Roles

Tạo các role sau:
- `accounts`
- `cards`
- `loans`

### Gán Roles cho Client

1. Vào client (`easybank-callcenter-cc`)
2. Điều hướng đến "Service Account Roles"
3. Nhấp "Assign Role"
4. Gán tất cả các role cần thiết cho ứng dụng client

### Kiểm tra với Postman

Cập nhật URL access token trong Postman từ cổng `7080` sang cổng `80` để phù hợp với cấu hình Helm chart. Sau khi gán roles, bạn sẽ có thể lấy access token thành công.

## Hiểu về Keycloak DNS trong Kubernetes

Khi Helm cài đặt Keycloak, nó cung cấp một tên DNS để truy cập Keycloak từ bên trong cluster:

```
keycloak.<namespace>.svc.cluster.local
```

Tên DNS này nên được sử dụng trong cấu hình microservices của bạn (ví dụ: trong values.yaml của Helm chart cụ thể môi trường) để các dịch vụ như Gateway Server có thể kết nối với Keycloak từ trong cùng một Kubernetes cluster.

## Lợi ích của việc sử dụng Helm Charts

Sử dụng Helm charts cho việc cài đặt Keycloak mang lại:
- **Triển khai đơn giản:** Không cần tạo nhiều tệp manifest Kubernetes thủ công
- **Tiêu chuẩn Production:** Bitnami duy trì các chart theo các best practices
- **Quản lý Dependencies:** Tự động xử lý các dependencies như PostgreSQL
- **Tính nhất quán:** Quy trình triển khai giống nhau trên các môi trường

Thư mục templates trong Keycloak Helm chart chứa nhiều template đối tượng Kubernetes. Việc tạo tất cả các template này thủ công sẽ là một quá trình cực kỳ phức tạp.

## Cân nhắc về tài nguyên hệ thống

### Thiết lập phát triển cục bộ

Khi thực hiện nhiều cài đặt trong Kubernetes cluster của bạn, bạn có thể gặp phải các ràng buộc về bộ nhớ trên hệ thống cục bộ.

**Cài đặt Docker Desktop được khuyến nghị:**

1. Mở Docker Desktop Dashboard
2. Nhấp vào "Settings"
3. Điều hướng đến "Resources"
4. Tăng tài nguyên được phân bổ:
   - CPUs: 6 (từ mặc định 4)
   - Memory: 12GB (từ mặc định 8GB)

Các tài nguyên tăng lên này sẽ đảm bảo:
- Cài đặt nhanh hơn
- Thời gian phản hồi microservices tốt hơn
- Hiệu suất tổng thể mượt mà hơn

### Môi trường Production

Trong môi trường cloud production, các ràng buộc về bộ nhớ và CPU thường không phải là vấn đề vì bạn sẽ có quyền truy cập vào tài nguyên đáng kể.

### Giải pháp thay thế: Triển khai Cloud

Nếu laptop của bạn không thể đáp ứng yêu cầu tài nguyên, bạn có thể làm theo các quy trình triển khai tương tự trong môi trường cloud nơi tài nguyên có sẵn nhiều hơn.

## Các bước tiếp theo

Sau khi cài đặt thành công Keycloak, bạn sẽ cần thiết lập các thành phần khác:
- **Kafka** cho event streaming
- **Grafana** cho visualization
- **Prometheus** cho monitoring

Tất cả những thứ này có thể được cài đặt bằng cách sử dụng các Bitnami Helm chart tương ứng theo quy trình tương tự.

## Kết luận

Helm charts, đặc biệt là những chart từ Bitnami, đơn giản hóa đáng kể việc triển khai các ứng dụng phức tạp như Keycloak trong môi trường Kubernetes. Bằng cách tận dụng các chart này, bạn có thể tập trung vào việc cấu hình microservices của mình thay vì quản lý sự phức tạp của cơ sở hạ tầng.




FILE: 64-deploying-kafka-to-kubernetes-with-helm.md


# Triển khai Kafka lên Kubernetes với Helm Charts

## Tổng quan

Hướng dẫn này trình bày cách triển khai Apache Kafka vào Kubernetes cluster sử dụng Helm charts, sau khi đã cài đặt thành công Keycloak. Chúng ta sẽ tìm hiểu các lưu ý quan trọng cho môi trường phát triển local và giải quyết các vấn đề thường gặp khi cài đặt Helm.

## Yêu cầu tiên quyết

- Kubernetes cluster đang chạy trên máy local
- Helm đã được cài đặt và cấu hình
- Keycloak đã được triển khai trong cluster
- kubectl đã được cấu hình để truy cập cluster

## Xác minh cài đặt Keycloak

Trước khi tiến hành với Kafka, hãy xác minh rằng Keycloak đã được cài đặt đúng cách:

1. **Kiểm tra Pods**: Điều hướng đến phần Pods trong Kubernetes dashboard
   - Bạn sẽ thấy hai pods:
     - Pod Keycloak
     - Pod Keycloak PostgreSQL

2. **Kiểm tra Services**: Xác minh các services liên quan đến Keycloak đang chạy
   - Tất cả services phải hiển thị trong phần Services

3. **Kiểm tra ConfigMaps và Secrets**: Xác nhận các thành phần Keycloak có mặt trong cả ConfigMaps và Secrets

## Quan trọng: Hạn chế của Helm Uninstall

### Vấn đề với PVC

Có một lỗi đã biết trong Helm liên quan đến Persistent Volume Claims (PVCs):

- Khi bạn gỡ cài đặt Helm chart bằng lệnh `helm uninstall`, các PVCs được tạo trong quá trình cài đặt **không tự động bị xóa**
- PVCs cho phép pods yêu cầu không gian lưu trữ bên trong worker nodes
- Các PVCs còn tồn tại có thể gây ra vấn đề khi cài đặt lại cùng một Helm chart

### Kiểm tra các PVCs hiện có

Để xem tất cả PVCs trong cluster của bạn:

```bash
kubectl get pvc
```

### Xóa PVCs

Bạn có hai cách để xóa PVCs:

**Cách 1: Sử dụng Kubernetes Dashboard**
1. Điều hướng đến phần PVC
2. Chọn PVC bạn muốn xóa
3. Nhấp vào nút delete

**Cách 2: Sử dụng lệnh kubectl**

```bash
kubectl delete pvc <tên-pvc>
```

Ví dụ: Nếu bạn thấy các PVCs từ cài đặt WordPress trước đó, hãy xóa chúng trước khi cài đặt lại để tránh xung đột.

## Triển khai Kafka với Helm

### Bước 1: Chuẩn bị Kafka Helm Chart

1. Lấy Kafka Helm chart và đặt nó vào thư mục Helm charts của bạn
2. Chart sẽ được commit vào GitHub repository với tất cả các cấu hình cần thiết

### Bước 2: Chỉnh sửa values.yaml cho môi trường phát triển Local

Kafka Helm chart mặc định được cấu hình cho môi trường production, điều này có thể tiêu tốn quá nhiều tài nguyên cho phát triển local.

#### Giảm số lượng Replica

1. Mở file `values.yaml` trong thư mục Kafka Helm chart
2. Tìm kiếm `replicaCount`
3. Thay đổi giá trị từ `3` thành `1`:

```yaml
replicaCount: 1
```

**Lưu ý**: Trong môi trường production, quản trị viên Kafka của bạn sẽ quản lý số lượng replica và các cài đặt production khác.

#### Đơn giản hóa cấu hình bảo mật

Mặc định, Kafka sử dụng các giao thức truyền thông bảo mật phù hợp cho production. Đối với môi trường test local, chúng ta có thể đơn giản hóa điều này.

1. Tìm kiếm `SASL_PLAINTEXT` trong `values.yaml`
2. Thay thế tất cả các lần xuất hiện của `SASL_PLAINTEXT` bằng `PLAINTEXT`

**Các giá trị giao thức hợp lệ**:
- `PLAINTEXT` (cho phát triển local)
- `SSL`
- `SASL_PLAINTEXT`
- `SASL_SSL`

**Quan trọng**: Chỉ thay đổi các giá trị trong cấu hình thực tế, không thay đổi trong phần comments.

### Bước 3: Build Dependencies

Trước khi cài đặt, build các dependencies của Helm chart:

```bash
cd kafka
helm dependencies build
```

### Bước 4: Cài đặt Kafka

Quay lại thư mục cha và chạy:

```bash
helm install kafka kafka
```

## Xác minh cài đặt Kafka

### Thông tin kết nối

Sau khi cài đặt, bạn sẽ thấy output chứa các thông tin kết nối quan trọng:

- **Port**: 9092
- **DNS Name**: Mỗi Kafka broker có thể được truy cập bởi producers thông qua DNS name được cung cấp

Các DNS names này cần được cấu hình trong các microservices của bạn (accounts microservice và message microservice) để kích hoạt giao tiếp bất đồng bộ với Kafka.

### Xác minh trong Kubernetes Dashboard

1. **Kiểm tra Pods**: Điều hướng đến phần Pods
   - Xác minh các pods liên quan đến Kafka đang chạy

2. **Kiểm tra Services**: Điều hướng đến phần Services
   - Xác nhận các services Kafka đã có mặt
   - Tất cả services phải được định nghĩa là loại `ClusterIP`

3. **Kiểm tra ConfigMaps**: Xác minh các giá trị ConfigMap bao gồm chi tiết kết nối Kafka
   - Các giá trị này được định nghĩa trong các Helm charts theo từng environment

## Cấu hình ConfigMap

Đảm bảo các giá trị ConfigMap trong các Helm charts theo environment của bạn bao gồm các DNS names của Kafka broker. Điều này cho phép các microservices của bạn kết nối với Kafka để truyền tin bất đồng bộ.

## Kiểm tra thiết lập

Mặc dù output của Helm installation cung cấp hướng dẫn để kiểm tra với các tin nhắn mẫu, bạn có thể xác thực thiết lập thông qua các ứng dụng của mình. Các accounts và message microservices của bạn sẽ gửi các tin nhắn thực tế để kiểm tra tích hợp Kafka.

## Tóm tắt

Bạn đã hoàn thành thành công:
- ✅ Xác minh cài đặt Keycloak trong Kubernetes
- ✅ Hiểu rõ hạn chế PVC của Helm và quy trình dọn dẹp
- ✅ Cấu hình Kafka Helm chart cho phát triển local
- ✅ Triển khai Kafka lên Kubernetes cluster
- ✅ Xác minh cài đặt và services của Kafka

Kubernetes cluster của bạn giờ đã sẵn sàng với cả Keycloak cho authentication/authorization và Kafka cho giao tiếp bất đồng bộ hướng sự kiện giữa các microservices.

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ cấu hình các microservices để giao tiếp với Kafka và triển khai các mẫu hướng sự kiện cho messaging bất đồng bộ.




FILE: 65-setting-up-prometheus-and-grafana-in-kubernetes.md


# Cài Đặt Prometheus và Grafana trong Kubernetes

## Tổng Quan

Hướng dẫn này trình bày cách cài đặt Prometheus để thu thập metrics và chuẩn bị triển khai Grafana trong Kubernetes cluster để giám sát các microservices được xây dựng bằng Java Spring Boot.

## Yêu Cầu Trước Khi Bắt Đầu

- Kubernetes cluster đang hoạt động
- Đã cài đặt Helm
- Đã tải về Bitnami Helm charts repository
- Các microservices đã được cấu hình Spring Boot Actuator

## Cài Đặt Prometheus

### Bước 1: Chuẩn Bị Helm Chart

1. Điều hướng đến Bitnami repository và tìm thư mục `kube-prometheus`
2. Sao chép thư mục `kube-prometheus` vào thư mục helm của bạn

```bash
# Sao chép thư mục kube-prometheus vào thư mục helm
cp -r bitnami/kube-prometheus ./helm/
```

### Bước 2: Cấu Hình values.yaml

Mở file `values.yaml` trong thư mục `kube-prometheus` và thực hiện các thay đổi sau:

#### Bật Additional Scrape Configs

Tìm kiếm "additional scrape configs" và chỉnh sửa:

```yaml
additionalScrapeConfigs:
  enabled: true
  type: internal  # Thay đổi từ external sang internal
```

**Lý do**: Chúng ta đặt type là `internal` vì tất cả microservices đều nằm trong Kubernetes cluster, nên không cần thu thập metrics từ các nguồn bên ngoài.

#### Cấu Hình Jobs Cho Microservices

Trong danh sách internal job list, thêm cấu hình cho từng microservice theo định dạng JSON:

```json
[
  {
    "job_name": "config-server",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["configserver:8071"]
      }
    ]
  },
  {
    "job_name": "eureka-server",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["eurekaserver:8070"]
      }
    ]
  },
  {
    "job_name": "accounts",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["accounts:8080"]
      }
    ]
  },
  {
    "job_name": "loans",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["loans:8090"]
      }
    ]
  },
  {
    "job_name": "cards",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["cards:9000"]
      }
    ]
  },
  {
    "job_name": "gateway-server",
    "metrics_path": "/actuator/prometheus",
    "static_configs": [
      {
        "targets": ["gatewayserver:8072"]
      }
    ]
  }
]
```

**Chi Tiết Cấu Hình**:
- **job_name**: Định danh cho microservice
- **metrics_path**: Endpoint của Actuator để expose metrics cho Prometheus
- **targets**: Tên service và port trong Kubernetes cluster

### Bước 3: Build Helm Chart

Điều hướng đến thư mục `kube-prometheus` và build các dependencies:

```bash
cd helm/kube-prometheus
helm dependency build
```

### Bước 4: Cài Đặt Prometheus

Cài đặt Prometheus sử dụng Helm:

```bash
cd ..
helm install prometheus ./kube-prometheus
```

Lệnh này cài đặt Prometheus với tên release là "prometheus".

### Bước 5: Truy Cập Prometheus (Tùy Chọn)

Mặc định, Prometheus được cài đặt với ClusterIP, khiến nó không thể truy cập từ bên ngoài cluster. Để truy cập tạm thời, sử dụng port forwarding:

```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
```

**Lưu ý**: Đợi 1-2 phút sau khi cài đặt để tất cả pods sẵn sáng trước khi chạy lệnh port-forward.

### Bước 6: Xác Minh Cài Đặt Prometheus

1. Mở trình duyệt và truy cập `http://localhost:9090`
2. Vào **Status → Targets** để xem tất cả các targets đã cấu hình
3. Ban đầu, các microservices sẽ hiển thị trạng thái màu đỏ (down) vì chúng chưa được triển khai
4. Prometheus cũng sẽ tự động giám sát các thành phần khác của Kubernetes cluster

### Bước 7: Dừng Port Forwarding

Nhấn `Ctrl+C` trong terminal để dừng port forwarding. Sau khi dừng, Prometheus sẽ không còn truy cập được từ hệ thống local của bạn.

## Các Bước Tiếp Theo

Sau khi cài đặt thành công Prometheus, giai đoạn tiếp theo bao gồm:

1. Cài đặt **Grafana** để trực quan hóa dữ liệu
2. Cấu hình **Loki** để tổng hợp logs
3. Cài đặt **Tempo** cho distributed tracing
4. Tích hợp Grafana với Prometheus để tạo dashboards cho metrics
5. Triển khai microservices lên Kubernetes cluster để kiểm thử end-to-end

## Những Điểm Chính Cần Nhớ

- Prometheus yêu cầu cấu hình scrape tùy chỉnh cho từng microservice
- Tất cả cấu hình sử dụng tên service và port nội bộ trong Kubernetes
- Endpoint actuator Prometheus (`/actuator/prometheus`) expose metrics theo định dạng mà Prometheus có thể scrape
- Prometheus tự động giám sát nhiều thành phần của Kubernetes cluster trong các thiết lập production-ready
- Port forwarding hữu ích cho việc truy cập tạm thời các services được cấu hình với ClusterIP

## Khắc Phục Sự Cố

**Vấn đề**: Lệnh port forward thất bại  
**Giải pháp**: Đợi cho pods của Prometheus hoàn toàn sẵn sàng. Kiểm tra trạng thái pod bằng `kubectl get pods`

**Vấn đề**: Targets hiển thị trạng thái down  
**Giải pháp**: Điều này là bình thường trước khi triển khai microservices. Triển khai microservices của bạn để thấy chúng hoạt động.

**Vấn đề**: Không thể truy cập Prometheus sau khi dừng port-forward  
**Giải pháp**: Đây là hành vi mong đợi. Khởi động lại lệnh port-forward hoặc cấu hình Ingress để truy cập vĩnh viễn.

## Kết Luận

Bạn đã cài đặt thành công Prometheus trong Kubernetes cluster của mình. Nền tảng giám sát đã sẵn sàng để thu thập metrics từ các Spring Boot microservices của bạn sau khi chúng được triển khai.




FILE: 66-setting-up-grafana-loki-and-tempo-in-kubernetes.md


# Cài Đặt Grafana, Loki và Tempo trong Kubernetes

## Tổng Quan

Hướng dẫn này sẽ giúp bạn triển khai các thành phần liên quan đến Grafana (Loki, Tempo và Grafana) trong Kubernetes cluster bằng cách sử dụng Helm charts. Các thành phần này hoạt động cùng nhau để cung cấp khả năng quan sát toàn diện cho microservices:

- **Loki**: Tổng hợp logs từ các microservices riêng lẻ
- **Tempo**: Xử lý distributed tracing (theo dõi phân tán)
- **Grafana**: Trực quan hóa logs và traces

## Yêu Cầu Trước Khi Bắt Đầu

- Kubernetes cluster đang chạy trên máy local
- Helm đã được cài đặt và cấu hình
- Các microservices có OpenTelemetry Java agent

## Bước 1: Cài Đặt Grafana Loki

### Quy Trình Cài Đặt

1. **Sao Chép Helm Charts**: Sao chép các thư mục `grafana-loki` và `grafana-tempo` vào thư mục Helm của bạn.

2. **Điều Hướng đến Thư Mục Loki**:
   ```bash
   cd grafana-loki
   ```

3. **Build Dependencies**: Loki có dependencies với các charts khác như Memcached. Build chúng trước:
   ```bash
   helm dependencies build
   ```

4. **Cài Đặt Loki**: Quay lại thư mục cha và cài đặt chart:
   ```bash
   cd ..
   helm install loki grafana-loki
   ```

### Các Thành Phần Được Cài Đặt

Quá trình cài đặt Loki sẽ tạo ra nhiều thành phần trong Kubernetes cluster:
- Ingester
- Distributor
- Querier
- Promtail
- Compactor
- Gateway

### Lợi Ích Khi Sử Dụng Helm

Việc cài đặt thủ công các thành phần này sẽ yêu cầu:
- Sự hợp tác sâu rộng giữa Kubernetes administrators, developers và Grafana admins
- Hàng tháng nỗ lực để cấu hình đúng cách
- Quản lý cấu hình phức tạp

Với Helm, toàn bộ quá trình setup được đơn giản hóa và tự động hóa.

## Bước 2: Cài Đặt Grafana Tempo

### Thay Đổi Cấu Hình

1. **Mở File Values**: Điều hướng đến thư mục `grafana-tempo` và mở file `values.yaml`.

2. **Bật OpenTelemetry Protocol (OTLP)**: Tìm kiếm `otlp` trong file. Mặc định, cả HTTP và gRPC protocols đều bị tắt. Hãy bật chúng lên:
   ```yaml
   otlp:
     http:
       enabled: true
     grpc:
       enabled: true
   ```

   Thay đổi này là cần thiết để OpenTelemetry Java agent trong microservices của bạn có thể gửi chi tiết tracing đến Tempo.

### Quy Trình Cài Đặt

1. **Build Dependencies**:
   ```bash
   cd grafana-tempo
   helm dependencies build
   ```

2. **Cài Đặt Tempo**:
   ```bash
   cd ..
   helm install tempo grafana-tempo
   ```

### Các Thành Phần Được Cài Đặt

Quá trình cài đặt Tempo sẽ tạo ra:
- Ingester
- Distributor
- Querier
- Query-frontend
- Compactor
- Vulture

## Bước 3: Cấu Hình Microservices Kết Nối với Tempo

### Tìm URL Service Tempo

1. **Liệt Kê Các Kubernetes Services**:
   ```bash
   kubectl get services
   ```

2. **Xác Định Distributor Service**: Trong số tất cả các services liên quan đến Tempo (gossip-ring, ingester, generator, querier, vulture, compactor, distributor), OpenTelemetry agent nên kết nối đến service **distributor**.

3. **Cấu Hình Chi Tiết Kết Nối**:
   - Tên service: `tempo-distributor` (hoặc tương tự, dựa trên cài đặt của bạn)
   - Port: `4317`

### Cập Nhật ConfigMap

Thêm URL Tempo vào ConfigMap của microservices:
```yaml
tempo:
  url: tempo-distributor:4317
```

Điều này thiết lập kết nối giữa OpenTelemetry agent của microservices và Grafana Tempo.

### Hiểu Về Việc Chọn Service

Việc chọn distributor service dựa trên:
- Tài liệu chính thức của Grafana Tempo
- Best practices cho kiến trúc distributed tracing
- Vai trò của distributor trong việc nhận và xử lý dữ liệu trace đến

**Mẹo**: Luôn tham khảo tài liệu chính thức khi gặp các thách thức cấu hình tương tự.

## Bước Tiếp Theo

Với Loki và Tempo đã được cài đặt thành công, bước cuối cùng là cài đặt Grafana, công cụ sẽ cung cấp lớp visualization cho logs và traces của bạn.

## Những Điểm Chính Cần Nhớ

- Helm charts đơn giản hóa đáng kể các triển khai Kubernetes phức tạp
- Loki tổng hợp logs từ tất cả microservices
- Tempo xử lý distributed tracing với OpenTelemetry
- Cấu hình service đúng cách rất quan trọng cho giao tiếp giữa các microservices
- Luôn tham khảo tài liệu chính thức để biết chi tiết cấu hình




FILE: 67-deploying-grafana-to-kubernetes-cluster.md


# Triển khai Grafana lên Kubernetes Cluster với Helm

## Tổng quan

Hướng dẫn này đề cập đến quá trình thiết lập Grafana trong Kubernetes cluster sử dụng Helm charts, bao gồm cấu hình các nguồn dữ liệu (data sources) để tích hợp với Prometheus, Loki và Tempo.

## Yêu cầu trước khi bắt đầu

- Kubernetes cluster đang hoạt động
- Helm đã được cài đặt
- Bitnami Helm charts có sẵn
- Prometheus, Loki và Tempo đã được triển khai trong cluster

## Các bước cài đặt

### 1. Chuẩn bị Grafana Helm Chart

Đầu tiên, sao chép Grafana Helm chart từ thư mục Bitnami vào thư mục helm của bạn:

```bash
# Sao chép Grafana helm chart vào thư mục helm
cp -r bitnami/grafana helm/grafana
```

**Lưu ý**: Khuyến nghị sử dụng các Helm charts đã được commit vào GitHub repository để tránh phải thực hiện các thay đổi cấu hình thủ công trong file `values.yaml`.

### 2. Cấu hình Data Sources

Trước khi triển khai Grafana, bạn cần cấu hình các kết nối data source tới Prometheus, Loki và Tempo trong file `values.yaml`.

#### Xác định vị trí cấu hình Data Source

Mở file `values.yaml` và tìm kiếm "data source". Bạn sẽ tìm thấy một phần về data sources nơi bạn cần định nghĩa chi tiết data source dưới phần tử `secretDefinition`.

#### Cấu hình Data Source

Thay thế cấu hình mặc định bằng cấu trúc sau:

```yaml
secretDefinition:
  apiVersion: 1
  deleteDatasources:
    - name: Prometheus
    - name: Tempo
    - name: Loki
  datasources:
    - name: Prometheus
      type: prometheus
      url: http://prometheus-server-dns-name
      access: proxy
      isDefault: true
    
    - name: Tempo
      type: tempo
      url: http://grafana-tempo-query-frontend:3200
      access: proxy
    
    - name: Loki
      type: loki
      url: http://loki-gateway:80
      access: proxy
      jsonData:
        derivedFields:
          - datasourceUid: tempo
            matcherRegex: "traceId=(\\w+)"
            name: TraceId
            url: "$${__value.raw}"
```

#### Chi tiết cấu hình quan trọng

- **Prometheus**: Sử dụng tên DNS của Prometheus service trong Kubernetes cluster
- **Tempo**: Kết nối tới service `grafana-tempo-query-frontend` trên port 3200
- **Loki**: Kết nối tới service `loki-gateway` trên port 80
- **Derived Fields**: Được cấu hình để tích hợp Loki với Tempo cho việc tương quan traces

### 3. Build Helm Chart

Di chuyển vào thư mục Grafana và build dependencies:

```bash
cd helm/grafana
helm dependencies build
```

### 4. Cài đặt Grafana

Quay lại thư mục cha và cài đặt Grafana:

```bash
cd ..
helm install grafana grafana
```

Mặc định, Grafana sẽ được expose dưới dạng ClusterIP service.

### 5. Truy cập Grafana

Để truy cập Grafana cho mục đích debug hoặc quản trị, sử dụng kubectl port forwarding:

```bash
kubectl port-forward service/grafana 3000:3000
```

**Lưu ý**: Ban đầu, bạn có thể thử port 8080, nhưng nếu có microservices khác (như accounts microservice) đang sử dụng port đó, hãy chuyển sang port 3000 để tránh xung đột.

Truy cập Grafana trong trình duyệt tại: `http://localhost:3000`

### 6. Thông tin đăng nhập

- **Username**: `admin`
- **Password**: Lấy bằng các lệnh sau:

```bash
kubectl get secret grafana-admin -o jsonpath="{.data.admin-password}" | base64 --decode
```

Nhập thông tin đăng nhập vào trang login để truy cập Grafana.

### 7. Xác minh kết nối Data Source

Sau khi đăng nhập:

1. Điều hướng tới **Explore** trong giao diện Grafana
2. Kiểm tra menu dropdown - bạn sẽ thấy ba data sources:
   - Loki
   - Prometheus
   - Tempo

Điều này xác nhận rằng thiết lập Grafana của bạn đã hoàn tất và tất cả các data sources đã được cấu hình đúng cách.

## Quản lý Helm Releases

Để xem tất cả các Helm releases trong cluster:

```bash
helm ls
```

Lệnh này sẽ hiển thị tất cả các installations bao gồm:
- Grafana
- Kafka
- Keycloak
- Loki
- Prometheus
- Tempo

## Quản lý Port Forwarding

Để dừng port forwarding, chỉ cần kết thúc lệnh bằng `Ctrl+C`. Bạn có thể khởi động lại bất cứ lúc nào cần truy cập Grafana bằng cách chạy lại lệnh port-forward.

## Các bước tiếp theo

Với Grafana đã được triển khai và cấu hình thành công, bạn đã sẵn sàng triển khai các microservices của mình lên Kubernetes cluster. Observability stack (Prometheus, Loki, Tempo và Grafana) giờ đây đã sẵn sàng để giám sát và khắc phục sự cố cho các microservices của bạn.

## Tóm tắt

Trong hướng dẫn này, bạn đã học cách:
- Cấu hình data sources của Grafana trong `values.yaml`
- Build và cài đặt Grafana sử dụng Helm
- Truy cập Grafana sử dụng kubectl port-forward
- Xác minh kết nối data sources
- Quản lý Helm releases trong Kubernetes cluster

Thiết lập Grafana cung cấp một nền tảng giám sát và observability tập trung cho kiến trúc microservices của bạn.




FILE: 68-deploying-microservices-to-kubernetes-with-helm-complete-setup.md


# Triển khai Microservices lên Kubernetes với Helm - Thiết lập Hoàn chỉnh

## Tổng quan

Hướng dẫn này trình bày cách triển khai một kiến trúc microservices hoàn chỉnh lên Kubernetes cluster sử dụng Helm charts. Chúng ta sẽ triển khai nhiều microservices Spring Boot cùng với các thành phần hỗ trợ bao gồm Kafka, Grafana, Prometheus, Loki và Tempo.

## Yêu cầu Tiên quyết

- Kubernetes cluster đang chạy (local hoặc cloud)
- Helm đã được cài đặt
- Docker Desktop với Kubernetes được kích hoạt (cho thiết lập local)
- Tối thiểu 12GB RAM được phân bổ cho Docker/Kubernetes
- Helm charts theo môi trường đã được chuẩn bị (dev, prod, qa)

## Kiến trúc Triển khai

Hệ sinh thái microservices bao gồm:
- **Config Server** - Quản lý cấu hình tập trung
- **Eureka Server** - Service discovery (khám phá dịch vụ)
- **Gateway Server** - API Gateway với bảo mật OAuth2
- **Accounts Microservice** - Dịch vụ quản lý tài khoản
- **Cards Microservice** - Dịch vụ quản lý thẻ
- **Loans Microservice** - Dịch vụ quản lý khoản vay
- **Messages Microservice** - Dịch vụ nhắn tin theo sự kiện
- **Kafka** - Nền tảng streaming sự kiện
- **Grafana** - Giám sát và trực quan hóa
- **Prometheus** - Thu thập metrics
- **Loki** - Tổng hợp log
- **Tempo** - Distributed tracing (truy vết phân tán)
- **Keycloak** - Quản lý danh tính và truy cập

## Quy trình Triển khai

### Bước 1: Di chuyển đến Thư mục Environment

Đảm bảo bạn đang ở trong thư mục `environments` chứa ba charts:
- `dev-env` - Môi trường Development
- `qa-env` - Môi trường QA
- `prod-env` - Môi trường Production

### Bước 2: Triển khai sử dụng Helm

Để triển khai lên môi trường production, thực thi:

```bash
helm install easybank prod-env
```

**Giải thích lệnh:**
- `helm install` - Lệnh cài đặt Helm
- `easybank` - Tên release
- `prod-env` - Tên chart cho profile production

### Bước 3: Giám sát Triển khai

Sau khi thực thi lệnh, bạn sẽ nhận được xác nhận rằng việc triển khai đã được khởi động hoặc hoàn thành.

## Hiểu về Hành vi Khởi động Pod

### Thách thức Khởi động Ban đầu

Khi tất cả microservices khởi động đồng thời, chúng có thể thất bại ban đầu do:
- Config Server chưa sẵn sàng
- Eureka Server chưa sẵn sàng
- Các phụ thuộc giữa các service chưa sẵn sàng

### Tự động Phục hồi của Kubernetes

Kubernetes tự động xử lý lỗi pod:
- **Khởi động lại Tự động** - Pods được khởi động lại cho đến khi thành công hoặc đạt số lần thử tối đa
- **Exponential Backoff** - Độ trễ khởi động lại tăng dần (2s, 4s, 5s, v.v.)
- **Self-Healing** - Cluster tự động duy trì trạng thái mong muốn

## Xác minh Khởi động Microservices

### Truy cập Kubernetes Dashboard

Điều hướng đến Kubernetes dashboard để giám sát trạng thái pod và logs.

### Xác minh Từng bước

#### 1. Config Server (Quan trọng - Khởi động Đầu tiên)

Config Server phải khởi động trước vì các service khác phụ thuộc vào nó.

**Kiểm tra logs:**
- Click vào Config Server pod
- Chọn "View Logs"
- Bật "Auto refresh every 5 seconds"
- Đợi thông báo: "Config server started successfully"

**Lưu ý:** Trên hệ thống có tài nguyên hạn chế (16GB RAM với 12GB phân bổ cho Docker), quá trình khởi động có thể mất 5-10 phút.

#### 2. Eureka Server

Eureka Server phụ thuộc vào Config Server.

**Hành vi mong đợi:**
- Có thể hiển thị nhiều lần thử khởi động lại ban đầu
- Bộ đếm khởi động lại sẽ tăng cho đến khi Config Server sẵn sàng
- Tìm kiếm: "Started Eureka Server application in X seconds"

#### 3. Accounts Microservice

**Hành vi mong đợi:**
- Phụ thuộc vào cả Config Server và Eureka Server
- Sẽ khởi động lại cho đến khi các phụ thuộc sẵn sàng
- Nên kết nối thành công với Eureka Server khi đã khởi động

#### 4. Cards Microservice

**Xác minh:**
- Kiểm tra logs để xác nhận khởi động thành công
- Xác minh kết nối Eureka Server

#### 5. Loans Microservice

**Xác minh:**
- Kiểm tra logs để xác nhận khởi động thành công
- Xác minh kết nối Eureka Server

#### 6. Gateway Server

**Xác minh:**
- Tìm kiếm: "Gateway server application started successfully"
- Quan trọng cho việc định tuyến API và bảo mật

#### 7. Messages Microservice

**Hành vi mong đợi:**
- Không phụ thuộc vào Config Server hoặc Eureka Server
- Nên có số lần khởi động lại bằng không
- Xác minh kết nối Kafka broker

## Kiểm thử Microservices đã Triển khai

### 1. Kiểm thử Accounts Service

**Kiểm thử Configuration API:**
```bash
GET /contact-info
```

**Kết quả mong đợi:**
- Trả về properties từ production profile
- Xác nhận ứng dụng khởi động với profile đúng

### 2. Kiểm thử Cards Service

**Kiểm thử Java Version API:**
```bash
GET /api/java-version
```

### 3. Kiểm thử Loans Service

**Kiểm thử Build Info API:**
```bash
GET /api/build-info
```

### 4. Kiểm thử Tạo Account với OAuth2

**Lấy Access Token:**
```bash
POST /oauth2/token
- Bao gồm client secret
- Sử dụng Keycloak URL với port 80
```

**Tạo Account Mới:**
```bash
POST /api/accounts
Authorization: Bearer {access_token}
```

**Phản hồi mong đợi:** 201 Created - Account được tạo thành công

### 5. Kiểm thử Tạo Cards

**Các bước:**
1. Cập nhật client secret trong request
2. Cập nhật Keycloak port thành 80 trong access token URL
3. Lấy access token
4. Gọi Cards API với access token

### 6. Kiểm thử Tạo Loans

**Các bước:**
1. Cập nhật client secret trong request
2. Cập nhật port thành 80 trong access token URL
3. Lấy access token
4. Tạo loan mới cho số điện thoại đã cho

### 7. Kiểm thử Thông tin Khách hàng Tổng hợp

**Lấy Thông tin Khách hàng Hoàn chỉnh:**
```bash
GET /api/fetchCustomerDetails?mobileNumber={number}
Authorization: Bearer {access_token}
```

**Phản hồi mong đợi:**
- Thông tin accounts đầy đủ
- Thông tin loans
- Thông tin cards

**Lưu ý:** Có thể gặp timeout ở lần thử đầu tiên với tài nguyên hạn chế. Thử lại nếu cần.

## Thiết lập Giám sát và Quan sát

### Cấu hình Grafana

**Truy cập Grafana:**
- Được expose trên port 3000
- Sử dụng port forwarding: `kubectl port-forward svc/grafana 3000:3000`

### 1. Loki - Tổng hợp Log

**Xem Logs:**
1. Điều hướng đến "Explore" trong Grafana
2. Chọn "Loki" làm data source
3. Chọn label: "container"
4. Chọn tên container: "gateway-server"
5. Chạy query để xem tất cả Gateway Server logs

**Tích hợp Distributed Tracing:**
- Click vào bất kỳ log entry nào
- Truy cập link đến Tempo cho trace ID
- Xem chi tiết distributed tracing đầy đủ

### 2. Tempo - Distributed Tracing

**Tính năng:**
- Trực quan hóa trace hoàn chỉnh
- Luồng request qua các microservices
- Xác định điểm nghẽn hiệu suất
- Tích hợp với Loki để tương quan log-to-trace

### 3. Prometheus - Thu thập Metrics

**Xem Metrics:**
1. Điều hướng đến "Explore"
2. Chọn "Prometheus" làm data source
3. Tìm kiếm metric: "up"
4. Chọn label: "container"
5. Chạy query

**Trực quan hóa:**
- Xem biểu đồ cho 15 phút cuối
- Thay đổi kiểu biểu đồ thành "stacked lines"
- Giám sát uptime cho tất cả containers

**Phân tích Metric:**
- Metrics uptime cho containers đang chạy
- Chỉ số sức khỏe dịch vụ
- Xu hướng sử dụng tài nguyên

## Cân nhắc về Hiệu suất

### Môi trường Development Local

**Yêu cầu Hệ thống:**
- Tối thiểu 16GB RAM
- 12GB phân bổ cho Docker Desktop/Kubernetes
- Khuyến nghị SSD để có hiệu suất tốt hơn

**Hành vi Mong đợi:**
- Thời gian khởi động: 5-10 phút
- Nhiều lần khởi động lại pod trong quá trình initialization
- CPU sử dụng cao trong khi khởi động
- Trạng thái nhất quán cuối cùng khi tất cả services đang chạy

### Mẹo Tối ưu hóa Tài nguyên

1. Khởi động services theo thứ tự phụ thuộc khi có thể
2. Giám sát sử dụng tài nguyên qua Kubernetes dashboard
3. Điều chỉnh giới hạn tài nguyên trong Helm values
4. Sử dụng readiness và liveness probes
5. Triển khai retry logic phù hợp trong microservices

## Khắc phục Sự cố

### Vấn đề Thường gặp

**Pods Liên tục Khởi động lại:**
- Kiểm tra Config Server logs trước
- Xác minh kết nối Eureka Server
- Đảm bảo cấu hình profile đúng

**Lỗi Timeout:**
- Bình thường trong môi trường hạn chế tài nguyên
- Thử lại các request thất bại
- Cân nhắc tăng giá trị timeout

**Vấn đề Truy cập Port:**
- Xác minh port forwarding đang hoạt động
- Kiểm tra cấu hình service exposure
- Đảm bảo không có xung đột port

## Kết luận

Triển khai thành công một hệ sinh thái microservices hoàn chỉnh lên Kubernetes bao gồm:

✅ Helm charts theo môi trường (dev, qa, prod)  
✅ Sắp xếp khởi động và quản lý phụ thuộc phù hợp  
✅ Cơ chế tự động phục hồi của Kubernetes  
✅ Giám sát toàn diện với Grafana, Prometheus, Loki, Tempo  
✅ Truy cập bảo mật với tích hợp OAuth2/Keycloak  
✅ Event streaming với Kafka  
✅ Distributed tracing và tổng hợp log  

### Thành tựu Đã mở khóa

Bạn đã học thành công cách:
- Triển khai kiến trúc microservices phức tạp sử dụng Helm
- Quản lý cấu hình multi-environment
- Triển khai observability toàn diện
- Tích hợp bảo mật với Keycloak
- Thiết lập kiến trúc event-driven với Kafka
- Khắc phục sự cố triển khai Kubernetes

### Bước tiếp theo

Trong các phần sắp tới, chúng ta sẽ khám phá:
- Thiết lập môi trường trong hạ tầng cloud phù hợp
- Chiến lược triển khai production-grade
- Tính năng Kubernetes nâng cao
- Best practices cloud-native

## Điểm Chính Cần nhớ

1. **Helm đơn giản hóa triển khai** - Một lệnh duy nhất triển khai toàn bộ hệ sinh thái
2. **Kubernetes tự phục hồi** - Khởi động lại và phục hồi tự động
3. **Observability rất quan trọng** - Logs, metrics và traces là thiết yếu
4. **Tích hợp bảo mật** - OAuth2 với Keycloak cung cấp xác thực mạnh mẽ
5. **Kiến trúc Event-driven** - Kafka cho phép giao tiếp async có khả năng mở rộng
6. **Kiểm thử local khả thi** - Thiết lập giống production hoàn chỉnh trên máy local

---

**Chúc mừng!** Bây giờ bạn là một trong số ít các developer hiểu được quy trình hoàn chỉnh của việc triển khai và quản lý microservices trong Kubernetes với cơ sở hạ tầng hỗ trợ cấp doanh nghiệp.




FILE: 69-helm-upgrade-and-rollback-microservices.md


# Nâng Cấp và Khôi Phục Microservices với Helm

## Tổng Quan

Khi quản lý các microservices được triển khai bằng Helm charts trong Kubernetes, bạn sẽ thường xuyên cần triển khai các thay đổi mới hoặc cập nhật deployments. Hướng dẫn này trình bày cách nâng cấp và khôi phục microservices bằng các lệnh Helm, tương tự như chức năng rollout và rollback của `kubectl`.

## Các Trường Hợp Sử Dụng Phổ Biến

- **Mở rộng ứng dụng**: Tăng hoặc giảm số lượng replica (ví dụ: từ 1 lên 2 hoặc từ 2 lên 5)
- **Triển khai Docker images mới**: Cập nhật lên phiên bản mới hơn của microservices
- **Thay đổi cấu hình**: Điều chỉnh các thiết lập ứng dụng và giá trị theo môi trường

## Yêu Cầu Trước Khi Bắt Đầu

- Helm charts đã được cài đặt trong Kubernetes cluster
- Quyền truy cập vào cấu trúc thư mục helm chart
- Biết tên release và các chart dependencies

## Nâng Cấp Microservices với Helm

### Bước 1: Di Chuyển Đến Thư Mục Helm Chart

```bash
cd helm/environments/prod-env
```

### Bước 2: Thực Hiện Thay Đổi Values

Chỉnh sửa file `values.yaml` cho microservice cụ thể. Ví dụ, để thay đổi image tag của Gateway Server:

```yaml
# gateway-server/values.yaml
image:
  tag: s11  # Đã thay đổi từ s14 sang s11
```

### Bước 3: Build Lại Chart Dependencies

Nếu environment chart của bạn có dependencies với các microservice charts riêng lẻ, hãy build lại chúng:

```bash
cd prod-env
helm dependency build
```

### Bước 4: Thực Thi Lệnh Helm Upgrade

Di chuyển trở lại thư mục cha và chạy lệnh upgrade:

```bash
cd ..
helm upgrade easybank prod-env
```

**Điểm quan trọng:**
- `easybank` là tên release
- `prod-env` là tên helm chart
- Helm tự động nhận diện các thay đổi và chỉ triển khai những gì cần thiết
- Mỗi lần upgrade sẽ tăng số revision (ví dụ: revision 2, 3, v.v.)

## Giám Sát Quá Trình Nâng Cấp

### Kiểm Tra Kubernetes Dashboard

1. Truy cập vào phần Pods
2. Tìm kiếm pods có tên microservice của bạn (ví dụ: gateway-server)
3. Kiểm tra tuổi của pod để xác định pods mới được tạo
4. Xem logs để xác nhận khởi động thành công

### Xác Minh Triển Khai

Sau khi ứng dụng khởi động thành công, hãy kiểm tra các API của bạn để xác nhận các thay đổi hoạt động như mong đợi. Ví dụ:

```bash
# Kiểm tra một endpoint không cần xác thực (nếu đã loại bỏ security)
POST http://gateway-server/api/accounts
```

## Xử Lý Các Vấn Đề Thường Gặp

### Sai Image Tag

**Vấn đề**: Triển khai sai tag của Docker image (ví dụ: s12 thay vì s11)

**Giải pháp**: 
1. Sửa lại tag trong `values.yaml`
2. Build lại dependencies: `helm dependency build`
3. Chạy lại upgrade: `helm upgrade easybank prod-env`
4. Số revision sẽ tăng (ví dụ: lên revision 3)

## Các Phương Pháp Hay Nhất

### 1. **Quản Lý Số Lượng Replica**

Bạn có thể dễ dàng scale microservices bằng cách cập nhật replica count:

```yaml
replicaCount: 3  # Đã thay đổi từ 1 lên 3
```

### 2. **Cân Nhắc Tài Nguyên**

Lưu ý về tài nguyên hệ thống khi scaling:
- Giám sát CPU và memory usage
- Cân nhắc khả năng hạ tầng trước khi tăng replicas
- Kiểm tra ở các môi trường thấp hơn trước

### 3. **Quản Lý Phiên Bản**

- Luôn theo dõi các thay đổi trong files `values.yaml`
- Sử dụng Git để duy trì lịch sử phiên bản
- Ghi chép lý do cho mỗi lần upgrade

## Khôi Phục với Helm

Trong khi hướng dẫn này tập trung vào nâng cấp, Helm cũng cung cấp khả năng rollback. Nếu việc nâng cấp gây ra vấn đề, bạn có thể rollback về revision trước đó bằng cách sử dụng:

```bash
helm rollback easybank <revision-number>
```

## Quy Trình Ví Dụ

```bash
# 1. Di chuyển đến thư mục chart
cd helm/environments/prod-env

# 2. Chỉnh sửa values
vi gateway-server/values.yaml

# 3. Build lại dependencies
helm dependency build

# 4. Quay lại thư mục cha
cd ..

# 5. Nâng cấp release
helm upgrade easybank prod-env

# 6. Xác minh deployment
kubectl get pods
kubectl logs <gateway-server-pod-name>
```

## Tóm Tắt

Chức năng upgrade của Helm cung cấp một cách mạnh mẽ để quản lý các deployments microservices:
- **Triển khai thông minh**: Chỉ các tài nguyên thay đổi mới được cập nhật
- **Theo dõi revision**: Mỗi lần upgrade được phiên bản hóa để dễ dàng rollback
- **Quản lý dependencies**: Tự động xử lý các chart dependencies
- **Giảm thiểu downtime**: Rolling updates đảm bảo tính khả dụng của dịch vụ

Bằng cách làm theo các bước này, bạn có thể tự tin quản lý và cập nhật microservices của mình trong môi trường Kubernetes bằng Helm charts.




FILE: 7-testing-oauth2-security-in-microservices.md


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




FILE: 70-helm-rollback-microservices-tutorial.md


# Hướng Dẫn Helm Rollback cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách quay lại (rollback) phiên bản hoạt động trước đó của microservices deployment bằng cách sử dụng Helm. Khác với Kubectl, yêu cầu rollback từng thành phần một, Helm cho phép rollback toàn bộ các thành phần Kubernetes cluster về trạng thái mong muốn trước đó chỉ với một lệnh duy nhất.

## Lợi Ích Chính của Helm Rollback

- **Rollback Bằng Một Lệnh Duy Nhất**: Quay lại toàn bộ các thành phần Kubernetes cluster chỉ với một lệnh
- **Hỗ Trợ Đa Dịch Vụ**: Bất kể bạn đã thay đổi bao nhiêu microservices, rollback vẫn được thực hiện chỉ với một lệnh duy nhất
- **Theo Dõi Lịch Sử Phiên Bản**: Duy trì lịch sử rõ ràng về tất cả các deployments và upgrades

## Lệnh Helm History

Trước khi thực hiện rollback, bạn có thể xem lịch sử deployment bằng lệnh Helm History.

### Cú Pháp
```bash
helm history <tên-release>
```

### Ví Dụ
```bash
helm history easybank
```

Lệnh này hiển thị tất cả các cài đặt và nâng cấp đã xảy ra cho một Helm chart cụ thể, bao gồm:
- Số revision
- Trạng thái cài đặt/deployment
- Các thay đổi được thực hiện trong mỗi revision

### Cấu Trúc Output Mẫu
- **Revision 1**: Cài đặt ban đầu hoàn tất
- **Revision 2**: Deploy với tag name s12 (có lỗi)
- **Revision 3**: Cập nhật với tag name s11, trạng thái hiện tại đang deployed

## Thực Hiện Rollback

### Cú Pháp Lệnh
```bash
helm rollback <tên-release> <số-revision>
```

### Ví Dụ: Rollback về Revision 1
```bash
helm rollback easybank 1
```

Lệnh này sẽ:
1. Rollback về revision được chỉ định (revision 1 trong ví dụ này)
2. Thực thi rollback chỉ với một lệnh duy nhất
3. Trả về thông báo thành công khi hoàn tất

## Xác Minh Rollback

### Sử Dụng Kubernetes Dashboard

1. Điều hướng đến Kubernetes dashboard
2. Vào phần **Pods**
3. Mở pod mới được tạo
4. Kiểm tra tab **Events** để xem:
   - Docker image mới đang được deploy (ví dụ: s14)
   - Tiến trình deployment

### Kiểm Tra Application Logs

Giám sát logs để xác minh ứng dụng đã khởi động thành công:
- Gateway server application nên khởi động không có lỗi
- Tất cả services nên đang chạy bình thường

### Kiểm Tra Bằng API Calls

Xác thực rollback bằng cách test các API của bạn:
- Trong ví dụ này, thử gọi API nên trả về **lỗi 401** (như mong đợi với bảo mật thích hợp)
- Điều này xác nhận gateway server hiện đã được bảo mật đúng cách

## Lịch Sử Sau Rollback

Sau khi hoàn thành rollback, chạy lại lệnh history sẽ hiển thị:

```bash
helm history easybank
```

Bạn sẽ thấy một revision mới (ví dụ: Revision 4) với comment chỉ ra "rollback to 1". Điều này cung cấp tài liệu rõ ràng cho:
- Các thao tác rollback trong tương lai
- Hiểu lịch sử deployment
- Theo dõi các thay đổi cho một release cụ thể

## Best Practices (Thực Hành Tốt Nhất)

1. **Luôn Kiểm Tra History Trước**: Xem lại lịch sử revision trước khi thực hiện rollback
2. **Ghi Chép Các Thay Đổi**: Duy trì tài liệu rõ ràng về những thay đổi được thực hiện trong mỗi revision
3. **Kiểm Tra Sau Rollback**: Luôn xác minh rollback thành công thông qua logs và API testing
4. **Cập Nhật File Cấu Hình**: Sau rollback, cập nhật file values.yaml để phản ánh trạng thái hiện tại trước khi check-in vào version control (ví dụ: GitHub)

## Kết Luận

Helm rollback là một tính năng mạnh mẽ giúp đơn giản hóa quy trình quay lại các phiên bản hoạt động trước đó của microservices deployment. Chỉ với một lệnh duy nhất, bạn có thể đảm bảo toàn bộ Kubernetes cluster của mình quay trở lại trạng thái ổn định, mong muốn, khiến nó trở thành công cụ thiết yếu để quản lý microservices trong môi trường production.

---

**Lưu Ý**: Hướng dẫn này là một phần của series toàn diện về microservices bao gồm Spring Boot, Kubernetes và Helm.




FILE: 71-helm-uninstall-command-guide.md


# Hướng Dẫn Lệnh Helm Uninstall

## Tổng Quan

Giống như cách Helm cho phép bạn cài đặt toàn bộ hệ thống microservice chỉ với một lệnh duy nhất, nó cũng cung cấp khả năng gỡ cài đặt tất cả microservices chỉ bằng một lệnh. Hướng dẫn này sẽ trình bày cách sử dụng lệnh Helm Uninstall để xóa các microservices khỏi Kubernetes cluster.

## Tại Sao Sử Dụng Helm Uninstall?

Lệnh Helm Uninstall rất hữu ích khi bạn cần:
- Tắt toàn bộ Kubernetes cluster
- Dọn dẹp tài nguyên trong các môi trường phát triển
- Giải phóng tài nguyên hệ thống trong quá trình phát triển

## Liệt Kê Các Helm Release Hiện Tại

Trước khi gỡ cài đặt, bạn có thể xem tất cả các cài đặt Helm hiện tại bằng lệnh:

```bash
helm ls
```

Lệnh này hiển thị tất cả các release đã được cài đặt với Helm.

## Gỡ Cài Đặt Helm Releases

### Cú Pháp Lệnh Uninstall Cơ Bản

Cú pháp để gỡ cài đặt một Helm release:

```bash
helm uninstall <tên-release>
```

### Ví Dụ: Gỡ Cài Đặt Microservices

#### Bước 1: Gỡ Cài Đặt Ứng Dụng Chính
```bash
helm uninstall easybank
```

Lệnh này sẽ xóa tất cả các microservices được triển khai dưới Easy Bank release.

#### Bước 2: Gỡ Cài Đặt Các Thành Phần Bổ Sung

Gỡ cài đặt các thành phần còn lại theo thứ tự:

```bash
helm uninstall grafana
helm uninstall tempo
helm uninstall loki
helm uninstall prometheus
helm uninstall kafka
helm uninstall keycloak
```

### Xác Minh

Sau khi gỡ cài đặt tất cả các releases, xác minh việc dọn dẹp:

```bash
helm ls
```

Bạn sẽ thấy kết quả trống, xác nhận rằng tất cả các releases đã được xóa.

## Xác Minh Qua Kubernetes Dashboard

Bạn cũng có thể xác thực việc gỡ cài đặt thông qua Kubernetes dashboard:
- Truy cập vào Kubernetes dashboard của bạn
- Xác minh rằng các pods, deployments, services, config maps và secrets đã được xóa

## Quan Trọng: Persistent Volume Claims (PVCs)

### Vấn Đề Đã Biết

**Lưu Ý Quan Trọng**: Persistent Volume Claims (PVCs) **không tự động bị xóa** trong quá trình gỡ cài đặt Helm.

### Tại Sao Điều Này Quan Trọng

- PVCs còn sót lại có thể gây ra vấn đề khi cài đặt lại Helm charts
- Điều này đặc biệt ảnh hưởng đến các thành phần như Keycloak, Kafka và các ứng dụng có trạng thái khác
- Chưa rõ đây là lỗi hay hành vi cố ý của Helm

### Dọn Dẹp PVC Thủ Công

Để xóa persistent volume claims:

1. Chọn các PVCs trong Kubernetes dashboard
2. Nhấp vào nút delete
3. Lặp lại cho tất cả các PVCs còn lại

**Luôn xóa PVCs sau khi gỡ cài đặt Helm releases để tránh các vấn đề cài đặt trong tương lai.**

## Giải Pháp Thay Thế Cho Helm: Kustomize

### Kustomize Là Gì?

Kustomize (có sẵn tại [kustomize.io](https://kustomize.io)) là một đối thủ cạnh tranh với Helm, giải quyết các thách thức triển khai tương tự.

### So Sánh Kustomize vs Helm

#### Ưu Điểm của Kustomize:
- Dễ học hơn
- Đường cong học tập thấp hơn
- Cách tiếp cận cấu hình đơn giản hơn

#### Ưu Điểm của Helm:
- Hệ sinh thái mạnh mẽ hơn
- Nhiều community charts (Bitnami và các nguồn khác)
- Có thể cài đặt nhiều thành phần/sản phẩm dễ dàng
- Nhiều tính năng và khả năng hơn
- Tốt hơn cho các triển khai phức tạp

### Khuyến Nghị

**Sử dụng Helm** vì những lý do sau:
- Hỗ trợ cộng đồng mạnh mẽ hơn
- Truy cập vào các Bitnami charts và community charts có sẵn
- Khả năng toàn diện hơn
- Nhiều dự án bắt đầu với Kustomize cuối cùng cũng chuyển sang Helm

Tuy nhiên, nếu Kustomize đáp ứng các yêu cầu dự án của bạn và bạn thích sự đơn giản của nó, hãy thoải mái sử dụng nó.

## Tài Nguyên Bổ Sung

Để biết thêm chi tiết về Kustomize, tham khảo [tài liệu chính thức](https://kustomize.io).

## Tóm Tắt

- Sử dụng `helm ls` để liệt kê tất cả các releases đã cài đặt
- Sử dụng `helm uninstall <tên-release>` để xóa releases
- Luôn xóa thủ công Persistent Volume Claims sau khi gỡ cài đặt
- Helm cung cấp hệ sinh thái mạnh mẽ với sự hỗ trợ của cộng đồng
- Cân nhắc nhu cầu dự án khi lựa chọn giữa Helm và Kustomize

## Kết Luận

Helm cung cấp các lệnh mạnh mẽ để quản lý microservices trong Kubernetes clusters. Hiểu rõ quy trình gỡ cài đặt, bao gồm cả việc dọn dẹp đúng cách các PVCs, là điều thiết yếu để duy trì một môi trường Kubernetes khỏe mạnh.




FILE: 72-helm-commands-quick-reference-guide.md


# Hướng Dẫn Tham Khảo Nhanh Các Lệnh Helm

## Tổng Quan

Hướng dẫn này cung cấp một cái nhìn tổng quan toàn diện về các lệnh Helm thiết yếu được sử dụng để quản lý ứng dụng Kubernetes thông qua Helm charts. Các lệnh này bao gồm toàn bộ vòng đời quản lý Helm chart, từ khởi tạo đến triển khai và bảo trì.

## Các Lệnh Helm Thiết Yếu

### 1. Lệnh Helm Create

Lệnh `helm create` tạo ra một Helm chart trống hoặc mặc định với tên được chỉ định.

```bash
helm create <tên-chart>
```

Khi bạn tạo một Helm chart bằng lệnh này, thư mục chart sẽ chứa:
- `Chart.yaml` - Thông tin metadata của chart
- `values.yaml` - Các giá trị cấu hình mặc định
- Thư mục `charts/` - Dành cho các chart phụ thuộc
- Thư mục `templates/` - Các template manifest Kubernetes

### 2. Lệnh Helm Dependencies Build

Lệnh này xây dựng một Helm chart cụ thể và biên dịch tất cả các phụ thuộc được định nghĩa trong chart.

```bash
helm dependencies build
```

Tất cả các chart phụ thuộc sẽ được sao chép vào thư mục `charts/` trong quá trình này.

### 3. Lệnh Helm Install

Lệnh install triển khai Helm chart của bạn lên Kubernetes cluster.

```bash
helm install <tên-release> <thư-mục-chart>
```

Khi thực thi, Helm sẽ cài đặt tất cả các hướng dẫn triển khai từ chart của bạn và các chart phụ thuộc vào Kubernetes cluster.

### 4. Lệnh Helm Upgrade

Sử dụng lệnh này để triển khai các thay đổi mới sau khi cập nhật Helm chart của bạn.

```bash
helm upgrade <tên-release> <thư-mục-chart>
```

Đầu tiên, cập nhật và biên dịch lại Helm chart của bạn, sau đó chạy lệnh upgrade để áp dụng các thay đổi.

### 5. Lệnh Helm History

Xem lịch sử cài đặt của các Helm release để hiểu các phiên bản trước đó.

```bash
helm history <tên-release>
```

Điều này giúp bạn xác định phiên bản nào bạn muốn rollback nếu cần.

### 6. Lệnh Helm Rollback

Quay lại phiên bản hoạt động trước đó hoặc revision cụ thể.

```bash
helm rollback <tên-release> <số-revision>
```

Nếu bạn không chỉ định số revision, Helm sẽ rollback về revision ngay trước đó.

### 7. Lệnh Helm Uninstall

Gỡ bỏ hoàn toàn tất cả microservices khỏi Kubernetes cluster của bạn.

```bash
helm uninstall <tên-release>
```

Lệnh này xóa release được chỉ định và tất cả các tài nguyên liên quan.

### 8. Lệnh Helm Template

Render tất cả các file manifest Kubernetes mà Helm sẽ sử dụng trong quá trình cài đặt.

```bash
helm template <thư-mục-chart>
```

Điều này hữu ích cho việc debug bằng cách xem trước những gì sẽ được triển khai mà không thực sự cài đặt.

### 9. Lệnh Helm List

Liệt kê tất cả các release được quản lý bởi Helm trong cluster của bạn.

```bash
helm ls
```

Lệnh này cung cấp tổng quan về tất cả các Helm release hiện đang được triển khai.

## Tham Khảo GitHub Repository

Tất cả các file và chart Helm được thảo luận trong hướng dẫn này đều có sẵn trong GitHub repository dưới **Section 16** trong thư mục `helm/`. Bạn có thể sử dụng các chart này để thực hành các lệnh Helm trên hệ thống local hoặc trong bất kỳ môi trường cloud nào.

## Triển Khai Cloud

Trong các phần tiếp theo, những Helm chart này sẽ được triển khai lên môi trường cloud. Quy trình triển khai sẽ rất giống với triển khai local, với điểm khác biệt chính là dung lượng tăng lên của các Kubernetes cluster trên cloud.

## Kết Luận

Hướng dẫn này bao gồm tất cả các lệnh Helm thiết yếu để quản lý triển khai Kubernetes. Những lệnh này tạo thành nền tảng của quản lý Helm chart, từ khởi tạo ban đầu qua triển khai, cập nhật và bảo trì. Hãy giữ tài liệu tham khảo này bên cạnh khi làm việc với Helm để nhanh chóng ôn lại kiến thức của bạn.

## Tài Nguyên Bổ Sung

- Thực hành với các Helm chart được cung cấp trong GitHub repository
- Thử nghiệm với cả môi trường Kubernetes local và cloud
- Xem lại hướng dẫn này bất cứ khi nào bạn cần làm mới kiến thức về Helm

---

*Hướng dẫn này cung cấp cái nhìn tổng quan toàn diện về các lệnh Helm cho việc quản lý ứng dụng Kubernetes hiệu quả.*




FILE: 73-server-side-service-discovery-and-load-balancing.md


# Khám Phá Dịch Vụ và Cân Bằng Tải Phía Máy Chủ trong Kubernetes

## Tổng Quan

Tài liệu này giải thích sự khác biệt giữa các phương pháp khám phá dịch vụ và cân bằng tải phía client và phía server trong kiến trúc microservices, tập trung vào việc triển khai khám phá phía server sử dụng Kubernetes.

## Khám Phá và Cân Bằng Tải Phía Client (Phương Pháp Eureka Server)

### Cách Hoạt Động

Trong phương pháp phía client sử dụng Eureka Server:

1. **Đăng Ký Dịch Vụ**: Tất cả microservices tự đăng ký với Eureka Server trong quá trình khởi động
2. **Cơ Chế Heartbeat**: Microservices gửi heartbeat định kỳ để chứng minh trạng thái khỏe mạnh
3. **Khám Phá Dịch Vụ**: Khi một microservice cần giao tiếp với microservice khác, nó truy vấn Eureka Server để lấy các instance khả dụng
4. **Cân Bằng Tải**: Client microservice thực hiện cân bằng tải sử dụng Spring Cloud Load Balancer

### Ví Dụ Luồng Giao Tiếp

Xét tình huống microservice Accounts muốn giao tiếp với microservice Loans:

**Bước 1**: Các instance của microservice Loans đăng ký với Eureka Server trong quá trình khởi động, cung cấp thông tin như hostname, port number và thông tin instance

**Bước 2**: Microservice Accounts truy vấn Eureka Server để lấy thông tin chi tiết về microservice Loans

**Bước 3**: Eureka Server phản hồi với tất cả thông tin instance của microservice Loans khả dụng (ví dụ: hai địa chỉ IP)

**Bước 4**: Microservice Accounts thực hiện cân bằng tải sử dụng Spring Cloud Load Balancer và chuyển tiếp request đến một trong các instance được chọn

### Ưu Điểm

- **Kiểm Soát Hoàn Toàn**: Ứng dụng client có toàn quyền kiểm soát các chiến lược cân bằng tải
- **Nhiều Chiến Lược**: Spring Cloud Load Balancer cung cấp nhiều thuật toán cân bằng tải khác nhau
- **Linh Hoạt**: Developer có thể tùy chỉnh hành vi cân bằng tải

### Nhược Điểm

- **Bảo Trì Thủ Công**: Developer phải bảo trì Eureka Server một cách thủ công
- **Chi Phí Cấu Hình**: Yêu cầu tạo ứng dụng Spring Boot và chuyển đổi nó thành Eureka Server
- **Thay Đổi Microservice**: Tất cả microservices cần thay đổi cấu hình để kết nối với Eureka Server
- **Gánh Nặng Phát Triển**: Trách nhiệm cấu hình và bảo trì thêm cho developer

## Khám Phá và Cân Bằng Tải Phía Server (Phương Pháp Kubernetes)

### Yêu Cầu Tiên Quyết

Phương pháp này **chỉ** có thể được sử dụng khi triển khai microservices lên Kubernetes cluster.

### Cách Hoạt Động

Trong phương pháp phía server sử dụng Kubernetes:

1. **Khám Phá Tự Động**: Kubernetes Discovery Server tự động giám sát tất cả các instance ứng dụng
2. **Không Cần Đăng Ký Rõ Ràng**: Ứng dụng không cần tự đăng ký
3. **Tích Hợp Kubernetes API**: Discovery server sử dụng Kubernetes APIs để lấy thông tin dịch vụ và endpoint
4. **Cân Bằng Tải Minh Bạch**: Cân bằng tải xảy ra ở cấp độ Kubernetes service

### Ví Dụ Luồng Giao Tiếp

Sử dụng cùng tình huống microservice Accounts và Loans:

**Bước 1**: Kubernetes Discovery Server truy vấn Kubernetes API để lấy tất cả thông tin instance của microservice Loans (không cần đăng ký rõ ràng)

**Bước 2**: Microservice Accounts gửi request trực tiếp đến Kubernetes service sử dụng tên service làm hostname/DNS

**Bước 3**: Kubernetes service làm việc với Discovery Server để thực hiện cân bằng tải

**Bước 4**: Request được chuyển tiếp đến một trong các instance của microservice Loans

### Điểm Khác Biệt Chính So Với Phương Pháp Phía Client

- **Không Có Discovery Client**: Ứng dụng client không kết nối với bất kỳ discovery server nào
- **Tên Service Làm Endpoint**: Request được gửi đến Kubernetes service sử dụng tên service
- **Cân Bằng Tải Phía Server**: Cân bằng tải xảy ra trong Kubernetes cluster
- **Không Cần Cấu Hình Phía Client**: Microservice Accounts không xử lý cân bằng tải hoặc khám phá dịch vụ

### Ưu Điểm

- **Không Cần Bảo Trì**: Không cần bảo trì Eureka Server thủ công
- **Không Thay Đổi Cấu Hình**: Microservices không yêu cầu cấu hình kết nối discovery server
- **Khám Phá Tự Động**: Kubernetes Discovery Server tự động lấy các instance microservice đang chạy
- **Kiến Trúc Đơn Giản**: Giảm độ phức tạp trong code microservice

### Nhược Điểm

- **Không Kiểm Soát Cân Bằng Tải**: Developer và ứng dụng client không có quyền kiểm soát chiến lược cân bằng tải
- **Phụ Thuộc Kubernetes**: Thuật toán cân bằng tải được quyết định hoàn toàn bởi Kubernetes cluster
- **Tùy Chỉnh Hạn Chế**: Không thể triển khai các chiến lược cân bằng tải tùy chỉnh

## Bảng So Sánh Tổng Kết

| Khía Cạnh | Phía Client (Eureka) | Phía Server (Kubernetes) |
|-----------|---------------------|--------------------------|
| Đăng Ký Dịch Vụ | Yêu cầu đăng ký thủ công | Tự động qua Kubernetes API |
| Kiểm Soát Cân Bằng Tải | Kiểm soát đầy đủ với nhiều chiến lược | Không kiểm soát, do Kubernetes xử lý |
| Bảo Trì | Yêu cầu bảo trì Eureka Server | Không cần bảo trì server thêm |
| Cấu Hình | Cấu hình microservice rộng rãi | Cấu hình tối thiểu |
| Yêu Cầu Triển Khai | Bất kỳ môi trường nào | Chỉ Kubernetes cluster |
| Gánh Nặng Developer | Cao hơn | Thấp hơn |

## Phương Pháp Triển Khai

### Chuyển Đổi Sang Khám Phá Phía Server

Khi chuyển sang khám phá dịch vụ và cân bằng tải phía server trong Kubernetes:

1. Loại bỏ Eureka Server khỏi mạng microservice
2. Triển khai microservices lên Kubernetes cluster
3. Tạo Kubernetes services (các loại ClusterIP hoặc LoadBalancer)
4. Sử dụng tên service làm DNS endpoint cho giao tiếp giữa các service
5. Để Kubernetes tự động xử lý khám phá dịch vụ và cân bằng tải

## Lựa Chọn Phương Pháp Phù Hợp

Không có phương pháp nào "tốt" hay "xấu" một cách tuyệt đối. Lựa chọn phụ thuộc vào:

- **Môi Trường Triển Khai**: Kubernetes bắt buộc cho phương pháp phía server
- **Yêu Cầu Kiểm Soát**: Nhu cầu về các chiến lược cân bằng tải tùy chỉnh
- **Tài Nguyên Phát Triển**: Năng lực của team trong việc bảo trì cơ sở hạ tầng bổ sung
- **Yêu Cầu Kinh Doanh**: Nhu cầu cụ thể của tổ chức và các ràng buộc

Cả hai phương pháp đều hợp lệ và có các trường hợp sử dụng riêng. Hiểu cả hai giúp bạn đưa ra quyết định kiến trúc có cơ sở cho hệ sinh thái microservices của mình.

## Kết Luận

Khám phá dịch vụ và cân bằng tải phía server trong Kubernetes cung cấp một phương pháp đơn giản hóa cho giao tiếp microservice bằng cách loại bỏ nhu cầu đăng ký dịch vụ rõ ràng và cân bằng tải phía client. Mặc dù nó giảm gánh nặng cho developer và chi phí bảo trì, nó cũng hạn chế quyền kiểm soát các chiến lược cân bằng tải. Chìa khóa là hiểu cả hai phương pháp và chọn phương pháp phù hợp nhất với yêu cầu cụ thể của bạn.




FILE: 74-setting-up-discovery-server-in-kubernetes-with-spring-cloud.md


# Thiết Lập Discovery Server trong Kubernetes với Spring Cloud Kubernetes

## Tổng Quan

Hướng dẫn này giải thích cách thiết lập service discovery và load balancing phía server trong Kubernetes cluster sử dụng Spring Cloud Kubernetes. Mặc định, Kubernetes không bao gồm server để service discovery và registration, vì vậy chúng ta cần tự cấu hình.

## Yêu Cầu Trước

- Kubernetes cluster (local hoặc cloud)
- Hiểu biết cơ bản về Spring Boot và microservices
- Quen thuộc với các khái niệm Kubernetes (pods, services, deployments)

## Giới Thiệu về Spring Cloud Kubernetes

Spring Cloud Kubernetes là một dự án Spring Cloud giúp triển khai service discovery và load balancing trong môi trường Kubernetes. Khác với các triển khai truyền thống có thể sử dụng Eureka Server, Kubernetes yêu cầu một phương pháp tiếp cận chuyên biệt.

## Bắt Đầu

### Tài Liệu Chính Thức

Nhóm Spring Cloud Kubernetes đã xuất bản một blog vào năm 2021 giới thiệu các khả năng service discovery và registration. Blog này cung cấp một file Kubernetes manifest làm nền tảng để thiết lập Discovery Server.

### Cấu Trúc Dự Án

Tạo cấu trúc thư mục như sau:
```
section_17/
  └── Kubernetes/
      └── kubernetes-discoveryserver.yaml
```

## Cấu Hình Kubernetes Manifest

### Tạo File Manifest

Tạo file có tên `kubernetes-discoveryserver.yaml` với cấu trúc sau:

### 1. API Version và Kind

```yaml
apiVersion: v1
kind: List
```

`kind: List` cho phép bạn tạo nhiều đối tượng Kubernetes trong phần `items`.

### 2. Cấu Hình Service

```yaml
- apiVersion: v1
  kind: Service
  metadata:
    labels:
      app: spring-cloud-kubernetes-discoveryserver
    name: spring-cloud-kubernetes-discoveryserver
  spec:
    ports:
    - port: 80
      targetPort: 8761
    type: ClusterIP
```

**Điểm Chính:**
- **Port 80**: Cổng bên ngoài được expose cho các microservices khác
- **TargetPort 8761**: Cổng nội bộ nơi Discovery Server chạy
- **Service Type**: ClusterIP (không xung đột với Keycloak service trên port 80)

### 3. Service Account

```yaml
- apiVersion: v1
  kind: ServiceAccount
  metadata:
    name: spring-cloud-kubernetes-discoveryserver
```

Service account này sẽ được deployment Discovery Server sử dụng.

### 4. Role Binding

```yaml
- apiVersion: rbac.authorization.k8s.io/v1
  kind: RoleBinding
  metadata:
    name: spring-cloud-kubernetes-discoveryserver:view
  roleRef:
    kind: Role
    name: namespace-reader
  subjects:
  - kind: ServiceAccount
    name: spring-cloud-kubernetes-discoveryserver
```

Điều này liên kết role `namespace-reader` với service account.

### 5. Cấu Hình Role

```yaml
- apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    name: namespace-reader
  rules:
  - apiGroups: [""]
    resources:
    - services
    - endpoints
    - pods
    verbs:
    - get
    - list
    - watch
```

**Cập Nhật Quan Trọng:** Blog gốc từ 2021 chỉ bao gồm `services` và `endpoints`, nhưng dựa trên yêu cầu hiện tại, bạn phải thêm `pods` vào danh sách resources để Discovery Server hoạt động đúng cách.

### 6. Cấu Hình Deployment

```yaml
- apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: spring-cloud-kubernetes-discoveryserver-deployment
  spec:
    selector:
      matchLabels:
        app: spring-cloud-kubernetes-discoveryserver
    template:
      metadata:
        labels:
          app: spring-cloud-kubernetes-discoveryserver
      spec:
        serviceAccountName: spring-cloud-kubernetes-discoveryserver
        containers:
        - name: spring-cloud-kubernetes-discoveryserver
          image: springcloud/spring-cloud-kubernetes-discoveryserver:3.0.4
          imagePullPolicy: IfNotPresent
```

**Cập Nhật Chính:**
- **Image Tag**: Sử dụng `3.0.4` thay vì phiên bản cũ `2.1.0-M3`
- **Image Pull Policy**: `IfNotPresent` - chỉ pull image nếu không có sẵn trong local

### 7. Cấu Hình Health Probes

#### Readiness Probe

```yaml
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8761
            initialDelaySeconds: 100
            periodSeconds: 30
```

#### Liveness Probe

```yaml
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8761
            initialDelaySeconds: 100
            periodSeconds: 30
```

**Tham Số Cấu Hình Quan Trọng:**

- **initialDelaySeconds: 100**: Kubernetes đợi 100 giây trước khi thực hiện health check đầu tiên. Điều này ngăn việc restart sớm trong quá trình khởi động ứng dụng.
- **periodSeconds: 30**: Sau lần check đầu tiên, Kubernetes thực hiện health check mỗi 30 giây.

**Tại Sao Các Giá Trị Này Quan Trọng:**

Nếu không có các cấu hình này, Kubernetes sử dụng giá trị mặc định (thường là 10-15 giây), có thể gây ra:
- Các lần restart sớm
- Vòng lặp restart liên tục
- Triển khai thất bại

Nếu 100 giây không đủ cho môi trường của bạn, tăng lên 150 hoặc 200 giây.

### 8. Cấu Hình Port

```yaml
          ports:
          - containerPort: 8761
```

## Hiểu về Health Probes

### Readiness Probe
- Xác định khi nào pod sẵn sàng nhận traffic
- Sử dụng endpoint: `/actuator/health/readiness`
- Nếu thất bại, Kubernetes ngừng định tuyến traffic đến pod

### Liveness Probe
- Xác định ứng dụng có đang chạy đúng cách không
- Sử dụng endpoint: `/actuator/health/liveness`
- Nếu thất bại, Kubernetes restart pod

## Ưu Điểm của Kubernetes so với Docker Compose

Mặc dù chúng ta định nghĩa health probes cho Discovery Server, nó không thực sự cần thiết cho tất cả microservices trong Kubernetes bởi vì:

1. **Tự Động Restart**: Kubernetes tự động restart các pod bị lỗi
2. **Quản Lý Replica**: Kubernetes duy trì số lượng replica mong muốn
3. **Tự Phục Hồi**: Kubernetes liên tục giám sát và phục hồi cluster

Trong môi trường Docker Compose, containers không tự động restart, làm cho health checks trở nên quan trọng hơn.

## Chi Tiết Docker Image

Nhóm Spring Cloud Kubernetes cung cấp Docker image đã được build sẵn:
- **Image**: `springcloud/spring-cloud-kubernetes-discoveryserver`
- **Tag Khuyến Nghị**: `3.0.4` (phiên bản ổn định)
- **Docker Hub**: Có sẵn tại Docker Hub để kiểm tra phiên bản

Bạn không cần build ứng dụng Discovery Server của riêng mình - chỉ cần sử dụng image được cung cấp.

## Các Bước Triển Khai

1. Tạo file `kubernetes-discoveryserver.yaml` với tất cả cấu hình
2. Apply manifest:
   ```bash
   kubectl apply -f kubernetes-discoveryserver.yaml
   ```
3. Xác minh deployment:
   ```bash
   kubectl get pods
   kubectl get services
   ```

## Xử Lý Sự Cố

### Pod Liên Tục Restart
- Tăng `initialDelaySeconds` lên 150 hoặc 200
- Kiểm tra logs của pod: `kubectl logs <pod-name>`

### Service Không Truy Cập Được
- Xác minh service type là ClusterIP
- Kiểm tra ánh xạ port (80 → 8761)

### Vấn Đề Role Binding
- Đảm bảo resource `pods` được bao gồm trong Role
- Xác minh service account binding

## Best Practices (Thực Hành Tốt Nhất)

1. **Luôn sử dụng stable image tags** thay vì phiên bản development
2. **Cấu hình thời gian health probe phù hợp** dựa trên thời gian khởi động ứng dụng
3. **Sử dụng ClusterIP cho internal services** để tránh xung đột port
4. **Bao gồm pods trong Role resources** cho các phiên bản Kubernetes hiện tại
5. **Giám sát trạng thái pod** sau khi deploy để đảm bảo khởi động thành công

## Kết Luận

Thiết lập Discovery Server trong Kubernetes sử dụng Spring Cloud Kubernetes khá đơn giản với cấu hình phù hợp. Điều quan trọng là đảm bảo:
- Quyền role đúng (bao gồm pods)
- Thời gian health probe phù hợp
- Phiên bản Docker image ổn định mới nhất

Trong các bước tiếp theo, bạn sẽ apply manifest file này vào Kubernetes cluster và xác minh Discovery Server đang chạy đúng cách.

## Tài Nguyên Bổ Sung

- [Tài Liệu Spring Cloud Kubernetes](https://spring.io/projects/spring-cloud-kubernetes)
- [Tài Liệu Chính Thức Kubernetes](https://kubernetes.io/docs/)
- [Spring Boot Actuator Health Endpoints](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)




FILE: 75-deploying-discovery-server-to-kubernetes-without-helm.md


# Triển Khai Discovery Server lên Kubernetes Không Sử Dụng Helm

## Tổng Quan

Hướng dẫn này trình bày cách triển khai Discovery Server lên Kubernetes cluster bằng cách sử dụng các file manifest của Kubernetes thay vì Helm charts. Chúng ta sẽ tìm hiểu tại sao phương pháp này phù hợp cho thành phần này và thực hiện quy trình triển khai từng bước.

## Tại Sao Không Sử Dụng Helm Charts?

Có hai lý do chính để chọn sử dụng file manifest thay vì Helm charts cho việc triển khai Discovery Server:

### 1. Thiết Lập Một Lần
Discovery Server là một thiết lập một lần duy nhất bên trong Kubernetes cluster của bạn. Không giống như các microservices cần cập nhật và thay đổi cấu hình thường xuyên, Discovery Server không cần nhiều sửa đổi theo thời gian. Đối với các hoạt động một lần như vậy, việc chạy các file manifest thủ công là hoàn toàn chấp nhận được và đơn giản.

### 2. Thiếu Helm Charts Từ Cộng Đồng
Hiện tại, chưa có Helm chart nào được phát triển bởi cộng đồng Helm, bao gồm cả Bitnami, dành riêng cho Discovery Server. Mặc dù có thể tích hợp các file manifest vào một Helm chart tùy chỉnh (như Helm chart của easybank), nhưng công sức cần thiết sẽ rất lớn và không xứng đáng cho một thành phần chỉ cần triển khai một lần.

## Quy Trình Triển Khai

### Yêu Cầu Trước
- Quyền truy cập vào Kubernetes cluster
- Công cụ kubectl CLI đã được cài đặt và cấu hình
- File manifest của Discovery Server (`kubernetes-discoveryserver.yaml`)

### Lệnh Triển Khai

Để triển khai Discovery Server, thực thi lệnh sau từ terminal của bạn:

```bash
kubectl apply -f kubernetes-discoveryserver.yaml
```

### Các Tài Nguyên Được Tạo

Lệnh này sẽ tạo các tài nguyên Kubernetes sau:
- **Service**: Expose Discovery Server trong cluster
- **Service Account**: Cung cấp định danh cho các pod của Discovery Server
- **Role Binding**: Liên kết role với service account
- **Role**: Định nghĩa quyền cho Discovery Server
- **Deployment**: Quản lý vòng đời pod của Discovery Server

## Các Bước Xác Minh

### 1. Truy Cập Kubernetes Dashboard
Điều hướng đến Kubernetes dashboard để giám sát trạng thái triển khai.

### 2. Kiểm Tra Trạng Thái Pod
- Vào phần Pods
- Tìm pod của Discovery Server
- Xác minh rằng nó đang ở trạng thái running (chỉ báo màu xanh)

### 3. Xem Logs
Mở logs của pod để xác nhận khởi động thành công:
- Discovery Server nên khởi động trong khoảng 20 giây
- Tìm các log từ Spring Boot xác nhận đây là ứng dụng Spring Boot
- Xác minh không có thông báo lỗi

### Kết Quả Log Mong Đợi
Bạn sẽ thấy các log từ Spring Framework cho biết Discovery Server đã khởi động thành công. Điều này xác nhận rằng:
- Triển khai hoạt động chính xác
- Discovery Server là một ứng dụng Spring Boot
- Tất cả các thành phần (deployment, pods, replica sets) đều khỏe mạnh

## Chuẩn Bị Code Microservices

### Di Chuyển Code
Sau khi triển khai thành công Discovery Server, chuẩn bị code microservices của bạn:

1. **Sao Chép Microservices từ Section 14**
   - accounts
   - cards
   - config server
   - gateway server
   - loans
   - message

2. **Loại Trừ Các Mục Sau**
   - Eureka Server (đang được thay thế bởi Kubernetes Discovery Server)
   - Các file Docker Compose (không cần thiết cho triển khai Kubernetes)

3. **Sao Chép Thư Mục Helm từ Section 16**
   - Thư mục này sẽ cần sửa đổi để loại bỏ các tham chiếu đến Eureka Server

### Thiết Lập Môi Trường Phát Triển

1. Mở thư mục section_17 trong IntelliJ IDEA
2. Load các project như Maven projects
3. Bật annotation processing khi được nhắc
4. Build các project

## Các Bước Tiếp Theo

Sau khi triển khai thành công Discovery Server:

1. **Cập Nhật Code Microservices**
   - Loại bỏ các dependency và configuration liên quan đến Eureka
   - Thêm tích hợp với Kubernetes Discovery Server

2. **Sửa Đổi Helm Charts**
   - Loại bỏ các tham chiếu đến Eureka Server
   - Cập nhật cấu hình service discovery

3. **Xác Minh Trạng Thái Cluster**
   - Đảm bảo tất cả các deployment hiển thị trạng thái màu xanh
   - Xác nhận pods và replica sets đều khỏe mạnh
   - Kiểm tra rằng Discovery Server đang chạy không có vấn đề

## Kết Luận

Discovery Server hiện đã được triển khai thành công và đang chạy trong Kubernetes cluster của bạn. Với tất cả các thành phần hiển thị trạng thái màu xanh (deployment, pods, replica sets), nền tảng đã sẵn sàng để triển khai và cấu hình các microservices của bạn hoạt động với cơ chế discovery tích hợp sẵn của Kubernetes.

## Các Điểm Chính Cần Nhớ

- Discovery Server là thành phần thiết lập một lần
- Các file manifest của Kubernetes đủ cho việc triển khai này
- Discovery Server chạy như một ứng dụng Spring Boot
- Kubernetes cung cấp khả năng service discovery tích hợp sẵn
- Các microservices sẽ được cập nhật để sử dụng Kubernetes Discovery Server thay vì Eureka




FILE: 76-migrating-microservices-from-eureka-to-kubernetes-discovery.md


# Chuyển đổi Microservices từ Eureka sang Kubernetes Discovery Server

## Tổng quan

Hướng dẫn này trình bày quy trình chuyển đổi các microservices Spring Boot từ Netflix Eureka Server sang Kubernetes Discovery Server tích hợp sẵn. Việc di chuyển này loại bỏ nhu cầu có một thành phần service discovery riêng biệt bằng cách tận dụng cơ chế service discovery có sẵn trong Kubernetes.

## Yêu cầu trước

- Kiến trúc microservices Spring Boot
- Kubernetes cluster
- Maven để quản lý dependencies
- Hiểu biết cơ bản về Spring Cloud và Kubernetes

## Thay đổi Kiến trúc

Khi chuyển từ Eureka sang Kubernetes Discovery:
- **Eureka Server**: Thành phần service registry riêng biệt (được loại bỏ)
- **Kubernetes Discovery**: DNS và service discovery tích hợp sẵn trong Kubernetes (native)
- **Service Communication**: Sử dụng tên service của Kubernetes thay vì tên application của Eureka

## Các bước Di chuyển

### 1. Accounts Microservice

#### Cập nhật Dependencies (pom.xml)

**Xóa dependency Eureka:**
```xml
<!-- Xóa dependency này -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

**Thêm dependency Kubernetes Discovery:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-discovery-client</artifactId>
</dependency>
```

**Cập nhật Docker image tag:**
```xml
<tag>s17</tag>
```

#### Sửa Import HTTP Status

Sau khi xóa dependencies Eureka, cập nhật import HTTP status trong `CustomerController`:
```java
import org.apache.hc.core5.http.HttpStatus;
```

#### Kích hoạt Discovery Client

Thêm annotation vào class application chính (`AccountsApplication`):
```java
@EnableDiscoveryClient
public class AccountsApplication {
    // ... code hiện có
}
```

#### Cập nhật Cấu hình Application (application.yml)

**Xóa tất cả cấu hình Eureka:**
- Tìm kiếm và xóa tất cả các properties `eureka.*`

**Thêm cấu hình Kubernetes Discovery:**
```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        all-namespaces: true
```

**Mục đích của `all-namespaces: true`:**
- Cho phép service discovery trên nhiều namespaces của Kubernetes
- Cần thiết khi microservices được triển khai trong các namespaces khác nhau
- Hỗ trợ sử dụng namespace mặc định nhưng cung cấp tính linh hoạt

#### Cập nhật Feign Clients

**Thay đổi CardsFeignClient và LoansFeignClient:**

Vấn đề với Kubernetes Discovery là không giống Eureka, không có tích hợp service registry tự động. Chúng ta cần cung cấp URL service một cách rõ ràng.

**Ví dụ CardsFeignClient:**
```java
@FeignClient(name = "cards", url = "http://cards:9000")
public interface CardsFeignClient {
    // ... các methods hiện có
}
```

**Ví dụ LoansFeignClient:**
```java
@FeignClient(name = "loans", url = "http://loans:8090")
public interface LoansFeignClient {
    // ... các methods hiện có
}
```

**Điểm chính:**
- `name`: Định danh application (giữ nguyên để nhất quán)
- `url`: Tên service và port của Kubernetes
- Định dạng: `http://<tên-service>:<port>`
- Chỉ hoạt động bên trong Kubernetes cluster
- Để test local, sử dụng URLs `localhost`

**Lưu ý về Load Balancing:**
- Feign client chuyển tiếp requests trực tiếp đến Kubernetes service
- Load balancing được xử lý bởi Kubernetes service, không phải client
- Không có load balancing phía client như với Eureka

### 2. Cards Microservice

#### Cập nhật Dependencies (pom.xml)

Thay thế dependency Eureka bằng Kubernetes Discovery:
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-discovery-client</artifactId>
</dependency>
```

Cập nhật tag: `s14` → `s17`

#### Kích hoạt Discovery Client

Thêm annotation vào `CardsApplication`:
```java
@EnableDiscoveryClient
public class CardsApplication {
    // ... code hiện có
}
```

#### Cập nhật Cấu hình Application (application.yml)

Xóa tất cả properties Eureka và thêm:
```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        all-namespaces: true
```

**Lưu ý:** Cards microservice không có tích hợp Feign client, nên không cần thay đổi thêm.

### 3. Loans Microservice

#### Cập nhật Cấu hình Application (application.yml)

Thêm cấu hình Kubernetes Discovery:
```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        all-namespaces: true
```

#### Cập nhật Dependencies (pom.xml)

Xóa dependency Eureka và thêm Kubernetes Discovery client:
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-discovery-client</artifactId>
</dependency>
```

Cập nhật tag: `s14` → `s17`

#### Kích hoạt Discovery Client

Thêm annotation vào `LoansApplication`:
```java
@EnableDiscoveryClient
public class LoansApplication {
    // ... code hiện có
}
```

### 4. Config Server

#### Thay đổi Tối thiểu

Config Server không tích hợp với Eureka, nên chỉ cần thay đổi tối thiểu:
- Cập nhật Docker image tag lên `s17` để nhất quán
- Không cần thay đổi dependency
- Không cần thay đổi cấu hình

### 5. Message Microservice

#### Thay đổi Tối thiểu

Message microservice cũng không có tích hợp Eureka:
- Cập nhật Docker image tag: `s14` → `s17`
- Không cần thay đổi khác

### 6. Gateway Server

**Lưu ý:** Các thay đổi cho Gateway server sẽ được trình bày trong phần/bài giảng tiếp theo.

## Tóm tắt Thay đổi

| Microservice | Dependencies | Cấu hình | Annotations | Feign Clients |
|--------------|-------------|-----------|-------------|---------------|
| Accounts | ✓ Đã cập nhật | ✓ Đã cập nhật | ✓ @EnableDiscoveryClient | ✓ Đã thêm URLs |
| Cards | ✓ Đã cập nhật | ✓ Đã cập nhật | ✓ @EnableDiscoveryClient | N/A |
| Loans | ✓ Đã cập nhật | ✓ Đã cập nhật | ✓ @EnableDiscoveryClient | N/A |
| Config Server | Chỉ tag | Không đổi | Không đổi | N/A |
| Message | Chỉ tag | Không đổi | Không đổi | N/A |
| Gateway | Đang chờ | Đang chờ | Đang chờ | N/A |

## Sự khác biệt chính: Eureka vs Kubernetes Discovery

### Eureka Discovery
- Yêu cầu triển khai Eureka Server riêng
- Load balancing phía client
- Đăng ký application với Eureka Server
- Service discovery thông qua Eureka client
- Hoạt động ngoài Kubernetes

### Kubernetes Discovery
- Sử dụng DNS tích hợp của Kubernetes
- Load balancing phía server (thông qua Kubernetes Service)
- Không cần discovery server riêng
- Service discovery thông qua Kubernetes API
- Chỉ hoạt động trong Kubernetes cluster

## Cân nhắc về Testing

### Trong Kubernetes Cluster
- Sử dụng tên service của Kubernetes (ví dụ: `http://cards:9000`)
- Phân giải DNS tự động
- Load balancing thông qua Kubernetes Service

### Phát triển Local (Ngoài Kubernetes)
- Tên service Kubernetes sẽ không phân giải được
- Sử dụng `localhost` hoặc URLs host thực tế
- Cân nhắc sử dụng profiles cho các môi trường khác nhau

## Best Practices

1. **Chiến lược Namespace**: Sử dụng `all-namespaces: true` cho cross-namespace discovery
2. **Đặt tên Service**: Giữ tên Kubernetes service nhất quán với tên application
3. **Cấu hình Port**: Ghi chú rõ ràng các ports của service
4. **Quản lý Tag**: Giữ đồng bộ Docker image tags giữa các services
5. **Testing**: Test cả trong cluster và môi trường phát triển local

## Xử lý Sự cố

### Các vấn đề thường gặp

**Vấn đề**: Feign client không thể phân giải tên service
- **Giải pháp**: Đảm bảo service đã được triển khai trong Kubernetes và URL được chỉ định đúng

**Vấn đề**: Lỗi import HTTP status sau khi xóa Eureka
- **Giải pháp**: Cập nhật import thành `org.apache.hc.core5.http.HttpStatus`

**Vấn đề**: Service discovery thất bại giữa các namespaces
- **Giải pháp**: Xác minh `all-namespaces: true` đã được cấu hình

## Các bước tiếp theo

- Hoàn thành di chuyển Gateway Server
- Triển khai các microservices đã cập nhật lên Kubernetes
- Xác minh giao tiếp giữa các services
- Giám sát hiệu suất service discovery

## Kết luận

Di chuyển từ Eureka sang Kubernetes Discovery đơn giản hóa kiến trúc microservices bằng cách tận dụng các khả năng tích hợp sẵn của Kubernetes. Điều này loại bỏ chi phí vận hành việc duy trì một service registry riêng biệt trong khi vẫn cung cấp service discovery mạnh mẽ trong hệ sinh thái Kubernetes.




FILE: 77-migrating-gateway-server-to-kubernetes-discovery.md


# Chuyển Gateway Server sang Kubernetes Discovery

## Tổng Quan

Bài giảng này hướng dẫn cách chuyển đổi Gateway Server từ Eureka Discovery sang Kubernetes Discovery Server, bao gồm cập nhật các dependency cần thiết, thay đổi cấu hình và chuẩn bị triển khai.

## Bước 1: Cập Nhật Maven Dependencies

### Xóa Eureka Client Dependency

Mở file `pom.xml` và tìm dependency Eureka client cần được thay thế.

### Thêm Kubernetes Discovery Client

Thay thế dependency Eureka bằng Spring Cloud Kubernetes Discovery Client:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-client-discovery</artifactId>
</dependency>
```

### Cập Nhật Version Tag

Tìm tag `s14` và cập nhật thành `s17`:

```xml
<tag>s17</tag>
```

Sau khi thực hiện các thay đổi này, tải lại Maven changes và thực hiện build.

## Bước 2: Cập Nhật Gateway Server Main Class

Điều hướng đến main class của Gateway Server (`GatewayserverApplication`).

### Thêm Discovery Client Annotation

Thêm annotation `@EnableDiscoveryClient` để kích hoạt service discovery:

```java
@EnableDiscoveryClient
@SpringBootApplication
public class GatewayserverApplication {
    // ...
}
```

### Cập Nhật URI Routing Configurations

#### Cấu Hình Hiện Tại (Dựa trên Eureka)

Cấu hình routing hiện tại sử dụng load balancer URIs:
- `lb://ACCOUNTS`
- `lb://LOANS`
- `lb://CARDS`

Tiền tố `lb` chỉ định Spring Cloud Load Balancer, thực hiện load balancing phía client tại Gateway Server.

#### Cấu Hình Mới (Dựa trên Kubernetes)

Vì chúng ta không còn sử dụng Eureka nữa, hãy cập nhật các URI để sử dụng URL service trực tiếp:

**Accounts Service:**
```
http://accounts:8080
```

**Loans Service:**
```
http://loans:8090
```

**Cards Service:**
```
http://cards:9000
```

**Lợi Ích Chính:** Các cấu hình này sử dụng tên service của Kubernetes (accounts, loans, cards) mà không cần hardcode hostname hoặc domain name. Miễn là các microservices được triển khai với tên service khớp, tích hợp Gateway Server sẽ hoạt động liền mạch.

## Bước 3: Cập Nhật Cấu Hình application.yml

### Xóa Các Properties Của Eureka

Xóa các properties liên quan đến Eureka server sau:

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
          lowerCaseServiceId: true
```

### Thêm Kubernetes Discovery Properties

Thêm các properties đặc thù cho Kubernetes:

```yaml
spring:
  cloud:
    kubernetes:
      discovery:
        enabled: true
        all-namespaces: true
    discovery:
      client:
        health-indicator:
          enabled: false
```

#### Giải Thích Các Properties

**`spring.cloud.kubernetes.discovery.enabled: true`**
- Yêu cầu Gateway Server tận dụng Kubernetes discovery server để định tuyến request đến các microservices (accounts, cards, loans)

**`spring.cloud.kubernetes.discovery.all-namespaces: true`**
- Kích hoạt service discovery trên tất cả các namespace của Kubernetes

**`spring.cloud.discovery.client.health-indicator.enabled: false`**
- Vô hiệu hóa health indicator bean mặc định
- **Tại sao cần thiết:** Điều này ngăn chặn một vấn đề đã biết khi thư viện Kubernetes discovery client không thể tạo bean cần thiết
- **Trạng thái:** Đây là giải pháp tạm thời cho một issue đang mở trên GitHub của dự án Spring Cloud Kubernetes
- **Tương lai:** Property này có thể được xóa bỏ khi issue được giải quyết bởi team Spring Cloud Kubernetes

> **Lưu ý:** Các properties bổ sung này được yêu cầu đặc biệt cho Gateway Server vì nó hoạt động như một edge server chịu trách nhiệm xử lý tất cả traffic đến.

## Bước 4: Build và Deploy

### Tạo Docker Images

Tạo Docker images cho tất cả microservices với tag `s17`:

```bash
docker build -t <service-name>:s17 .
```

Điều này sẽ được thực hiện cho tất cả các microservices.

### Chuẩn Bị Kubernetes Cluster

Thiết lập Kubernetes cluster với tất cả các thành phần cần thiết:
- Apache Kafka
- Keycloak
- Grafana
- Prometheus

### Cập Nhật Helm Charts

Cập nhật Helm charts của Easy Bank với tag name mới nhất (`s17`):

```yaml
image:
  tag: s17
```

### Triển Khai Microservices

Sử dụng Helm charts đã cập nhật để triển khai tất cả microservices lên Kubernetes cluster:

```bash
helm upgrade --install <release-name> <chart-path>
```

## Tóm Tắt

Quá trình chuyển đổi này bao gồm:

1. ✅ Thay thế Eureka client dependency bằng Kubernetes discovery client
2. ✅ Cập nhật version tags từ s14 lên s17
3. ✅ Thêm annotation `@EnableDiscoveryClient`
4. ✅ Thay thế load balancer URIs bằng Kubernetes service URLs trực tiếp
5. ✅ Xóa các properties cấu hình đặc thù của Eureka
6. ✅ Thêm các properties cấu hình Kubernetes discovery
7. ✅ Áp dụng giải pháp tạm thời cho health indicator do issue đã biết
8. ✅ Build Docker images với tag s17
9. ✅ Cập nhật và triển khai Helm charts

## Những Điểm Chính Cần Nhớ

- **Không Load Balancing Phía Client:** Kubernetes xử lý service discovery và load balancing một cách native
- **Service Name Resolution:** Sử dụng tên service của Kubernetes để tích hợp liền mạch
- **Cấu Hình Edge Server:** Gateway Server yêu cầu các properties discovery bổ sung
- **Giải Pháp Tạm Thời Cho Issue Đã Biết:** Health indicator phải được tạm thời vô hiệu hóa
- **Triển Khai Dựa Trên Helm:** Đơn giản hóa việc triển khai microservices bằng Helm charts

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ xác minh việc triển khai và kiểm tra toàn bộ thiết lập microservices trong Kubernetes cluster.




FILE: 78-kubernetes-discovery-server-helm-charts-update-guide.md


# Hướng Dẫn Cập Nhật Helm Charts cho Kubernetes Discovery Server

## Tổng Quan

Hướng dẫn này cung cấp quy trình từng bước để cập nhật Helm charts của microservices nhằm di chuyển từ Netflix Eureka sang Spring Cloud Kubernetes Discovery Server. Bao gồm giải quyết vấn đề cấu hình, cập nhật dependencies và triển khai thành công lên Kubernetes cluster.

## Bối Cảnh

Các microservices trước đây sử dụng Netflix Eureka cho service discovery. Sau khi tạo Docker images với các thay đổi section 17 (được tag là `s17`), hệ thống cần chuyển sang service discovery gốc của Kubernetes sử dụng Spring Cloud Kubernetes Discovery Server.

## Trạng Thái Ban Đầu

### Các Thành Phần Đã Cài Đặt
- **Keycloak**: Quản lý danh tính và truy cập
- **Kafka**: Nền tảng streaming sự kiện
- **Grafana**: Giám sát và quan sát
- **Prometheus**: Thu thập metrics
- **Tất cả microservices**: Docker images được tag là `s17`

## Quy Trình Di Chuyển Từng Bước

### Giai Đoạn 1: Dọn Dẹp Helm Chart

#### 1.1 Xóa Folder Eureka Server
Điều hướng đến thư mục Helm charts và xóa folder Eureka server:

```bash
cd section17/helm/easybank-services
# Xóa folder eureka-server
```

#### 1.2 Cập Nhật Image Tags

Cập nhật `values.yaml` cho từng microservice:

**Accounts Microservice** (`accounts/values.yaml`):
```yaml
replicaCount: 2  # Để demo load balancing
image:
  tag: s17
```

**Cards Microservice** (`cards/values.yaml`):
```yaml
image:
  tag: s17
```

**Config Server** (`config-server/values.yaml`):
```yaml
image:
  tag: s17
```

**Gateway Server** (`gateway/values.yaml`):
```yaml
image:
  tag: s17
```

**Loans Microservice** (`loans/values.yaml`):
```yaml
image:
  tag: s17
```

**Message Microservice** (`message/values.yaml`):
```yaml
image:
  tag: s17
```

### Giai Đoạn 2: Cập Nhật Cấu Hình Môi Trường

#### 2.1 Xóa Dependencies Eureka

Cho mỗi folder môi trường (dev-env, prod-env, qa-env), chỉnh sửa `chart.yaml`:

**Trước:**
```yaml
dependencies:
  - name: eureka-server
    version: 1.0.0
    repository: file://../easybank-services/eureka-server
  # ... các dependencies khác
```

**Sau:**
```yaml
dependencies:
  # Đã xóa dependency eureka server
  # ... các dependencies khác
```

#### 2.2 Dọn Dẹp và Rebuild Dependencies

Xóa các file lock và rebuild dependencies cho từng môi trường:

```bash
cd helm/environments/dev-env
rm chart.lock
helm dependency build

cd ../prod-env
rm chart.lock
helm dependency build

cd ../qa-env
rm chart.lock
helm dependency build
```

### Giai Đoạn 3: Thử Triển Khai Lần Đầu

Triển khai các microservices:

```bash
cd environments
helm install easybank prod-env
```

**Kết quả**: Triển khai được khởi động nhưng các microservices không thể khởi động.

### Giai Đoạn 4: Xử Lý Sự Cố và Giải Quyết

#### 4.1 Xác Định Vấn Đề

Sau khi theo dõi Kubernetes dashboard, các microservices sau không khởi động được:
- Gateway Server
- Loans Microservice
- Cards Microservice
- Accounts Microservice

**Thông Báo Lỗi:**
```
Discovery server URL not provided
```

**Phân Tích Nguyên Nhân:**
Các microservices yêu cầu thuộc tính `spring.cloud.kubernetes.discovery.discovery-server-url` được cấu hình, nhưng nó không có trong Helm charts.

#### 4.2 Các Bước Giải Quyết

**Bước 1: Gỡ Cài Đặt Triển Khai Thất Bại**
```bash
helm uninstall easybank
```

**Bước 2: Cập Nhật Common Helm Chart**

Điều hướng đến Helm chart `easybank-common`:

**File: `templates/configmap.yaml`**

Thay thế cấu hình Eureka:
```yaml
EUREKA.CLIENT.SERVICE-URL.DEFAULT-ZONE: {{ .Values.eurekaServerURL }}
```

Bằng cấu hình Kubernetes Discovery:
```yaml
SPRING.CLOUD.KUBERNETES.DISCOVERY.DISCOVERY-SERVER-URL: {{ .Values.discoveryServerURL }}
```

**File: `templates/deployment.yaml`**

Cập nhật việc inject biến môi trường:

**Trước:**
```yaml
{{- if .Values.eurekaEnabled }}
- name: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
  valueFrom:
    configMapKeyRef:
      name: {{ .Values.name }}-configmap
      key: EUREKA_CLIENT_SERVICEURL_DEFAULTZONE
{{- end }}
```

**Sau:**
```yaml
{{- if .Values.discoveryEnabled }}
- name: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
  valueFrom:
    configMapKeyRef:
      name: {{ .Values.name }}-configmap
      key: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
{{- end }}
```

**Bước 3: Cập Nhật Values của Từng Microservice**

Cho mỗi microservice (accounts, cards, config-server, gateway, loans, message), cập nhật `values.yaml`:

**Trước:**
```yaml
eurekaEnabled: true
```

**Sau:**
```yaml
discoveryEnabled: true
```

**Bước 4: Cập Nhật Values Môi Trường**

Cho mỗi môi trường (dev-env, prod-env, qa-env), cập nhật `values.yaml`:

**Trước:**
```yaml
eurekaServerURL: http://eureka-server:8070/eureka/
```

**Sau:**
```yaml
discoveryServerURL: http://spring-cloud-kubernetes-discoveryserver:80
```

**Lưu ý:** Tên service `spring-cloud-kubernetes-discoveryserver` được định nghĩa trong file Kubernetes manifest dùng để triển khai Discovery Server.

### Giai Đoạn 5: Biên Dịch Lại

Biên dịch lại tất cả Helm charts sau các thay đổi:

**Microservices:**
```bash
cd helm/easybank-services/accounts
helm dependency build

cd ../cards
helm dependency build

cd ../config-server
helm dependency build

cd ../gateway
helm dependency build

cd ../loans
helm dependency build

cd ../message
helm dependency build
```

**Môi Trường:**
```bash
cd ../../environments/dev-env
helm dependency build

cd ../prod-env
helm dependency build

cd ../qa-env
helm dependency build
```

### Giai Đoạn 6: Xác Thực

Trước khi triển khai, xác thực các Helm charts:

```bash
cd environments
helm template easybank prod-env
```

**Các Điểm Xác Minh:**
- Kiểm tra biến môi trường Discovery Server URL có mặt
- Xác minh ConfigMap chứa thuộc tính đúng
- Đảm bảo không có lỗi biên dịch

**Xác Minh Đầu Ra Mẫu:**
Tìm biến môi trường trong deployment của loans microservice:
```yaml
env:
  - name: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
    valueFrom:
      configMapKeyRef:
        name: loans-configmap
        key: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
```

### Giai Đoạn 7: Triển Khai Cuối Cùng

Triển khai với cấu hình đã sửa:

```bash
cd environments
helm install easybank prod-env
```

### Giai Đoạn 8: Giám Sát

Theo dõi triển khai trong Kubernetes Dashboard:

1. **Kiểm Tra Config Server Trước:**
   - Config Server phải khởi động thành công trước các microservices khác
   - Xem lại logs để đảm bảo khởi động đúng

2. **Theo Dõi Các Microservices Khác:**
   - Accounts: Nên hiển thị 2 pods (replica count = 2)
   - Cards, Loans, Message, Gateway: Nên hiển thị 1 pod mỗi cái

3. **Đợi Khởi Động:**
   - Khởi động ban đầu có thể mất vài phút
   - Hạn chế tài nguyên trên hệ thống local có thể làm chậm quá trình

## Tài Liệu Tham Khảo Cấu Hình

### Các Thuộc Tính Quan Trọng

**Thuộc Tính Spring Cloud Kubernetes Discovery:**
```properties
spring.cloud.kubernetes.discovery.discovery-server-url=http://spring-cloud-kubernetes-discoveryserver:80
```

**Cấu Trúc ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.name }}-configmap
data:
  SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL: {{ .Values.discoveryServerURL }}
```

**Biến Môi Trường Deployment:**
```yaml
env:
  - name: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
    valueFrom:
      configMapKeyRef:
        name: {{ .Values.name }}-configmap
        key: SPRING_CLOUD_KUBERNETES_DISCOVERY_DISCOVERY_SERVER_URL
```

## Kiến Trúc Microservices

### Tổng Quan Thành Phần

| Thành Phần | Replicas | Mục Đích |
|-----------|----------|----------|
| Accounts | 2 | Dịch vụ tài khoản ngân hàng cốt lõi (load balanced) |
| Cards | 1 | Quản lý thẻ tín dụng/ghi nợ |
| Loans | 1 | Ứng dụng và quản lý khoản vay |
| Message | 1 | Spring Cloud Functions messaging |
| Config Server | 1 | Quản lý cấu hình tập trung |
| Gateway | 1 | API Gateway với OAuth2 Resource Server |
| Discovery Server | 1 | Spring Cloud Kubernetes service discovery |

### Các Dependencies của Service

```
Gateway Server
  ├─→ Discovery Server (service discovery)
  ├─→ Config Server (configuration)
  ├─→ Keycloak (authentication)
  └─→ Backend Services
        ├─→ Accounts (2 replicas)
        ├─→ Cards
        ├─→ Loans
        └─→ Message
```

## Hướng Dẫn Xử Lý Sự Cố

### Vấn Đề: Pods Không Khởi Động

**Triệu Chứng:**
- Pods vẫn ở trạng thái `Pending` hoặc `CrashLoopBackOff`
- Error logs hiển thị "Discovery server URL not provided"

**Giải Pháp:**
1. Xác minh `discoveryEnabled: true` trong tất cả file `values.yaml` của microservice
2. Kiểm tra `discoveryServerURL` được đặt trong `values.yaml` của môi trường
3. Xác nhận biến môi trường được inject đúng bằng `helm template`
4. Đảm bảo Discovery Server service đang chạy và có thể truy cập

### Vấn Đề: Helm Dependency Build Thất Bại

**Triệu Chứng:**
- Thông báo lỗi về dependencies xung đột
- Xung đột file Chart.lock

**Giải Pháp:**
1. Xóa các file `chart.lock` trong thư mục bị ảnh hưởng
2. Chạy lại `helm dependency build`
3. Xác minh dependencies trong `chart.yaml` được chỉ định đúng

### Vấn Đề: Config Server Không Khởi Động

**Triệu Chứng:**
- Các microservices khác đợi vô thời hạn
- Config Server pod hiển thị lỗi

**Giải Pháp:**
1. Kiểm tra logs của Config Server cho các lỗi cụ thể
2. Xác minh kết nối Git repository (nếu sử dụng Git backend)
3. Đảm bảo phân bổ tài nguyên đúng trong Kubernetes
4. Kiểm tra cấu hình ConfigMap và Secret

### Vấn Đề: Triển Khai Chậm Trên Hệ Thống Local

**Triệu Chứng:**
- Pods mất hơn 5 phút để khởi động
- Hiệu suất hệ thống giảm

**Giải Pháp:**
1. Tăng phân bổ tài nguyên Docker Desktop
2. Giảm số lượng replicas tạm thời
3. Triển khai các thành phần từng bước
4. Cân nhắc sử dụng Kubernetes cluster trên cloud

## Thực Hành Tốt Nhất

### 1. Triển Khai Từng Bước
- Triển khai Config Server trước và xác minh khởi động
- Triển khai Discovery Server tiếp theo
- Triển khai các microservices còn lại sau khi hạ tầng sẵn sàng

### 2. Quản Lý Helm Chart
- Luôn sử dụng `helm template` để xác thực trước khi cài đặt
- Giữ các file `chart.lock` trong version control (sau khi build thành công)
- Sử dụng quy ước đặt tên nhất quán qua các môi trường

### 3. Quản Lý Cấu Hình
- Sử dụng các file `values.yaml` theo môi trường
- Externalize cấu hình nhạy cảm vào Kubernetes Secrets
- Tài liệu hóa tất cả thuộc tính cấu hình tùy chỉnh

### 4. Giám Sát và Quan Sát
- Bật Prometheus metrics trên tất cả microservices
- Cấu hình Grafana dashboards để giám sát
- Thiết lập cảnh báo cho các lỗi service quan trọng
- Xem lại logs thường xuyên trong quá trình triển khai

### 5. Load Balancing
- Cấu hình nhiều replicas cho các services có lưu lượng cao
- Sử dụng load balancing của Kubernetes service
- Triển khai client-side load balancing với Spring Cloud LoadBalancer

## Tham Chiếu Lệnh Helm

### Các Lệnh Cơ Bản

```bash
# Cài đặt một release
helm install <release-name> <chart-path>

# Gỡ cài đặt một release
helm uninstall <release-name>

# Nâng cấp một release
helm upgrade <release-name> <chart-path>

# Liệt kê các releases
helm list

# Lấy trạng thái release
helm status <release-name>

# Xác thực template (dry-run)
helm template <release-name> <chart-path>

# Build dependencies
helm dependency build

# Liệt kê dependencies
helm dependency list
```

### Các Lệnh Debug

```bash
# Lấy rendered templates
helm get manifest <release-name>

# Lấy values được sử dụng cho release
helm get values <release-name>

# Hiển thị thông tin chart
helm show chart <chart-path>

# Hiển thị default values
helm show values <chart-path>
```

## Tài Nguyên Bổ Sung

### Tài Liệu Spring Cloud Kubernetes
- Tài liệu tham khảo chính thức Spring Cloud Kubernetes: [https://spring.io/projects/spring-cloud-kubernetes](https://spring.io/projects/spring-cloud-kubernetes)
- Hướng dẫn cấu hình Discovery Server

### Tài Liệu Helm
- Thực hành tốt nhất của Helm charts
- Quản lý dependency
- Template functions và pipelines

### Tài Nguyên Kubernetes
- Service discovery trong Kubernetes
- Quản lý ConfigMaps và Secrets
- Vòng đời Pod và xử lý sự cố

## Kết Luận

Di chuyển thành công từ Eureka sang Kubernetes Discovery Server yêu cầu:

1. **Cấu Hình Đúng**: Đặt thuộc tính `discovery-server-url` chính xác
2. **Cập Nhật Helm Chart**: Cập nhật templates và values qua tất cả charts
3. **Phương Pháp Có Hệ Thống**: Tuân theo quy trình triển khai có cấu trúc
4. **Xác Thực**: Sử dụng `helm template` để phát hiện vấn đề trước triển khai
5. **Giám Sát**: Theo dõi tích cực logs và metrics trong quá trình triển khai

Bằng cách làm theo hướng dẫn này, bạn có thể đảm bảo quá trình chuyển đổi mượt mà sang service discovery gốc của Kubernetes trong khi duy trì độ tin cậy và khả năng mở rộng của kiến trúc microservices của bạn.




FILE: 79-testing-kubernetes-discovery-server-with-microservices.md


# Kiểm Thử Kubernetes Discovery Server với Microservices

## Tổng Quan

Hướng dẫn này trình bày cách kiểm thử triển khai Kubernetes Discovery Server với các microservices Spring Boot, bao gồm xác minh cân bằng tải và hiểu các lợi ích của việc sử dụng service discovery tích hợp Kubernetes.

## Yêu Cầu Trước

- Cụm Kubernetes với microservices đã triển khai
- Keycloak được cấu hình cho xác thực OAuth2
- Postman hoặc công cụ kiểm thử API tương tự
- Nhiều bản sao (replicas) của accounts microservice đang chạy
- Gateway server đã được cấu hình và đang hoạt động

## Chuẩn Bị Kiểm Thử

### 1. Cấu Hình Client Keycloak

Một client đã được tạo trong Keycloak với các chi tiết sau:
- **Tên Client**: `easybank-callcenter-cc`
- **Vai trò**: Các vai trò cần thiết được gán để truy cập microservices

### 2. Kiến Trúc Microservices

- **Accounts Microservice**: Chạy với 2 bản sao (replicas)
- Mỗi bản sao có cơ sở dữ liệu H2 in-memory riêng
- Gateway Server: Định tuyến các yêu cầu đến microservices
- Discovery Server: Service discovery tích hợp Kubernetes

## Quy Trình Kiểm Thử

### Bước 1: Lấy Access Token

1. Mở Postman
2. Yêu cầu access token mới sử dụng Keycloak client đã cấu hình
3. Sử dụng token thu được cho các lần gọi API tiếp theo

### Bước 2: Kiểm Thử API Tạo Tài Khoản

**Endpoint**: `POST /api/create` (qua Accounts microservice)

1. Gọi API tạo tài khoản thông qua gateway
2. Kết quả mong đợi: "Account created successfully"
3. Lưu ý: Yêu cầu đầu tiên có thể mất vài giây

**Số điện thoại mẫu**: Kết thúc bằng `88`

### Bước 3: Kiểm Thử API Lấy Thông Tin Tài Khoản

**Endpoint**: `GET localhost:8072/easybank/accounts/api/fetch`

**Tham số truy vấn**: Số điện thoại đã sử dụng khi tạo tài khoản

#### Kiểm Thử Cân Bằng Tải

1. Gọi API fetch nhiều lần
2. Ban đầu, các yêu cầu trả về dữ liệu tài khoản thành công
3. Sau nhiều yêu cầu, bạn có thể nhận được lỗi "Not Found"
4. Điều này xác nhận cân bằng tải đang hoạt động - các yêu cầu được phân phối đến các pods khác nhau

## Hiểu Về Sticky Sessions

### Sticky Session Là Gì?

Cụm Kubernetes có thể duy trì sticky sessions khi:
- Các yêu cầu từ cùng một client (cùng địa chỉ IP)
- Được chuyển tiếp đến cùng một pod đã xử lý yêu cầu ban đầu
- Hành vi này là có chủ ý để duy trì tính nhất quán của phiên làm việc

### Kiểm Thử Không Có Sticky Sessions

Để xem phản hồi từ các pods khác nhau:

1. **Đợi 1-2 phút** giữa các yêu cầu
2. Sử dụng **chế độ ẩn danh của trình duyệt** để mô phỏng client khác
3. Hoặc sử dụng các IP client hoặc công cụ khác nhau

### Hành Vi Quan Sát Được

- Yêu cầu thường xuyên từ cùng client → Phản hồi từ cùng pod (sticky session)
- Yêu cầu sau khoảng thời gian nghỉ hoặc từ client khác → Phản hồi từ pod khác
- Điều này xác nhận Kubernetes Discovery Server đang định tuyến lưu lượng một cách thông minh

## Lợi Ích Của Kubernetes Discovery Server

### 1. Giảm Gánh Nặng Cho Nhà Phát Triển

- **Không cần bảo trì Eureka Server**
- Microservices không cần tự đăng ký trong quá trình khởi động
- Không cần gửi heartbeats thường xuyên
- Kubernetes xử lý service discovery một cách tự nhiên

### 2. Kiến Trúc Đơn Giản Hóa

- Kubernetes tự động giám sát và theo dõi tất cả các instances đang chạy
- Tích hợp tự nhiên với cụm Kubernetes
- Giảm độ phức tạp trong cấu hình microservices

### 3. Tự Động Service Discovery

- Các pods được Kubernetes tự động phát hiện
- Các endpoints của service được cập nhật động
- Không cần các thành phần cơ sở hạ tầng bổ sung

## Đánh Đổi và Cân Nhắc

### Kiểm Soát Cân Bằng Tải Hạn Chế

**Hạn chế**: Với Kubernetes Discovery Server, bạn có quyền kiểm soát hạn chế đối với các thuật toán cân bằng tải.

**Giải pháp thay thế**: Nếu bạn cần kiểm soát chi tiết cân bằng tải:
- Sử dụng **Spring Cloud Load Balancer**
- Triển khai **Eureka Server** cho cân bằng tải phía client
- Cấu hình các chiến lược cân bằng tải tùy chỉnh

### Khi Nào Sử Dụng Từng Phương Pháp

| Tính năng | Kubernetes Discovery | Eureka Server |
|-----------|---------------------|---------------|
| Độ phức tạp cài đặt | Thấp | Cao |
| Bảo trì | Tối thiểu | Cần quản lý |
| Kiểm soát cân bằng tải | Hạn chế | Toàn quyền kiểm soát |
| Tích hợp Kubernetes | Có | Không |
| Phù hợp nhất cho | Triển khai cloud-native | Yêu cầu tùy chỉnh |

## Kết Quả Xác Minh

✅ **Cân bằng tải hoạt động chính xác**
- Các yêu cầu được phân phối qua nhiều pods
- Các phản hồi khác nhau xác nhận việc phân phối lưu lượng

✅ **Kubernetes Discovery Server hoạt động**
- Các pods được tự động phát hiện và đăng ký
- Định tuyến service hoạt động như mong đợi

✅ **Hành vi sticky session**
- Định tuyến nhất quán cho các yêu cầu thường xuyên từ cùng client
- Tối ưu hóa hiệu suất thông qua session affinity

## Thực Hành Tốt Nhất

1. **Kiểm thử với nhiều clients** để xác minh cân bằng tải
2. **Giám sát sức khỏe pod** thông qua bảng điều khiển Kubernetes
3. **Sử dụng timeouts phù hợp** cho các yêu cầu API
4. **Triển khai logging đúng cách** để theo dõi pod nào phục vụ yêu cầu
5. **Cân nhắc sticky sessions** khi thiết kế ứng dụng có trạng thái

## Kết Luận

Kubernetes Discovery Server cung cấp một phương pháp đơn giản hóa cho service discovery trong kiến trúc microservices. Mặc dù nó cung cấp độ phức tạp và chi phí bảo trì giảm, các nhà phát triển nên cân nhắc yêu cầu cân bằng tải của họ khi lựa chọn giữa discovery tích hợp Kubernetes và các giải pháp phía client như Eureka Server.

## Các Bước Tiếp Theo

- Các Docker images cho section 17 sẽ được đẩy lên Docker Hub
- Code được check in vào kho GitHub trong thư mục `section_17`
- Xem lại code để biết chi tiết triển khai
- Tham khảo `section_17` cho các câu hỏi và tài liệu tham khảo

## Tài Nguyên

- **GitHub Repository**: Thư mục section_17
- **Docker Hub**: Các images liên quan đến Section 17
- **Tài liệu**: Tham khảo tài liệu dự án để biết cấu hình chi tiết

---

*Nếu có câu hỏi hoặc cần làm rõ, vui lòng tham khảo code trong thư mục section_17 của repository.*




FILE: 8-configuring-role-based-authorization-in-gateway.md


# Cấu Hình Phân Quyền Dựa Trên Role Trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách triển khai phân quyền dựa trên role trong Spring Cloud Gateway khi sử dụng OAuth2 với Keycloak làm máy chủ ủy quyền. Chúng ta sẽ vượt qua việc chỉ kiểm tra xác thực đơn giản để thực thi phân quyền dựa trên các role của client.

## Từ Xác Thực Đến Phân Quyền

### Trạng Thái Hiện Tại
Hiện tại, gateway chỉ kiểm tra xem ứng dụng client đã được **xác thực** (authenticated) hay chưa, nhưng không kiểm tra **phân quyền** (authorization) cụ thể (roles hoặc privileges).

### Tại Sao Phân Quyền Quan Trọng
Trong các tình huống thực tế, bạn thường cần xử lý yêu cầu chỉ khi ứng dụng client có các role hoặc quyền cụ thể được gán.

## Triển Khai Kiểm Soát Truy Cập Dựa Trên Role

### Bước 1: Cấu Hình Yêu Cầu Role Trong Gateway

Thay vì sử dụng `.authenticated()`, hãy dùng phương thức `.hasRole()` để chỉ định các role cần thiết:

```java
// Cho các API liên quan đến accounts
.hasRole("ACCOUNTS")

// Cho các API liên quan đến cards
.hasRole("CARDS")

// Cho các API liên quan đến loans
.hasRole("LOANS")
```

Điều này thực thi phân quyền ở cấp độ gateway, đảm bảo chỉ các client có role phù hợp mới có thể truy cập các microservice cụ thể.

## Cấu Hình Roles Trong Keycloak

### Bước 2: Tạo Realm Roles

1. Điều hướng đến **Keycloak Admin Console**
2. Vào **Realm roles**
3. Nhấp **Create role**
4. Tạo roles:
   - Tên role: `ACCOUNTS`
   - Mô tả: "Accounts Role"
   - Nhấp **Save**

**Lưu ý**: Ban đầu chỉ tạo role ACCOUNTS cho mục đích kiểm thử. Các role Cards và Loans sẽ được thêm sau khi kiểm thử negative.

### Bước 3: Gán Roles Cho Service Account

Đối với loại cấp quyền client credentials (machine-to-machine), roles phải được gán trong **Service account roles**, không phải roles thông thường:

1. Vào **Clients** → Chọn client của bạn (ví dụ: `eazybank-callcenter-cc`)
2. Điều hướng đến tab **Service account roles**
3. Nhấp **Assign Role**
4. Chọn role `ACCOUNTS`
5. Nhấp **Assign**

## Hiểu Cấu Trúc JWT Token

### Thông Tin Role Trong Access Token

Sau khi lấy access token mới, kiểm tra nó tại [jwt.io](https://jwt.io). Thông tin role xuất hiện trong payload:

```json
{
  "realm_access": {
    "roles": [
      "ACCOUNTS",
      "default-roles-keycloak",
      "offline_access",
      "uma_authorization"
    ]
  }
}
```

Mảng `realm_access.roles` chứa:
- **Custom roles**: `ACCOUNTS` (role chúng ta cấu hình)
- **Default roles**: Các role chuẩn của Keycloak

## Tạo Custom Role Converter

### Bước 4: Triển Khai KeycloakRoleConverter

Spring Security cần trích xuất thông tin role từ JWT và chuyển đổi sang định dạng `GrantedAuthority`.

Tạo file `KeycloakRoleConverter.java`:

```java
public class KeycloakRoleConverter implements Converter<Jwt, Collection<GrantedAuthority>> {
    
    @Override
    public Collection<GrantedAuthority> convert(Jwt jwt) {
        Map<String, Object> realmAccess = (Map<String, Object>) jwt.getClaims().get("realm_access");
        
        if (realmAccess == null || realmAccess.isEmpty()) {
            return Collections.emptyList();
        }
        
        Collection<String> roles = (Collection<String>) realmAccess.get("roles");
        
        return roles.stream()
            .map(role -> "ROLE_" + role)
            .map(SimpleGrantedAuthority::new)
            .collect(Collectors.toList());
    }
}
```

### Hiểu Logic Chuyển Đổi

1. **Trích xuất Claims**: `jwt.getClaims()` lấy dữ liệu payload
2. **Lấy Realm Access**: Truy cập key `realm_access` chứa một map
3. **Trích xuất Roles**: Lấy mảng `roles` từ map realm_access
4. **Thêm Prefix**: Thêm tiền tố `ROLE_` cho mỗi tên role (yêu cầu của Spring Security)
5. **Chuyển đổi sang GrantedAuthority**: Tạo đối tượng `SimpleGrantedAuthority` cho mỗi role

### Tại Sao Cần Tiền Tố ROLE_?

Khi sử dụng `.hasRole("USER")` trong cấu hình Spring Security, framework tự động chuyển đổi thành `ROLE_USER`. Do đó:
- **Trong Converter**: Thêm tiền tố `ROLE_`
- **Trong Security Config**: Dùng tên role không có tiền tố (framework tự động thêm)

## Tích Hợp Converter Với Cấu Hình Security

### Bước 5: Cấu Hình JWT Authentication Converter

Thêm phương thức để tạo granted authorities extractor:

```java
private Converter<Jwt, Mono<AbstractAuthenticationToken>> grantedAuthoritiesExtractor() {
    JwtAuthenticationConverter jwtAuthenticationConverter = new JwtAuthenticationConverter();
    jwtAuthenticationConverter.setJwtGrantedAuthoritiesConverter(new KeycloakRoleConverter());
    return new ReactiveJwtAuthenticationConverterAdapter(jwtAuthenticationConverter);
}
```

### Bước 6: Cập Nhật Cấu Hình Security

Thay thế cấu hình JWT mặc định:

**Trước:**
```java
.jwt(Customizer.withDefaults())
```

**Sau:**
```java
.jwt(jwtSpec -> jwtSpec
    .jwtAuthenticationConverter(grantedAuthoritiesExtractor()))
```

Điều này thiết lập liên kết giữa `KeycloakRoleConverter` tùy chỉnh của bạn và cấu hình Spring Security.

## Tóm Tắt

Bằng cách triển khai phân quyền dựa trên role, bạn đã nâng cao bảo mật microservices:

1. ✅ Cấu hình yêu cầu role trong gateway
2. ✅ Tạo và gán roles trong Keycloak
3. ✅ Triển khai custom JWT role converter
4. ✅ Tích hợp converter với cấu hình Spring Security

Gateway giờ đây kiểm tra cả **xác thực** (bạn là ai) và **phân quyền** (bạn có thể truy cập gì) trước khi định tuyến yêu cầu đến các microservice.

## Các Bước Tiếp Theo

- Build dự án
- Kiểm thử phân quyền với các role khác nhau
- Triển khai negative testing
- Thêm roles CARDS và LOANS
- Kiểm thử hoàn chỉnh kiểm soát truy cập dựa trên role

---

**Các Chủ Đề Liên Quan:**
- OAuth2 Client Credentials Grant Flow
- Spring Security Authorization
- Keycloak Service Account Roles
- Cấu Trúc JWT Token




FILE: 80-deploying-microservices-to-cloud-kubernetes-cluster.md


# Triển Khai Microservices lên Kubernetes Cluster trên Cloud

## Tổng Quan

Trong phần này, chúng ta sẽ học cách triển khai microservices vào Kubernetes cluster được tạo trên nhà cung cấp dịch vụ đám mây. Sau khi đã triển khai thành công tất cả microservices lên Kubernetes cluster cục bộ, bước tiếp theo là chuyển sang môi trường cloud sẵn sàng cho sản xuất.

## Tại Sao Nên Dùng Kubernetes trên Cloud?

Kubernetes có tính mô-đun cao, linh hoạt và có khả năng mở rộng, cho phép triển khai trong nhiều môi trường khác nhau:

- **Trung tâm dữ liệu tại chỗ (on-premises)**
- **Trung tâm dữ liệu bên thứ ba**
- **Các nhà cung cấp dịch vụ cloud**
- **Triển khai đa đám mây** (trên nhiều nhà cung cấp cloud)

Tuy nhiên, việc tạo và duy trì Kubernetes cluster có thể rất thách thức, đặc biệt là ở môi trường on-premises. Đây là lý do tại sao nhiều tổ chức doanh nghiệp ưu tiên sử dụng các nhà cung cấp cloud, giúp đơn giản hóa việc quản lý kiến trúc microservices bằng Kubernetes cluster.

## Các Nhà Cung Cấp Cloud Kubernetes Chính

Khi làm việc trên các dự án thực tế triển khai microservices lên Kubernetes cluster, các tổ chức thường sử dụng một trong các nhà cung cấp cloud lớn sau:

### Amazon Web Services (AWS)
- **Tên Sản Phẩm**: EKS (Elastic Kubernetes Service)
- Một trong những lựa chọn phổ biến nhất cho các ứng dụng doanh nghiệp

### Google Cloud Platform (GCP)
- **Tên Sản Phẩm**: GKE (Google Kubernetes Engine)
- Cung cấp khả năng Kubernetes mạnh mẽ với tích hợp liền mạch

### Microsoft Azure
- **Tên Sản Phẩm**: AKS (Azure Kubernetes Service)
- Tích hợp tốt với hệ sinh thái Microsoft

## Tại Sao Chọn GCP Cho Khóa Học Này

Trong khóa học này, chúng ta sẽ triển khai ứng dụng lên Kubernetes cluster được tạo trên **Google Cloud Platform (GCP)**. Lý do như sau:

### Tín Dụng Miễn Phí
Khi tạo tài khoản GCP mới, bạn sẽ nhận được **$300 tín dụng miễn phí** để khám phá các sản phẩm của GCP.

### Kubernetes Cluster Miễn Phí
Khác với AWS và Azure, GCP cho phép bạn tạo Kubernetes cluster chỉ sử dụng tín dụng miễn phí hoặc gói miễn phí. Với AWS và Azure, bạn cần phải trả tiền ngay cả khi là người dùng mới để tạo Kubernetes cluster.

### Học Tập Tiết Kiệm Chi Phí
Cách tiếp cận này cho phép bạn:
- Tạo Kubernetes cluster trên cloud mà không tốn tiền của bạn
- Triển khai microservices lên Kubernetes cluster do GCP cung cấp
- Có được kinh nghiệm thực tế với cơ sở hạ tầng cloud cấp độ sản xuất

## Những Gì Bạn Sẽ Học

Trong các bài giảng sắp tới, bạn sẽ:
1. Tạo Kubernetes cluster trên Google Cloud Platform
2. Cấu hình cluster cho việc triển khai microservices
3. Triển khai các microservices Spring Boot lên GCP Kubernetes cluster
4. Quản lý và giám sát microservices trên cloud

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ bắt đầu quá trình tạo Kubernetes cluster trên GCP và chuẩn bị cho việc triển khai microservices.

---

**Điểm Chính**: Các nhà cung cấp Kubernetes trên cloud giúp việc duy trì kiến trúc microservices dễ dàng hơn, và GCP cung cấp cơ hội tuyệt vời để học và thử nghiệm với triển khai Kubernetes trên cloud mà không tốn chi phí.




FILE: 81-setting-up-google-cloud-and-gcloud-cli-for-kubernetes.md


# Thiết Lập Google Cloud và gcloud CLI để Triển Khai Kubernetes

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập tài khoản Google Cloud với credit miễn phí và cấu hình Google Cloud CLI (gcloud) trên hệ thống local. Đây là bước quan trọng để triển khai microservices lên Kubernetes cluster trong Google Cloud.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Gmail (tốt nhất là tài khoản mới để nhận $300 credit miễn phí)
- Thẻ tín dụng để xác minh (không tự động tính phí sau khi hết trial)
- Hiểu biết cơ bản về cloud computing

## Tại Sao Chọn Google Cloud?

Google Cloud được chọn cho việc triển khai microservices vì:
- **$300 Credit Miễn Phí**: Người dùng mới nhận $300 credit có hiệu lực trong 90 ngày
- **Google Kubernetes Engine (GKE)**: Được hỗ trợ trong free tier
- **Không Tự Động Tính Phí**: Không tự động billing sau khi hết free trial
- **Free Tier Tốt Hơn**: So với AWS và Azure cho việc thử nghiệm Kubernetes

## Bước 1: Tạo Tài Khoản Google Cloud

### 1.1 Truy Cập Google Cloud Console

1. Truy cập [cloud.google.com](https://cloud.google.com)
2. Đăng nhập bằng tài khoản Gmail của bạn
3. Nếu bạn là người dùng mới, bạn sẽ thấy ưu đãi $300 credit miễn phí

**Quan Trọng**: Nếu bạn đã từng sử dụng Gmail với Google Cloud trước đây, hãy tạo tài khoản Gmail mới để đủ điều kiện nhận credit miễn phí.

### 1.2 Kích Hoạt Free Trial

1. Click vào banner "$300 free credit"
2. Xem lại các sản phẩm free tier, bao gồm **Google Kubernetes Engine**
3. Click nút "Console" để truy cập Google Cloud Console
4. Click "Try for free" để bắt đầu quá trình kích hoạt

### 1.3 Hoàn Tất Đăng Ký

1. Chọn quốc gia và loại hình kinh doanh (ví dụ: "Business idea/Startup")
2. Chọn checkbox Terms of Service (Điều khoản dịch vụ)
3. Click "Continue"
4. Nhập thông tin thẻ tín dụng để xác minh

**Cảnh Báo**: 
- Các nhà cung cấp cloud yêu cầu xác minh thẻ tín dụng
- Hãy cẩn thận khi tạo các tài nguyên không cần thiết
- Luôn xóa các tài nguyên sau khi khám phá để bảo toàn credit miễn phí
- Nếu không thoải mái cung cấp thông tin thẻ tín dụng, bạn có thể theo dõi mà không cần tạo tài nguyên

### 1.4 Xác Minh Thiết Lập Tài Khoản

1. Đợi thông báo "Setting up your billing" và "Setting up your free trial"
2. Bạn sẽ được chuyển hướng đến trang chủ Google Cloud Console (hoặc truy cập [console.cloud.google.com](https://console.cloud.google.com))
3. Google Cloud tự động tạo một project mặc định có tên "My First Project"

## Bước 2: Cài Đặt Google Cloud SDK

### 2.1 Tại Sao Cần Cài Google Cloud SDK?

Google Cloud SDK cho phép bạn:
- Kết nối với Kubernetes clusters trong Google Cloud từ hệ thống local
- Thực thi commands trực tiếp từ terminal local
- Cài đặt và quản lý Helm charts từ local
- Giao tiếp với các sản phẩm Google Cloud mà không cần dùng web console

### 2.2 Tải Và Cài Đặt

1. Truy cập [cloud.google.com/sdk](https://cloud.google.com/sdk)
2. Click "Get started"
3. Xác minh các yêu cầu:
   - ✅ Đã tạo Google Cloud project (My First Project)
   - ✅ Đã bật billing (đã thêm thẻ tín dụng)
4. Làm theo các bước cài đặt dựa trên hệ điều hành của bạn:
   - **Windows**: Tải installer và chạy
   - **macOS**: Dùng installer hoặc Homebrew
   - **Linux**: Dùng package manager hoặc cài thủ công

### 2.3 Xác Minh Cài Đặt

Mở terminal và chạy:

```bash
gcloud --version
```

Bạn sẽ thấy output hiển thị phiên bản Google Cloud SDK đã cài đặt và các components.

## Bước 3: Cấu Hình Google Cloud CLI

### 3.1 Khởi Tạo gcloud

Chạy lệnh khởi tạo:

```bash
gcloud init
```

### 3.2 Các Bước Cấu Hình

1. **Chọn tùy chọn cấu hình**: Chọn option 3 để khởi tạo lại cấu hình "default" hiện có
2. **Đợi kết nối mạng**: CLI sẽ thiết lập kết nối với Google Cloud
3. **Prompt đăng nhập**: Khi được hỏi "Do you want to log in", gõ `Y` (Yes) và nhấn Enter
4. **Xác thực qua trình duyệt**: 
   - Trình duyệt sẽ tự động mở
   - Chọn tài khoản Gmail bạn đã dùng để tạo Google Cloud account
   - Cấp quyền bằng cách click "Allow"
5. **Xác nhận thành công**: Bạn sẽ thấy "You are now authenticated with the Google Cloud CLI"

### 3.3 Chọn Project

1. CLI sẽ hiển thị các Google Cloud projects có sẵn
2. Chọn project của bạn bằng cách nhập số tương ứng (ví dụ: `1` cho "liquid-muse-397814")
3. Nhấn Enter để xác nhận

### 3.4 Xác Minh Cấu Hình

Bạn sẽ thấy output xác nhận:
- ✅ "Your Google Cloud SDK is configured and ready to use"
- Email account của bạn
- Tên và ID của project đã kết nối

## Các Bước Tiếp Theo

Với tài khoản Google Cloud và CLI đã được cấu hình, bạn đã sẵn sàng để:
1. Tạo Kubernetes cluster trong Google Cloud
2. Triển khai microservices lên cluster
3. Quản lý tài nguyên bằng kubectl và Helm

## Những Điều Quan Trọng Cần Nhớ

### Quản Lý Chi Phí
- Theo dõi việc sử dụng $300 credit trong Google Cloud Console
- Xóa tài nguyên khi không sử dụng để bảo toàn credit
- Thiết lập cảnh báo billing để theo dõi chi tiêu

### Best Practices (Thực Hành Tốt Nhất)
- Sử dụng các sản phẩm free tier bất cứ khi nào có thể
- Khám phá các tính năng Google Kubernetes Engine trong 90 ngày trial
- Cập nhật gcloud CLI thường xuyên để có features và bảo mật mới nhất

### Các Lệnh Hữu Ích

```bash
# Kiểm tra phiên bản gcloud
gcloud --version

# Xem cấu hình hiện tại
gcloud config list

# Chuyển đổi giữa các projects
gcloud config set project PROJECT_ID

# Liệt kê các projects có sẵn
gcloud projects list

# Xem trợ giúp cho bất kỳ lệnh nào
gcloud help
```

## Khắc Phục Sự Cố

### Lệnh gcloud không tìm thấy
- Đảm bảo cài đặt hoàn tất thành công
- Thêm gcloud vào system PATH
- Khởi động lại terminal

### Vấn đề xác thực
- Chạy `gcloud auth login` để xác thực lại
- Kiểm tra kết nối internet
- Xác minh quyền của tài khoản Gmail

### Project không hiển thị
- Đảm bảo bạn đã tạo project trong Google Cloud Console
- Chạy `gcloud projects list` để xem tất cả projects có sẵn
- Xác minh billing đã được bật cho project

## Tóm Tắt

Bạn đã thành công:
- ✅ Tạo tài khoản Google Cloud với $300 credit miễn phí
- ✅ Thiết lập billing không tự động tính phí sau trial
- ✅ Cài đặt Google Cloud CLI trên hệ thống local
- ✅ Xác thực và cấu hình gcloud với tài khoản Google
- ✅ Kết nối với Google Cloud project của bạn

Bây giờ bạn đã sẵn sàng để tạo và quản lý Kubernetes cluster cho việc triển khai các Spring Boot microservices!

---

**Các Chủ Đề Liên Quan**:
- Tạo Kubernetes cluster trong Google Cloud
- Triển khai microservices với Helm charts
- Cấu hình kubectl cho GKE clusters
- Quản lý tài nguyên Google Cloud hiệu quả




FILE: 82-creating-kubernetes-cluster-in-google-cloud.md


# Tạo Kubernetes Cluster trên Google Cloud (GKE)

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện các bước tạo một Kubernetes cluster trên Google Cloud Platform (GCP) sử dụng Google Kubernetes Engine (GKE). Đây là bước quan trọng để triển khai các microservices được xây dựng bằng Java Spring Boot lên môi trường Kubernetes trên cloud.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Google Cloud Platform đang hoạt động
- Đã kích hoạt tính năng thanh toán (billing) trên tài khoản GCP
- Quyền truy cập vào Google Cloud Console

## Các Bước Tạo GKE Cluster

### 1. Truy Cập Kubernetes Engine

Có hai cách để truy cập Kubernetes Engine:

- **Tùy chọn 1**: Nhấp vào "Create a GKE cluster" từ dashboard chính
- **Tùy chọn 2**: Sử dụng ô tìm kiếm để tìm "Kubernetes" và chọn "Kubernetes Engine"

### 2. Kích Hoạt Kubernetes Engine API

Khi truy cập Kubernetes Engine lần đầu tiên trong tài khoản của bạn:

1. Hệ thống sẽ yêu cầu bạn kích hoạt **Kubernetes Engine API**
2. Nhấp vào nút **Enable** (Kích hoạt)
3. Bạn cũng cần **kích hoạt billing** nếu chưa thực hiện
4. Nhấp vào tùy chọn **Enable billing**

### 3. Tạo Cluster

Sau khi Kubernetes Engine API được kích hoạt:

1. Nhấp vào tùy chọn **tạo Kubernetes cluster**
2. Bạn sẽ thấy giao diện tạo cluster

### 4. Chọn Loại Cluster: Standard vs Autopilot

Mặc định, GCP hiển thị tùy chọn **Autopilot cluster**:

#### Autopilot Cluster
- Tự động điều chỉnh dung lượng cluster dựa trên lưu lượng truy cập
- Google Cloud xử lý phần lớn công việc nặng nhọc
- Tùy chọn dễ nhất cho các tổ chức
- Hạn chế trong việc khám phá chi tiết về Kubernetes cluster

#### Standard Cluster (Khuyến Nghị cho Việc Học)
- Kiểm soát nhiều hơn về cấu hình cluster
- Tốt hơn cho việc học và khám phá các tính năng Kubernetes
- Bắt buộc cho khóa học này

**Hành động**: Nhấp vào **"Switch to Standard Cluster"** và xác nhận lựa chọn của bạn.

### 5. Cấu Hình Cluster

1. **Tên Cluster**: Chấp nhận tên mặc định `cluster-1` hoặc đặt tên riêng
2. **Cài Đặt Mặc Định**: Giữ nguyên tất cả các giá trị mặc định cho hướng dẫn này
3. Di chuyển đến cuối trang cấu hình

### 6. Xem Xét Chi Phí

Trước khi tạo cluster, hãy xem xét chi phí ước tính:

- **Chi phí ước tính hàng tháng**: $176 (nếu chạy liên tục trong một tháng)
- **Phí theo giờ**: $0.24 mỗi giờ
- **Lưu ý**: Nếu bạn làm theo hướng dẫn và sử dụng credits miễn phí, bạn sẽ không bị tính phí
- Hướng dẫn sẽ hoàn thành trong vòng một giờ

### 7. Tạo Cluster

1. Nhấp vào nút **Create** (Tạo)
2. Quá trình tạo Kubernetes cluster sẽ bắt đầu
3. **Dung lượng mặc định**: 3 nodes
4. **Thời gian tạo**: Khoảng 5 phút

### 8. Đợi Hoàn Thành

Quá trình tạo cluster mất khoảng 5 phút. Hãy đợi cluster được tạo thành công trước khi tiến hành các bước tiếp theo.

## Các Bước Tiếp Theo

Sau khi Kubernetes cluster của bạn được tạo, bạn có thể:

- Khám phá chi tiết và cấu hình của cluster
- Triển khai các Spring Boot microservices lên cluster
- Cấu hình networking và service mesh
- Thiết lập monitoring và logging
- Triển khai CI/CD pipelines

## Mẹo Quản Lý Chi Phí

- Xóa cluster khi không sử dụng để tránh phát sinh chi phí
- Sử dụng credits miễn phí do GCP cung cấp
- Thường xuyên theo dõi bảng điều khiển thanh toán
- Thiết lập cảnh báo thanh toán để tránh chi phí bất ngờ

## Tóm Tắt

Việc tạo Kubernetes cluster trên Google Cloud là một quy trình đơn giản, cung cấp nền tảng mạnh mẽ để triển khai và quản lý microservices. Tùy chọn Standard cluster mang lại nhiều quyền kiểm soát và cơ hội học tập hơn, làm cho nó trở nên lý tưởng để hiểu các khái niệm Kubernetes trong môi trường cloud.

## Tài Nguyên Bổ Sung

- Tài liệu Google Kubernetes Engine
- Tài liệu Kubernetes chính thức
- Best Practices cho Spring Boot trên Kubernetes




FILE: 83-deploying-microservices-to-google-cloud-kubernetes.md


# Triển Khai Microservices Lên Google Cloud Kubernetes

## Tổng Quan

Hướng dẫn này sẽ giúp bạn triển khai các microservices Spring Boot lên Google Cloud Kubernetes cluster, bao gồm việc thiết lập cluster, cấu hình kết nối, và triển khai các thành phần khác nhau sử dụng Helm charts và Kubernetes manifests.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Google Cloud có kích hoạt billing
- Google Cloud CLI (gcloud) đã cài đặt trên máy local
- kubectl đã cài đặt
- Docker Desktop với Kubernetes được bật
- Helm đã cài đặt
- Dự án microservices với Helm charts đã chuẩn bị sẵn

## Tạo Kubernetes Cluster Trên Google Cloud

### Tạo Cluster

1. Truy cập Google Cloud Console
2. Tạo một Kubernetes cluster mới
3. Đợi khoảng 5 phút để cluster được tạo xong
4. Xác nhận trạng thái cluster hiển thị dấu tích màu xanh

### Chi Tiết Cluster

Sau khi tạo xong, bạn có thể xem thông tin chi tiết về cluster:

- **Vị trí**: Zone và quốc gia nơi cluster được triển khai
- **Nodes**: Danh sách các nodes trong cluster (mặc định: 3 nodes)
- **Tài nguyên**: Thông tin CPU, memory, và disk cho mỗi node
- **Pods**: Các system pods được Google Cloud cài đặt để quản lý cluster

#### Các System Pods Mặc Định

Google Cloud tự động cài đặt một số pods để quản lý cluster:

- **gke-metrics-agent**: Thu thập các metrics về CPU, memory, và disk
- Các pods quản lý khác để duy trì sức khỏe của cluster

### Thêm Nodes

Nếu cần mở rộng cluster:
1. Click vào cluster trong Google Cloud Console
2. Chọn "Add node pool"
3. Cấu hình các thiết lập cho node pool mới

## Kết Nối Tới Google Cloud Kubernetes Cluster

### Thiết Lập Kết Nối

1. Trong Google Cloud Console, click vào ba chấm bên cạnh cluster của bạn
2. Chọn "Connect"
3. Copy lệnh gcloud được cung cấp
4. Thực thi lệnh trong terminal local của bạn:

```bash
gcloud container clusters get-credentials [CLUSTER_NAME] --zone [ZONE] --project [PROJECT_ID]
```

### Xác Minh Kết Nối

```bash
kubectl get nodes
```

Bạn sẽ thấy output hiển thị cả ba nodes trong cluster.

## Quản Lý Kubernetes Contexts

### Hiểu Về Contexts

Kubernetes contexts cho phép bạn kết nối đến nhiều clusters và chuyển đổi giữa chúng dễ dàng.

### Xem Các Contexts Có Sẵn

Trong Docker Desktop:
1. Click vào biểu tượng Docker Desktop
2. Vào phần cài đặt Kubernetes
3. Xem tất cả các contexts có sẵn

### Chuyển Đổi Contexts

Để chuyển sang local Kubernetes cluster:
```bash
# Chuyển sang Docker Desktop context
kubectl config use-context docker-desktop

# Xác minh - sẽ hiển thị 1 node
kubectl get nodes
```

Để chuyển lại sang Google Cloud cluster:
```bash
# Chuyển sang GKE context
kubectl config use-context [GKE_CONTEXT_NAME]

# Xác minh - sẽ hiển thị 3 nodes
kubectl get nodes
```

## Triển Khai Các Thành Phần Lên Kubernetes

### Cấu Trúc Dự Án

Di chuyển đến thư mục section_17 chứa:
- Các Kubernetes manifest files
- Helm charts cho microservices
- Các configuration files

### 1. Triển Khai Discovery Server

Đầu tiên, triển khai Eureka Discovery Server:

```bash
cd kubernetes
kubectl apply -f kubernetes-discoveryserver.yaml
```

**Lưu ý**: Nếu gặp lỗi connection timeout, chạy lại lệnh kết nối gcloud và thử lại.

### 2. Kiểm Tra Các Helm Installations

Kiểm tra các Helm installations hiện có:
```bash
helm ls
```

Ban đầu, sẽ không có installations nào trong remote cluster.

### 3. Triển Khai Keycloak (Quản Lý Định Danh và Truy Cập)

```bash
cd ../helm
helm install keycloak keycloak
```

Lệnh này triển khai Keycloak cho các dịch vụ authentication và authorization.

### 4. Triển Khai Kafka (Nền Tảng Message Streaming)

```bash
helm install kafka kafka
```

Lệnh này thiết lập Apache Kafka cho việc giao tiếp microservices theo hướng event-driven.

### 5. Triển Khai Prometheus (Giám Sát)

```bash
helm install prometheus kube-prometheus
```

Prometheus cung cấp khả năng thu thập metrics và giám sát.

### 6. Triển Khai Loki (Tập Hợp Logs)

```bash
helm install loki grafana-loki
```

Loki tập hợp logs từ tất cả microservices để quản lý logs tập trung.

### 7. Triển Khai Tempo (Distributed Tracing)

```bash
helm install tempo grafana-tempo
```

Tempo cung cấp khả năng distributed tracing để theo dõi requests qua các microservices.

### 8. Triển Khai Grafana (Trực Quan Hóa)

```bash
helm install grafana grafana
```

Grafana cung cấp dashboards để trực quan hóa metrics, logs, và traces.

### 9. Triển Khai Microservices Với Helm

Cuối cùng, triển khai tất cả Spring Boot microservices:

```bash
cd ../environments
helm install easybank prod-env
```

Lệnh này:
- Triển khai tất cả microservices được định nghĩa trong prod-env Helm chart
- Sử dụng cấu hình môi trường production
- Tạo tất cả các Kubernetes resources cần thiết (Deployments, Services, ConfigMaps, v.v.)

## Quy Trình Triển Khai

### Thời Gian

- Discovery Server: ~2-3 phút
- Mỗi Helm chart: ~3-5 phút
- Triển khai Microservices: ~5-10 phút

### Giám Sát Quá Trình Triển Khai

Kiểm tra trạng thái pods:
```bash
kubectl get pods
```

Kiểm tra trạng thái deployments:
```bash
kubectl get deployments
```

Xem các service endpoints:
```bash
kubectl get services
```

## Sự Khác Biệt So Với Local Kubernetes

### Điểm Tương Đồng

- Cùng Helm charts và Kubernetes manifests
- Cùng các lệnh và quy trình triển khai
- Cùng kiến trúc microservices

### Điểm Khác Biệt

- **Dung lượng**: Cloud cluster có nhiều CPU, memory, và storage hơn
- **Tính Sẵn Sàng Cao**: Nhiều nodes cung cấp khả năng dự phòng
- **Khả Năng Mở Rộng**: Dễ dàng thêm nodes khi cần
- **Dịch Vụ Quản Lý**: Google Cloud xử lý bảo trì cluster
- **Mạng**: Thiết lập networking khác so với local

## Xử Lý Sự Cố

### Lỗi Connection Timeout

Nếu gặp lỗi connection timeout:
1. Chạy lại lệnh kết nối gcloud
2. Kiểm tra kết nối internet
3. Xác minh cluster đang chạy trong Google Cloud Console

### Vấn Đề Context

Nếu các lệnh kubectl không hoạt động:
1. Xác minh bạn đang ở đúng context: `kubectl config current-context`
2. Chuyển sang context phù hợp nếu cần
3. Chạy `kubectl get nodes` để xác nhận kết nối

### Lỗi Triển Khai

Nếu pods không khởi động:
1. Kiểm tra logs của pods: `kubectl logs [POD_NAME]`
2. Mô tả pod để xem events: `kubectl describe pod [POD_NAME]`
3. Xác minh resource limits và tính khả dụng
4. Kiểm tra ConfigMaps và Secrets được tạo đúng cách

## Các Bước Tiếp Theo

Sau khi triển khai hoàn tất (5-10 phút):
1. Xác minh tất cả pods đang chạy
2. Truy cập Grafana dashboard để giám sát
3. Kiểm thử các endpoints của microservices
4. Cấu hình Keycloak với users và roles
5. Thiết lập ingress cho truy cập từ bên ngoài

## Best Practices (Thực Hành Tốt Nhất)

1. **Sử dụng namespaces** để tổ chức resources
2. **Đặt resource limits** cho tất cả containers
3. **Cấu hình health checks** (liveness và readiness probes)
4. **Sử dụng ConfigMaps và Secrets** cho cấu hình
5. **Bật monitoring và logging** ngay từ đầu
6. **Triển khai RBAC đúng cách** cho bảo mật
7. **Sao lưu định kỳ** dữ liệu persistent
8. **Sử dụng Helm cho deployments nhất quán** qua các môi trường

## Tóm Tắt

Hướng dẫn này đã trình bày quy trình hoàn chỉnh để triển khai Spring Boot microservices lên Google Cloud Kubernetes, bao gồm:
- Tạo và kết nối đến GKE cluster
- Quản lý nhiều Kubernetes contexts
- Triển khai các thành phần cơ sở hạ tầng (Keycloak, Kafka, Prometheus, Loki, Tempo, Grafana)
- Triển khai microservices sử dụng Helm charts

Cloud Kubernetes cluster cung cấp môi trường production-ready với tính sẵn sàng cao, khả năng mở rộng, và cơ sở hạ tầng được quản lý.




FILE: 84-deploying-and-validating-microservices-in-kubernetes-cloud.md


# Triển Khai và Xác Thực Microservices trên Kubernetes Cloud

## Tổng Quan

Hướng dẫn này bao gồm việc triển khai và xác thực các microservices Spring Boot trong cụm Kubernetes trên Google Cloud Platform (GCP), bao gồm Gateway Server, xác thực Keycloak và kiểm thử REST APIs với Postman.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Google Cloud Platform với cụm Kubernetes đã được tạo
- kubectl CLI đã được cấu hình
- Postman để kiểm thử API
- Helm charts đã chuẩn bị cho microservices
- Hiểu biết cơ bản về các khái niệm Kubernetes

## Chờ Đợi Quá Trình Triển Khai Hoàn Tất

Sau khi triển khai ứng dụng lên Kubernetes:

**Quan trọng:** Hãy đợi ít nhất **10 phút** để tất cả các cài đặt hoàn thành. Mặc dù một số triển khai có thể hoàn tất trong vòng 5 phút, nhưng nên đợi đủ 10 phút trước khi cho rằng có vấn đề xảy ra.

## Xác Thực Triển Khai Kubernetes

### 1. Kiểm Tra Các Node trong Cluster

1. Điều hướng đến cụm Kubernetes của bạn trong GCP Console
2. Vào phần **Nodes** để xem tất cả các node trong cluster (thường là 3 nodes)
3. Click vào bất kỳ node nào để xem các pod đang chạy trong node đó
4. Thay đổi "rows per page" thành 30 hoặc 50 để xem tất cả pods cùng lúc

### 2. Xác Minh Trạng Thái Pod

Tìm kiếm các dấu hiệu triển khai thành công:
- **Dấu tick màu xanh** bên cạnh tất cả các pods
- Trạng thái Running cho tất cả containers
- Các thành phần chính có thể thấy:
  - Pods liên quan đến Prometheus
  - Pods liên quan đến Loki
  - Pods liên quan đến Kafka
  - Pod Gateway Server
  - Pods Microservice (accounts, cards, loans)

### 3. Định Vị Pod Gateway Server

#### Sử Dụng Lệnh kubectl

```bash
# Lấy danh sách tất cả pods
kubectl get pods

# Tìm pod Gateway Server (tìm pod có tên bắt đầu bằng "gateway-server")
# Copy tên đầy đủ của pod

# Mô tả pod để lấy thông tin chi tiết
kubectl describe pod <gateway-server-pod-name>
```

Kết quả lệnh `describe` hiển thị:
- Node nơi pod được cài đặt
- Container images được sử dụng
- Events và thông tin trạng thái

#### Sử Dụng GCP Console

1. Điều hướng đến **Workloads** để xem tất cả deployments
2. Vào **Services and Ingress** để xem tất cả services
3. Tìm kiếm pod "gateway-server"
4. Click vào pod để xem:
   - Trạng thái container
   - Log events
   - Logs của container

## Hiểu Về Các Thành Phần Kubernetes

### Workloads (Deployments)

Xem tất cả các deployments tạo ra replicas, pods và containers trong cụm Kubernetes của bạn.

### Services

- **Cluster IP**: Hầu hết các microservices chỉ được expose nội bộ
- **LoadBalancer**: Gateway Server và Keycloak được expose ra bên ngoài
  - Tự động tạo địa chỉ IP công khai
  - Có thể được map đến tên miền bởi Kubernetes admins

### ConfigMaps và Secrets

Xác minh rằng tất cả configuration maps và secrets đã được tạo thành công trong phần **Config and Storage**.

## Cấu Hình Xác Thực Keycloak

### 1. Truy Cập Keycloak Admin Console

1. Điều hướng đến **Services and Ingress**
2. Copy địa chỉ IP công khai của Keycloak service
3. Mở URL trong tab trình duyệt ẩn danh (incognito)
4. Click vào **Administration Console**
5. Đăng nhập với thông tin mặc định:
   - **Username**: `admin`
   - **Password**: `password`

### 2. Tạo OAuth2 Client

1. Vào phần **Clients**
2. Click **Create Client**
3. Nhập client ID: `easybank-callcenter-cc`
4. Click **Next**
5. Bật **Client Authentication**
6. Tắt tất cả các tùy chọn khác trừ **Service Account Roles**
7. Click **Next**, sau đó **Save**
8. Vào tab **Credentials**
9. Copy **Client Secret** để sử dụng trong Postman

### 3. Tạo Các Roles

Tạo các roles sau trong Keycloak:
1. `accounts`
2. `cards`
3. `loans`

**Các bước:**
1. Vào **Realm Roles**
2. Click **Create Role**
3. Nhập tên role
4. Save và lặp lại cho cả ba roles

### 4. Gán Roles cho Service Account

1. Vào **Clients** → `easybank-callcenter-cc`
2. Click tab **Service Account Roles**
3. Gán cả ba roles: `accounts`, `cards`, `loans`
4. Lưu role mapping

## Kiểm Thử APIs Microservices với Postman

### 1. Cấu Hình Postman OAuth2 Settings

Cập nhật những thông tin sau trong Postman:
- **Access Token URL**: Thay thế `localhost` bằng IP công khai của Keycloak
  - Định dạng: `http://<keycloak-public-ip>/realms/<realm-name>/protocol/openid-connect/token`
- **Client ID**: `easybank-callcenter-cc`
- **Client Secret**: (paste secret đã copy từ Keycloak)

### 2. Kiểm Thử GET APIs (Không Yêu Cầu Xác Thực)

Thay thế `localhost` bằng IP công khai của Gateway Server trong tất cả requests.

#### Thông Tin Liên Hệ Accounts
```
GET http://<gateway-public-ip>:8080/eazybank/accounts/api/contact-info
```

#### Thông Tin Liên Hệ Cards
```
GET http://<gateway-public-ip>:8080/eazybank/cards/api/contact-info
```

#### Thông Tin Liên Hệ Loans
```
GET http://<gateway-public-ip>:8080/eazybank/loans/api/contact-info
```

**Kết quả mong đợi**: Thành công với dữ liệu cấu hình

### 3. Kiểm Thử POST APIs (Với Xác Thực OAuth2)

#### Lấy Access Token
1. Trong Postman, vào tab **Authorization**
2. Chọn **OAuth 2.0**
3. Click **Get New Access Token**
4. Click **Proceed** và **Use Token**

#### Tạo Account
```
POST http://<gateway-public-ip>:8080/eazybank/accounts/api/create
```

**Kết quả mong đợi**: `201 Account created successfully`

#### Tạo Card
```
POST http://<gateway-public-ip>:8080/eazybank/cards/api/create
```

**Kết quả mong đợi**: `201 Card created successfully`

#### Tạo Loan
```
POST http://<gateway-public-ip>:8080/eazybank/loans/api/create
```

**Kết quả mong đợi**: `201 Loan created successfully`

### 4. Kiểm Thử Composite API

#### Lấy Thông Tin Chi Tiết Khách Hàng (Accounts + Cards + Loans)
```
GET http://<gateway-public-ip>:8080/eazybank/accounts/api/fetchCustomerDetails
```

**Kết quả mong đợi**: JSON với dữ liệu khách hàng kết hợp từ cả ba microservices

## Danh Sách Kiểm Tra Xác Thực

- ✅ Tất cả pods hiển thị dấu tick màu xanh
- ✅ Pod Gateway Server chạy thành công
- ✅ Keycloak có thể truy cập qua IP công khai
- ✅ OAuth2 client được tạo với cấu hình đúng
- ✅ Roles được tạo và gán
- ✅ GET APIs trả về responses thành công
- ✅ Access token được tạo thành công
- ✅ POST APIs tạo resources thành công
- ✅ Composite API trả về dữ liệu kết hợp

## Điểm Chính Cần Nhớ

1. **Kiên Nhẫn Với Triển Khai**: Luôn đợi 10 phút cho các triển khai Kubernetes
2. **Loại Service Quan Trọng**: LoadBalancer expose services ra ngoài với IP công khai
3. **Gateway Pattern**: Tất cả traffic đi qua Gateway Server
4. **Bảo Mật OAuth2**: Keycloak cung cấp xác thực tập trung
5. **Xác Thực Cloud**: Kiểm thử tất cả APIs với IP công khai, không phải localhost

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ xác thực các **thành phần Grafana** để giám sát và quan sát kiến trúc microservices.

## Xử Lý Sự Cố

### Pods Không Khởi Động
- Kiểm tra logs của pod: `kubectl logs <pod-name>`
- Mô tả pod để xem events: `kubectl describe pod <pod-name>`
- Xác minh resource quotas và limits

### Không Thể Truy Cập Services
- Xác minh LoadBalancer đã tạo IP công khai
- Kiểm tra firewall rules trong GCP
- Đảm bảo số port đúng

### Lỗi Xác Thực
- Xác minh client secret đúng
- Kiểm tra định dạng access token URL
- Đảm bảo roles được gán cho service account

## Kết Luận

Triển khai và xác thực microservices thành công trong môi trường Kubernetes trên cloud đòi hỏi sự chú ý cẩn thận đến thời gian, cấu hình đúng các thành phần bảo mật như Keycloak, và kiểm thử kỹ lưỡng tất cả các API endpoints. Thiết lập này minh họa một kiến trúc microservices sẵn sàng production với API Gateway, service discovery và bảo mật OAuth2.




FILE: 85-validating-grafana-in-kubernetes-cluster.md


# Xác Thực Các Thành Phần Grafana Trong Kubernetes Cluster Trên Google Cloud

## Tổng Quan

Hướng dẫn này trình bày cách xác thực các thành phần Grafana được triển khai trong Kubernetes cluster trên Google Cloud và cách truy cập các dịch vụ Grafana được expose dưới dạng ClusterIP.

## Cấu Hình Dịch Vụ Grafana

Theo mặc định, Grafana được triển khai dưới dạng dịch vụ **ClusterIP** trong Kubernetes cluster. Điều này có nghĩa là:
- Không có địa chỉ IP công khai được gán
- Không thể truy cập trực tiếp từ bên ngoài
- Cần kết nối thông qua Kubernetes cluster để truy cập

## Các Tùy Chọn Truy Cập Dịch Vụ ClusterIP

Quản trị viên Kubernetes có hai tùy chọn chính để cung cấp quyền truy cập vào dịch vụ ClusterIP:

### Tùy Chọn 1: Cập Nhật Thành LoadBalancer
- Sửa đổi Helm chart để thay đổi loại dịch vụ thành `LoadBalancer`
- Chạy lệnh `helm upgrade`
- Lập trình viên sau đó có thể truy cập Grafana thông qua IP công khai được cấp

### Tùy Chọn 2: Port Forwarding (Khuyến Nghị Cho Môi Trường Development)
- Kết nối với Kubernetes cluster từ hệ thống local của bạn
- Sử dụng thông tin xác thực Kubernetes của bạn (admin hoặc developer)
- Sử dụng lệnh `kubectl port-forward` để expose dịch vụ cục bộ

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi truy cập Grafana, đảm bảo bạn có:
1. **Google Cloud CLI (gcloud)** đã được cài đặt và cấu hình
2. **kubectl** đã được cấu hình để kết nối với Kubernetes cluster của bạn
3. Thông tin xác thực Kubernetes phù hợp (quyền truy cập admin hoặc developer)

## Quy Trình Xác Thực Từng Bước

### Bước 1: Lấy Thông Tin Đăng Nhập Admin Của Grafana

Khi Grafana được cài đặt qua Helm, các hướng dẫn cài đặt sẽ được cung cấp trong terminal output. Để lấy mật khẩu admin:

```bash
# Lấy tên người dùng admin (thường là 'admin')
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-user}" | base64 --decode

# Lấy mật khẩu admin
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

**Lưu ý:** Tên người dùng mặc định thường là `admin`.

### Bước 2: Thiết Lập Port Forwarding

Chạy lệnh kubectl port-forward để expose Grafana trên máy local của bạn:

```bash
kubectl port-forward --namespace default svc/grafana 8080:80
```

Lệnh này sẽ:
- Chuyển tiếp cổng local `8080` đến cổng dịch vụ Grafana `80`
- Tiếp tục chạy trong terminal (tiến trình nền)
- Làm cho Grafana có thể truy cập tại `localhost:8080`

### Bước 3: Truy Cập Giao Diện Web Grafana

1. Mở trình duyệt web của bạn
2. Truy cập `http://localhost:8080`
3. Nhập thông tin đăng nhập:
   - **Username:** `admin`
   - **Password:** (lấy từ Bước 1)
4. Nhấp vào nút **Login**

## Xác Thực Các Tích Hợp Grafana

Sau khi đăng nhập, xác minh rằng Grafana đã được tích hợp đúng cách với các thành phần giám sát:

### 1. Tích Hợp Loki (Log Aggregation - Tổng Hợp Log)

**Mục đích:** Xác thực khả năng thu thập và xem log

1. Điều hướng đến trang **Explore** trong Grafana
2. Mở menu dropdown nguồn dữ liệu
3. Chọn **Loki** làm nguồn dữ liệu
4. Cấu hình truy vấn:
   - **Label:** `container`
   - **Value:** `gateway-server` (hoặc tên microservice của bạn)
5. Nhấp vào **Run Query**
6. Xem lại các log được hiển thị cho container đã chọn

**Tính Năng Nâng Cao - Distributed Tracing:**
- Nhấp vào bất kỳ bản ghi log nào
- Tìm trường **Trace ID**
- Nhấp vào nút để điều hướng đến **Tempo**
- Xem chi tiết distributed tracing để phân tích hiệu suất

### 2. Tích Hợp Tempo (Distributed Tracing - Truy Vết Phân Tán)

**Mục đích:** Xác thực distributed tracing qua các microservice

1. Từ một bản ghi log Loki, nhấp vào liên kết Tempo
2. Đợi vài giây để dữ liệu trace được tải
3. Xác minh rằng chi tiết distributed tracing được hiển thị
4. Sử dụng thông tin này để:
   - Phân tích luồng request qua các service
   - Xác định các điểm nghẽn hiệu suất
   - Debug các vấn đề về độ trễ

### 3. Tích Hợp Prometheus (Metrics Collection - Thu Thập Số Liệu)

**Mục đích:** Xác thực thu thập và trực quan hóa số liệu

1. Điều hướng đến trang **Explore**
2. Chọn **Prometheus** làm nguồn dữ liệu
3. Cấu hình truy vấn metric:
   - **Metric:** `up` (số liệu về tính khả dụng hệ thống)
   - **Label filters:** `container` = (tên container của bạn)
   - **Time range:** Last 15 minutes (15 phút gần nhất)
4. Nhấp vào **Run Query**
5. Chuyển sang chế độ xem **Graph** để trực quan hóa
6. Bật **Stacked lines** để có hình ảnh đẹp hơn

**Kết Quả Mong Đợi:**
- Biểu đồ hiển thị dữ liệu metric theo thời gian
- Xác nhận Prometheus đang scrape metrics thành công

## Danh Sách Kiểm Tra Xác Thực

Đảm bảo tất cả các thành phần đang hoạt động chính xác:

- [x] Đăng nhập Grafana thành công
- [x] Tích hợp Loki hoạt động (log hiển thị)
- [x] Tích hợp Tempo hoạt động (trace có thể truy cập từ log)
- [x] Tích hợp Prometheus hoạt động (metric hiển thị)

## Lưu Ý Quan Trọng

### Cân Nhắc Về Bảo Mật
- Dịch vụ ClusterIP không được expose ra internet
- Chỉ người dùng có quyền truy cập Kubernetes cluster mới có thể sử dụng port-forward
- Điều này cung cấp một lớp bảo mật bổ sung cho các dịch vụ production

### Giới Hạn Của Port Forwarding
- Kết nối chỉ hoạt động khi lệnh đang chạy
- Nếu terminal bị đóng, port forwarding sẽ dừng
- Phù hợp cho development/debugging, không phải cho truy cập production

### Truy Cập Production
Đối với môi trường production, hãy xem xét:
- Sử dụng LoadBalancer hoặc Ingress cho truy cập vĩnh viễn
- Triển khai xác thực và ủy quyền phù hợp
- Thiết lập VPN hoặc bastion host cho truy cập an toàn

## Xử Lý Sự Cố

### Không Thể Kết Nối Với Grafana
- Xác minh kubectl đã kết nối với cluster đúng
- Đảm bảo cổng 8080 chưa được sử dụng
- Kiểm tra pod Grafana đang chạy: `kubectl get pods | grep grafana`

### Nguồn Dữ Liệu Không Hiển Thị
- Xác minh Prometheus, Loki và Tempo đã được triển khai và đang chạy
- Kiểm tra cấu hình nguồn dữ liệu Grafana
- Xem lại các network policy có thể chặn giao tiếp

### Không Có Log Hoặc Metric Hiển Thị
- Xác nhận microservice đang chạy và tạo dữ liệu
- Xác minh các collector agent (Promtail, OpenTelemetry) đã được triển khai
- Kiểm tra các service label và selector khớp với filter truy vấn

## Kết Luận

Việc xác thực thành công Grafana và các tích hợp của nó (Loki, Tempo, Prometheus) trong Kubernetes cluster trên Google Cloud đảm bảo rằng observability stack của bạn đang hoạt động chính xác. Thiết lập này cho phép khả năng giám sát, logging và tracing toàn diện cho các ứng dụng microservice được xây dựng bằng Java Spring Boot.

## Các Bước Tiếp Theo

- Cấu hình dashboard tùy chỉnh cho microservice của bạn
- Thiết lập các quy tắc cảnh báo trong Prometheus
- Khám phá truy vấn nâng cao với PromQL và LogQL
- Triển khai distributed tracing trong ứng dụng Spring Boot của bạn




FILE: 86-uninstalling-microservices-and-deleting-kubernetes-cluster.md


# Gỡ Cài Đặt Microservices và Xóa Kubernetes Cluster Trên Google Cloud

## Tổng Quan

Sau khi triển khai và xác thực thành công tất cả các microservices trong Google Cloud Kubernetes cluster, việc dọn dẹp tài nguyên một cách đúng đắn là rất quan trọng để tránh các khoản phí bất ngờ. Hướng dẫn này sẽ đi qua toàn bộ quy trình gỡ cài đặt tất cả các thành phần và xóa Kubernetes cluster.

## Yêu Cầu Trước Khi Bắt Đầu

- Tất cả microservices và các thành phần hỗ trợ đã được triển khai và xác thực
- Helm đã được cài đặt và cấu hình
- kubectl đã được cấu hình để truy cập Google Cloud Kubernetes cluster của bạn
- Có quyền truy cập vào Google Cloud Console

## Xác Thực Trước Khi Dọn Dẹp

Trước khi tiến hành gỡ cài đặt, hãy đảm bảo tất cả các thành phần đang hoạt động đúng:

1. **Trạng Thái Microservices**: Tất cả microservices và các thành phần hỗ trợ phải hoạt động như mong đợi
2. **Kịch Bản Event-Driven**: Kiểm tra logs của accounts và message microservices để xác thực các kịch bản event-driven dựa trên Kafka
3. **Tình Trạng Tổng Thể**: Xác minh rằng toàn bộ hệ thống đang hoạt động bình thường

## Gỡ Cài Đặt Các Thành Phần Với Helm

Quy trình gỡ cài đặt sử dụng Helm để xóa tất cả các releases đã triển khai. Thực hiện theo các bước sau theo thứ tự:

### Bước 1: Gỡ Cài Đặt Microservices Release

```bash
helm uninstall easybank
```

Lệnh này sẽ xóa tất cả microservices được triển khai dưới tên release `easybank`.

### Bước 2: Gỡ Cài Đặt Grafana

```bash
helm uninstall grafana
```

### Bước 3: Gỡ Cài Đặt Tempo

```bash
helm uninstall tempo
```

### Bước 4: Gỡ Cài Đặt Loki

```bash
helm uninstall loki
```

### Bước 5: Gỡ Cài Đặt Prometheus

```bash
helm uninstall prometheus
```

Đợi quá trình gỡ cài đặt hoàn tất trước khi tiếp tục.

### Bước 6: Gỡ Cài Đặt Kafka

```bash
helm uninstall kafka
```

### Bước 7: Gỡ Cài Đặt Keycloak

```bash
helm uninstall keycloak
```

### Bước 8: Xác Minh Các Helm Releases

Sau khi gỡ cài đặt tất cả các thành phần, hãy xác minh rằng không còn release nào:

```bash
helm ls
```

Kết quả đầu ra không nên hiển thị bất kỳ release nào, xác nhận rằng tất cả các cài đặt dựa trên Helm đã được xóa.

## Gỡ Cài Đặt Discovery Server

Discovery Server được triển khai bằng các file manifest của Kubernetes, không phải Helm, do đó cần một cách tiếp cận gỡ cài đặt khác.

### Di Chuyển Đến Thư Mục Kubernetes

```bash
cd kubernetes
```

### Xóa Bằng Kubectl

```bash
kubectl delete -f <tên-file-manifest>
```

Thay thế `<tên-file-manifest>` bằng tên thực tế của file manifest Discovery Server của bạn.

## Xác Minh Việc Gỡ Cài Đặt Hoàn Toàn

Trước khi xóa cluster, hãy xác minh rằng tất cả tài nguyên đã được xóa:

### Kiểm Tra Workloads

Điều hướng đến phần Kubernetes workloads trong Google Cloud Console. Xác minh rằng tất cả workloads đã trống.

### Kiểm Tra Services

Điều hướng đến phần Services. Đảm bảo tất cả services đã được xóa.

### Kiểm Tra Secrets và ConfigMaps

Điều hướng đến các phần Secrets và ConfigMaps. Xác nhận rằng tất cả tài nguyên liên quan đến các triển khai của bạn đã được xóa.

## Xóa Kubernetes Cluster

Sau khi tất cả các thành phần đã được gỡ cài đặt và xác minh, hãy tiến hành xóa cluster:

### Bước 1: Điều Hướng Đến Clusters

Trong Google Cloud Console, điều hướng đến trang Kubernetes Engine > Clusters.

### Bước 2: Chọn Cluster Của Bạn

Chọn cluster bạn muốn xóa (ví dụ: `cluster-one`).

### Bước 3: Xóa Cluster

1. Nhấp vào nút **Delete**
2. Một hộp thoại xác nhận sẽ xuất hiện
3. Nhập tên cluster của bạn (ví dụ: `cluster-one`) để xác nhận
4. Nhấp vào nút **Delete** để bắt đầu quá trình xóa

### Bước 4: Đợi Quá Trình Xóa

Quá trình xóa cluster mất khoảng 2-3 phút. Hãy đợi quá trình hoàn tất.

### Bước 5: Xác Minh Việc Xóa

Sau khi xóa, trang clusters nên trống rỗng, xác nhận rằng Kubernetes cluster của bạn đã được xóa vĩnh viễn.

## Các Cân Nhắc Về Chi Phí

- **Thời Gian Sử Dụng**: Cluster được sử dụng trong khoảng 1 giờ
- **Chi Phí Ước Tính**: $0.30 - $0.50 (cho cả tài khoản miễn phí và trả phí)
- **Quan Trọng**: Luôn xóa cluster của bạn sau khi hoàn thành công việc để tránh các khoản phí bất ngờ

## Các Thực Hành Tốt Nhất

1. **Luôn Dọn Dẹp**: Tạo thói quen xóa tài nguyên ngay lập tức sau khi hoàn thành công việc
2. **Xác Minh Việc Xóa**: Luôn xác nhận rằng các cluster đã được xóa hoàn toàn trước khi đóng console
3. **Theo Dõi Hóa Đơn**: Kiểm tra bảng điều khiển thanh toán Google Cloud thường xuyên
4. **Thiết Lập Cảnh Báo**: Cấu hình các cảnh báo thanh toán để thông báo cho bạn về các khoản phí bất ngờ

## Những Điểm Chính Cần Nhớ

- Quy trình triển khai và quản lý nhất quán giữa các Kubernetes clusters cục bộ và trên cloud
- Các lệnh giống nhau hoạt động trên các môi trường Kubernetes khác nhau
- Việc dọn dẹp đúng cách là cần thiết cho quản lý chi phí
- Cả Helm releases và các tài nguyên được triển khai bằng kubectl cần được xóa riêng biệt

## Kết Luận

Bạn đã triển khai, xác thực và dọn dẹp thành công các microservices từ Google Cloud Kubernetes cluster. Quy trình được trình bày ở đây áp dụng cho dịch vụ Kubernetes của bất kỳ nhà cung cấp cloud nào, đảm bảo bạn có kỹ năng để quản lý các triển khai microservices trên các nền tảng khác nhau.

## Các Bước Tiếp Theo

Tiếp tục đến phần tiếp theo để khám phá thêm các chủ đề nâng cao về triển khai và quản lý microservices.




FILE: 87-kubernetes-ingress-and-service-types-introduction.md


# Kubernetes Ingress và Các Loại Service Nâng Cao

## Giới Thiệu

Phần này tập trung vào các khái niệm DevOps nâng cao thường được áp dụng trong môi trường microservices production thực tế. Mặc dù các lập trình viên không cần phải học chi tiết các khái niệm này, nhưng việc hiểu ở mức độ tổng quan sẽ mang lại lợi thế đáng kể trong các buổi phỏng vấn về microservices và công việc hàng ngày.

## Tại Sao Cần Học Các Khái Niệm DevOps Nâng Cao?

Khi tham gia phỏng vấn về microservices, ứng viên thường trả lời câu hỏi từ góc độ lập trình viên. Tuy nhiên, nếu bạn có thể cung cấp thêm những hiểu biết về các thực tiễn trong môi trường production sử dụng các khái niệm DevOps khác nhau, bạn chắc chắn sẽ gây ấn tượng với người phỏng vấn nhờ kiến thức rộng hơn của mình.

## Tổng Quan Về Các Loại Service Trong Kubernetes

Chúng ta đã học cách expose microservices bằng cách sử dụng các đối tượng Service trong Kubernetes. Tài liệu chính thức của Kubernetes mô tả nhiều loại service:

### Các Loại Service Phổ Biến
- **ClusterIP**: Giao tiếp nội bộ trong cluster (mặc định)
- **NodePort**: Expose service trên IP của mỗi Node tại một cổng tĩnh
- **LoadBalancer**: Expose service ra bên ngoài sử dụng load balancer của cloud provider

### Loại Service ExternalName

Ngoài ba loại service phổ biến, Kubernetes còn cung cấp loại service **ExternalName**.

#### Trường Hợp Sử Dụng ExternalName
ExternalName được sử dụng khi bạn muốn ánh xạ service của mình đến một tên DNS hoặc tên miền mà tổ chức của bạn sở hữu. Loại service này cung cấp tính linh hoạt cho các quản trị viên Kubernetes để ánh xạ các service đến các tên miền cụ thể.

#### Lợi Ích
- Các ứng dụng client có thể đơn giản chỉ cần forward request đến tên miền được cung cấp
- Loại service ExternalName xử lý việc chuyển tiếp request đến pod hoặc container tương ứng trong Kubernetes cluster
- Cung cấp sự trừu tượng hóa giữa DNS bên ngoài và định tuyến service nội bộ

## Giới Thiệu Về Kubernetes Ingress

### Ingress Là Gì?

Ingress là một cách khác để expose microservices ra ngoài Kubernetes cluster. Tuy nhiên, điều quan trọng cần hiểu là:

- **Ingress KHÔNG phải là một loại service**
- Ingress là một khái niệm và đối tượng riêng biệt trong Kubernetes
- Nó xuất hiện như một chủ đề riêng trong tài liệu chính thức của Kubernetes (không nằm trong các loại Service)

### Ingress vs LoadBalancer Service

Cả Ingress và LoadBalancer service type đều có thể expose microservices ra ngoài Kubernetes cluster, nhưng chúng phục vụ các mục đích khác nhau và có những đặc điểm riêng biệt:

| Khía Cạnh | LoadBalancer Service | Ingress |
|-----------|---------------------|---------|
| Loại | Loại service | Đối tượng Kubernetes riêng biệt |
| Mục đích | Expose một service duy nhất | Có thể expose nhiều service |
| Định tuyến | Đơn giản dựa trên port | Quy tắc định tuyến nâng cao (path, host-based) |
| Trường hợp sử dụng | Expose service riêng lẻ | Định tuyến cấp ứng dụng |

### Sự Khác Biệt Chính

Sự khác biệt chính là trong khi LoadBalancer là một loại service, Ingress là một khái niệm Kubernetes độc lập cung cấp khả năng định tuyến phức tạp hơn để expose nhiều service thông qua một điểm vào duy nhất.

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu vào:
- Các khái niệm và kiến trúc Ingress chi tiết
- Cách cấu hình các tài nguyên Ingress
- Các ví dụ thực tế về việc sử dụng Ingress
- Best practices cho môi trường production

## Tóm Tắt

- Kiến thức DevOps nâng cao mang lại lợi thế trong phỏng vấn và công việc thực tế
- Kubernetes cung cấp nhiều loại service: ClusterIP, NodePort, LoadBalancer và ExternalName
- Loại service ExternalName ánh xạ các service đến tên miền của tổ chức
- Ingress là một khái niệm riêng biệt với các loại Service
- Ingress cung cấp khả năng định tuyến nâng cao để expose microservices

---

*Tài liệu này đề cập đến phần giới thiệu về Kubernetes Ingress và các loại service nâng cao như một phần của loạt bài về microservices DevOps.*




FILE: 88-kubernetes-ingress-vs-spring-cloud-gateway.md


# Kubernetes Ingress: Hiểu về Ingress và Vai trò của nó trong Kiến trúc Microservices

## Giới thiệu

Trong bài giảng này, chúng ta sẽ tìm hiểu sâu về Kubernetes Ingress và so sánh nó với các phương pháp khác để expose microservices ra bên ngoài.

## LoadBalancer Service Type vs Kubernetes Ingress

### LoadBalancer Service Type

Khi bạn sử dụng service type là LoadBalancer, bạn đang expose một microservice cụ thể ra bên ngoài Kubernetes cluster. Mỗi microservice với LoadBalancer service type sẽ có:

- Địa chỉ IP public riêng
- LoadBalancer riêng được cung cấp bởi cloud provider
- Cấu hình expose riêng cho từng service

**Ví dụ:** Nếu bạn có 5 microservices với LoadBalancer service type, bạn sẽ có 5 địa chỉ IP public khác nhau và 5 LoadBalancer riêng biệt.

### Nhu cầu về Một Điểm Truy cập Duy nhất

Đôi khi chúng ta cần một **điểm truy cập duy nhất** vào Kubernetes cluster có khả năng:
- Chuyển tiếp tất cả các request từ bên ngoài đến container hoặc microservice phù hợp
- Hoạt động như một gateway tập trung để quản lý traffic

## Kubernetes Ingress là gì?

**Kubernetes Ingress** expose các route HTTP và HTTPS từ bên ngoài cluster đến các services bên trong cluster. Nó hoạt động như một edge server trong kiến trúc microservices của bạn.

### Các Khả năng Chính của Ingress

1. **Traffic Routing** - Định tuyến traffic dựa trên các rules được định nghĩa trong Ingress resource
2. **Load Balancing** - Phân phối traffic giữa nhiều instances
3. **SSL/TLS Termination** - Xử lý các kết nối bảo mật
4. **Name-based Virtual Hosting** - Hỗ trợ nhiều domains
5. **Authentication & Authorization** - Có thể tích hợp với các sản phẩm OAuth2/OIDC như Keycloak hoặc Okta

## Spring Cloud Gateway vs Kubernetes Ingress

### Phương pháp Spring Cloud Gateway

**Spring Cloud Gateway** là phương pháp tập trung vào developer, trong đó:
- Developers xây dựng ứng dụng Spring Boot sử dụng dependencies của Spring Cloud Gateway
- Developers tự implement các cross-cutting concerns
- Cung cấp tính linh hoạt để viết custom business logic bằng Java
- Hiện đang hoạt động như edge server trong mạng microservice của chúng ta

### Phương pháp Kubernetes Ingress

**Kubernetes Ingress** là phương pháp tập trung vào infrastructure, trong đó:
- DevOps team cấu hình routing rules một cách declarative
- Các khả năng built-in xử lý các cross-cutting concerns phổ biến
- Được quản lý ở cấp độ Kubernetes cluster

### Khi nào nên Chọn từng Phương pháp?

#### Chọn Spring Cloud Gateway khi:
1. Bạn có các developers tài năng có khả năng xây dựng edge servers phức tạp
2. Bạn cần custom business logic mà Kubernetes Ingress không thể đáp ứng
3. Bạn cần tính linh hoạt của Java programming cho các kịch bản routing phức tạp

#### Chọn Kubernetes Ingress khi:
1. Bạn có các thành viên DevOps team có kinh nghiệm và hiểu sâu về Kubernetes
2. Các yêu cầu routing của bạn có thể được đáp ứng bằng declarative configurations
3. Bạn muốn tận dụng các khả năng native của Kubernetes

### Các Yếu tố Quyết định Chính

Sự lựa chọn phụ thuộc vào:
- **Cấu trúc Team** - Chuyên môn của developer vs DevOps
- **Sở thích của Tổ chức** - Bạn muốn đặt trách nhiệm ở đâu
- **Yêu cầu Business** - Độ phức tạp của routing logic cần thiết

> **Lưu ý:** Cả hai phương pháp đều đạt được cùng một mục tiêu. Quyết định phụ thuộc vào việc bạn muốn developers hay DevOps team members sở hữu trách nhiệm này.

## Hiểu về Ingress Resources

### Cấu hình Ingress Mẫu

```yaml
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /accounts
            backend:
              service:
                name: account-service
                port:
                  number: 80
```

### Các Thành phần Cấu hình

- **kind: Ingress** - Chỉ ra đây là một Ingress resource
- **metadata.name** - Tên của Ingress resource
- **spec.rules** - Định nghĩa các routing rules
  - **host** - Hostname cơ sở của tổ chức bạn
  - **paths** - Các cấu hình routing dựa trên path
  - **backend.service** - Service đích bên trong cluster

> **Quan trọng:** Bạn không cần phải nhớ các cấu hình này. Đây chủ yếu là trách nhiệm của các thành viên DevOps team hoặc Kubernetes administrators.

## Ingress Controller

### Ingress Controller là gì?

**Ingress Controller** là một component có nhiệm vụ:
- Implement các routing rules được định nghĩa trong Ingress resources
- Theo dõi các Ingress resources và cấu hình các network components tương ứng
- Phải được cài đặt và cấu hình trong Kubernetes cluster của bạn

**Quan trọng:** Mặc định, Ingress resources không thể hoạt động nếu không có Ingress Controller.

### Các Ingress Controllers Phổ biến

1. **NGINX Ingress Controller** - Được sử dụng phổ biến nhất, open-source
2. **Traefik** - Reverse proxy và load balancer HTTP hiện đại
3. **HAProxy Ingress** - Load balancer hiệu suất cao

Kubernetes chính thức hỗ trợ hơn 30 Ingress Controllers khác nhau. Các tổ chức lựa chọn dựa trên yêu cầu cụ thể của họ.

> **Lưu ý:** NGINX Ingress Controller là lựa chọn phổ biến nhất vì nó là open-source và được maintain bởi NGINX team.

## Luồng Traffic với Kubernetes Ingress

### Tổng quan Kiến trúc

```
External Client (Client Bên ngoài)
    ↓
Ingress-Managed Load Balancer
    ↓
Ingress Controller (có thể có nhiều instances)
    ↓
Service (ClusterIP)
    ↓
Pod
    ↓
Container (Accounts/Loans/Cards)
```

### Luồng Chi tiết

1. **Triển khai Microservices**
   - Containers (accounts, loans, cards) chạy bên trong pods
   - Services được expose sử dụng ClusterIP (chỉ internal)
   - Không thể truy cập trực tiếp từ bên ngoài cluster

2. **Service Layer**
   - Mỗi microservice có một Service object tương ứng
   - Services chuyển tiếp requests đến các containers phù hợp
   - Ví dụ: Account Service → Account Container

3. **Ingress Layer**
   - External clients gửi requests đến Ingress-managed Load Balancer
   - Load Balancer chuyển tiếp đến một trong các Ingress Controller instances
   - Ingress Controller áp dụng các routing rules

4. **Ví dụ về Routing Rules**
   - `example.com/accounts` → Account Service → Account Container
   - `example.com/loans` → Loan Service → Loan Container
   - `example.com/cards` → Card Service → Card Container

### Load Balancing

Các tổ chức có thể triển khai nhiều Ingress Controller instances để đảm bảo high availability. Trong trường hợp này:
- Một Ingress-managed Load Balancer phân phối traffic giữa các Ingress Controller instances
- Mỗi controller có thể xử lý requests một cách độc lập

## So sánh với Spring Cloud Gateway

Cả hai phương pháp đều tương tự ở chỗ:
- Hoạt động như một edge server cho Kubernetes cluster
- Phục vụ như điểm truy cập cho external traffic
- Xử lý routing và quản lý traffic

Sự khác biệt chính là **ai quản lý và cấu hình** edge server:
- **Spring Cloud Gateway**: Được quản lý bởi developers
- **Kubernetes Ingress**: Được quản lý bởi DevOps/Infrastructure team

## Tóm tắt

- **Kubernetes Ingress** cung cấp một cách native của Kubernetes để expose services
- **Ingress Controller** là cần thiết để implement Ingress rules
- Lựa chọn giữa Spring Cloud Gateway và Kubernetes Ingress dựa trên:
  - Chuyên môn và cấu trúc team
  - Độ phức tạp của business logic
  - Sở thích của tổ chức
- Cả hai phương pháp đều hợp lệ và đạt được cùng một mục tiêu
- Có nhiều Ingress Controllers khác nhau để đáp ứng các yêu cầu khác nhau

## Các Bước Tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá thêm các chi tiết về cấu hình Kubernetes Ingress và triển khai thực tế.

---

*Tài liệu này được tạo dựa trên bài giảng kỹ thuật về Kubernetes Ingress và kiến trúc microservices với Spring Boot.*




FILE: 89-kubernetes-ingress-benefits-and-traffic-management.md


# Kubernetes Ingress: Lợi Ích và Quản Lý Lưu Lượng

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá lý do tại sao các tổ chức nên sử dụng Kubernetes Ingress và hiểu những lợi ích mà nó mang lại cho kiến trúc microservices.

## Lợi Ích của Kubernetes Ingress

### 1. Điểm Truy Cập Duy Nhất

Lợi thế chính đầu tiên của Ingress là nó hoạt động như một **điểm truy cập duy nhất** vào Kubernetes cluster của bạn. Nó đóng vai trò như một edge server thông qua đó bạn có thể cấu hình quyền truy cập cho nhiều microservices trong cluster. Điều này giúp đơn giản hóa việc quản lý quyền truy cập từ bên ngoài vào các microservices của bạn.

> **Lưu ý:** Spring Cloud Gateway cũng cung cấp lợi thế tương tự. Không có cách tiếp cận nào "tốt" hay "xấu" giữa Spring Cloud Gateway và Kubernetes Ingress - nó phụ thuộc vào cấu trúc nhóm và kỹ năng kỹ thuật của tổ chức bạn.

### 2. Chấm Dứt TLS/SSL

Kubernetes Ingress có khả năng **chấm dứt TLS/SSL (TLS/SSL termination)**, điều này rất quan trọng cho bảo mật web.

#### Tại Sao Cần TLS/SSL?

- Tất cả các giao tiếp web sử dụng các giao thức bảo mật như TLS/SSL (bạn thấy HTTPS trên trình duyệt)
- Ngăn chặn việc đánh cắp dữ liệu trong quá trình truyền từ client đến server
- Mã hóa dữ liệu để hacker không thể chặn và đánh cắp thông tin
- Chỉ có servers mới có thể giải mã dữ liệu đã được mã hóa

#### Cân Nhắc Về Hiệu Suất

Tuy nhiên, giao tiếp HTTPS/TLS đi kèm với **chi phí về hiệu suất**. Vì không có hacker nào có thể xâm nhập vào Kubernetes cluster của bạn ngoại trừ thông qua edge server, nên không cần thiết phải duy trì giao tiếp HTTPS bên trong cluster.

**Giải pháp:** Nhiều tổ chức chấm dứt giao tiếp TLS tại lớp Ingress:
- Tại edge server, HTTPS được chuyển đổi thành HTTP
- Khi dữ liệu vào cluster, nó di chuyển qua giao thức HTTP
- Điều này tránh các tác động nghiêm trọng đến hiệu suất trong khi vẫn duy trì bảo mật

### 3. Định Tuyến Dựa Trên Đường Dẫn và Host

Ingress hỗ trợ hai loại định tuyến:

#### Định Tuyến Dựa Trên Đường Dẫn (Path-Based Routing)
```
example.com/app1 → Service 1
example.com/app2 → Service 2
```

#### Định Tuyến Dựa Trên Host (Host-Based Routing)
```
app1.example.com → Service 1
app2.example.com → Service 2
```

Các tổ chức có thể định nghĩa các quy tắc định tuyến dựa trên cấu trúc subdomain và các mẫu truy cập của họ.

### 4. Cân Bằng Tải

Ingress có khả năng **cân bằng tải các yêu cầu** và phân phối lưu lượng truy cập giữa nhiều pods của cùng một service.

**Cách hoạt động:**
1. Ingress chuyển tiếp yêu cầu đến ClusterIP service
2. ClusterIP service phân phối yêu cầu đến các pods có sẵn
3. Lưu lượng được cân bằng giữa các containers được triển khai trong các pods đó

### 5. Annotations Cho Cấu Hình Nâng Cao

Ingress hỗ trợ **annotations** cho phép các khả năng bổ sung:
- Quy tắc viết lại (Rewriting rules)
- Custom headers
- Xác thực và ủy quyền (Authentication và Authorization)
- Các cài đặt nâng cao khác

## Spring Cloud Gateway vs Kubernetes Ingress

### So Sánh Khả Năng

Cả hai giải pháp đều cung cấp các khả năng tương tự:

| Tính Năng | Spring Cloud Gateway | Kubernetes Ingress |
|-----------|---------------------|-------------------|
| Điểm Truy Cập Duy Nhất | ✓ | ✓ |
| Định Tuyến Theo Đường Dẫn | ✓ | ✓ |
| Định Tuyến Theo Host | ✓ | ✓ |
| Cân Bằng Tải | ✓ | ✓ |
| Chấm Dứt TLS/SSL | ✓ | ✓ |
| Xác Thực | ✓ | ✓ |
| Cross-Cutting Concerns | ✓ | ✓ |

### Lựa Chọn Giữa Chúng

Sự lựa chọn phụ thuộc vào:
- Quyết định của kiến trúc sư dự án
- Sở thích của ban lãnh đạo dự án
- Kỹ năng kỹ thuật của nhóm
- Cấu trúc tổ chức

**Quan trọng:** Là các developer, chúng ta nên sẵn sàng làm việc với cả hai cách tiếp cận dựa trên yêu cầu của tổ chức.

## Ingress Controller vs Load Balancer Service

Cả hai đều có thể expose microservices ra thế giới bên ngoài, nhưng chúng khác nhau về khả năng:

### Ingress Controller
- Khả năng định tuyến nâng cao
- Quản lý lưu lượng phức tạp
- Phù hợp cho các microservices quy mô lớn, quan trọng

### Load Balancer Service
- Thiết lập đơn giản hơn
- Chức năng expose cơ bản
- Phù hợp cho:
  - Các tổ chức nhỏ
  - Số lượng microservices hạn chế
  - Các microservices mức độ quan trọng thấp

## Các Loại Lưu Lượng và Thuật Ngữ

### Các Thuật Ngữ Quan Trọng Trong Thảo Luận Về Microservices

#### 1. Ingress Traffic
Lưu lượng **đi vào** một Kubernetes cluster.

#### 2. Egress Traffic
Lưu lượng **đi ra khỏi** một Kubernetes cluster (ngược lại với Ingress traffic).

#### 3. North-South Traffic
Thuật ngữ khác cho Ingress và Egress traffic - lưu lượng đi vào và ra khỏi cluster.

**Lưu ý:** Ingress controllers được thiết kế để xử lý North-South traffic (Ingress/Egress traffic).

### Còn Lưu Lượng Nội Bộ Thì Sao?

**Câu hỏi:** Nếu Ingress xử lý lưu lượng đi vào và ra khỏi cluster, thì lưu lượng giữa các microservices *bên trong* Kubernetes cluster thì sao?

**Trả lời:** Đây là lúc **Service Mesh** phát huy tác dụng.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá chi tiết về Service Mesh và hiểu cách nó quản lý giao tiếp microservice nội bộ trong các Kubernetes clusters.

## Góc Nhìn Của Developer

Là developers, bạn không cần phải học mọi thứ về Kubernetes Ingress - việc thiết lập Ingress thường là trách nhiệm của các quản trị viên Kubernetes. Tuy nhiên, hiểu những khái niệm này đảm bảo bạn đã chuẩn bị sẵn sàng khi:
- Các tổ chức chọn Kubernetes Ingress thay vì Spring Cloud Gateway
- Bạn cần tham gia vào các cuộc thảo luận về kiến trúc
- Bạn được yêu cầu làm việc với các hệ thống dựa trên Ingress

Luôn cập nhật thông tin và sẵn sàng cho mọi tình huống!

---

*Cảm ơn bạn, và hẹn gặp lại trong bài giảng tiếp theo!*




FILE: 9-role-based-authorization-demo-with-keycloak.md


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




FILE: 90-service-mesh-introduction-and-sidecar-pattern.md


# Giới Thiệu Service Mesh và Mô Hình Sidecar

## Tổng Quan

Tài liệu này trình bày các khái niệm cơ bản về Service Mesh trong môi trường Kubernetes, giải thích cách Service Mesh xử lý luồng east-west traffic giữa các microservices và triển khai mô hình sidecar để tách biệt logic nghiệp vụ khỏi các yêu cầu phi chức năng.

## North-South Traffic vs East-West Traffic

### North-South Traffic (Luồng Bắc-Nam)
- Luồng dữ liệu ra vào Kubernetes cluster
- Được xử lý bởi các **Ingress** controller
- Quản lý các yêu cầu từ client bên ngoài đến các service nội bộ

### East-West Traffic (Luồng Đông-Tây)
- Luồng dữ liệu giữa các service trong Kubernetes cluster
- Giao tiếp service-to-service
- Được quản lý bởi **Service Mesh**

## Service Mesh Là Gì?

**Service Mesh** là một lớp hạ tầng chuyên dụng để quản lý toàn bộ giao tiếp giữa các microservices trong các ứng dụng container hóa như Kubernetes cluster.

### Các Khả Năng Chính

Service Mesh cung cấp các tính năng toàn diện bao gồm:

1. **Service Discovery** - Tự động phát hiện các service instance
2. **Load Balancing** - Phân phối lưu lượng thông minh
3. **Circuit Breaking** - Khả năng chịu lỗi và xử lý sự cố
4. **Fault Tolerance** - Triển khai các mô hình phục hồi
5. **Metrics và Tracing** - Quan sát và giám sát
6. **Security** - Bảo mật giao tiếp giữa các service

### Lợi Ích Bảo Mật

Service Mesh cung cấp bảo mật đa lớp:

- **Lớp Đầu Tiên**: Các microservices không được phơi bày ra thế giới bên ngoài
  - Chỉ có thể truy cập bởi các ứng dụng nội bộ hoặc edge servers
  - Tường lửa bảo vệ xung quanh tất cả microservices
  
- **Lớp Thứ Hai**: Service Mesh cung cấp bảo mật bổ sung
  - Bảo mật east-west traffic giữa các service nội bộ
  - Chỉ edge servers (như Spring Cloud Gateway) cần bảo mật OAuth2/OpenID

## Service Mesh vs Phương Pháp Truyền Thống

### Phương Pháp Truyền Thống (Không Có Service Mesh)

Trong kiến trúc microservices truyền thống:

```
┌─────────────────────────────────────┐
│   Container Microservice            │
├─────────────────────────────────────┤
│ • Logic nghiệp vụ                   │
│ • Metrics (Prometheus)              │
│ • Tracing (Grafana)                 │
│ • Resiliency (Resilience4j)         │
│ • Service Discovery (Eureka)        │
│ • Cấu hình bảo mật                  │
└─────────────────────────────────────┘
```

**Nhược Điểm:**
- Mỗi microservice chứa nhiều code và cấu hình không liên quan đến nghiệp vụ
- Thay đổi về security, tracing, hoặc resiliency cần cập nhật trên tất cả microservices
- Developer phải quản lý thay đổi nhất quán trên tất cả services
- Làm sao nhãng sự tập trung của developer khỏi logic nghiệp vụ cốt lõi

### Phương Pháp Service Mesh

Với triển khai Service Mesh:

```
┌──────────────────────────────────────────┐
│              Pod                         │
├────────────────────┬─────────────────────┤
│  Container Chính   │  Sidecar Proxy      │
├────────────────────┼─────────────────────┤
│ • Logic Nghiệp Vụ  │ • Security          │
│   DUY NHẤT         │ • Metrics           │
│                    │ • Tracing           │
│                    │ • Resiliency        │
│                    │ • Load Balancing    │
└────────────────────┴─────────────────────┘
```

**Ưu Điểm:**
- Developer chỉ tập trung vào logic nghiệp vụ
- Các yêu cầu phi chức năng được xử lý bởi service mesh
- Cấu hình và quản lý tập trung
- Triển khai nhất quán trên tất cả services

## Mô Hình Sidecar Pattern

### Nguồn Gốc Khái Niệm

Mô hình sidecar được lấy cảm hứng từ xe phụ gắn bên xe máy:
- Xe máy (container chính) có động cơ (logic nghiệp vụ)
- Xe phụ cung cấp chức năng bổ sung mà không ảnh hưởng đến mục đích cốt lõi
- Cả hai hoạt động cùng nhau và chia sẻ cùng một vòng đời

### Đặc Điểm Của Sidecar Container

1. **Gắn Vào Parent**: Sidecar container được gắn vào container ứng dụng cha
2. **Tính Năng Hỗ Trợ**: Cung cấp security, metrics, tracing, resiliency và các tính năng hỗ trợ khác
3. **Vòng Đời Chung**: Được tạo và hủy cùng với container cha
4. **Runtime Độc Lập**: Độc lập với ứng dụng chính về:
   - Môi trường runtime
   - Ngôn ngữ lập trình
   - Technology stack

### Ví Dụ

Nếu các microservices của bạn (Accounts, Loans, Cards) được phát triển bằng Java:
- Các container chính cần JDK/JRE để chạy
- Các sidecar container có thể sử dụng bất kỳ ngôn ngữ hoặc môi trường runtime nào
- Sự độc lập này cung cấp tính linh hoạt trong triển khai

## Khi Nào Nên Sử Dụng Service Mesh

### Được Khuyến Nghị Cho:
- Các tổ chức có đủ chuyên môn DevOps
- Các dự án có ngân sách đầy đủ cho hạ tầng
- Các ứng dụng có độ nghiêm trọng cao cần tính năng cấp doanh nghiệp
- Kiến trúc microservices quy mô lớn

### Không Bắt Buộc Cho:
- Các tổ chức không có chuyên môn DevOps để thiết lập service mesh
- Các dự án hạn chế ngân sách
- Các microservices có độ nghiêm trọng thấp
- Các ứng dụng quy mô nhỏ

### Lưu Ý Quan Trọng

Ngay cả khi tổ chức của bạn sử dụng Service Mesh, việc hiểu các phương pháp truyền thống vẫn rất quan trọng vì:
- Không phải tất cả tổ chức đều áp dụng Service Mesh do độ phức tạp hoặc chi phí
- Một số dự án có thể không cần khả năng của Service Mesh
- Bạn cần chuẩn bị cho nhiều kịch bản kiến trúc khác nhau
- Hiểu các kiến thức nền tảng giúp bạn trở thành developer tốt hơn

## Các Cân Nhắc Khi Triển Khai

### Đối Với Developers
- Tập trung vào logic nghiệp vụ khi có Service Mesh
- Hiểu các mô hình truyền thống để có tính linh hoạt
- Sẵn sàng triển khai các yêu cầu phi chức năng nếu không sử dụng Service Mesh

### Đối Với Đội Ngũ DevOps
- Thiết lập Service Mesh cần chuyên môn kỹ thuật đáng kể
- Cấu hình và bảo trì phức tạp
- Cần đầu tư hạ tầng lớn
- Phải đánh giá lợi ích-chi phí cho từng dự án

## So Sánh Công Nghệ

Các triển khai truyền thống sử dụng:
- **Prometheus & Grafana**: Metrics và tracing
- **Resilience4j**: Fault tolerance và circuit breaking
- **Eureka Server**: Client-side service discovery
- **Kubernetes Discovery**: Server-side service discovery
- **Spring Security & OAuth2**: Bảo mật tại edge servers

Service Mesh cung cấp tất cả các khả năng này thông qua một lớp hạ tầng thống nhất.

## Kết Luận

Service Mesh đại diện cho sự chuyển đổi mô hình trong kiến trúc microservices bằng cách:
- Tách biệt logic nghiệp vụ khỏi các vấn đề hạ tầng
- Cung cấp các tính năng cấp doanh nghiệp sẵn có
- Cho phép developers tập trung vào chức năng cốt lõi
- Yêu cầu chuyên môn DevOps chuyên biệt để thiết lập và bảo trì

Hiểu cả Service Mesh và các phương pháp truyền thống đảm bảo bạn sẵn sàng cho bất kỳ môi trường microservices nào.

---

*Chủ Đề Tiếp Theo: Các Thành Phần Kỹ Thuật Của Service Mesh - Hiểu cách Service Mesh thực hiện các khả năng của nó*




FILE: 91-service-mesh-components-and-architecture.md


# Các Thành Phần và Kiến Trúc của Service Mesh

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ tìm hiểu các thành phần quan trọng của service mesh, những thành phần chịu trách nhiệm xử lý các yêu cầu phi nghiệp vụ trong kiến trúc microservices.

## Các Thành Phần Cốt Lõi của Service Mesh

Các triển khai service mesh thường bao gồm hai thành phần quan trọng:

### 1. Data Plane (Tầng Dữ Liệu)

**Data plane** chịu trách nhiệm định tuyến lưu lượng giữa các microservices.

**Đặc điểm chính:**
- Xử lý tất cả lưu lượng truy cập đến các container của bạn
- Sử dụng proxy để quản lý giao tiếp
- Mỗi instance microservice đi kèm với một proxy sidecar container nhẹ
- Các proxy chặn mỗi request và response đến container microservice thực tế
- Data plane là tầng mà service mesh triển khai tất cả các sidecar container

### 2. Control Plane (Tầng Điều Khiển)

**Control plane** chịu trách nhiệm cấu hình, quản lý và giám sát tất cả các proxy.

**Tính năng chính:**
- Tạo các sidecar container trong data plane mỗi khi có pod hoặc container mới được tạo
- Bao gồm các thành phần quan trọng như:
  - Control-plane API
  - Service discovery (Khám phá dịch vụ)
  - Configuration management (Quản lý cấu hình)

## Các Triển Khai Service Mesh Phổ Biến

Service mesh là một khái niệm hoặc đặc tả. Để triển khai nó trong các deployment microservice, chúng ta sử dụng một trong các implementation có sẵn:

- **Istio** (phổ biến nhất)
- **Linkerd** (phổ biến nhất)
- **Consul**
- **Kong**
- **AWS App Mesh**
- **Azure Service Mesh**

Việc lựa chọn service mesh phụ thuộc vào yêu cầu cụ thể của tổ chức và ngân sách.

## Service Mesh trong Kubernetes

### Tổng Quan Kiến Trúc

Khi sử dụng một triển khai service mesh như Istio trong Kubernetes cluster:

1. **Kubernetes Cluster** chứa các pod với các microservices (ví dụ: accounts, loans, và cards microservices)
2. **Main Containers** chạy logic nghiệp vụ cốt lõi
3. **Sidecar Proxies** được tự động tạo bởi Istio control plane cho mỗi pod
4. Trong Istio, các sidecar proxy này được gọi là **Envoy proxies**

### Luồng Lưu Lượng

```
Request Từ Bên Ngoài → Sidecar Container (Envoy Proxy) → Main Container
```

**Cách hoạt động:**
- Lưu lượng không bao giờ đi trực tiếp đến pod thực tế
- Lưu lượng trước tiên đi đến sidecar container (Envoy proxy)
- Envoy proxy thực thi logic liên quan đến:
  - Giám sát bảo mật
  - Thu thập metrics
  - Các yêu cầu phi nghiệp vụ khác
- Cuối cùng, request được chuyển tiếp đến container thực tế

Mô hình này áp dụng cho tất cả các microservices (accounts, loans, cards, v.v.).

### Tầng Data Plane

Tầng mà tất cả các Envoy proxy (sidecar container) được triển khai được gọi là **Istio data plane**. Lý do là vì chúng chịu trách nhiệm quản lý tất cả lưu lượng đến các microservices của bạn.

## Tài Nguyên Học Tập

Để biết thêm chi tiết về service mesh, hãy truy cập các trang web triển khai như:
- **Istio**: [https://istio.io](https://istio.io)
  - Tuyên bố đơn giản hóa observability, traffic management, security và policy
  - Cung cấp tài liệu mở rộng về khả năng và triển khai

## Tại Sao Developer Nên Biết Về Service Mesh

Mặc dù service mesh là một kỹ năng kỹ thuật riêng biệt và các developer không cần phải là chuyên gia, nhưng việc hiểu các khái niệm này rất quan trọng:

### Lợi Ích Cho Developer:
- Giúp các cuộc thảo luận về chủ đề microservices nâng cao dễ dàng hơn
- Chuẩn bị cho các câu hỏi phỏng vấn về môi trường production
- Giúp hiểu kiến trúc tổng thể của microservices hiện đại

### Những Gì Bạn Nên Biết:
- Service mesh là gì?
- Khả năng của nó là gì?
- Nó phù hợp như thế nào trong hệ sinh thái microservices

### Các Khái Niệm Nâng Cao Cần Biết:
- Ingress
- Service mesh
- Sidecar containers

## Bảo Mật Với Service Mesh

### Mutual TLS (mTLS)

Service mesh có thể bảo mật giao tiếp service-to-service nội bộ trong cluster bằng cách sử dụng **Mutual TLS (mTLS)**.

**Tại sao điều này quan trọng:**
- Bạn có thể bảo mật edge server với OAuth2 và Spring Security
- Nhưng còn các microservices nội bộ trong Kubernetes cluster của bạn thì sao?
- **Câu trả lời là mTLS**

Đây là một khái niệm quan trọng có thể xuất hiện trong các cuộc phỏng vấn khi thảo luận về kiến trúc bảo mật microservices.

## Kết Luận

Service mesh cung cấp một cách mạnh mẽ để xử lý các cross-cutting concerns trong kiến trúc microservices mà không thêm độ phức tạp vào logic nghiệp vụ của bạn. Hiểu các thành phần của nó (data plane và control plane) và các tính năng bảo mật (như mTLS) là điều cần thiết cho các developer microservices hiện đại.

---

*Bài giảng này cung cấp nền tảng để hiểu kiến trúc service mesh. Bài giảng tiếp theo sẽ đi sâu hơn vào mTLS và bảo mật giao tiếp microservices nội bộ.*




FILE: 92-understanding-mtls-and-tls-in-microservices.md


# Hiểu về mTLS và TLS trong Microservices

## Giới thiệu

Bài giảng này giải thích mTLS (Mutual Transport Layer Security) là gì và tại sao nó lại quan trọng để bảo mật giao tiếp giữa các microservices. Để hiểu đầy đủ về mTLS, trước tiên chúng ta cần nắm vững cách TLS hoạt động, vì mTLS là một biến thể của TLS.

## TLS là gì?

**TLS (Transport Layer Security)** là một giao thức mã hóa đã thay thế SSL (Secure Socket Layer) đã bị loại bỏ và hiện đang được sử dụng trong giao tiếp HTTPS.

### Tại sao TLS quan trọng

Khi một client (như trình duyệt) giao tiếp với máy chủ backend, chúng cần giao tiếp trong môi trường bảo mật bằng định dạng mã hóa. Nếu không có giao thức HTTPS:

- Bất kỳ ai lắng nghe lưu lượng mạng đều có thể thấy văn bản thuần túy di chuyển từ trình duyệt đến máy chủ backend
- Dữ liệu nhạy cảm như thông tin thẻ tín dụng có thể dễ dàng bị đánh cắp trong quá trình truyền
- Không có cách nào xác minh danh tính của máy chủ

### Hạn chế của TLS trong Microservices

Mặc dù TLS bảo mật hiệu quả giao tiếp từ trình duyệt đến máy chủ, nhưng nó có những hạn chế đối với microservices:

- Trong TLS, chỉ có máy chủ backend (chủ sở hữu tên miền) chứng minh danh tính của mình thông qua chứng chỉ
- Microservices không sử dụng trình duyệt để giao tiếp - chúng sử dụng giao tiếp API
- Trong môi trường microservices, **cả hai microservices đều cần chứng minh danh tính của mình**
- TLS đơn thuần không thể bảo mật các microservices nội bộ trong cụm Kubernetes

## Hiểu về mTLS (Mutual TLS)

**mTLS (Mutual Transport Layer Security)** khắc phục những hạn chế của TLS bằng cách yêu cầu cả hai bên (cả hai ứng dụng) phải xác thực lẫn nhau trước khi giao tiếp có thể diễn ra.

### Môi trường Zero Trust (Không tin cậy)

mTLS thường được sử dụng trong **framework bảo mật không tin cậy (zero trust)**, trong đó:

- Mặc dù các microservices được triển khai trong cụm Kubernetes của riêng bạn, bạn không tin tưởng lưu lượng nội bộ theo mặc định
- Không có người dùng, thiết bị hoặc lưu lượng nào được tự động tin cậy
- Tất cả các thành phần phải chứng minh danh tính của chúng trước khi giao tiếp

### Tại sao Zero Trust quan trọng

Hãy xem xét những rủi ro bảo mật này:

1. **Lỗ hổng từ bên thứ ba**: Một thư viện bên thứ ba trong container của bạn có thể có lỗ hổng bảo mật, có khả năng để lộ lưu lượng không mã hóa
2. **Giao tiếp trái phép**: Một container microservice có thể cố gắng giao tiếp với container khác mà nó không được phép truy cập
3. **Mối đe dọa nội bộ**: Chỉ vì lưu lượng là nội bộ không có nghĩa là nó an toàn

## Cách TLS hoạt động

Trước khi hiểu mTLS, hãy xem xét quy trình TLS một cách chi tiết.

### Tổng quan về TLS

TLS được sử dụng rộng rãi trên internet để mã hóa. Bạn có thể nghe "SSL" và "TLS" được sử dụng thay thế cho nhau, nhưng TLS là tiêu chuẩn hiện tại - SSL đã bị loại bỏ do các vấn đề bảo mật.

### Certificate Authorities (Tổ chức phát hành chứng chỉ)

**Certificate Authorities (CAs)** là các tổ chức đáng tin cậy:

- Phát hành chứng chỉ cho các tổ chức sau khi xác minh quyền sở hữu tên miền
- Xác thực chứng chỉ được trình bày bởi máy chủ
- Cung cấp nền tảng tin cậy cho giao tiếp HTTPS

### Quy trình TLS Handshake

Hãy xem xét cách TLS bảo mật giao tiếp giữa trình duyệt và amazon.com:

#### Bước 1: TCP Handshake
Trình duyệt và máy chủ web thiết lập kết nối TCP để xác nhận không có vấn đề mạng.

#### Bước 2: Thông điệp Hello
Trình duyệt gửi thông điệp "hello" yêu cầu máy chủ chứng minh danh tính của nó.

#### Bước 3: Trình bày Chứng chỉ
Máy chủ web chia sẻ chứng chỉ của nó (chứa khóa công khai) với trình duyệt.

#### Bước 4: Xác thực Chứng chỉ
- Trình duyệt xác thực chứng chỉ với Certificate Authorities
- Nếu hợp lệ, trình duyệt hiển thị biểu tượng ổ khóa cho biết kết nối an toàn
- Nếu không hợp lệ, trình duyệt cảnh báo người dùng không nhập thông tin nhạy cảm

#### Bước 5: Thiết lập Mã hóa Bất đối xứng
Chứng chỉ chứa hai loại khóa:

- **Khóa Công khai (Public Key)**: Được chia sẻ với trình duyệt; được sử dụng để mã hóa dữ liệu
- **Khóa Riêng tư (Private Key)**: Được giữ bí mật bởi máy chủ; được sử dụng để giải mã dữ liệu

Điều này được gọi là **mã hóa bất đối xứng (asymmetric encryption)** vì mã hóa và giải mã sử dụng các thành phần khác nhau.

#### Bước 6: Tạo Session Key (Khóa phiên)
Trình duyệt tạo một **session key** và mã hóa nó bằng khóa công khai của máy chủ, sau đó gửi nó đến máy chủ. Ngay cả khi ai đó chặn khóa phiên được mã hóa này, họ cũng không thể giải mã nó nếu không có khóa riêng tư.

#### Bước 7: Giải mã Session Key
Máy chủ web giải mã khóa phiên bằng khóa riêng tư của nó và xác nhận đã nhận với trình duyệt.

#### Bước 8: Giao tiếp Mã hóa Đối xứng
Bây giờ cả hai bên đều có cùng một khóa phiên. Họ sử dụng nó cho giao tiếp dữ liệu thực tế, được gọi là **mã hóa đối xứng (symmetric encryption)** vì cùng một khóa được sử dụng cho cả mã hóa và giải mã.

### Tại sao chuyển từ Mã hóa Bất đối xứng sang Đối xứng?

Mã hóa bất đối xứng có những hạn chế cho giao tiếp đang diễn ra:

1. **Mã hóa một chiều**: Chỉ trình duyệt có thể gửi dữ liệu được mã hóa đến máy chủ
2. **Không giải mã phản hồi**: Trình duyệt không có khóa riêng tư để giải mã các phản hồi được mã hóa
3. **Chi phí hiệu suất**: Mã hóa bất đối xứng chậm hơn mã hóa đối xứng

Ưu điểm của mã hóa đối xứng:

- **Hiệu suất tốt hơn**: Nhanh hơn mã hóa bất đối xứng
- **Bảo mật hai chiều**: Cả hai bên đều có thể mã hóa và giải mã dữ liệu
- **Bí mật được chia sẻ**: Chỉ trình duyệt và máy chủ biết khóa phiên

### Xem TLS trong thực tế

Khi bạn truy cập bất kỳ trang web HTTPS nào (như amazon.com):

1. Trình duyệt xác thực chứng chỉ ở hậu trường
2. Biểu tượng ổ khóa xuất hiện cho biết kết nối an toàn
3. Bạn có thể nhấp vào ổ khóa để xem chi tiết chứng chỉ
4. Chứng chỉ cho thấy nó đã được xác thực và phát hành cho chủ sở hữu tên miền hợp pháp

### Mô hình Xác thực TLS

Trong TLS tiêu chuẩn:

- **Client (trình duyệt) yêu cầu máy chủ chứng minh danh tính của nó** thông qua chứng chỉ
- **Máy chủ không bao giờ yêu cầu trình duyệt chứng minh danh tính của nó**
- Người dùng chứng minh danh tính thông qua xác thực tên người dùng/mật khẩu
- Điều này hoạt động vì có hàng tỷ trình duyệt tồn tại - chứng chỉ cá nhân không thực tế

## Tại sao cần mTLS cho Microservices?

Mô hình TLS truyền thống không hoạt động cho giao tiếp ứng dụng với ứng dụng vì:

1. Cả hai ứng dụng đều là các bên tham gia quan trọng ngang nhau
2. Không có người dùng tham gia để cung cấp thông tin xác thực
3. Cả hai bên cần xác minh danh tính của nhau
4. Kiến trúc service mesh yêu cầu xác thực lẫn nhau

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách mTLS hoạt động trong thực tế với các triển khai service mesh trong môi trường Kubernetes.

## Tóm tắt

- **TLS** bảo mật giao tiếp từ trình duyệt đến máy chủ thông qua xác thực máy chủ dựa trên chứng chỉ
- **mTLS** mở rộng điều này bằng cách yêu cầu cả hai bên xác thực lẫn nhau
- **Bảo mật không tin cậy (Zero trust)** giả định không có lưu lượng nội bộ nào an toàn theo mặc định
- **Mã hóa bất đối xứng** được sử dụng cho handshake ban đầu và trao đổi khóa
- **Mã hóa đối xứng** được sử dụng cho giao tiếp dữ liệu thực tế do lợi ích về hiệu suất
- **mTLS là thiết yếu** để bảo mật giao tiếp microservice-to-microservice trong cụm Kubernetes

---

*Tài liệu này dựa trên bài giảng kỹ thuật về bảo mật microservices sử dụng Spring Boot và Kubernetes.*




FILE: 93-understanding-mtls-mutual-tls-in-microservices.md


# Hiểu về mTLS (Mutual TLS) trong Microservices

## Giới thiệu

Hướng dẫn này giải thích khái niệm Mutual TLS (mTLS) và sự khác biệt của nó so với TLS chuẩn trong bối cảnh kiến trúc microservices, đặc biệt là trong các Kubernetes cluster.

## mTLS là gì?

**Mutual TLS (mTLS)** là một phần mở rộng của giao thức TLS chuẩn, trong đó **cả hai bên** trong một giao tiếp phải chứng minh danh tính của họ bằng cách chia sẻ thông tin chứng chỉ hoặc khóa.

### Sự khác biệt chính: TLS vs mTLS

| Khía cạnh | TLS | mTLS |
|-----------|-----|------|
| **Xác thực** | Một chiều (server chứng minh danh tính với client) | Hai chiều (cả hai bên đều chứng minh danh tính) |
| **Trường hợp sử dụng** | Trình duyệt đến server (internet công cộng) | Giao tiếp service-to-service (mạng nội bộ) |
| **Yêu cầu chứng chỉ** | Chỉ server | Cả client và server |

### Khi nào sử dụng mTLS

- **Lưu lượng nội bộ** trong Kubernetes cluster
- **Chiến lược bảo mật Zero-Trust** trong kiến trúc microservices
- **Giao tiếp service-to-service** trong tổ chức
- **Không khuyến nghị** cho các trường hợp dựa trên trình duyệt (sử dụng TLS chuẩn thay thế)

## Quản lý Chứng chỉ trong mTLS

### Cách tiếp cận TLS truyền thống

- **Certificate Authority (CA)**: Nhà cung cấp bên thứ ba (ví dụ: Let's Encrypt, DigiCert)
- **Thời hạn**: Thường là 1 năm
- **Chi phí**: Chứng chỉ trả phí sau khi xác minh domain
- **Thách thức**: Không phù hợp cho microservices động

### Cách tiếp cận mTLS

Trong môi trường microservices, **tổ chức tự đóng vai trò là Certificate Authority** thông qua các thành phần service mesh như **Istio**.

#### Tại sao cần CA nội bộ?

1. **Tính động**: Microservice pod có thể bị hủy và tạo lại thường xuyên
2. **Tiết kiệm chi phí**: Không cần trả phí CA bên thứ ba cho mỗi chứng chỉ
3. **Khả năng mở rộng**: Dễ dàng cấp phát và quản lý nhiều chứng chỉ
4. **Tự động hóa**: Tự động cấp phát và gia hạn chứng chỉ

## mTLS hoạt động như thế nào trong Kubernetes

### Kịch bản: Giao tiếp Service-to-Service

Hãy xem xét cách mTLS bảo mật giao tiếp giữa hai microservices (Accounts và Loans) trong một Kubernetes cluster.

#### Không có mTLS (Không an toàn)

```
Accounts Microservice → Plain HTTP → Loans Microservice
```

**Rủi ro:**
- Giao tiếp không được mã hóa
- Dễ bị chặn bởi microservices độc hại hoặc thư viện bên thứ ba
- Không có xác minh danh tính

#### Với mTLS (An toàn)

```
Accounts Container → Sidecar Proxy → Mã hóa → Sidecar Proxy → Loans Container
```

### Quy trình mTLS từng bước

**Bước 1: Khởi tạo Request**
- Accounts microservice gửi HTTP request thông thường
- Sidecar proxy chặn lưu lượng

**Bước 2: TLS Handshake**
- Accounts sidecar proxy gửi thông điệp "hello" đến Loans sidecar proxy
- Hai sidecar proxy thực hiện TLS handshake

**Bước 3: Xác minh Danh tính**
- Accounts sidecar yêu cầu Loans sidecar chứng minh danh tính
- Loans sidecar phản hồi bằng chứng chỉ của nó

**Bước 4: Xác thực Chứng chỉ**
- Accounts sidecar xác thực chứng chỉ với Certificate Authority (Service Mesh Control Plane)
- Service mesh xác nhận tính hợp lệ của chứng chỉ

**Bước 5: Giao tiếp Mã hóa**
- Request được chuyển tiếp ở định dạng mã hóa
- Loans sidecar giải mã dữ liệu
- Dữ liệu đã giải mã được chuyển đến Loans container thực tế

### Điểm chính

- **Trong suốt với Ứng dụng**: Microservices không nhận biết quá trình mã hóa
- **Hai chiều**: Nếu Loans khởi tạo giao tiếp với Accounts, quá trình đảo ngược
- **Tự động**: Sidecar proxies xử lý tất cả các thao tác bảo mật

## Vai trò của Service Mesh

Service mesh (ví dụ: Istio, Linkerd) cung cấp:

1. **Cấp phát Chứng chỉ**: Tự động tạo chứng chỉ cho microservices mới
2. **Quản lý Chứng chỉ**: Chính sách hết hạn và gia hạn có thể cấu hình
3. **Áp dụng mTLS**: Quản lý giao tiếp an toàn giữa các services
4. **Không cần cấu hình**: Developer không cần triển khai mTLS thủ công

### Góc nhìn của Developer

Là một developer, bạn nên:
- ✅ Hiểu các khái niệm mTLS
- ✅ Nhận biết lợi ích và trường hợp sử dụng
- ❌ Không cần triển khai mTLS thủ công
- ❌ Không cần là chuyên gia về cấu hình service mesh

## Ưu điểm của mTLS

### 1. Xác thực Lẫn nhau
Cả client và server đều xác minh danh tính của nhau, đảm bảo giao tiếp đáng tin cậy.

### 2. Bảo vệ chống Giả mạo
- Không có thành phần trái phép nào có thể đánh cắp dữ liệu
- Yêu cầu chứng chỉ số hợp lệ cho giao tiếp
- Ngăn chặn tấn công man-in-the-middle

### 3. Kiểm soát Truy cập Chi tiết
- Định nghĩa microservices nào có thể giao tiếp với nhau
- Áp dụng các chính sách chi tiết
- Ngăn chặn các cuộc gọi service-to-service trái phép

### 4. Kháng cự với Thông tin đăng nhập bị xâm phạm
- Hoạt động như lớp bảo mật thứ hai ngoài service accounts
- Ngay cả khi thông tin đăng nhập bị đánh cắp, giao tiếp vẫn yêu cầu chứng chỉ hợp lệ
- Giảm thiểu tấn công brute force và đánh cắp thông tin đăng nhập

### 5. Quản lý Khóa Đơn giản
- CA nội bộ (service mesh) xử lý các thao tác chứng chỉ
- Không tốn chi phí cho việc cấp phát hoặc gia hạn chứng chỉ
- Dễ dàng xoay vòng và gia hạn chứng chỉ
- Có thể mở rộng cho bất kỳ số lượng microservices nào

### 6. Tuân thủ và Tiêu chuẩn
mTLS giúp tổ chức tuân thủ các tiêu chuẩn ngành:
- **GDPR** (Quy định Bảo vệ Dữ liệu Chung)
- **HIPAA** (Đạo luật Trách nhiệm và Khả năng chuyển đổi Bảo hiểm Y tế)
- **PCI DSS** (Tiêu chuẩn Bảo mật Dữ liệu Ngành Thẻ Thanh toán)

### 7. Khung Bảo mật Zero Trust
- Không có sự tin tưởng ngầm định, ngay cả trong mạng tổ chức
- Mọi giao tiếp đều yêu cầu chứng chỉ số hợp lệ
- Nguyên tắc "Không bao giờ tin tưởng, luôn xác minh"

## Thực hành Tốt nhất

1. **Sử dụng mTLS cho giao tiếp microservices nội bộ** trong Kubernetes cluster
2. **Sử dụng TLS chuẩn cho lưu lượng bên ngoài** (trình duyệt đến server)
3. **Tận dụng service mesh** cho triển khai mTLS tự động
4. **Cấu hình chính sách hết hạn chứng chỉ phù hợp**
5. **Giám sát xoay vòng chứng chỉ** và các quy trình gia hạn
6. **Triển khai chính sách kiểm soát truy cập chi tiết** giữa các services

## Kết luận

mTLS là một tính năng bảo mật quan trọng cho kiến trúc microservices hiện đại, cung cấp:
- Xác thực lẫn nhau giữa các services
- Giao tiếp được mã hóa
- Bảo vệ chống lại các mối đe dọa bảo mật khác nhau
- Quản lý chứng chỉ đơn giản ở quy mô lớn

Là một developer microservices nâng cao, việc hiểu các khái niệm mTLS là cần thiết, ngay cả khi bạn không cần phải là chuyên gia về cấu hình service mesh. Service mesh xử lý sự phức tạp trong khi bạn tập trung vào việc xây dựng các ứng dụng an toàn, có khả năng mở rộng.

## Điểm chính cần nhớ

- ✅ mTLS = Xác thực lẫn nhau giữa cả hai bên
- ✅ Sử dụng mTLS cho giao tiếp cluster nội bộ
- ✅ Service mesh hoạt động như Certificate Authority nội bộ
- ✅ Sidecar proxies xử lý mã hóa một cách trong suốt
- ✅ Thiết yếu cho kiến trúc bảo mật zero-trust
- ✅ Tuân thủ các tiêu chuẩn bảo mật ngành

---

**Các chủ đề liên quan:**
- Kiến thức cơ bản về TLS/SSL
- Bảo mật Kubernetes
- Service Mesh (Istio, Linkerd)
- Kiến trúc Zero Trust
- Quản lý Chứng chỉ




FILE: 94-best-practices-managing-dependencies-with-bom-in-microservices.md


# Thực Hành Tốt Nhất: Quản Lý Dependencies với BOM trong Microservices

## Giới Thiệu

Mọi lập trình viên microservice nên tuân theo các thực hành tốt nhất để tối ưu hóa và hợp lý hóa quy trình duy trì các dependencies bên trong microservices của họ. Hướng dẫn này giải thích một thực hành quan trọng sử dụng Bill of Materials (BOM) để quản lý dependencies một cách hiệu quả.

## Vấn Đề: Phiên Bản Dependencies Được Hard-Code

### Các Điểm Đau Hiện Tại

Khi xây dựng microservices, các lập trình viên thường gặp phải những thách thức đáng kể với việc quản lý dependencies:

- Mỗi microservice (accounts, cards, config server, Eureka server, gateway server, loans, message) đều có file `pom.xml` hoặc `build.gradle` riêng
- Các dependencies và phiên bản được hard-code trực tiếp trong cấu hình của từng microservice
- Thông tin phiên bản bao gồm:
  - Phiên bản Spring Boot
  - Phiên bản Java
  - Phiên bản Spring Cloud
  - Phiên bản OpenTelemetry
  - Phiên bản các thư viện bên thứ ba
  - Các build plugins (ví dụ: Google Jib Maven plugin để tạo Docker image)

### Thách Thức

Hãy tưởng tượng tổ chức của bạn có hơn 30 microservices. Nếu bạn cần migrate từ một phiên bản Spring Boot sang phiên bản khác, bạn sẽ phải:

1. Truy cập tất cả các file `pom.xml` của mọi microservice
2. Cập nhật thủ công số phiên bản trong từng file
3. Đảm bảo tính nhất quán trên tất cả các services

**Đây rõ ràng không phải là một thực hành tốt nhất!**

Các lập trình viên buộc phải truy cập tất cả các microservices chỉ để cập nhật một số phiên bản đơn giản, điều này:
- Tốn thời gian
- Dễ xảy ra lỗi
- Khó duy trì
- Thiếu kiểm soát tập trung

## Giải Pháp: BOM (Bill of Materials)

### BOM Là Gì?

BOM là một loại file Project Object Model (POM) đặc biệt giúp quản lý các phiên bản của một tập hợp các dependencies liên quan.

### BOM Hoạt Động Như Thế Nào

Hãy nghĩ về BOM như **interfaces trong Java**:
- Interfaces định nghĩa các contract chung mà các subclass hoặc child class phải tuân theo
- Tương tự, BOM định nghĩa tất cả các properties chung và dependencies cần thiết cho các microservices
- Các thay đổi luôn được thực hiện ở một nơi duy nhất

### Lợi Ích Của Việc Sử Dụng BOM

1. **Quản Lý Dependencies Tập Trung**: Tất cả định nghĩa phiên bản ở một nơi
2. **Cập Nhật Phiên Bản Dễ Dàng**: Cập nhật một lần, áp dụng mọi nơi
3. **Tính Nhất Quán**: Tất cả microservices sử dụng cùng phiên bản dependencies
4. **Giảm Bảo Trì**: Không cần truy cập nhiều cấu hình microservice
5. **Kiểm Soát Phiên Bản Tốt Hơn**: Theo dõi thay đổi dependencies trong một file duy nhất

## Bối Cảnh Triển Khai

Ví dụ này dựa trên:
- **Phần 20** của khóa học (code được sao chép từ Phần 14)
- Event-driven microservices sử dụng Apache Kafka
- Tập trung vào các thực hành tốt nhất về quản lý dependencies mà không có độ phức tạp của Kubernetes

## Kết Luận

Áp dụng BOM trong phát triển microservices của bạn là điều cần thiết để:
- Quản lý dependencies có khả năng mở rộng
- Giảm nợ kỹ thuật (technical debt)
- Cải thiện năng suất của lập trình viên
- Duy trì tính nhất quán trên các services

Bằng cách triển khai BOM, bạn chuyển đổi quản lý dependencies từ một quy trình phân tán, dễ xảy ra lỗi thành một thực hành tập trung, hiệu quả có thể mở rộng theo sự phát triển của tổ chức.

---

**Các Bước Tiếp Theo**: Trong các bài giảng tiếp theo, chúng ta sẽ triển khai BOM và xem nó đơn giản hóa quản lý dependencies trong microservices như thế nào trong thực tế.




FILE: 95-creating-bom-project-for-microservices-step-by-step.md


# Tạo Dự Án BOM Cho Microservices: Hướng Dẫn Từng Bước

## Tổng Quan

Hướng dẫn này trình bày cách tạo dự án Bill of Materials (BOM) từ đầu để quản lý tập trung các dependencies trong các microservices Spring Boot. Dự án BOM hoạt động như một parent cho tất cả microservices, cung cấp quản lý phiên bản dependencies nhất quán.

## Bước 1: Tạo Dự Án Maven Spring Boot Mới

### Tạo Module

1. Nhấp chuột phải vào thư mục `section_20`
2. Chọn **New Module**
3. Trong cửa sổ tạo module, chọn tùy chọn **Spring Boot**
4. Cấu hình dự án với các thông tin sau:
   - **Tên**: `eazy-bom` (BOM là viết tắt của Bill of Materials)
   - **Ngôn ngữ**: Java
   - **Loại**: Maven
   - **Group**: `com.eazybyte`
   - **Artifact**: `eazy-bom`
   - **Tên Package**: `com.eazybyte.eazybom`
   - **Phiên bản JDK**: 21
   - **Phiên bản Java**: 21
   - **Packaging**: Jar (sẽ được thay đổi thành POM sau)

5. Nhấp nút **Next**
6. **Quan trọng**: Không thêm bất kỳ Spring Boot starter dependencies nào
7. Nhấp nút **Create**

Điều này tạo ra một dự án Maven Spring Boot mới có tên `eazy-bom`.

## Bước 2: Dọn Dẹp Cấu Trúc Dự Án

### Xóa Thư Mục Source

Vì dự án BOM chỉ nên chứa thông tin quản lý dependencies và không có mã nguồn thực tế:

1. Mở dự án `eazy-bom` vừa tạo
2. Xóa toàn bộ thư mục `src`

> **Thực Hành Tốt Nhất**: Đây là thực hành tốt để chỉ duy trì thông tin liên quan đến dependencies trong dự án BOM, không có bất kỳ mã nguồn nào. Điều này giữ cho BOM sạch sẽ và chỉ tập trung vào quản lý dependencies.

## Bước 3: Chỉnh Sửa File pom.xml

Mở file `pom.xml`. Bạn sẽ thấy một file `pom.xml` thông thường của microservice Spring Boot. Chúng ta cần thực hiện các thay đổi đáng kể để biến nó thành file BOM.

### 3.1 Xóa Thông Tin Parent

Xóa toàn bộ phần `<parent>` tham chiếu đến Spring Boot starter parent:

```xml
<!-- XÓA PHẦN NÀY -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>x.x.x</version>
    <relativePath/>
</parent>
```

### 3.2 Thêm Mô Tả

Thêm tag description sau thông tin dự án cơ bản:

```xml
<description>Common BOM cho EazyBank Microservices</description>
```

Bạn có thể viết bất cứ điều gì có ý nghĩa với bạn trong phần mô tả này.

### 3.3 Thêm Metadata Dự Án Tùy Chọn

Các tag này là tùy chọn nhưng được khuyến nghị cho một thiết lập dự án hoàn chỉnh:

```xml
<url>https://www.eazybytes.com</url>

<licenses>
    <license>
        <name>Apache License, Version 2.0</name>
        <url>https://www.apache.org/licenses/LICENSE-2.0</url>
    </license>
</licenses>

<developers>
    <developer>
        <id>eazybytes</id>
        <name>EazyBytes Team</name>
        <email>info@eazybytes.com</email>
    </developer>
</developers>

<scm>
    <connection>scm:git:git://github.com/eazybytes/eazybank.git</connection>
    <developerConnection>scm:git:ssh://github.com/eazybytes/eazybank.git</developerConnection>
    <url>https://github.com/eazybytes/eazybank</url>
</scm>
```

> **Lưu ý**: Các tag này (URL, licenses, developers, SCM) là tùy chọn và không liên quan cụ thể đến chức năng BOM. Bạn có thể xóa chúng nếu muốn, nhưng chúng là thực hành tốt cho tài liệu dự án.

### 3.4 Đặt Loại Packaging Thành POM (Quan Trọng!)

Ngay sau tag `<description>`, thêm tag packaging:

```xml
<packaging>pom</packaging>
```

> **Cực Kỳ Quan Trọng**: Nếu không đề cập `pom` làm loại packaging, bạn không thể sử dụng tính năng BOM (Bill of Materials). Đây là điều phân biệt dự án BOM với dự án thông thường.

**Dự án BOM là gì?**
- BOM = **Project Object Model**
- Đây là loại dự án Maven đặc biệt được thiết kế cho quản lý dependencies

## Bước 4: Định Nghĩa Properties

Trong phần `<properties>`, định nghĩa tất cả các properties cần thiết cho microservices của bạn.

Thay thế các properties hiện có bằng:

```xml
<properties>
    <!-- Phiên bản Java -->
    <java.version>21</java.version>
    
    <!-- Phiên bản Spring Framework -->
    <spring-boot.version>3.2.0</spring-boot.version>
    <spring-cloud.version>2023.0.0</spring-cloud.version>
    
    <!-- Phiên bản Thư Viện Bên Thứ Ba -->
    <lombok.version>1.18.30</lombok.version>
    <h2.version>2.2.224</h2.version>
    <springdoc.version>2.3.0</springdoc.version>
    
    <!-- Observability -->
    <opentelemetry.version>1.32.0</opentelemetry.version>
    <micrometer.version>1.12.0</micrometer.version>
    
    <!-- Build Tools -->
    <jib.version>3.4.0</jib.version>
    <image.tag>latest</image.tag>
</properties>
```

### Hiểu Về Properties

Tất cả properties đều dễ hiểu và sẽ được microservices sử dụng. Các điểm chính:

#### Thư Viện Bên Thứ Ba
Đối với bất kỳ thư viện bên thứ ba nào được sử dụng bên ngoài hệ sinh thái Spring Boot, bạn **phải** chỉ định phiên bản chính xác:
- SpringDoc (tài liệu OpenAPI/Swagger)
- H2 Database
- Lombok
- OpenTelemetry
- Micrometer

#### Tại Sao Phải Chỉ Định Phiên Bản Thư Viện Bên Thứ Ba?

Mặc dù microservices có thể hoạt động mà không cần phiên bản rõ ràng (các dependencies Spring Boot có thể tự động áp dụng phiên bản mới nhất), **bạn không bao giờ nên dựa vào điều này**. Luôn duy trì kiểm soát bằng cách chỉ định phiên bản chính xác vì:
- Ngăn chặn các thay đổi breaking không mong muốn
- Đảm bảo tính nhất quán trên tất cả microservices
- Làm cho việc nâng cấp phiên bản có chủ đích và được kiểm soát
- Đơn giản hóa việc khắc phục sự cố

#### Properties Khác
- **jib.version**: Phiên bản của Google Jib Maven plugin để tạo Docker image
- **image.tag**: Tên tag của Docker image (ví dụ: "latest")

## Bước 5: Cấu Hình Dependency Management

### 5.1 Xóa Dependencies Mặc Định

Xóa toàn bộ phần `<dependencies>` chứa các dependencies Spring Boot mặc định:

```xml
<!-- XÓA TOÀN BỘ PHẦN NÀY -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
    </dependency>
</dependencies>
```

Giữ tag `<dependencies>` trống hoặc xóa nó hoàn toàn.

### 5.2 Tạo Phần Dependency Management

Thêm phần `<dependencyManagement>` mới với tất cả dependencies cần thiết:

```xml
<dependencyManagement>
    <dependencies>
        
        <!-- Spring Boot Dependencies BOM -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- H2 Database -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <version>${h2.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- SpringDoc OpenAPI -->
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi</artifactId>
            <version>${springdoc.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- Spring Boot Starter Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <version>${spring-boot.version}</version>
        </dependency>

        <!-- Spring Cloud Dependencies -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

    </dependencies>
</dependencyManagement>
```

### Hiểu Từng Dependency

#### 1. Spring Boot Dependencies
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-dependencies</artifactId>
    <version>${spring-boot.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Spring Boot framework có file BOM riêng của nó
- Chúng ta import nó để làm cho tất cả dependencies Spring Boot có sẵn cho các microservices con
- Sử dụng property `${spring-boot.version}` đã định nghĩa trước đó
- **type**: Phải là `pom` cho BOM imports
- **scope**: Phải là `import` cho BOM imports

#### 2. Lombok
```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>${lombok.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Lombok là thư viện bên thứ ba ngoài hệ sinh thái Spring Boot
- Phải được thêm riêng với phiên bản rõ ràng
- Theo cùng cấu trúc: groupId, artifactId, version từ properties
- type: `pom`, scope: `import`

#### 3. H2 Database
```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <version>${h2.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- H2 cũng là một dependency bên thứ ba
- Yêu cầu chỉ định phiên bản rõ ràng
- Cùng mẫu BOM import

#### 4. SpringDoc OpenAPI
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi</artifactId>
    <version>${springdoc.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Được sử dụng để tài liệu hóa microservices với đặc tả OpenAPI và Swagger
- Thư viện bên thứ ba yêu cầu phiên bản rõ ràng

#### 5. Spring Boot Starter Test (Trường Hợp Đặc Biệt)
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <version>${spring-boot.version}</version>
</dependency>
```

**Lưu ý sự khác biệt**: Dependency này KHÔNG có `<type>pom</type>` và `<scope>import</scope>`!

**Tại sao?**
- Spring Boot Starter Test không hỗ trợ import kiểu POM
- Đây là thư viện nhỏ với sub-dependencies tối thiểu
- Chỉ hỗ trợ chức năng unit testing
- Được thêm như một dependency thông thường chỉ với groupId, artifactId và version

#### 6. Spring Cloud Dependencies
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-dependencies</artifactId>
    <version>${spring-cloud.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Spring Cloud chứa nhiều sub-projects khác nhau (Eureka, Config Server, Gateway, v.v.)
- Chúng ta muốn sử dụng chúng trong microservices của mình
- Import toàn bộ file BOM Spring Cloud
- type: `pom`, scope: `import`

### Tham Chiếu Properties

Lưu ý cú pháp để tham chiếu các properties đã định nghĩa trước đó:

```xml
<version>${tên-property}</version>
```

Ví dụ:
- `${spring-boot.version}` tham chiếu property phiên bản Spring Boot
- `${lombok.version}` tham chiếu property phiên bản Lombok

## Bước 6: Cấu Hình Build (Không Cần Thay Đổi)

Phần `<build>` không yêu cầu bất kỳ thay đổi nào cho dự án BOM. Bạn có thể để nó như vậy hoặc xóa các build plugins không cần thiết cho dự án BOM.

## Tóm Tắt Các Thay Đổi

Để tạo dự án BOM, bạn cần:

1. ✅ Tạo dự án Maven Spring Boot
2. ✅ Xóa thư mục `src` (không có mã nguồn trong BOM)
3. ✅ Xóa phần `<parent>` khỏi `pom.xml`
4. ✅ Thêm description và metadata tùy chọn
5. ✅ **Đặt `<packaging>pom</packaging>` (Quan trọng!)**
6. ✅ Định nghĩa tất cả properties cần thiết với phiên bản
7. ✅ Xóa phần `<dependencies>` mặc định
8. ✅ Tạo phần `<dependencyManagement>` với tất cả dependencies
9. ✅ Sử dụng `<type>pom</type>` và `<scope>import</scope>` cho BOM imports
10. ✅ Giữ phần `<build>` không thay đổi

## Những Điểm Chính

### Các Yếu Tố Bắt Buộc Cho BOM
- **packaging**: Phải là `pom`
- **dependencyManagement**: Chứa tất cả dependencies được quản lý
- **properties**: Định nghĩa tất cả phiên bản tập trung

### Mẫu Import Dependency
Đối với hầu hết dependencies hỗ trợ BOM:
```xml
<type>pom</type>
<scope>import</scope>
```

Đối với dependencies không hỗ trợ BOM (như starter-test):
- Chỉ chỉ định groupId, artifactId và version

### Triết Lý Kiểm Soát Phiên Bản
- Luôn chỉ định phiên bản cho thư viện bên thứ ba
- Không bao giờ dựa vào resolution phiên bản tự động
- Duy trì kiểm soát rõ ràng đối với tất cả dependencies
- Tham chiếu phiên bản từ properties sử dụng `${tên-property}`

## Bước Tiếp Theo?

Trong bài giảng tiếp theo, chúng ta sẽ:
- Áp dụng dự án `eazy-bom` này vào các microservices riêng lẻ
- Thấy được sự kỳ diệu của quản lý dependencies tập trung
- Học cách các microservices con kế thừa phiên bản tự động
- Hiểu cách cập nhật phiên bản ở một nơi cho tất cả services

## Lợi Ích Bạn Sẽ Trải Nghiệm

Sau khi áp dụng BOM này trong microservices của bạn:
- ✅ Không còn phiên bản hard-coded trong các microservices riêng lẻ
- ✅ Cập nhật phiên bản ở một nơi
- ✅ Phiên bản dependencies nhất quán trên tất cả services
- ✅ Bảo trì và nâng cấp dễ dàng hơn
- ✅ Kiểm soát tốt hơn các phiên bản thư viện bên thứ ba
- ✅ Giảm cấu hình trùng lặp

Cảm ơn bạn!




FILE: 96-managing-dependencies-with-bom-in-spring-boot-microservices.md


# Quản Lý Dependencies với BOM trong Spring Boot Microservices

## Tổng Quan

Hướng dẫn này trình bày cách hợp lý hóa quản lý dependencies trên nhiều microservices bằng cách sử dụng phương pháp Bill of Materials (BOM). Bằng cách tập trung kiểm soát phiên bản trong file BOM cha, bạn có thể quản lý dependencies hiệu quả hơn và duy trì tính nhất quán trên tất cả các microservices.

## BOM (Bill of Materials) là gì?

Bill of Materials (BOM) là một loại file POM đặc biệt giúp tập trung quản lý phiên bản dependencies. Thay vì định nghĩa phiên bản trong từng microservice riêng lẻ, bạn định nghĩa chúng một lần trong file BOM cha, giúp bạn kiểm soát tập trung tất cả các phiên bản dependencies.

## Lợi Ích của Việc Sử Dụng BOM

- **Kiểm Soát Phiên Bản Tập Trung**: Quản lý tất cả phiên bản dependencies tại một vị trí duy nhất
- **Tính Nhất Quán**: Đảm bảo tất cả microservices sử dụng các phiên bản tương thích
- **Cập Nhật Dễ Dàng**: Thay đổi phiên bản một lần trong file BOM thay vì cập nhật từng microservice
- **Giảm Trùng Lặp**: Loại bỏ các số phiên bản hardcode trên các microservices
- **Bảo Trì Đơn Giản**: Hợp lý hóa quy trình phát triển và triển khai

## Các Bước Triển Khai

### 1. Tạo Dự Án BOM

Đầu tiên, tạo một dự án BOM chuyên dụng (ví dụ: `eazy-bom`) với file `pom.xml` định nghĩa tất cả các dependencies chung và phiên bản của chúng.

**Các yếu tố chính trong pom.xml của BOM:**
- Định nghĩa properties cho tất cả phiên bản dependencies
- Sử dụng `<dependencyManagement>` để import Spring Boot và Spring Cloud BOMs
- Thiết lập cấu hình chung như phiên bản Java, image tags và phiên bản plugins

### 2. Cấu Hình Microservices Sử Dụng BOM

**Bước 1: Cập Nhật Khai Báo Parent**

Thay thế Spring Boot parent chuẩn bằng BOM parent của bạn:

```xml
<parent>
    <groupId>com.example</groupId>
    <artifactId>eazy-bom</artifactId>
    <version>1.0.0</version>
    <relativePath>../eazy-bom/pom.xml</relativePath>
</parent>
```

**Quan trọng**: `<relativePath>` phải trỏ đến vị trí pom.xml của BOM tương đối với microservice.

**Bước 2: Xóa Phần Properties**

Xóa phần properties khỏi pom.xml của microservice, vì chúng đã được định nghĩa trong BOM cha.

**Bước 3: Cập Nhật Dependencies**

Đối với dependencies, tuân theo các quy tắc sau:

- **Spring Boot dependencies**: Không cần phiên bản (kế thừa từ BOM)
  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
  </dependency>
  ```

- **Third-party dependencies**: Tham chiếu các properties phiên bản từ BOM
  ```xml
  <dependency>
      <groupId>io.opentelemetry</groupId>
      <artifactId>opentelemetry-api</artifactId>
      <version>${otel.version}</version>
  </dependency>
  ```

**Bước 4: Cập Nhật Build Plugins**

Tham chiếu phiên bản plugins từ properties của BOM:

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <version>${jib.version}</version>
    <configuration>
        <to>
            <image>username/microservice-name:${image.tag}</image>
        </to>
    </configuration>
</plugin>
```

**Bước 5: Xóa Dependency Management Trùng Lặp**

Xóa phần `<dependencyManagement>` khỏi microservices vì nó đã có trong BOM.

## Ví Dụ: Migration Accounts Microservice

### Trước (với Spring Boot Parent):
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.3</version>
</parent>

<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2023.0.0</spring-cloud.version>
    <!-- ... nhiều properties khác ... -->
</properties>
```

### Sau (với BOM Parent):
```xml
<parent>
    <groupId>com.example</groupId>
    <artifactId>eazy-bom</artifactId>
    <version>1.0.0</version>
    <relativePath>../eazy-bom/pom.xml</relativePath>
</parent>

<!-- Không cần phần properties -->
```

## Các Properties Thường Được Quản Lý trong BOM

BOM thường quản lý các properties sau:

- **spring-boot.version**: Phiên bản Spring Boot framework
- **spring-cloud.version**: Phiên bản Spring Cloud
- **java.version**: Phiên bản ngôn ngữ Java
- **maven.compiler.source**: Phiên bản source của Maven compiler
- **maven.compiler.target**: Phiên bản target của Maven compiler
- **otel.version**: Phiên bản OpenTelemetry
- **micrometer.version**: Phiên bản Micrometer metrics
- **h2.version**: Phiên bản H2 database
- **lombok.version**: Phiên bản Lombok
- **spring-doc.version**: Phiên bản SpringDoc OpenAPI
- **jib.version**: Phiên bản Google Jib plugin
- **image.tag**: Docker image tag cho tất cả microservices

## Hiểu về Spring Boot BOM Import

Khi bạn import Spring Boot dependencies trong BOM của mình:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Điều này **không** tự động thêm tất cả Spring Boot dependencies vào microservices của bạn. Thay vào đó:

1. BOM import các phiên bản Spring Boot dependency
2. Mỗi microservice khai báo các dependencies cụ thể mà nó cần
3. Các phiên bản được kế thừa từ BOM
4. Chỉ các dependencies được khai báo mới được tải xuống

Cách tiếp cận này cho bạn quyền kiểm soát dependencies nào mà mỗi microservice sử dụng trong khi vẫn duy trì tính nhất quán về phiên bản.

## Kiểm Tra Cấu Hình BOM

### 1. Reload Maven Projects
Sau khi thực hiện thay đổi, reload tất cả Maven projects trong IDE để đảm bảo không có lỗi biên dịch.

### 2. Test một Microservice
Khởi động một microservice đơn giản (ví dụ: Config Server) để xác minh nó chạy đúng với cấu hình BOM.

### 3. Test Thay Đổi Phiên Bản
Để xác minh BOM đang hoạt động:
1. Thay đổi một phiên bản trong BOM (ví dụ: Spring Boot version từ 3.3.3 sang 3.3.2)
2. Xóa thư mục `target` trong microservice
3. Reload Maven projects
4. Khởi động microservice và kiểm tra nó sử dụng phiên bản mới

**Lưu ý**: Nếu thay đổi không được áp dụng, hãy thử:
- Reload Maven projects nhiều lần
- Xóa Maven cache
- Khởi động lại IDE

## Best Practices (Thực Hành Tốt Nhất)

### 1. Chiến Lược Kiểm Soát Phiên Bản
- **Spring Boot/Cloud**: Quản lý trong BOM, không cần phiên bản trong microservices
- **Third-party libraries**: Định nghĩa properties phiên bản trong BOM, tham chiếu trong microservices
- Điều này cho bạn quyền kiểm soát rõ ràng đối với phiên bản third-party dependencies

### 2. Cấu Hình Relative Path
Luôn chỉ định `<relativePath>` trong khai báo parent, đặc biệt cho CI/CD pipelines:
```xml
<relativePath>../eazy-bom/pom.xml</relativePath>
```

### 3. Quản Lý Image Tag
Sử dụng property image tag chung (ví dụ: `image.tag`) để duy trì versioning nhất quán trên tất cả Docker images của microservices.

### 4. Migration Từng Bước
Migrate từng microservice một để kiểm tra cấu hình BOM trước khi áp dụng cho tất cả microservices.

## Xử Lý Sự Cố

### IDE Không Nhận Diện BOM
- Đảm bảo relative path đúng
- Reload Maven projects
- Khởi động lại IDE

### Xung Đột Phiên Bản
- Kiểm tra tất cả microservices tham chiếu cùng phiên bản BOM
- Xác minh không có phiên bản hardcode ghi đè cài đặt BOM

### Vấn Đề Maven Cache
- Chạy `mvn clean install` trong dự án BOM trước
- Xóa local Maven repository cache nếu cần
- Sử dụng chức năng "Reload All Maven Projects" của IDE

## Kết Luận

Triển khai cấu trúc BOM cho kiến trúc microservices của bạn mang lại:

- **Kiểm soát tập trung** đối với tất cả phiên bản dependencies
- **Bảo trì đơn giản** khi cập nhật phiên bản
- **Tính nhất quán** trên tất cả microservices
- **Giảm lỗi** do không khớp phiên bản
- **Hợp lý hóa** quy trình phát triển

Bằng cách tuân theo phương pháp này, bạn có thể quản lý dependencies hiệu quả trên toàn bộ hệ sinh thái microservices của mình từ một vị trí duy nhất.

---

*Hướng dẫn này dựa trên Spring Boot 3.x và Spring Cloud 2023.x. Điều chỉnh cấu hình theo phiên bản và yêu cầu cụ thể của bạn.*




FILE: 97-managing-dependencies-with-bom-in-microservices-advanced.md


# Quản Lý Dependencies với BOM trong Microservices - Khái Niệm Nâng Cao

## Tổng Quan

Hướng dẫn này trình bày các kỹ thuật nâng cao để quản lý dependencies trong microservices sử dụng Bill of Materials (BOM), bao gồm ghi đè phiên bản, quản lý dependencies chung, và tạo Docker image với cấu hình BOM.

## Ghi Đè Phiên Bản trong Từng Microservice

Mặc dù BOM cho phép kiểm soát phiên bản tập trung từ `pom.xml` cha, các microservice riêng lẻ vẫn có thể linh hoạt sử dụng các phiên bản khác nhau khi cần thiết.

### Cách Ghi Đè Phiên Bản

Thay vì tham chiếu phiên bản từ BOM cha, bạn có thể định nghĩa phiên bản riêng trong microservice:

**Ví dụ: Ghi Đè Phiên Bản Lombok trong Loans Microservice**

Xóa tham chiếu thuộc tính và chỉ định phiên bản của bạn:

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.8.32</version>
</dependency>
```

Ngay cả khi BOM cha định nghĩa phiên bản `1.8.34`, loans microservice có thể sử dụng `1.8.32`.

### Lưu Ý Quan Trọng

- Cách tiếp cận này hoạt động với bất kỳ dependency nào (Spring Boot dependencies hoặc thư viện bên thứ ba)
- Bạn có toàn quyền tự do ghi đè phiên bản khi cần thiết
- Sử dụng khả năng này một cách thận trọng để duy trì tính nhất quán giữa các microservices

## Quản Lý Dependencies Chung với BOM

### Vấn Đề

Trong kiến trúc microservices, nhiều service thường sử dụng cùng các thư viện. Ví dụ, tất cả microservices thường bao gồm:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
</dependency>
```

Việc lặp lại dependency này trong `pom.xml` của mỗi microservice tạo ra gánh nặng bảo trì.

### Giải Pháp: Tập Trung Dependencies Chung

Định nghĩa dependencies chung một lần trong BOM cha, và tất cả microservices con sẽ tự động kế thừa chúng.

### Các Bước Triển Khai

#### Bước 1: Xóa Dependency khỏi Tất Cả Microservices

Xóa dependency `spring-boot-starter-test` khỏi:
- Gateway
- Message microservice
- Cards microservice
- Config Server
- Eureka Server
- Accounts microservice

Sau khi xóa, reload Maven changes cho mỗi microservice.

#### Bước 2: Hiểu về Dependency Management vs Dependencies

**Sự Khác Biệt Quan Trọng:**

- `<dependencyManagement>`: Chỉ sử dụng cho quản lý phiên bản
- `<dependencies>`: Dependencies thực tế được kế thừa bởi các project con

Nếu bạn chỉ định nghĩa dependencies dưới `<dependencyManagement>`, các microservices con sẽ không tự động import chúng.

#### Bước 3: Thêm Dependency Chung vào BOM Cha

Trong `pom.xml` của project `eazy-bom`, thêm dependency dưới phần `<dependencies>` (không phải `<dependencyManagement>`):

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
    </dependency>
</dependencies>
```

#### Bước 4: Reload và Xác Minh

1. Lưu các thay đổi trong BOM `pom.xml`
2. Reload Maven changes cho project `eazy-bom`
3. Tất cả microservices con sẽ tự động fetch dependency chung
4. Build project để xác minh các lỗi compilation đã được giải quyết

### Lợi Ích

- **Giảm Trùng Lặp**: Định nghĩa dependencies chung một lần
- **Bảo Trì Dễ Dàng Hơn**: Cập nhật phiên bản ở một vị trí duy nhất
- **Tính Nhất Quán**: Đảm bảo tất cả microservices sử dụng cùng phiên bản
- **Code Sạch Hơn**: POM của các microservice riêng lẻ tập trung vào các dependencies độc đáo

## Tạo Docker Image với BOM

### Xác Minh Cấu Hình BOM với Docker

Sau khi triển khai BOM, quan trọng là phải xác minh rằng việc tạo Docker image không bị ảnh hưởng.

### Kiểm Tra Tạo Docker Image

#### Bước 1: Tạo Docker Image

Điều hướng đến thư mục microservice (ví dụ: Config Server):

```bash
cd config-server
mvn compile jib:dockerBuild
```

Docker image sẽ được tạo thành công mà không có bất kỳ vấn đề nào.

#### Bước 2: Xác Minh Image trong Docker Desktop

Kiểm tra Docker Desktop cho image mới tạo:
- Tên image: `config-server`
- Tag: `S20`
- Kích thước: ~354 MB (không ảnh hưởng đến kích thước image)

#### Bước 3: Kiểm Tra Khởi Động Container

Chạy container để đảm bảo nó khởi động đúng cách:

```bash
docker run -p 8071:8071 config-server:S20
```

**Kết Quả Mong Đợi:**
- Ứng dụng Spring Boot khởi động không có vấn đề
- Ứng dụng sử dụng phiên bản Spring Boot được chỉ định trong BOM cha (ví dụ: 3.3.2)
- Container xuất hiện trong Docker Desktop với logs đầy đủ

### Điểm Xác Minh

✅ Docker image được tạo thành công  
✅ Kích thước image vẫn tối ưu  
✅ Container khởi động không có lỗi  
✅ Ứng dụng sử dụng phiên bản từ BOM  
✅ Tất cả chức năng hoạt động như mong đợi  

## Thực Hành Tốt Nhất

1. **Áp Dụng BOM trong Production**: Luôn triển khai Bill of Materials trong các dự án microservices doanh nghiệp
2. **Giảm Thiểu Thay Đổi Thủ Công**: BOM giảm quản lý phiên bản thủ công giữa các services
3. **Sử Dụng Ghi Đè Phiên Bản Một Cách Tiết Kiệm**: Chỉ ghi đè phiên bản khi thực sự cần thiết
4. **Tập Trung Dependencies Chung**: Định nghĩa các dependencies được chia sẻ trong BOM cha
5. **Kiểm Tra Tích Hợp Docker**: Xác minh việc tạo Docker image sau khi triển khai BOM
6. **Ghi Chép Quyết Định Phiên Bản**: Theo dõi bất kỳ ghi đè phiên bản nào và lý do của chúng

## Tóm Tắt

Mô hình Bill of Materials (BOM) cung cấp:

- **Kiểm Soát Phiên Bản Tập Trung**: Quản lý tất cả phiên bản dependency từ một parent POM duy nhất
- **Linh Hoạt**: Các microservice riêng lẻ có thể ghi đè phiên bản khi cần
- **Quản Lý Dependency Chung**: Định nghĩa dependencies được chia sẻ một lần
- **Giảm Bảo Trì**: Loại bỏ các khai báo dependency lặp lại
- **Tương Thích Docker**: Hoạt động liền mạch với quy trình containerization
- **Sẵn Sàng Doanh Nghiệp**: Cách tiếp cận đã được chứng minh cho kiến trúc microservices quy mô lớn

Bằng cách triển khai BOM đúng cách, bạn tạo ra một hệ sinh thái microservices dễ bảo trì, nhất quán và có khả năng mở rộng hơn.

## Kết Luận

Cấu hình BOM nâng cao phát triển microservices bằng cách cung cấp chiến lược quản lý dependency mạnh mẽ. Nó loại bỏ các điều chỉnh thủ công, đảm bảo tính nhất quán về phiên bản, và đơn giản hóa việc bảo trì trên tất cả các services trong kiến trúc của bạn.

---

**Chủ Đề Liên Quan:**
- Tạo BOM Project cho Microservices
- Thực Hành Tốt Nhất cho Quản Lý Dependency Microservices
- Tối Ưu Hóa Docker Image trong Spring Boot




FILE: 98-managing-shared-libraries-in-microservices.md


# Quản Lý Thư Viện Dùng Chung Trong Microservices

## Tổng Quan

Một trong những thách thức phổ biến trong phát triển microservices là xử lý việc trùng lặp code giữa nhiều dịch vụ. Tài liệu này khám phá các cách tiếp cận khác nhau để quản lý thư viện dùng chung và cung cấp hướng dẫn về thời điểm và cách triển khai chúng một cách hiệu quả.

## Vấn Đề: Trùng Lặp Code

Trong kiến trúc microservices, các developer thường viết code trùng lặp trên nhiều dịch vụ. Ví dụ, một class `ErrorResponseDto` có thể được nhân bản trên tất cả các microservices nghiệp vụ như accounts, cards và loans. Mặc dù các dịch vụ hỗ trợ (Eureka server, Config server, Gateway server) có thể không cần các DTO như vậy, nhưng các microservices nghiệp vụ thường chia sẻ nhiều class chung.

Khi hệ sinh thái microservices của bạn phát triển, sự trùng lặp này trở nên rõ ràng hơn và khó duy trì hơn.

## Cách Tiếp Cận 1: Dự Án Maven Dùng Chung Duy Nhất

### Mô Tả
Tạo một dự án Maven dùng chung chứa tất cả các dependency và code chung, bao gồm:
- Các class tiện ích (Utility classes)
- Cấu hình (Configurations)
- Logic ghi log (Logging)
- Triển khai bảo mật (Security)
- Bất kỳ chức năng chung nào khác

### Nhược Điểm
- **Vấn Đề Fat JAR**: Thư viện trở thành một file JAR lớn, nguyên khối
- **Dependency Không Cần Thiết**: Các dịch vụ phải bao gồm tất cả code, ngay cả chức năng chúng không sử dụng
- **Docker Image Cồng Kềnh**: Docker images chứa logic không sử dụng, tăng kích thước
- **Không Được Khuyến Nghị**: Cách tiếp cận này không phải là best practice

## Cách Tiếp Cận 2: Nhiều Thư Viện Nhỏ Hơn

### Mô Tả
Tách code dùng chung thành nhiều thư viện nhỏ, tập trung:
- Thư viện tiện ích
- Thư viện bảo mật
- Thư viện ghi log
- Các thư viện tập trung khác

### Ưu Điểm
- Các dịch vụ có thể chọn lọc dependency họ cần
- Kích thước thư viện nhỏ hơn, dễ quản lý hơn

### Nhược Điểm
- **Độ Phức Tạp Quản Lý**: Dự án lớn có thể có 20-30+ dự án Maven khác nhau
- **Quản Lý Phiên Bản**: Khó duy trì versioning trên nhiều thư viện
- **Overhead Pull Request**: Quy trình phức tạp cho thay đổi code và phê duyệt
- **Thách Thức Xuất Bản**: Quản lý nhiều releases rất phức tạp
- **Không Được Khuyến Nghị**: Chi phí quản lý lớn hơn lợi ích

## Cách Tiếp Cận 3: Dự Án Maven Multi-Module (BOM) ✅ Được Khuyến Nghị

### Mô Tả
Tạo một dự án cha Bill of Materials (BOM) với nhiều submodules, trong đó mỗi module tập trung vào một chức năng cụ thể:
- Module ghi log
- Module bảo mật
- Module kiểm toán (Auditing)
- Các module chức năng khác

Tất cả các submodules chia sẻ một file BOM cha chung.

### Ưu Điểm
- **Repository Duy Nhất**: Tất cả thư viện chung tồn tại trong một GitHub repository
- **Versioning Đơn Giản**: Dễ dàng duy trì số phiên bản trên tất cả modules
- **Quản Lý Dễ Dàng**: Quy trình pull request và code review đơn giản
- **Dependency Chọn Lọc**: Các dịch vụ vẫn chọn modules họ cần
- **Best Practice**: Giải quyết các thách thức từ cách tiếp cận trước

### Triển Khai
Cách tiếp cận BOM cung cấp sự linh hoạt của nhiều thư viện với sự đơn giản quản lý của một cấu trúc dự án duy nhất.

## Cân Nhắc Quan Trọng: Khi Nào Nên Sử Dụng Thư Viện Dùng Chung

### Cuộc Tranh Luận
Chia sẻ code giữa các microservices là một chủ đề gây tranh cãi trong cộng đồng phát triển. Không có câu trả lời đúng duy nhất - nó phụ thuộc vào tình huống cụ thể của bạn.

### Hướng Dẫn Quyết Định

#### ✅ Sử Dụng Thư Viện Dùng Chung Khi:
- Code chung không tạo ra sự ghép nối chặt chẽ giữa các dịch vụ
- Triển khai vẫn đơn giản và độc lập
- Gánh nặng duy trì của sự trùng lặp là đáng kể
- Logic dùng chung thực sự ổn định và không có khả năng phân kỳ

#### ❌ Tránh Thư Viện Dùng Chung Khi:
- Chúng tạo ra sự ghép nối chặt chẽ giữa các microservices
- Chúng làm phức tạp quy trình triển khai
- Các dịch vụ cần phát triển độc lập
- Code dùng chung có khả năng phân kỳ theo thời gian

### Cách Tiếp Cận Thực Dụng
Nếu việc duy trì code trùng lặp trong nhiều microservices đơn giản hơn việc quản lý thư viện dùng chung, **hãy giữ sự trùng lặp**. Mục tiêu của microservices là tính độc lập và đơn giản - đừng hy sinh những nguyên tắc này vì DRY (Don't Repeat Yourself).

## Kết Luận

Cách tiếp cận Multi-Module Maven Project (BOM) là giải pháp được khuyến nghị để quản lý thư viện dùng chung trong microservices. Tuy nhiên, hãy luôn đánh giá xem thư viện dùng chung có thực sự cần thiết cho trường hợp sử dụng của bạn hay không. Đôi khi, chấp nhận một số trùng lặp code là lựa chọn tốt hơn để duy trì tính độc lập và sự đơn giản trong triển khai microservices.

## Điểm Chính Cần Nhớ

1. **Dự án dùng chung duy nhất** tạo ra fat JARs với các dependency không cần thiết
2. **Nhiều thư viện nhỏ** khó quản lý ở quy mô lớn
3. **Dự án BOM multi-module** cung cấp sự cân bằng tốt nhất giữa tính linh hoạt và khả năng quản lý
4. **Đánh giá cẩn thận** xem thư viện dùng chung có thực sự mang lại lợi ích cho kiến trúc của bạn
5. **Ưu tiên tính độc lập** hơn việc loại bỏ tất cả sự trùng lặp

---

*Tài liệu này dựa trên các best practices cho kiến trúc microservices sử dụng Java và Spring Boot.*




FILE: 99-managing-shared-libraries-with-maven-multi-modules-in-microservices.md


# Quản Lý Thư Viện Dùng Chung với Maven Multi-Modules trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách tạo và quản lý các thư viện dùng chung trong kiến trúc microservices bằng cách sử dụng dự án Maven multi-module. Thay vì nhân bản code trên nhiều microservices, chúng ta sẽ sử dụng phương pháp Bill of Materials (BOM) với các submodule để chia sẻ code chung một cách hiệu quả.

## Tạo Cấu Trúc Multi-Module

### Bước 1: Tạo Submodule Common

1. Click chuột phải vào dự án `eazy-bom` và chọn **New Module**
2. Cấu hình module với các thiết lập sau:
   - **Tên Module**: `common` (có thể tùy chỉnh theo yêu cầu)
   - **Ngôn Ngữ**: Java
   - **Loại**: Maven
   - **Group**: `com.eazybytes`
   - **Artifact**: `common`
   - **JDK**: 21
   - **Phiên Bản Java**: 21
   - **Packaging**: jar

3. Thêm các dependency cần thiết:
   - Spring Web
   - Lombok

4. Click **Create** để tạo submodule trong `eazy-bom`

### Bước 2: Cấu Hình Parent POM

Trong file `eazy-bom/pom.xml`, thêm phần modules sau phần properties:

```xml
<modules>
    <module>common</module>
</modules>
```

Định nghĩa thuộc tính version cho module common:

```xml
<properties>
    <common-jib.version>1.0.0</common-jib.version>
</properties>
```

### Bước 3: Cấu Hình POM của Common Submodule

Trong file `common/pom.xml`, thực hiện các thay đổi sau:

1. Thay thế Spring Boot parent bằng tham chiếu đến eazy-bom parent
2. Cập nhật version để sử dụng thuộc tính:
   ```xml
   <version>${common-jib.version}</version>
   ```

3. Cập nhật phần mô tả:
   ```xml
   <description>Common project cho eazybank microservices</description>
   ```

4. Thêm dependency SpringDoc cho các annotation OpenAPI:
   ```xml
   <dependency>
       <groupId>org.springdoc</groupId>
       <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
   </dependency>
   ```

5. Cấu hình Lombok để sử dụng version từ parent POM

6. Xóa cấu hình build (đã có trong parent POM)

7. Xóa dependency Spring Boot Starter Test (đã có trong parent POM)

8. Xóa tất cả chi tiết properties vì chúng được kế thừa từ parent

## Di Chuyển Code Dùng Chung vào Common Module

### Bước 1: Chuẩn Bị Cấu Trúc Common Module

1. Xóa file `CommonApplication.java` (chúng ta không muốn submodule có thể thực thi)
2. Tạo package mới: `dto`

### Bước 2: Di Chuyển ErrorResponseDto

1. Copy `ErrorResponseDto` từ bất kỳ microservice nào
2. Paste vào module `common` trong package `dto`
3. Xóa `ErrorResponseDto` khỏi tất cả các microservices:
   - Accounts microservice
   - Cards microservice
   - Loans microservice

## Thêm Common Dependency vào Các Microservices

Mỗi microservice cần thư viện common phải thêm nó như một dependency trong `pom.xml`:

```xml
<dependency>
    <groupId>com.eazybytes</groupId>
    <artifactId>common</artifactId>
    <version>${common-jib.version}</version>
</dependency>
```

Thêm dependency này vào:
- Accounts microservice
- Loans microservice
- Cards microservice

Sau khi thêm dependency, load lại các thay đổi Maven trong mỗi microservice.

## Khắc Phục Lỗi Biên Dịch

Nếu bạn gặp lỗi biên dịch sau khi di chuyển code dùng chung:

1. Cập nhật các câu lệnh import trong các class sử dụng `ErrorResponseDto`:
   - `GlobalExceptionHandler`
   - Controllers (Accounts, Loans, Cards)

2. Mở các file bị ảnh hưởng và save lại để kích hoạt tự động giải quyết

3. Rebuild dự án để xác minh tất cả lỗi đã được giải quyết

## Publish Common Module

Để publish module common vào local Maven repository:

```bash
cd common
mvn clean install
```

Lệnh này sẽ:
- Build module common
- Publish JAR vào local Maven repository
- Làm cho nó có sẵn cho việc tạo Docker image và các build khác

JAR sẽ có sẵn trong local Maven repository (thường là `~/.m2/repository` hoặc `%USERPROFILE%\.m2\repository`).

## Tạo Docker Images

Sau khi build thành công module common, bạn có thể tạo Docker images cho các microservices:

```bash
cd accounts
mvn compile jib:dockerBuild
```

Quá trình tạo image sẽ lấy JAR của module common từ local Maven repository.

## Best Practices

1. **Nhiều Submodules**: Bạn có thể tạo nhiều submodule dưới `eazy-bom` cho các mục đích khác nhau:
   - Security
   - Logging
   - Auditing
   - Common utilities

2. **Tránh Single Jumbo Modules**: Đừng tạo một Maven module lớn duy nhất. Chia chức năng thành các module tập trung, có mục đích cụ thể.

3. **Cẩn Thận**: Mặc dù phương pháp này giảm việc nhân bản code, hãy cẩn thận để không tạo ra:
   - Thách thức về deployment
   - Sự liên kết chặt chẽ giữa các microservices
   - Shared state hoặc dependencies vi phạm nguyên tắc microservices

4. **Quản Lý Version**: Sử dụng properties trong parent POM để quản lý version một cách nhất quán trên tất cả các module

## Lợi Ích

- **Tái Sử Dụng Code**: Viết một lần, sử dụng trên nhiều microservices
- **Tính Nhất Quán**: Các model và utilities dùng chung đảm bảo hành vi nhất quán
- **Khả Năng Bảo Trì**: Cập nhật code dùng chung ở một nơi
- **Type Safety**: Kiểm tra tại thời điểm biên dịch trên các microservices

## Tóm Tắt

Phương pháp này cho phép bạn tạo các thư viện dùng chung cho microservices của mình trong khi vẫn duy trì lợi ích của việc triển khai độc lập và khả năng mở rộng. Bằng cách sử dụng Maven multi-modules và BOM files, bạn có thể quản lý dependencies hiệu quả và giảm việc nhân bản code mà không tạo ra sự liên kết chặt chẽ.

Hãy luôn cân nhắc sự đánh đổi giữa việc tái sử dụng code và tính độc lập của microservices khi quyết định những gì cần chia sẻ giữa các services.


