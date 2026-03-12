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