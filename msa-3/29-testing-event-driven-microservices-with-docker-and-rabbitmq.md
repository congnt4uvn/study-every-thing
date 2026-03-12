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