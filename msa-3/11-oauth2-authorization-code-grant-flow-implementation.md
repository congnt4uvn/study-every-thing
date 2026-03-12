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