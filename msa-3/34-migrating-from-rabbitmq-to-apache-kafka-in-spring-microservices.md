# Di Chuyển từ RabbitMQ sang Apache Kafka trong Spring Microservices

## Tổng Quan

Hướng dẫn này trình bày cách di chuyển các microservices Spring Boot từ RabbitMQ sang Apache Kafka cho giao tiếp bất đồng bộ. Quá trình di chuyển được đơn giản hóa bằng cách sử dụng Spring Cloud Stream và Spring Cloud Functions, chỉ yêu cầu thay đổi code tối thiểu.

## Yêu Cầu Tiên Quyết

- Dự án Spring Boot microservices (code Section 13)
- Apache Kafka chạy local trên cổng 9092
- IntelliJ IDEA với hỗ trợ Maven
- Plugin Kafkalytic (để giám sát Kafka cluster)
- Keycloak server (cho xác thực OAuth2)
- Docker Desktop

## Các Bước Di Chuyển

### 1. Thiết Lập Dự Án

Đầu tiên, tạo một thư mục workspace mới cho Section 14:

1. Sao chép code từ Section 13
2. Đổi tên thư mục thành `section14`
3. Xóa thư mục `.idea`
4. Mở dự án trong IntelliJ IDEA

### 2. Cập Nhật Maven Dependencies

#### Accounts Microservice

Mở file `pom.xml` trong Accounts microservice và thay thế dependency RabbitMQ:

**Trước đây:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-rabbit</artifactId>
</dependency>
```

**Sau khi thay đổi:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-kafka</artifactId>
</dependency>
```

Cập nhật tên tag từ `s13` thành `s14` và reload Maven.

#### Message Microservice

Thực hiện thay đổi dependency tương tự trong file `pom.xml` của Message microservice:

- Thay thế `spring-cloud-stream-binder-rabbit` bằng `spring-cloud-stream-binder-kafka`
- Cập nhật tên tag từ `s13` thành `s14`
- Reload các thay đổi Maven

### 3. Cập Nhật Cấu Hình Application

#### Cấu Hình Message Microservice

Mở file `application.yml` trong Message microservice:

1. **Xóa các properties RabbitMQ:**
   - Xóa tất cả chi tiết kết nối RabbitMQ

2. **Thêm cấu hình Kafka:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
```

#### Cấu Hình Accounts Microservice

Mở file `application.yml` trong Accounts microservice:

1. **Xóa các properties RabbitMQ:**
   - Xóa tất cả chi tiết kết nối RabbitMQ

2. **Thêm cấu hình Kafka:**
```yaml
spring:
  cloud:
    stream:
      kafka:
        binder:
          brokers: localhost:9092
```

> **Lưu ý:** Nếu bạn có nhiều Kafka brokers trong một cluster, hãy liệt kê tất cả các broker endpoints dưới dạng các phần tử mảng.

### 4. Hoàn Thành Cấu Hình

Như vậy là xong! Không cần thay đổi code nào khác. Sức mạnh của Spring Cloud Stream trừu tượng hóa tất cả các vấn đề về cơ sở hạ tầng, giúp việc chuyển đổi từ RabbitMQ sang Kafka trở nên liền mạch.

## Kiểm Thử Quá Trình Di Chuyển

### 1. Khởi Động Các Services Cần Thiết

Khởi động tất cả các microservices theo thứ tự sau:

1. Config Server
2. Eureka Server
3. Accounts Application
4. Message Application
5. Gateway Server Application

Cả Accounts và Message microservices giờ đây sẽ kết nối với Kafka instance local.

### 2. Xác Minh Thiết Lập Kafka với Plugin Kafkalytic

1. Cài đặt plugin **Kafkalytic** từ marketplace IntelliJ IDEA
2. Click nút **Add** và cấu hình:
   - Broker: `localhost:9092`
3. Click **Test Connection** để xác minh kết nối
4. Click **OK** để lưu

#### Xác Minh Các Thành Phần Kafka:

- **Brokers:** Sẽ hiển thị 1 broker (localhost:9092)
- **Consumers:** Sẽ hiển thị 2 consumers
  - Message microservice (tiêu thụ từ Accounts)
  - Accounts microservice (tiêu thụ từ Message)
- **Topics:** Sẽ hiển thị:
  - `communication-sent`
  - `send-communication`
  - `__consumer_offsets` (topic nội bộ của Kafka)

### 3. Kiểm Tra Giao Tiếp Bất Đồng Bộ

#### Khởi Động Keycloak Server

1. Mở Docker Desktop
2. Khởi động container Keycloak hiện có
3. Truy cập Keycloak tại `http://localhost:7080`
4. Đăng nhập với thông tin: `admin` / `admin`
5. Điều hướng đến **Clients** và tìm `eazybank-callcenter-cc`
6. Sao chép client credentials

