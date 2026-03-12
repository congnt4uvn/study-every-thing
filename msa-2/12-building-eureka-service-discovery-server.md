# Xây Dựng Eureka Service Discovery Server với Spring Cloud

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập một service discovery agent (tác nhân khám phá dịch vụ) sử dụng Eureka từ dự án Spring Cloud Netflix. Đây là một phần trong việc xây dựng kiến trúc microservices cho ứng dụng Eazy Bank.

## Yêu Cầu Trước

- Java 17
- Maven
- Spring Boot (phiên bản ổn định mới nhất)
- Các microservices đã có (accounts, loans, cards)
- Config Server đã được thiết lập

## Thiết Lập Ban Đầu

### 1. Tạo Cấu Trúc Dự Án

Tạo một thư mục mới `section 8` trong workspace của bạn và sao chép code từ `section 6 v2` (sử dụng H2 database thay vì MySQL).

### 2. Dọn Dẹp Dependencies

Xóa các dependencies không cần thiết như Spring Cloud Bus và RabbitMQ khỏi tất cả microservices:

**Từ `pom.xml`:**
- Xóa dependency `spring-cloud-bus`
- Xóa dependency `spring-cloud-config-monitor`

**Từ `application.yml`:**
- Xóa tất cả các properties liên quan đến RabbitMQ

> **Lưu ý:** Thực hiện việc dọn dẹp này cho Config Server, Accounts, Cards và Loans microservices để tránh các container không cần thiết có thể làm chậm hệ thống local của bạn.

## Tạo Eureka Server Project

### 1. Tạo Project Từ Spring Initializr

Truy cập [start.spring.io](https://start.spring.io) và cấu hình:

- **Project:** Maven
- **Language:** Java
- **Spring Boot:** Phiên bản ổn định mới nhất
- **Group:** com.eazybytes
- **Artifact:** eurekaserver
- **Name:** eurekaserver
- **Description:** Service discovery agent for Eazy Bank microservices
- **Package name:** Tự động điền dựa trên group và artifact
- **Packaging:** JAR
- **Java:** 17

### 2. Thêm Dependencies

Chọn các dependencies sau:

1. **Eureka Server** (KHÔNG phải Eureka Discovery Client)
2. **Config Client** - Để kết nối với Config Server
3. **Spring Boot Actuator** - Cho health checks

### 3. Import Vào Workspace

1. Generate và download project
2. Giải nén file zip vào thư mục `section 8`
3. Trong IntelliJ IDEA, vào tab Maven → Add Maven Projects → Chọn thư mục eurekaserver

## Cấu Hình Eureka Server

### 1. Bật Annotation Eureka Server

Trong class main application, thêm annotation `@EnableEurekaServer`:

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaserverApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaserverApplication.class, args);
    }
}
```

Annotation này chuyển đổi một Spring Boot project thông thường thành service discovery agent sử dụng thư viện Eureka.

### 2. Cấu Hình application.yml

Đổi tên `application.properties` thành `application.yml` và thêm cấu hình sau:

```yaml
spring:
  application:
    name: eurekaserver
  config:
    import: optional:configserver:http://localhost:8071

management:
  endpoints:
    web:
      exposure:
        include: "*"
  health:
    readinessstate:
      enabled: true
    livenessstate:
      enabled: true
  endpoint:
    health:
      probes:
        enabled: true
```

**Các Điểm Cấu Hình Quan Trọng:**

- **spring.application.name:** Phải khớp với tên file config trong Config Server
- **spring.config.import:** URL của Config Server để lấy properties
- **management.endpoints:** Expose tất cả actuator endpoints
- **health probes:** Bật readiness và liveness cho Docker health checks

### 3. Cấu Hình Properties Trong Config Server

Tạo file `eurekaserver.yml` trong GitHub config repository với nội dung sau:

```yaml
server:
  port: 8070

eureka:
  instance:
    hostname: localhost
  client:
    fetchRegistry: false
    registerWithEureka: false
    serviceUrl:
      defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
```

**Giải Thích Các Properties:**

- **server.port:** Eureka Server sẽ chạy trên port 8070
- **eureka.instance.hostname:** Hostname cho Eureka instance (localhost cho môi trường phát triển local)
- **eureka.client.fetchRegistry:** Đặt `false` vì Eureka Server không cần fetch registry details (nó là người duy trì chúng)
- **eureka.client.registerWithEureka:** Đặt `false` để ngăn Eureka Server tự đăng ký với chính nó
- **eureka.client.serviceUrl.defaultZone:** URL nơi Eureka Server expose chức năng của nó cho các microservices khác

> **Tại sao chỉ có một file config?** Không giống như các microservices khác, Eureka Server hoạt động giống nhau trên tất cả môi trường (dev, qa, prod) vì nó không phụ thuộc vào database credentials hay business logic phụ thuộc môi trường.

## Kiểm Tra Thiết Lập

### 1. Khởi Động Config Server

Khởi động Config Server trước vì Eureka Server phụ thuộc vào nó:

```bash
# Khởi động Config Server trên port 8071
```

### 2. Xác Minh Properties Từ Config Server

Truy cập Config Server để xác minh properties của Eureka đã được load:

```
http://localhost:8071/eurekaserver/default
```

Bạn sẽ thấy tất cả các Eureka-related properties mà bạn đã định nghĩa.

### 3. Khởi Động Eureka Server

Chạy main application class ở chế độ debug. Kiểm tra logs để xác nhận:
- Kết nối tới Config Server tại port 8071
- Load các default properties
- Server đã khởi động trên port 8070

### 4. Truy Cập Eureka Dashboard

Điều hướng tới:

```
http://localhost:8070
```

Bạn sẽ thấy Eureka Dashboard. Đây là UI được tích hợp sẵn do Spring Eureka Server cung cấp, hiển thị:
- System Status
- General Info
- Instance Info
- Registered Instances (hiện tại đang trống cho đến khi các microservices đăng ký)

## Tóm Tắt

Bạn đã thiết lập thành công một Eureka Service Discovery Server có các đặc điểm:
- ✅ Chạy trên port 8070
- ✅ Kết nối với Config Server để quản lý cấu hình tập trung
- ✅ Expose health check endpoints cho Docker orchestration
- ✅ Cung cấp dashboard để giám sát các services đã đăng ký

## Các Bước Tiếp Theo

Bước tiếp theo là thiết lập kết nối giữa các microservices riêng lẻ (accounts, loans, cards) và Eureka Service Discovery Server bằng cách:
1. Thêm Eureka Discovery Client dependency vào mỗi microservice
2. Cấu hình mỗi microservice để đăng ký với Eureka Server
3. Bật service-to-service communication thông qua service discovery

---

**Luồng Kiến Trúc:**
```
Microservices (accounts, loans, cards)
    ↓ (đăng ký với)
Eureka Server (port 8070)
    ↓ (lấy config từ)
Config Server (port 8071)
```