# Thiết Lập Spring Cloud Gateway Server

## Tổng Quan

Hướng dẫn này trình bày quy trình từng bước để tạo API Gateway (Edge Server) sử dụng Spring Cloud Gateway cho kiến trúc microservices. Gateway server đóng vai trò là điểm truy cập duy nhất cho tất cả các yêu cầu từ client và định tuyến chúng đến các microservices phù hợp.

## Yêu Cầu Tiên Quyết

- Java 17
- Spring Boot 3.1.2 (hoặc phiên bản ổn định mới nhất)
- Maven
- IntelliJ IDEA
- Các microservices đã có (accounts, loans, cards)
- Eureka Server (Service Discovery)
- Config Server

## Thiết Lập Dự Án

### 1. Tạo Spring Boot Project

Truy cập [start.spring.io](https://start.spring.io) và cấu hình dự án với các thiết lập sau:

- **Loại Dự Án**: Maven Project
- **Ngôn Ngữ**: Java
- **Phiên Bản Spring Boot**: 3.1.2 (hoặc phiên bản ổn định mới nhất)
- **Group**: com.easybytes
- **Artifact**: gateway-server
- **Name**: gateway-server
- **Description**: Easy Bank Gateway Server Application
- **Package Name**: com.easybytes.gateway
- **Packaging**: Jar
- **Phiên Bản Java**: 17

### 2. Thêm Các Dependencies Cần Thiết

Chọn các dependencies sau:

1. **Gateway** - Spring Cloud Gateway để xây dựng API gateway
2. **Eureka Discovery Client** - Để kết nối với Eureka server và lấy service registry
3. **Config Client** - Để tải cấu hình từ Config Server trong quá trình khởi động
4. **Actuator** - Để hiển thị các endpoints quản lý và giám sát
5. **DevTools** - Để phát triển nhanh hơn với khởi động lại tự động

### 3. Thiết Lập Cấu Trúc Dự Án

Sau khi tạo và tải xuống dự án:

1. Tạo thư mục `section9` trong workspace của bạn
2. Giải nén dự án gateway-server đã tải xuống vào thư mục `section9`
3. Xóa bất kỳ thư mục `.idea` nào từ các dự án đã sao chép
4. Mở thư mục `section9` trong IntelliJ IDEA

## Cấu Hình

### 1. Cập Nhật pom.xml

Thêm Google Jib plugin để tạo Docker image:

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <configuration>
        <to>
            <image>easybytes/${project.artifactId}:s9</image>
        </to>
    </configuration>
</plugin>
```

**Lưu ý**: Cập nhật tên tag từ `s8` sang `s9` trong tất cả các microservices khác (accounts, cards, loans, config-server, eureka-server).

### 2. Cấu Hình application.yml

Đổi tên `application.properties` thành `application.yml` và thêm cấu hình sau:

```yaml
spring:
  application:
    name: gateway-server
  config:
    import: optional:configserver:http://localhost:8071
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true

management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    gateway:
      enabled: true
  info:
    env:
      enabled: true

info:
  app:
    name: gateway-server
    description: Easy Bank Gateway Server Application
```

### 3. Cấu Hình Properties Gateway Server trong Config Server

Tạo file `gateway-server.yml` trong GitHub configuration repository của bạn:

```yaml
server:
  port: 8072

eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/
```

## Giải Thích Các Cấu Hình Chính

### Spring Cloud Gateway Discovery Locator

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
```

Cấu hình này yêu cầu gateway:
- Kết nối với Eureka discovery server
- Tự động tìm kiếm tất cả các microservices đã đăng ký
- Sử dụng thông tin này để định tuyến các yêu cầu đến các services phù hợp

### Actuator Gateway Endpoint

```yaml
management:
  endpoint:
    gateway:
      enabled: true
```

Kích hoạt các actuator endpoints cụ thể cho gateway để giám sát và quản lý.

### Cấu Hình Eureka Client

Gateway server tự đăng ký với Eureka và lấy service registry để biết các endpoints thực tế của tất cả microservices.

## Cách Hoạt Động

1. **Đăng Ký Service**: Tất cả microservices (accounts, loans, cards) đăng ký với Eureka Server
2. **Gateway Discovery**: Gateway Server kết nối với Eureka và lấy tất cả đăng ký services
3. **Định Tuyến Yêu Cầu**: Các client bên ngoài gửi yêu cầu đến Gateway Server
4. **Chuyển Tiếp Tự Động**: Gateway tự động định tuyến yêu cầu đến microservices phù hợp dựa trên tên service
5. **Cập Nhật Động**: Gateway luôn đồng bộ với Eureka về bất kỳ thay đổi nào trong các service instances

## Lợi Ích Của Dự Án

- **Điểm Truy Cập Duy Nhất**: Clients chỉ cần biết địa chỉ gateway
- **Tích Hợp Service Discovery**: Định tuyến tự động dựa trên Eureka service registry
- **Cấu Hình Tập Trung**: Tất cả cài đặt gateway được quản lý qua Config Server
- **Giám Sát**: Các actuator endpoints tích hợp sẵn cho health checks và metrics
- **Sẵn Sàng Docker**: Jib plugin được cấu hình để containerization dễ dàng

## Các Bước Tiếp Theo

1. Khởi động tất cả microservices (accounts, loans, cards)
2. Khởi động Config Server trên cổng 8071
3. Khởi động Eureka Server trên cổng 8070
4. Khởi động Gateway Server trên cổng 8072
5. Test microservices bằng cách gửi yêu cầu qua gateway thay vì trực tiếp đến microservices

## Tổng Kết Cấu Hình Cổng

- **Config Server**: 8071
- **Eureka Server**: 8070
- **Gateway Server**: 8072
- **Accounts Service**: (như đã cấu hình)
- **Loans Service**: (như đã cấu hình)
- **Cards Service**: (như đã cấu hình)

## Lưu Ý Quan Trọng

- Đảm bảo tất cả microservices được cấu hình để đăng ký với Eureka
- Cấu hình gateway server được duy trì trong Config Server để quản lý tập trung
- Gateway sử dụng service discovery để định tuyến yêu cầu động mà không cần URLs cố định
- Luôn cập nhật Docker image tags nhất quán trên tất cả services để quản lý phiên bản đúng cách

## Kiểm Thử

Sau khi gateway đang chạy, bạn có thể truy cập microservices thông qua:

```
http://localhost:8072/{service-name}/{endpoint}
```

Ví dụ:
- `http://localhost:8072/accounts/api/fetch`
- `http://localhost:8072/loans/api/fetch`
- `http://localhost:8072/cards/api/fetch`

Gateway sẽ tự động phát hiện và định tuyến đến các service instances phù hợp đã đăng ký trong Eureka.

## Kết Luận

Spring Cloud Gateway cung cấp một giải pháp mạnh mẽ và linh hoạt để xây dựng API Gateway cho kiến trúc microservices. Với sự tích hợp chặt chẽ với Eureka Service Discovery và Spring Cloud Config, nó cho phép định tuyến động, cấu hình tập trung và quản lý dễ dàng của tất cả các microservices trong hệ thống.