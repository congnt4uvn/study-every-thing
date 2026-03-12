# Spring Cloud Bus để Làm Mới Cấu Hình Động

## Tổng Quan

Hướng dẫn này trình bày cách sử dụng Spring Cloud Bus để làm mới cấu hình trên nhiều instance microservice mà không cần khởi động lại chúng. Bằng cách triển khai Spring Cloud Bus với message broker như RabbitMQ, bạn có thể tránh việc phải gọi API refresh trên từng instance microservice riêng lẻ.

## Vấn Đề

Khi sử dụng Spring Cloud Config Server, chúng ta gặp phải thách thức:
- Phải gọi API refresh cho **từng instance microservice** một cách riêng biệt
- Nếu bạn có 500 instance trong môi trường production, bạn cần gọi endpoint refresh 500 lần
- Điều này trở nên không thể quản lý được khi hệ thống của bạn mở rộng quy mô

## Giải Pháp: Spring Cloud Bus

Spring Cloud Bus kết nối tất cả các node của hệ thống phân tán với một message broker nhẹ. Nó có thể phát sóng các thay đổi trạng thái (như thay đổi cấu hình) hoặc hướng dẫn quản lý đến tất cả các microservice được kết nối.

### Lợi Ích Chính

- **Chỉ Một Lần Gọi API**: Chỉ cần gọi bus refresh API một lần trên bất kỳ instance nào
- **Tự Động Lan Truyền**: Các thay đổi được tự động truyền đạt đến tất cả các instance khác
- **Khả Năng Mở Rộng**: Hoạt động hiệu quả cho dù bạn có 5 hay 500 instance

## Các Bước Triển Khai

### Bước 1: Thiết Lập RabbitMQ

RabbitMQ đóng vai trò là message broker kết nối tất cả các microservice.

**Sử Dụng Docker (Khuyến Nghị)**:
```bash
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

Lệnh này:
- Cài đặt component quản lý RabbitMQ (UI)
- Cài đặt component core RabbitMQ (chức năng message queue)
- Mở port 5672 cho message broker
- Mở port 15672 cho giao diện quản lý

### Bước 2: Thêm Dependencies

Thêm dependency Spring Cloud Bus AMQP vào tất cả microservice (accounts, cards, loans) **và** config server.

**pom.xml**:
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
```

Dependency này bao gồm cả:
- Spring Cloud Starter Bus
- Tích hợp RabbitMQ (AMQP)

### Bước 3: Kích Hoạt Actuator Endpoints

Đảm bảo endpoint bus refresh được expose trong tất cả microservice.

**application.yml**:
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

Sử dụng `"*"` để expose tất cả actuator endpoints bao gồm:
- `/actuator/refresh`
- `/actuator/bus-refresh`

### Bước 4: Cấu Hình Kết Nối RabbitMQ

Thêm thông tin kết nối RabbitMQ trong `application.yml` của tất cả microservice.

