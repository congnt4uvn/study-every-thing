# Microservices Hướng Sự Kiện với RabbitMQ - Hướng Dẫn Demo

## Tổng Quan

Hướng dẫn này trình bày cách triển khai giao tiếp bất đồng bộ giữa các microservices sử dụng RabbitMQ làm message broker. Chúng ta sẽ kích hoạt các sự kiện từ Accounts microservice đến Message microservice bằng framework Spring Cloud Stream.

## Yêu Cầu Tiên Quyết

- Docker Desktop chạy trên hệ thống local
- RabbitMQ Docker container
- Spring Boot microservices với Spring Cloud Stream
- Keycloak Authorization Server
- Postman để test API

## Các Thành Phần Kiến Trúc

### Microservices
- **Config Server**: Quản lý cấu hình tập trung
- **Eureka Server**: Service discovery và registration
- **Accounts Microservice**: Xử lý các thao tác tài khoản và phát hành events
- **Message Microservice**: Tiêu thụ events và gửi thông báo email/SMS
- **Gateway Server**: Hoạt động như OAuth2 resource server với Spring Security

### Hạ Tầng
- **RabbitMQ**: Message broker cho giao tiếp bất đồng bộ
- **Keycloak**: OAuth2 authorization server
- **Docker**: Container runtime

## Thiết Lập Demo Từng Bước

### 1. Khởi Động RabbitMQ

Đầu tiên, khởi động RabbitMQ bằng Docker:

```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:management
```

**Tham số:**
- `-d`: Chạy ở chế độ detached (chạy nền)
- `-p 5672:5672`: Cổng giao thức AMQP
- `-p 15672:15672`: Cổng giao diện quản lý

**Xác Minh:**
- Kiểm tra Docker Desktop để thấy RabbitMQ container đang chạy
- Truy cập RabbitMQ console tại: `http://localhost:15672`
- Thông tin đăng nhập mặc định: `guest` / `guest`

### 2. Khởi Động Microservices

Khởi động các microservices theo thứ tự sau:

1. **Config Server**
   - Mở main class của Config Server
   - Chạy ở chế độ debug

2. **Eureka Server**
   - Khởi động sau khi Config Server đã hoạt động
   - Chạy ở chế độ debug

3. **Accounts Microservice**
   - Mở main class `AccountsApplication`
   - Chạy ở chế độ debug

4. **Message Microservice**
   - Mở main class `MessageApplication`
   - Chạy ở chế độ debug

5. **Gateway Server**
   - Khởi động như OAuth2 resource server
   - Được bảo mật bằng Spring Security

**Lưu ý:** Không cần khởi động Cards và Loans microservices cho demo này.

### 3. Khởi Động Keycloak

Khởi động container Keycloak đã tồn tại:

```bash
docker start <keycloak-container-name>
```

**Quan trọng:** Đừng xóa container Keycloak để giữ lại thông tin client, roles và người dùng. Chỉ dừng nó khi không cần thiết.

## Cấu Hình RabbitMQ Console

### Truy Cập Console

Truy cập `http://localhost:15672` và đăng nhập với:
- Username: `guest`
- Password: `guest`

### Các Thành Phần Chính

#### Exchanges
- **Tên**: `send-communication`
- **Nguồn**: Được định nghĩa trong `application.yml` của Accounts Microservice như là destination
- **Mục đích**: Định tuyến messages đến queue phù hợp

#### Queues
- **Tên**: `send-communication.message`
- **Binding**: Kết nối với exchange `send-communication`
- **Nguồn**: Được định nghĩa trong `application.yml` của Message Microservice

#### Cấu Hình Bindings

**Message Microservice (Input Binding):**
```yaml
spring:
  cloud:
    stream:
      bindings:
        input:
          destination: send-communication
          group: message
```

Tên queue được tạo bằng cách nối: `destination` + `.` + `group` = `send-communication.message`

#### Bindings Tự Động Tạo

Spring Cloud Stream tự động tạo output bindings dựa trên định nghĩa function:
- **Output Binding**: `emailsms-out-0`
- **Nguồn**: Composed function definition có tên `emailsms`
- **Trạng thái**: Chưa bind với queue nào (exchange rỗng)

## Kiểm Thử Triển Khai

### 1. Lấy Access Token

Sử dụng Keycloak để lấy OAuth2 token bằng Client Credentials flow:

1. Truy cập Keycloak Admin Console: `http://localhost:7080`
2. Đăng nhập với: `admin` / `admin`
3. Điều hướng đến: Clients → `EazyBankCallCenterCC`
4. Vào tab Credentials
5. Copy client secret

### 2. Kiểm Thử API với Postman

**Collection:** Gateway Security
**API:** `Accounts_POST_ClientCredentials`

**Các Bước:**
1. Cấu hình client credentials trong Postman
2. Lấy access token mới
3. Tạo tài khoản với số điện thoại test (ví dụ: kết thúc bằng 688)
4. Gửi POST request

**Kết Quả Mong Đợi:**
- HTTP Status: `201 Created`
- Response Time: ~51 milliseconds (ngay lập tức)
- Message được gửi thành công đến RabbitMQ

