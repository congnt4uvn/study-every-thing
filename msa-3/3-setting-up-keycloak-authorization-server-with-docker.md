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