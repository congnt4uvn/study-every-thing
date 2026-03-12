# Đăng Ký Microservices với Eureka Server

## Tổng Quan

Hướng dẫn này trình bày quy trình đăng ký các microservices Cards và Loans với Eureka Service Discovery server, hoàn thiện việc thiết lập đăng ký dịch vụ cho tất cả các microservices trong hệ thống.

## Yêu Cầu Tiên Quyết

- Eureka Server đang chạy trên cổng 8070
- Config Server đang chạy
- Microservice Accounts đã được đăng ký với Eureka
- Các microservices Cards và Loans sẵn sàng để cấu hình

## Các Bước Cấu Hình

### 1. Thêm Maven Dependencies

Thêm dependency Netflix Eureka Client vào cả hai microservices Cards và Loans:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

### 2. Cấu Hình application.yml cho Cards Microservice

Cập nhật file `application.yml` trong microservice Cards:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    shutdown:
      enabled: true
  info:
    env:
      enabled: true

eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/

info:
  app:
    name: "cards"
    description: "Eazy Bank Cards Application"
```

### 3. Cấu Hình application.yml cho Loans Microservice

Tương tự, cập nhật file `application.yml` trong microservice Loans:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    shutdown:
      enabled: true
  info:
    env:
      enabled: true

eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/

info:
  app:
    name: "loans"
    description: "Eazy Bank Loans Application"
```

## Khởi Động Microservices

1. Build cả hai microservices Cards và Loans
2. Đảm bảo Config Server và Eureka Server đang chạy
3. Khởi động microservice Cards (chạy trên cổng 9000)
4. Khởi động microservice Loans (chạy trên cổng 8090)

## Xác Thực

### Eureka Dashboard

Truy cập Eureka dashboard tại `http://localhost:8070` để xác minh tất cả microservices đã được đăng ký:

- Microservice Accounts
- Microservice Cards (cổng 9000)
- Microservice Loans (cổng 8090)

Mỗi microservice sẽ hiển thị thông tin chi tiết khi được nhấp vào.

### Eureka REST API

#### Lấy Tất Cả Ứng Dụng Đã Đăng Ký (Định Dạng XML)

```
GET http://localhost:8070/eureka/apps
```

Trả về tất cả các ứng dụng đã đăng ký và các instances của chúng ở định dạng XML theo mặc định.

#### Lấy Tất Cả Ứng Dụng Đã Đăng Ký (Định Dạng JSON)

Sử dụng Postman hoặc bất kỳ HTTP client nào:

```
GET http://localhost:8070/eureka/apps
Headers:
  Accept: application/json
```

**Response bao gồm:**
- Instance ID
- Hostname
- Tên ứng dụng
- Địa chỉ IP
- Trạng thái
- Số cổng
- Khoảng thời gian renewal
- Thời gian đăng ký
- Timestamp renewal cuối cùng
- Timestamp service khởi động
- Home page URL
- Status page URL
- Health check URL

#### Lấy Thông Tin Microservice Cụ Thể

Để lấy thông tin cho một microservice cụ thể:

```
GET http://localhost:8070/eureka/apps/accounts
GET http://localhost:8070/eureka/apps/cards
GET http://localhost:8070/eureka/apps/loans
```

Thêm header `Accept: application/json` để nhận response dạng JSON.

## Khái Niệm Chính

### Mô Hình Service Discovery và Registration

Việc triển khai tuân theo cách tiếp cận từng bước:

1. **Centralized Service Registry**: Eureka Server hoạt động như một server tập trung lưu trữ tất cả chi tiết service registry và hoạt động như một service discovery agent.

2. **Automatic Registration**: Tất cả microservices (Accounts, Cards, Loans) tự động đăng ký thông tin của chúng trong quá trình khởi động bằng cách bao gồm Eureka Client dependency và cấu hình phù hợp.

3. **Dynamic Service Discovery**: Các microservices có thể khám phá lẫn nhau mà không cần cấu hình địa chỉ IP thủ công, giúp giao tiếp nội bộ trở nên liền mạch.

4. **Hỗ Trợ Load Balancing**: Nhiều instances của cùng một microservice có thể được đăng ký, cho phép khả năng cân bằng tải.

## Lợi Ích Của Eureka Server

- **Tự Động Đăng Ký Service**: Không cần can thiệp thủ công để cập nhật địa chỉ IP trong registry
- **Khả Năng Mở Rộng**: Dễ dàng xử lý hàng trăm microservices
- **Cập Nhật Động**: Thông tin service được cập nhật tự động
- **Giám Sát Sức Khỏe Service**: Theo dõi trạng thái và tính khả dụng của service
- **Hỗ Trợ Nhiều Instance**: Quản lý nhiều instances cho mỗi microservice để đảm bảo tính sẵn sàng cao

## Thông Tin Instance Có Sẵn

Đối với mỗi instance đã đăng ký, Eureka cung cấp:
- Instance ID và hostname
- Tên ứng dụng và địa chỉ IP
- Trạng thái hiện tại và số cổng
- Khoảng thời gian renewal mặc định tính bằng giây
- Timestamp đăng ký
- Timestamp renewal cuối cùng
- Timestamp service khởi động
- URLs cho home page, status page và health check

## Các Bước Tiếp Theo

Với tất cả microservices đã được đăng ký thành công với Eureka Server, bây giờ bạn có thể triển khai:
- Client-side load balancing
- Giao tiếp giữa các microservices sử dụng tên service
- Các mô hình resilience với circuit breakers
- Tích hợp API Gateway

## Tóm Tắt

Hướng dẫn này đã trình bày cách đăng ký các microservices Cards và Loans với Eureka Server, hoàn thành việc thiết lập service discovery. Tất cả microservices giờ đây tự động đăng ký trong quá trình khởi động, cho phép khám phá service động và tạo điều kiện thuận lợi cho giao tiếp liền mạch giữa các microservices trong hệ thống phân tán.