### 3. Giám Sát Luồng Xử Lý

#### Console Accounts Microservice
```
Sending communication request for the details...
Is the communication request successfully triggered: true
```

#### RabbitMQ Console
- Điều hướng đến Exchanges → `send-communication`
- Kiểm tra biểu đồ để thấy message spike
- Xác minh message đã nhận

#### Console Message Microservice
```
Sending email with the details...
Sending SMS with the details...
```

## Minh Họa Giao Tiếp Bất Đồng Bộ

### Demo Chế Độ Chậm

Để minh họa tính chất bất đồng bộ:

1. **Đặt Breakpoint**
   - Đặt breakpoint trong hàm email của Message Microservice
   - Đây là hàm đầu tiên được kích hoạt khi nhận message

2. **Tạo Tài Khoản Mới**
   - Sử dụng số điện thoại kết thúc bằng 687
   - Lấy access token mới
   - Gửi POST request

3. **Quan Sát Hành Vi**
   - Accounts microservice trả về response ngay lập tức (51ms)
   - Breakpoint của Message microservice bị kích hoạt nhưng chưa xử lý
   - **Điểm Chính**: Accounts microservice không đợi Message microservice

4. **Hiểu Về Luồng Xử Lý**
   - Accounts microservice đưa message vào RabbitMQ
   - Tiếp tục với logic business còn lại
   - Trả về response ngay lập tức
   - Message microservice xử lý độc lập

5. **Nhả Breakpoint**
   - Message microservice tiếp tục xử lý
   - Logs email và SMS xuất hiện
   - Xử lý diễn ra bất đồng bộ (có thể là 1 phút, 2 phút, hoặc thậm chí 1 ngày sau)

## Các Khái Niệm Chính

### Lợi Ích Giao Tiếp Bất Đồng Bộ

1. **Loose Coupling**: Accounts microservice không biết về Message microservice
2. **Xử Lý Độc Lập**: Mỗi service hoạt động theo tốc độ riêng
3. **Khả Năng Chịu Lỗi**: Nếu Message service bị down, Accounts service vẫn hoạt động
4. **Khả Năng Mở Rộng**: Các services có thể scale độc lập
5. **Hiệu Suất**: Response ngay lập tức cho client mà không đợi xử lý downstream

### Vai Trò Message Broker

RabbitMQ hoạt động như trung gian:
- Accounts microservice chỉ biết về message broker
- Message microservice chỉ biết về message broker
- Không có giao tiếp trực tiếp service-to-service
- Broker xử lý routing và delivery message

## Cải Tiến Tương Lai

### Giao Tiếp Bất Đồng Bộ Hai Chiều

Các bước tiếp theo bao gồm triển khai giao tiếp ngược:

1. Message microservice gửi thông báo trả lại cho Accounts microservice
2. Thông báo được gửi sau khi hoàn thành xử lý email/SMS
3. Accounts microservice cập nhật bản ghi của mình
4. Thời gian: Có thể ngay lập tức hoặc trễ (phút, giờ, hoặc ngày)

**Lợi ích:** Audit trail hoàn chỉnh và theo dõi trạng thái qua các services.

## Cập Nhật Code

### Cải Thiện Log Statement

**Ban đầu:**
```java
// Is the communication request successfully processed?
```

**Sau khi cập nhật:**
```java
// Is the communication request successfully triggered?
```

**Lý do:** Phản ánh chính xác hơn rằng chúng ta đang kích hoạt request, không phải đợi xử lý hoàn tất.

## Best Practices

1. **Quản Lý Container**: Đừng xóa containers có cấu hình (như Keycloak)
2. **Thứ Tự Khởi Động Service**: Tuân theo phân cấp dependency (Config → Eureka → Services)
3. **Quản Lý Token**: Refresh access tokens khi hết hạn
4. **Debug Mode**: Sử dụng để troubleshooting tốt hơn trong quá trình phát triển
5. **Đặt Tên Message**: Sử dụng tên rõ ràng, nhất quán cho exchanges và queues

## Xử Lý Sự Cố

### Các Vấn Đề Thường Gặp

1. **401 Unauthorized**: Token hết hạn, lấy access token mới
2. **Connection Refused**: Đảm bảo Docker và tất cả services đang chạy
3. **No Message Received**: Kiểm tra cấu hình RabbitMQ bindings
4. **Service Not Starting**: Xác minh các dependent services đang chạy

## Kết Luận

Demo này giới thiệu sức mạnh của kiến trúc microservices hướng sự kiện sử dụng RabbitMQ. Pattern giao tiếp bất đồng bộ cho phép:

- Hiệu suất cao với responses ngay lập tức
- Kiến trúc linh hoạt với loose coupling
- Các services có khả năng mở rộng hoạt động độc lập
- Message delivery đáng tin cậy thông qua message broker

Triển khai này minh họa các patterns microservices thực tế được sử dụng trong môi trường production.

---

**Các Bước Tiếp Theo:** Triển khai giao tiếp bất đồng bộ hai chiều cho kiến trúc event-driven hoàn chỉnh.