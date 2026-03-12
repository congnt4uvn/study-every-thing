# Triển khai Gateway Server với Docker Compose

## Tổng quan

Hướng dẫn này bao gồm quy trình triển khai Spring Cloud Gateway server cùng với các microservice (Accounts, Loans, Cards) sử dụng Docker Compose. Chúng ta sẽ cấu hình health check, các phụ thuộc dịch vụ và xác thực tính năng correlation ID trên tất cả microservice.

## Yêu cầu trước khi bắt đầu

- Docker images đã được push lên Docker Hub với tag `S9`
- Các microservice hiện có: Accounts, Loans, Cards
- Config Server và Eureka Server đã được cấu hình
- Docker và Docker Compose đã được cài đặt

## Docker Images

Tất cả Docker images cho Section 9 đã được push lên Docker Hub với tag `S9`:
- `gatewayserver:S9`
- `accounts:S9`
- `loans:S9`
- `cards:S9`
- `configserver:S9`
- `eurekaserver:S9`

## Cấu hình Docker Compose

### 1. Thêm Gateway Server Service

Di chuyển đến thư mục `docker-compose/default` và mở file `docker-compose.yaml`. Thêm cấu hình Gateway Server service:

```yaml
gatewayserver:
  image: gatewayserver:S9
  container_name: gatewayserver-ms
  ports:
    - "8072:8072"
  environment:
    - SPRING_APPLICATION_NAME=gatewayserver
  depends_on:
    accounts:
      condition: service_healthy
    loans:
      condition: service_healthy
    cards:
      condition: service_healthy
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

### 2. Cập nhật Image Tags

Thay thế tất cả tag `S8` bằng `S9` trong toàn bộ file Docker Compose:
- Tìm kiếm: `S8`
- Thay thế bằng: `S9`

### 3. Cấu hình Health Checks

Thêm cấu hình health check cho từng microservice để đảm bảo thứ tự khởi động đúng.

#### Accounts Microservice (Cổng 8080)

```yaml
accounts:
  image: accounts:S9
  container_name: accounts-ms
  ports:
    - "8080:8080"
  healthcheck:
    test: "curl --fail --silent localhost:8080/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

#### Loans Microservice (Cổng 8090)

```yaml
loans:
  image: loans:S9
  container_name: loans-ms
  ports:
    - "8090:8090"
  healthcheck:
    test: "curl --fail --silent localhost:8090/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

#### Cards Microservice (Cổng 9000)

```yaml
cards:
  image: cards:S9
  container_name: cards-ms
  ports:
    - "9000:9000"
  healthcheck:
    test: "curl --fail --silent localhost:9000/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

## Thứ tự khởi động dịch vụ

Cấu hình Docker Compose đảm bảo các dịch vụ khởi động theo thứ tự sau:

1. **Config Server** - Quản lý cấu hình tập trung
2. **Eureka Server** - Khám phá và đăng ký dịch vụ
3. **Microservices** - Accounts, Loans và Cards (song song)
4. **Gateway Server** - Chỉ khởi động sau khi tất cả microservice đều healthy

## Các bước triển khai

### 1. Di chuyển đến thư mục Docker Compose

```bash
cd docker-compose/default
```

### 2. Khởi động tất cả Containers

```bash
docker compose up -d
```

Lệnh này sẽ khởi động tất cả container ở chế độ detached. Quá trình khởi động mất khoảng 1-2 phút.

### 3. Theo dõi tiến trình khởi động

Bạn có thể theo dõi các container sử dụng Docker Desktop hoặc dòng lệnh:

```bash
docker compose ps
```

Tất cả container sẽ hiển thị trạng thái "running" khi đã khởi động hoàn toàn.

## Kiểm thử triển khai

### 1. Tạo dữ liệu test

Sử dụng Gateway Server để tạo dữ liệu trong từng microservice:

**Tạo tài khoản:**
```http
POST http://localhost:8072/accounts/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Tạo thẻ:**
```http
POST http://localhost:8072/cards/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