#### Đặt Breakpoint Debug

1. Mở Message microservice
2. Điều hướng đến class `MessageFunctions`
3. Đặt breakpoint trong hàm `email`

#### Thực Hiện Kiểm Thử API với Postman

1. Lấy access token:
   - Sử dụng client ID và credentials đã sao chép
   - Click **Get New Access Token**
2. Sử dụng access token để gọi **Create API** trong Accounts microservice
3. Click **Send**

#### Xác Minh Kết Quả

1. Breakpoint sẽ được kích hoạt trong hàm `email`
2. Kiểm tra H2 console của Accounts microservice:
   - Điều hướng đến H2 console
   - Click **Connect**
   - Truy vấn bảng `accounts`
   - **Trước khi thả breakpoint:** cột `communication_switch` = `null`
3. Thả breakpoint
4. Truy vấn lại bảng `accounts`
   - **Sau khi thả breakpoint:** cột `communication_switch` = `true`

Điều này xác nhận rằng giao tiếp bất đồng bộ end-to-end đang hoạt động với Apache Kafka!

## Lợi Ích Chính của Spring Cloud Stream

- **Trừu Tượng Hóa Cơ Sở Hạ Tầng:** Tất cả các vấn đề về cơ sở hạ tầng được xử lý tự động
- **Di Chuyển Dễ Dàng:** Chuyển đổi giữa các hệ thống messaging với thay đổi tối thiểu
- **Trải Nghiệm Nhà Phát Triển:** Cấu hình dependency và properties đơn giản
- **Cách Tiếp Cận Hiện Đại:** Tận dụng các kỹ thuật mới nhất trong Spring ecosystem

## Các Bước Tiếp Theo

### Kiểm Thử Môi Trường Docker

Để kiểm thử trong môi trường Docker:

1. Tạo Docker images cụ thể cho Section 14
2. Push images lên Docker Hub
3. Cập nhật file Docker Compose
4. Thực thi và xác thực các thay đổi trong môi trường Docker

## Thực Hành Tốt Nhất

1. **Luôn sử dụng Spring Cloud Functions và Spring Cloud Stream** cho messaging trong microservices
2. **Tránh các cách tiếp cận cũ** cho tích hợp RabbitMQ/Kafka
3. **Tận dụng các công cụ hiện đại của Spring ecosystem** để có trải nghiệm nhà phát triển tốt hơn
4. **Chia sẻ kiến thức** với các nhà phát triển khác về những kỹ thuật hiệu quả này

## Kết Luận

Di chuyển từ RabbitMQ sang Apache Kafka với Spring Cloud Stream cực kỳ đơn giản. Framework xử lý toàn bộ sự phức tạp, cho phép các nhà phát triển tập trung vào logic nghiệp vụ thay vì các vấn đề về cơ sở hạ tầng. Điều này thể hiện sức mạnh và tính linh hoạt của Spring Cloud Stream trong việc xây dựng các microservices hướng sự kiện.

## Tài Nguyên Bổ Sung

- Tài liệu Spring Cloud Stream
- Tài liệu Apache Kafka
- Hướng dẫn Spring Cloud Functions
- Tài liệu Plugin Kafkalytic