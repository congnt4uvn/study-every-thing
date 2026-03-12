# Làm mới cấu hình Microservices với Spring Cloud Bus

## Tổng quan

Hướng dẫn này giải thích cách sử dụng Spring Cloud Bus để làm mới cấu hình trên nhiều instance microservice mà không cần can thiệp thủ công trên từng instance. Phương pháp này loại bỏ nhu cầu phải gọi API refresh riêng lẻ cho từng instance microservice.

## Vấn đề

Khi sử dụng Spring Cloud Config Server, việc làm mới cấu hình lúc runtime yêu cầu phải gọi API refresh cho **từng instance microservice một cách riêng biệt**. Trong môi trường production với hàng trăm instance, điều này trở nên không khả thi và tốn thời gian.

## Giải pháp: Spring Cloud Bus

**Spring Cloud Bus** kết nối tất cả các node của hệ thống phân tán với một message broker nhẹ. Nó có thể phát sóng các thay đổi trạng thái (như thay đổi cấu hình) hoặc lệnh quản lý đến tất cả các instance được kết nối.

### Lợi ích chính

- **Chỉ gọi API một lần**: Gọi API bus-refresh chỉ một lần trên bất kỳ instance nào
- **Tự động lan truyền**: Thay đổi tự động lan truyền đến tất cả instance kết nối với message broker
- **Khả năng mở rộng**: Hoạt động với 500+ instance mà không tăng thêm chi phí
- **Hỗ trợ nhiều broker**: RabbitMQ, Kafka, v.v.

## Kiến trúc

Spring Cloud Bus sử dụng message broker (RabbitMQ hoặc Kafka) để kết nối tất cả các instance microservice. Khi bạn gọi endpoint bus-refresh trên một instance, message broker sẽ truyền thông tin thay đổi cấu hình đến tất cả các node đã đăng ký.

## Các bước triển khai

### Bước 1: Cài đặt RabbitMQ

Sử dụng Docker để nhanh chóng cài đặt RabbitMQ:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

Lệnh này khởi động RabbitMQ với:
- **Core component** (port 5672): Xử lý chức năng message queue
- **Management UI** (port 15672): Cung cấp giao diện web để quản lý RabbitMQ

### Bước 2: Thêm Dependencies

Thêm dependency Spring Cloud Bus AMQP vào `pom.xml` của **tất cả microservices** và **Config Server**:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
```

Dependency này bao gồm:
- Spring Cloud Bus
- Tích hợp RabbitMQ (AMQP)

### Bước 3: Kích hoạt Actuator Endpoints

Đảm bảo dependency actuator có mặt trong tất cả microservices:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

Trong `application.yml` của mỗi microservice, expose endpoint bus-refresh:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"  # Expose tất cả actuator endpoints bao gồm bus-refresh
```

Bạn có thể chỉ định cụ thể chỉ expose `bus-refresh` nếu muốn:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "bus-refresh"
```

### Bước 4: Cấu hình kết nối RabbitMQ

Thêm thông tin kết nối RabbitMQ vào `application.yml` của **tất cả microservices** và **Config Server**:

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

**Lưu ý**: Đây là các giá trị mặc định. Nếu RabbitMQ đang chạy với cấu hình mặc định, Spring Boot sẽ tự động kết nối ngay cả khi không chỉ định rõ ràng các thuộc tính này. Tuy nhiên, đối với các thiết lập tùy chỉnh, hãy đảm bảo cung cấp giá trị chính xác.

### Bước 5: Build và khởi động lại Services

1. Dừng tất cả các instance microservice đang chạy
2. Thực hiện Maven clean build để tải xuống dependencies mới:
   ```bash
   mvn clean install
   ```
3. Khởi động Config Server trước
4. Khởi động tất cả microservices khác (Accounts, Loans, Cards, v.v.)

## Kiểm tra làm mới cấu hình

### Bước 1: Xác minh cấu hình ban đầu

Kiểm tra endpoint contact-info cho mỗi microservice để xác minh giá trị cấu hình hiện tại:

```http
GET http://localhost:8080/api/contact-info
```

Ví dụ response:
```json
{
  "message": "production APIs"
}
```

### Bước 2: Cập nhật cấu hình trong GitHub

Sửa đổi các file cấu hình trong GitHub repository (ví dụ: `accounts-prod.yml`, `loans-prod.yml`, `cards-prod.yml`):

```yaml
# Thay đổi từ
message: "production APIs"