**application.yml**:
```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

**Lưu ý**: Đây là các giá trị mặc định. Spring Boot sẽ tự động kết nối sử dụng các giá trị mặc định này ngay cả khi không được cấu hình rõ ràng. Tuy nhiên, khuyến nghị nên chỉ định chúng để rõ ràng và trong trường hợp sử dụng các giá trị khác trong môi trường của bạn.

### Bước 5: Build và Khởi Động Services

1. **Clean build** tất cả microservice để tải xuống các dependency mới:
   ```bash
   mvn clean install
   ```

2. **Khởi động services** theo thứ tự:
   - Config Server
   - Accounts Microservice
   - Loans Microservice
   - Cards Microservice

## Cách Hoạt Động

### Luồng Kiến Trúc

1. **Thiết Lập Ban Đầu**: Tất cả microservice và config server đăng ký làm client với RabbitMQ message broker

2. **Thay Đổi Cấu Hình**: Push các thay đổi cấu hình mới lên GitHub repository

3. **Kích Hoạt Refresh**: Gọi `/actuator/bus-refresh` trên **bất kỳ một** instance microservice

4. **Phát Sóng Sự Kiện**: Config server kích hoạt một config change event đến message broker

5. **Lan Truyền**: Message broker truyền đạt thay đổi đến tất cả các instance microservice đã đăng ký

6. **Tải Lại**: Tất cả instance kết nối với config server và tải lại properties mà không cần khởi động lại

### Ví Dụ Quy Trình

**Trước khi refresh**:
- Tất cả microservice hiển thị: `"This is production"`

**Thay đổi cấu hình**:
- Cập nhật GitHub: Đổi "production" thành "prod"
- Config server có thể đọc ngay các giá trị mới

**Gọi bus refresh**:
```http
POST http://localhost:8080/actuator/bus-refresh
```

**Kết quả**:
- Response: `204 No Content` (thành công)
- Tất cả microservice bây giờ hiển thị: `"This is prod"` mà không cần khởi động lại

## Kiểm Tra Triển Khai

1. **Xác minh giá trị ban đầu** bằng cách gọi endpoint `/contact-info` trên tất cả microservice

2. **Thay đổi giá trị property** trong GitHub repository (ví dụ: trong `accounts-prod.yml`, `cards-prod.yml`, `loans-prod.yml`)

3. **Gọi bus refresh** trên bất kỳ instance nào:
   ```http
   POST http://localhost:8080/actuator/bus-refresh
   ```

4. **Xác minh thay đổi** bằng cách gọi `/contact-info` trên tất cả microservice - tất cả phải phản ánh giá trị mới

## Tóm Tắt Các Yêu Cầu

| Bước | Hành Động | Áp Dụng Cho |
|------|-----------|-------------|
| 1 | Thêm dependency Actuator | Tất cả microservice |
| 2 | Kích hoạt endpoint bus refresh | Tất cả microservice |
| 3 | Thêm dependency Spring Cloud Bus AMQP | Tất cả microservice + Config Server |
| 4 | Thiết lập và khởi động RabbitMQ | Hệ thống local/Production |
| 5 | Cấu hình thông tin kết nối RabbitMQ | Tất cả microservice (tùy chọn nếu dùng mặc định) |

## Ưu Điểm

✅ **Khả Năng Mở Rộng**: Làm mới hàng trăm instance chỉ với một lần gọi API  
✅ **Hiệu Quả**: Không cần khởi động lại microservice  
✅ **Tự Động Hóa**: Các thay đổi lan truyền tự động qua message broker  
✅ **Linh Hoạt**: Hoạt động với RabbitMQ hoặc Apache Kafka

## Hạn Chế

⚠️ **Trách Nhiệm Bổ Sung**: Phải duy trì và giám sát hạ tầng message broker  
⚠️ **Kích Hoạt Thủ Công**: Vẫn phải có ai đó gọi endpoint bus refresh ít nhất một lần  
⚠️ **Phụ Thuộc**: Tất cả instance phải được kết nối với cùng một message broker  

## Khi Nào Nên Sử Dụng Phương Pháp Này

**Phù hợp khi**:
- Thay đổi cấu hình không thường xuyên (không hàng ngày)
- Bạn có nhiều instance microservice (100+)
- Việc refresh thủ công hoặc qua CI/CD là chấp nhận được

**Cân nhắc giải pháp khác nếu**:
- Thay đổi cấu hình xảy ra rất thường xuyên
- Bạn cần làm mới hoàn toàn tự động không cần can thiệp thủ công
- Bạn muốn tránh chi phí vận hành của việc quản lý message broker

## Bước Tiếp Theo

Để đạt được việc làm mới cấu hình hoàn toàn tự động mà không cần can thiệp thủ công, hãy xem xét:
- Sử dụng Spring Cloud Config Monitor với webhooks
- Triển khai GitHub webhooks để tự động kích hoạt bus refresh
- Khám phá các mẫu quản lý cấu hình thay thế

## Tài Nguyên Bổ Sung

- [Tài Liệu Spring Cloud Bus](https://spring.io/projects/spring-cloud-bus)
- [Tài Liệu RabbitMQ](https://www.rabbitmq.com/documentation.html)
- [Tài Liệu Spring Cloud Config](https://spring.io/projects/spring-cloud-config)