**Tạo khoản vay:**
```http
POST http://localhost:8072/loans/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

### 2. Lấy thông tin khách hàng

Kiểm tra API tổng hợp lấy dữ liệu từ tất cả microservice:

```http
GET http://localhost:8072/accounts/api/fetchCustomerDetails?mobileNumber=1234567890
```

**Kết quả mong đợi:**
- Thông tin tài khoản
- Thông tin khoản vay
- Thông tin thẻ
- Response header: `easybank-correlationid` với correlation ID duy nhất

## Xác thực Correlation ID

Tính năng correlation ID cho phép theo dõi request qua nhiều microservice.

### 1. Kiểm tra Response Headers

Sau khi thực hiện request, kiểm tra response headers để tìm:
```
easybank-correlationid: <unique-id>
```

### 2. Xác minh Logs trong từng Microservice

Copy correlation ID và tìm kiếm nó trong logs của từng container:

**Accounts Microservice:**
```bash
docker logs accounts-ms | grep <correlation-id>
```

**Loans Microservice:**
```bash
docker logs loans-ms | grep <correlation-id>
```

**Cards Microservice:**
```bash
docker logs cards-ms | grep <correlation-id>
```

Bạn sẽ tìm thấy các log entry với:
- `RequestTraceFilter` - Request đến
- `ResponseTraceFilter` - Response đi

## Dừng Containers

Để dừng tất cả container đang chạy:

```bash
docker compose down
```

## Triển khai đa môi trường

### Môi trường QA

Cập nhật `qa/docker-compose.yml` với cùng cấu hình và đảm bảo:
```yaml
environment:
  - SPRING_PROFILES_ACTIVE=qa
```

### Môi trường Production

Cập nhật `prod/docker-compose.yml` với cùng cấu hình và đảm bảo:
```yaml
environment:
  - SPRING_PROFILES_ACTIVE=prod
```

## Lợi ích của Gateway Server

1. **Điểm truy cập duy nhất** - Client bên ngoài chỉ cần biết một URL
2. **Logic Client đơn giản** - Không cần quản lý nhiều URL microservice
3. **Tập trung Cross-Cutting Concerns** - Authentication, logging, rate limiting
4. **Định tuyến Request** - Định tuyến động dựa trên patterns
5. **Load Balancing** - Client-side load balancing với Eureka integration

## Xử lý sự cố

### Gateway Server không khởi động

- Xác minh tất cả microservice phụ thuộc đều healthy
- Kiểm tra Eureka Server đang chạy và có thể truy cập
- Xem lại gateway server logs: `docker logs gatewayserver-ms`

### Health Check thất bại

- Đảm bảo actuator endpoints được kích hoạt
- Xác minh port mappings đúng
- Kiểm tra kết nối mạng giữa các container

### Correlation ID không có

- Xác minh custom filters được cấu hình trong Gateway Server
- Kiểm tra thứ tự filter trong cấu hình gateway
- Xem lại gateway server logs để kiểm tra việc thực thi filter

## Các bước tiếp theo

Trong các phần tiếp theo, chúng ta sẽ nâng cao Gateway Server với:
- **Bảo mật** - Authentication và authorization
- **Khả năng chịu lỗi** - Circuit breakers và retry mechanisms
- **Resilience** - Rate limiting và bulkhead patterns
- **Giám sát** - Distributed tracing và metrics

## Tóm tắt

Chúng ta đã thành công:
- ✅ Cấu hình Gateway Server trong Docker Compose
- ✅ Triển khai health checks cho tất cả microservice
- ✅ Thiết lập các phụ thuộc dịch vụ đúng cách
- ✅ Xác thực correlation ID tracking qua các microservice
- ✅ Tạo cấu hình đa môi trường (QA và Prod)

Gateway Server hiện đóng vai trò là điểm truy cập duy nhất cho tất cả client bên ngoài, đơn giản hóa kiến trúc microservice và cung cấp nền tảng để triển khai các pattern nâng cao.

## Tài nguyên

- Website chính thức: [eazybytes.com](https://eazybytes.com)
- Liên hệ: Có sẵn trên website chính thức
- LinkedIn: Link profile trên website chính thức

---

**Lưu ý:** Tài liệu này là một phần của khóa học microservices toàn diện. Để biết thêm các khóa học và cập nhật, hãy truy cập website chính thức.