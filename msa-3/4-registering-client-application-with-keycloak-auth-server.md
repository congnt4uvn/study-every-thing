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