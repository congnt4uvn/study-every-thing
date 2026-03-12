# Triển khai Microservices với Docker Compose và Eureka Server

## Tổng quan

Hướng dẫn này trình bày cách triển khai và cấu hình microservices với Eureka Server sử dụng Docker Compose, bao gồm xử lý các vấn đề cấu hình thường gặp và xác thực toàn bộ thiết lập.

## Yêu cầu

- Docker và Docker Compose đã được cài đặt
- Các microservices đã được build và container hóa
- Config Server đã được cấu hình
- Eureka Server đã được thiết lập

## Thiết lập ban đầu

### 1. Di chuyển đến thư mục Docker Compose

Di chuyển đến thư mục Docker Compose trong Section8:

```bash
cd Section8/docker-compose/default
```

### 2. Đảm bảo môi trường Docker sạch

Trước khi chạy Docker Compose, đảm bảo không có container nào đang chạy hoặc dừng để cung cấp đủ bộ nhớ:

```bash
docker ps -a
```

Nếu có containers tồn tại, hãy dọn dẹp chúng trước khi tiếp tục.

### 3. Khởi động các dịch vụ với Docker Compose

Thực thi lệnh Docker Compose:

```bash
docker compose up -d
```

## Trình tự khởi động dịch vụ

Các dịch vụ tuân theo thứ tự khởi động cụ thể:

1. **Config Server** khởi động trước
2. **Eureka Server** khởi động sau khi Config Server hoạt động tốt
3. **Microservices** (Accounts, Loans, Cards) khởi động sau khi Eureka Server đã sẵn sàng

## Xử lý sự cố kết nối

### Vấn đề 1: Eureka Server không kết nối được với Config Server

**Vấn đề**: Eureka Server không thể kết nối với Config Server.

**Nguyên nhân**: Service `microservice-base-config` chỉ cung cấp cấu hình mạng và triển khai, thiếu các thuộc tính kết nối Config Server cần thiết.

**Giải pháp**: Tạo một service cấu hình riêng cho Eureka.

### Tạo cấu hình riêng cho Eureka

Thêm service configuration mới trong `docker-compose.yml`:

```yaml
microservice-eureka-config:
  extends: microservice-configserver-config
  depends_on:
    eureka-server:
      condition: service_started
```

### Cập nhật cấu hình Eureka Server

Sửa đổi service Eureka Server để extend cấu hình mới:

```yaml
eureka-server:
  extends: microservice-configserver-config
  environment:
    SPRING_APPLICATION_NAME: "eurekaserver"
    # Các biến môi trường bổ sung
```

**Quan trọng**: Xóa dependency Config Server khỏi service Eureka Server vì nó đã có trong cấu hình chung.

### Cập nhật cấu hình Microservices

Cập nhật từng microservice (Accounts, Loans, Cards) để sử dụng cấu hình Eureka:

```yaml
accounts:
  extends: microservice-eureka-config
  # Cấu hình riêng của service

loans:
  extends: microservice-eureka-config
  # Cấu hình riêng của service

cards:
  extends: microservice-eureka-config
  # Cấu hình riêng của service
```

## Các lỗi cấu hình thường gặp

### Vấn đề 2: Lỗi thụt lề biến môi trường

**Vấn đề**: Eureka Server vẫn không kết nối được với Config Server.

**Nguyên nhân**: Các biến môi trường không được thụt lề đúng cách như các phần tử con dưới thuộc tính `environment`.

**Định dạng sai**:
```yaml
environment:
SPRING_PROFILES_ACTIVE: "default"
SPRING_CONFIG_IMPORT: "configserver:http://configserver:8071/"
```

**Định dạng đúng**:
```yaml
environment:
  SPRING_PROFILES_ACTIVE: "default"
  SPRING_CONFIG_IMPORT: "configserver:http://configserver:8071/"
```

**Giải pháp**: Đảm bảo tất cả các biến môi trường được thụt lề đúng cách như các phần tử con dưới thuộc tính `environment`.

## Các bước xác thực

### 1. Kiểm tra khởi động Container

Kiểm tra Docker Dashboard hoặc chạy:

```bash
docker ps
```

Xác minh rằng tất cả các containers đang chạy thành công:
- Config Server
- Eureka Server
- Accounts Microservice
- Loans Microservice
- Cards Microservice

### 2. Truy cập Eureka Dashboard

Mở trình duyệt và truy cập:

```
http://localhost:8070
```

Xác minh rằng tất cả các microservices đã đăng ký với Eureka Server.

### 3. Kiểm tra API Microservice

Sử dụng Postman hoặc bất kỳ API client nào để kiểm tra theo trình tự sau:

#### Tạo tài khoản
```http
POST http://localhost:8080/api/create
```

#### Tạo thẻ
```http
POST http://localhost:8080/api/cards/create
```
Sử dụng cùng số điện thoại với tài khoản.

#### Tạo khoản vay
```http
POST http://localhost:8080/api/loans/create
```
Sử dụng cùng số điện thoại với tài khoản.

#### Lấy thông tin chi tiết khách hàng
```http
GET http://localhost:8080/api/fetchCustomerDetails?mobileNumber={mobileNumber}
```

API này minh họa Feign Client tận dụng Eureka Server để gọi các microservices khác (Loans và Cards).

**Kết quả mong đợi**: Phản hồi thành công chứa:
- Thông tin chi tiết khách hàng
- Thông tin chi tiết tài khoản
- Thông tin chi tiết khoản vay
- Thông tin chi tiết thẻ

## Cấu hình đa môi trường

### Áp dụng thay đổi cho các Profile khác

Sau khi xác thực cấu hình trong profile default, sao chép các thay đổi sang các môi trường khác:

#### Môi trường QA

1. Sao chép `docker-compose.yml` vào `qa/docker-compose.yml`
2. Sao chép `common-config.yml` vào profile QA
3. Cập nhật tên profile từ "default" thành "qa"

#### Môi trường Production

1. Sao chép `docker-compose.yml` vào `prod/docker-compose.yml`
2. Sao chép `common-config.yml` vào profile Production
3. Cập nhật tên profile từ "default" thành "prod"

## Dọn dẹp

Để dừng và xóa tất cả containers:

```bash
docker compose down
```

Lệnh này xóa tất cả các containers đang chạy và đã dừng được tạo bởi Docker Compose.

## Thực hành tốt nhất

1. **Môi trường sạch**: Luôn đảm bảo không có containers xung đột đang chạy trước khi khởi động Docker Compose
2. **Thứ tự khởi động**: Tuân thủ các phụ thuộc dịch vụ - Config Server → Eureka Server → Microservices
3. **Tái sử dụng cấu hình**: Sử dụng service extension để tránh trùng lặp cấu hình
4. **Định dạng YAML**: Chú ý cẩn thận đến việc thụt lề trong các file YAML
5. **Health Checks**: Triển khai các health check dependencies phù hợp giữa các dịch vụ
6. **Kiểm tra**: Kiểm tra toàn bộ luồng sau khi triển khai để đảm bảo tất cả các tích hợp hoạt động

## Tóm tắt

Hướng dẫn này đã đề cập:
- Triển khai microservices với Docker Compose
- Cấu hình tích hợp Eureka Server
- Xử lý các vấn đề cấu hình thường gặp
- Xác thực đăng ký dịch vụ và giao tiếp
- Thiết lập cấu hình đa môi trường

Với cấu hình phù hợp, tất cả các microservices đăng ký thành công với Eureka Server và giao tiếp liền mạch thông qua service discovery và tích hợp Feign Client.