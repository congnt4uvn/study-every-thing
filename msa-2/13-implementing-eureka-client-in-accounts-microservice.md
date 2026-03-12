# Triển Khai Eureka Client trong Accounts Microservice

## Tổng Quan

Hướng dẫn này sẽ giúp bạn cấu hình accounts microservice để đăng ký với Eureka server nhằm thực hiện service discovery. Microservice sẽ tự động đăng ký trong quá trình khởi động và gửi heartbeat mỗi 30 giây để duy trì đăng ký.

## Yêu Cầu Tiên Quyết

Trước khi khởi động accounts microservice, hãy đảm bảo các dịch vụ sau đang chạy:
- Config Server
- Eureka Server (chạy trên cổng 8070)

## Bước 1: Thêm Dependency Eureka Client

Thêm dependency Eureka Discovery Client vào file `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

**Quan trọng:** Chọn **Eureka Discovery Client**, không phải Eureka Server.

## Bước 2: Cấu Hình Application Properties

Thêm các cấu hình sau vào file `application.yml`:

### Cấu Hình Eureka Client

```yaml
eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/
```

**Chi Tiết Cấu Hình Quan Trọng:**

- **`preferIpAddress: true`**: Đăng ký microservice sử dụng địa chỉ IP thay vì hostname. Điều này rất quan trọng cho môi trường phát triển local không có DNS mapping.
- **`fetchRegistry: true`**: Cho phép microservice lấy thông tin registry khi giao tiếp với các microservice khác.
- **`registerWithEureka: true`**: Đảm bảo microservice đăng ký với Eureka server.
- **`serviceUrl.defaultZone`**: Chỉ định URL của Eureka server.

### Cấu Hình Thông Tin Ứng Dụng

Thêm metadata sẽ được hiển thị trong Eureka dashboard:

```yaml
info:
  app:
    name: accounts
    description: Eazy Bank Accounts Application
    version: 1.0.0
```

### Kích Hoạt Info Endpoint

Kích hoạt actuator info endpoint để expose metadata của ứng dụng:

```yaml
management:
  info:
    env:
      enabled: true
```

### Kích Hoạt Graceful Shutdown

Cấu hình shutdown endpoint để hủy đăng ký một cách graceful:

```yaml
management:
  endpoint:
    shutdown:
      enabled: true

endpoints:
  shutdown:
    enabled: true
```

**Lưu ý:** Cấu hình `endpoints` phải ở cấp root của file YAML, không nằm dưới `management`.

## Bước 3: Khởi Động Accounts Microservice

1. Build project
2. Khởi động ứng dụng ở chế độ debug
3. Microservice sẽ tự động:
   - Đăng ký với Eureka server (HTTP response 204 cho biết đăng ký thành công)
   - Bắt đầu gửi heartbeat mỗi 30 giây

## Bước 4: Xác Minh Đăng Ký

Truy cập Eureka dashboard tại `http://localhost:8070` để xác minh đăng ký.

### Những Gì Cần Kiểm Tra:

- **Tên Ứng Dụng**: Được liệt kê trong "Instances currently registered with Eureka" (khớp với thuộc tính `spring.application.name`)
- **Trạng Thái**: Nên hiển thị là "UP"
- **Chi Tiết Instance**: Click vào link instance để xem:
  - Tên ứng dụng
  - Mô tả
  - Phiên bản
  
URL của info endpoint sẽ có định dạng: `http://<địa-chỉ-ip>:8080/actuator/info`

## Hiểu Về Địa Chỉ IP vs Hostname

Khi bạn click vào instance trong Eureka dashboard, bạn có thể thấy một hostname khác thay vì "localhost". Đây là hành vi bình thường do Docker hoặc phần mềm khác tạo host entries cho địa chỉ IP localhost. Service discovery vẫn sẽ hoạt động chính xác với địa chỉ IP.

## Cảnh Báo Thường Gặp

Bạn có thể thấy thông báo cảnh báo: "Emergency! Eureka may be incorrectly claiming instances." Đây là cảnh báo phổ biến của Eureka dashboard và có thể bỏ qua trong quá trình phát triển. Khái niệm này sẽ được giải thích chi tiết trong các bài giảng tiếp theo.

## Cách Service Discovery Hoạt Động

1. **Khởi động**: Accounts microservice đăng ký với Eureka server
2. **Heartbeats**: Gửi tín hiệu heartbeat mỗi 30 giây để duy trì đăng ký
3. **Giao Tiếp Service**: Các microservice khác có thể khám phá accounts microservice thông qua Eureka server bằng địa chỉ IP
4. **Shutdown**: Trong quá trình graceful shutdown, microservice tự động hủy đăng ký khỏi Eureka

## Bài Tập

Áp dụng các thay đổi cấu hình tương tự cho **loans** và **cards** microservices để kích hoạt service discovery cho toàn bộ hệ sinh thái microservices.

## Điểm Chính Cần Nhớ

- Cấu hình Eureka client cho phép tự động đăng ký và khám phá service
- Sử dụng địa chỉ IP (thay vì hostname) là cần thiết cho môi trường phát triển local
- Metadata ứng dụng cải thiện khả năng hiển thị trong Eureka dashboard
- Cơ chế heartbeat đảm bảo theo dõi tính khả dụng của service
- Graceful shutdown đảm bảo hủy đăng ký sạch sẽ khỏi service registry

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ đề cập đến:
- Cấu hình loans và cards microservices
- Hiểu về thông báo cảnh báo emergency của Eureka
- Các pattern service discovery nâng cao