# Cấu Hình Docker Compose và Tích Hợp RabbitMQ cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình và chạy microservices sử dụng Docker Compose, bao gồm thiết lập RabbitMQ để làm mới cấu hình động mà không cần khởi động lại containers.

## Yêu Cầu Trước

- Docker Desktop đã được cài đặt và đang chạy
- Không có containers nào đang chạy (môi trường sạch)
- Git repository chứa các file cấu hình
- Postman để test API

## Thiết Lập Ban Đầu

### Bước 1: Di Chuyển đến Thư Mục Docker Compose

```bash
cd docker-compose/default
```

### Bước 2: Khởi Động Containers với Docker Compose

```bash
docker compose up -d
```

Lệnh này khởi động tất cả containers ở chế độ detached. Thứ tự khởi động:
1. RabbitMQ service
2. Config Server
3. Các microservices Accounts, Cards và Loans

### Bước 3: Kiểm Tra Containers Đang Chạy

```bash
docker ps
```

Bạn sẽ thấy:
- **RabbitMQ**: Trạng thái hiển thị "healthy" (đã cấu hình health check)
- **Config Server**: Trạng thái hiển thị "healthy" (đã cấu hình health check)
- **Accounts, Cards, Loans**: Mới khởi động (chưa cấu hình health check)

## Kiểm Tra Profile Mặc Định

### Endpoint Build Info

```
GET http://localhost:8080/api/build-info
```

Kết quả mong đợi: Version 3.0 (profile mặc định)

### Endpoint Java Version

```
GET http://localhost:8080/api/java-version
```

Kết quả mong đợi: Đường dẫn JAVA_HOME bên trong container

### Endpoint Contact Info

```
GET http://localhost:8080/api/contact-info
```

Kết quả mong đợi: Các thuộc tính từ profile mặc định

## Cấu Hình Làm Mới Động với Webhooks

### Bước 1: Thiết Lập Hookdeck

