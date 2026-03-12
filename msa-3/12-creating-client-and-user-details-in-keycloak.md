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