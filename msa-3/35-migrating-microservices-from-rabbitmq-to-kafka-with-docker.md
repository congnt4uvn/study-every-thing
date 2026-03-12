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