1. Truy cập [Hookdeck](https://hookdeck.com)
2. Click vào "test webhook post"
3. Click "add destination" để tạo session mới

### Bước 2: Cài Đặt và Đăng Nhập Hookdeck CLI

```bash
# Nếu có session trước, logout trước
hookdeck logout

# Đăng nhập vào session mới
hookdeck login
```

### Bước 3: Khởi Động Webhook Listener

```bash
hookdeck listen 8071 /monitor localhost
```

Lệnh này tạo một webhook URL để tích hợp với GitHub.

### Bước 4: Cấu Hình GitHub Webhook

1. Điều hướng đến GitHub repository của bạn (ví dụ: `eazybytes-config`)
2. Vào **Settings** → **Webhooks**
3. Chỉnh sửa webhook có sẵn hoặc tạo mới
4. Cập nhật **Payload URL** với webhook URL từ Hookdeck
5. Click **Update webhook**

## Khắc Phục Sự Cố Kết Nối RabbitMQ

### Vấn Đề

Khi test làm mới cấu hình, bạn có thể gặp lỗi 500. Kiểm tra logs của Config Server cho thấy:

```
Attempting to connect to RabbitMQ at localhost:5672
```

Điều này thất bại vì RabbitMQ không chạy trên `localhost` mà trong một container riêng biệt.

### Giải Pháp: Cập Nhật Cấu Hình Docker Compose

Trong file `docker-compose.yml`, thêm chi tiết kết nối RabbitMQ vào cấu hình microservice chung:

```yaml
microservice-base-config:
  deploy:
    environment:
      SPRING_RABBITMQ_HOST: rabbit  # Tên service, không phải localhost
```

Cấu hình này áp dụng cho:
- Config Server
- Microservice Accounts
- Microservice Cards
- Microservice Loans

### Tại Sao Cách Này Hoạt Động

- Tất cả containers chạy trong cùng một Docker network
- Các services có thể kết nối bằng tên service (ví dụ: `rabbit`)
- Port mặc định (5672), username và password không thay đổi

## Khởi Động Lại Containers với Cấu Hình Đã Cập Nhật

### Bước 1: Dừng và Xóa Containers Hiện Tại

```bash
docker compose down
```

### Bước 2: Khởi Động Containers với Cấu Hình Mới

```bash
docker compose up -d
```

### Bước 3: Kiểm Tra Kết Nối Config Server

Kiểm tra logs của Config Server:

```
Attempting to connect to RabbitMQ at rabbit:5672
Successfully created new connection
```

### Bước 4: Kiểm Tra Trạng Thái Health

```
GET http://localhost:8080/actuator/health
```

Kết quả mong đợi: `"status": "UP"`

```
GET http://localhost:8080/actuator/health/readiness
```

Kết quả mong đợi: `"status": "UP"`

## Kiểm Tra Làm Mới Cấu Hình Động

### Bước 1: Cập Nhật Cấu Hình trên GitHub

1. Điều hướng đến `accounts.yml` trong GitHub repository
2. Chỉnh sửa file (ví dụ: thay đổi `local` thành `docker`)
3. Commit thay đổi

### Bước 2: Xác Minh Webhook Đã Kích Hoạt

Kiểm tra terminal Hookdeck - bạn sẽ thấy mã trạng thái 200 cho biết webhook đã được gửi thành công.

### Bước 3: Kiểm Tra Cập Nhật Cấu Hình

```
GET http://localhost:8080/api/contact-info
```

Kết quả phải phản ánh thuộc tính đã được cập nhật **mà không cần khởi động lại containers**.

### Bước 4: Hoàn Tác Thay Đổi (Tùy Chọn)

1. Chỉnh sửa `accounts.yml` lại (đổi `docker` về `local`)
2. Commit thay đổi
3. Xác minh mã trạng thái 200 trong terminal Hookdeck
4. Test endpoint lại để xác nhận thuộc tính đã được hoàn tác

## Các Khái Niệm Chính

### Độ Ưu Tiên của Biến Môi Trường

Biến môi trường có độ ưu tiên cao nhất trong hệ thống phân cấp cấu hình Spring Boot, ghi đè các giá trị trong `application.yml` và `commonconfig.yml`.

### Health Checks

- **Health endpoint**: Hiển thị trạng thái tổng thể của ứng dụng, bao gồm các phụ thuộc tùy chọn (RabbitMQ)
- **Readiness endpoint**: Hiển thị nếu ứng dụng sẵn sàng chấp nhận traffic (loại trừ các phụ thuộc tùy chọn)

### Service Discovery trong Docker Networks

Các containers trong cùng Docker network có thể giao tiếp bằng tên service được định nghĩa trong `docker-compose.yml`.

## Cấu Trúc File Cấu Hình

- **docker-compose.yml**: Cấu hình điều phối containers
- **application.yml**: Các thuộc tính đặc thù cho ứng dụng
- **commonconfig.yml**: Cấu hình chung cho tất cả microservices
- **accounts.yml**: Các thuộc tính của microservice Accounts

## Các Bước Tiếp Theo

- Thiết lập Docker Compose cho profile **prod**
- Thiết lập Docker Compose cho profile **qa**
- Xác thực tất cả profiles hoạt động đúng
- Cấu hình health checks cho Accounts, Cards và Loans microservices

## Tóm Tắt

Thiết lập này trình bày:
- Khởi động nhiều microservices với Docker Compose
- Cấu hình RabbitMQ cho quản lý cấu hình phân tán
- Triển khai làm mới cấu hình động qua GitHub webhooks
- Khắc phục sự cố kết nối mạng của containers
- Kiểm tra thay đổi cấu hình mà không cần khởi động lại containers

Thiết lập Docker Compose với tích hợp RabbitMQ cho phép cập nhật cấu hình liền mạch trên tất cả microservices trong profile mặc định.