# Thành
message: "prod APIs"
```

Commit và push thay đổi lên GitHub.

### Bước 3: Xác minh Config Server có giá trị mới nhất

Kiểm tra Config Server có thể đọc các giá trị đã cập nhật:

```http
GET http://localhost:8888/accounts/prod
```

Config Server nên trả về cấu hình đã cập nhật ngay lập tức mà không cần khởi động lại.

### Bước 4: Gọi Bus Refresh API

Gọi endpoint bus-refresh trên **bất kỳ một microservice nào** (ví dụ: Accounts):

```http
POST http://localhost:8080/actuator/bus-refresh
```

Response mong đợi: `204 No Content` (xử lý thành công không trả về nội dung)

### Bước 5: Xác minh tất cả Microservices đã làm mới

Kiểm tra endpoint contact-info trên **tất cả microservices** (Accounts, Loans, Cards):

```http
GET http://localhost:8080/api/contact-info  # Accounts
GET http://localhost:8090/api/contact-info  # Loans
GET http://localhost:9000/api/contact-info  # Cards
```

**Tất cả microservices nên trả về cấu hình đã cập nhật** mà không cần:
- Khởi động lại bất kỳ instance nào
- Gọi refresh/bus-refresh trên từng instance riêng lẻ

## Cách hoạt động: Luồng hoàn chỉnh

1. **Push thay đổi**: Developer push thay đổi cấu hình lên GitHub repository
2. **Gọi Bus Refresh**: Người vận hành gọi `actuator/bus-refresh` trên bất kỳ instance microservice nào
3. **Sự kiện thay đổi Config**: Microservice kích hoạt sự kiện thay đổi cấu hình đến message broker
4. **Phát sóng đến tất cả Nodes**: Message broker phát sóng sự kiện đến tất cả instance microservice đã đăng ký
5. **Tải lại cấu hình**: Mỗi microservice kết nối với Config Server và tải lại properties mà không khởi động lại

```
┌──────────────┐
│   GitHub     │
│  Repository  │
└──────┬───────┘
       │ 1. Push thay đổi
       ▼
┌──────────────────┐
│  Config Server   │◄────────────────┐
└──────┬───────────┘                 │
       │                             │
       │ 3. Kích hoạt sự kiện        │ 5. Tải lại Config
       ▼                             │
┌──────────────────┐                 │
│  RabbitMQ Broker │                 │
└──────┬───────────┘                 │
       │ 4. Phát sóng                │
       ├─────────────────────────────┤
       │                             │
   ┌───▼────┐  ┌────────┐  ┌────────▼┐
   │Accounts│  │ Loans  │  │  Cards  │
   │  (1)   │  │        │  │         │
   └────────┘  └────────┘  └─────────┘
   2. POST /actuator/bus-refresh
```

## Tóm tắt các thay đổi cần thiết

| Bước | Thành phần | Hành động |
|------|-----------|--------|
| 1 | Tất cả Microservices | Thêm dependency actuator |
| 2 | Tất cả Microservices | Kích hoạt endpoint bus-refresh trong `application.yml` |
| 3 | Tất cả Microservices + Config Server | Thêm dependency `spring-cloud-starter-bus-amqp` |
| 4 | Hệ thống Local | Cài đặt RabbitMQ (khuyến nghị dùng Docker) |
| 5 | Tất cả Microservices + Config Server | Cấu hình thông tin kết nối RabbitMQ |

## Ưu điểm

✅ **Chỉ gọi một lần**: Làm mới tất cả instance với một lần gọi API  
✅ **Không cần khởi động lại**: Cập nhật cấu hình mà không có downtime  
✅ **Khả năng mở rộng**: Hoạt động với hàng trăm hoặc hàng nghìn instance  
✅ **Kiểm soát tập trung**: Quản lý cấu hình từ một nơi

## Cân nhắc

### Trách nhiệm bổ sung

Sử dụng Spring Cloud Bus yêu cầu:
- **Cài đặt message broker**: RabbitMQ hoặc Kafka phải được cài đặt và bảo trì
- **Độ tin cậy mạng**: Kết nối message broker phải ổn định
- **Giám sát**: Đảm bảo tất cả instance được đăng ký đúng cách với broker

### Khi nào nên sử dụng phương pháp này

**Phù hợp cho:**
- Môi trường có nhiều instance microservice (10+)
- Thay đổi cấu hình không thường xuyên
- Tổ chức có cơ sở hạ tầng hỗ trợ message brokers

**Có thể không cần thiết cho:**
- Triển khai nhỏ (2-3 instance)
- Cấu hình tĩnh hiếm khi thay đổi
- Dự án không có cơ sở hạ tầng message broker

## Nhược điểm: Vẫn cần kích hoạt thủ công

Ngay cả với Spring Cloud Bus, ai đó vẫn phải gọi API bus-refresh ít nhất một lần. Properties sẽ không tự động làm mới nếu không có lệnh gọi này.

Điều này có thể là:
- **Thủ công**: Nhóm vận hành gọi API khi cần thiết
- **Tự động hóa**: Pipeline CI/CD kích hoạt bus-refresh sau deployment
- **Script**: Script tùy chỉnh giám sát thay đổi và kích hoạt refresh

Đối với các tổ chức thay đổi properties thường xuyên (hàng ngày hoặc nhiều hơn), việc kích hoạt thủ công này vẫn có thể gây phiền toái. Phương pháp tiếp theo sẽ liên quan đến làm mới cấu hình tự động bằng webhooks hoặc các cơ chế khác.

## Kết luận

Spring Cloud Bus cung cấp giải pháp mạnh mẽ để làm mới cấu hình trên nhiều instance microservice. Bằng cách chấp nhận trách nhiệm bổ sung duy trì message broker, bạn có được khả năng cập nhật cấu hình hiệu quả trên toàn bộ hệ sinh thái microservices của mình.

Phương pháp này đạt được sự cân bằng giữa tính đơn giản trong vận hành và khả năng mở rộng, làm cho nó lý tưởng cho hầu hết các môi trường production với yêu cầu thay đổi cấu hình vừa phải.