# Cấu Hình Routing Tùy Chỉnh với Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này giải thích cách cấu hình routing tùy chỉnh trong Spring Cloud Gateway để xử lý các yêu cầu định tuyến động vượt ra ngoài hành vi mặc định. Chúng ta sẽ triển khai mô hình routing chuyên nghiệp sử dụng tiền tố tổ chức cho các endpoint microservice.

## Hành Vi Routing Mặc Định

Theo mặc định, Spring Cloud Gateway tự động tạo các route dựa trên tên service đã đăng ký với Eureka Server. Gateway lấy thông tin routing từ Eureka và chuyển tiếp request đến các microservice.

**Mô hình routing mặc định:**
- `/accounts/**` → ACCOUNTS microservice
- `/loans/**` → LOANS microservice
- `/cards/**` → CARDS microservice

Điều này hoạt động tốt, nhưng có thể không phù hợp với tất cả các yêu cầu dự án.

## Yêu Cầu Routing Tùy Chỉnh

Để có cấu trúc API chuyên nghiệp hơn, chúng ta có thể triển khai routing tùy chỉnh với tiền tố tổ chức:

**Mô hình routing tùy chỉnh:**
- `/easybank/accounts/**` → ACCOUNTS microservice
- `/easybank/loans/**` → LOANS microservice
- `/easybank/cards/**` → CARDS microservice

Mô hình này cung cấp ngữ cảnh tốt hơn cho các ứng dụng client, làm rõ tổ chức và microservice nào mà họ đang tương tác.

## Các Bước Triển Khai

### 1. Tạo Bean RouteLocator

Điều hướng đến class chính trong Gateway server (`GatewayServerApplication.java`) và tạo một phương thức cấu hình:

```java
@Bean
public RouteLocator easybankRouteConfig(RouteLocatorBuilder routeLocatorBuilder) {
    return routeLocatorBuilder.routes()
        .route(p -> p
            .path("/easybank/accounts/**")
            .filters(f -> f.rewritePath(
                "/easybank/accounts/(?<segment>.*)", 
                "/${segment}"))
            .uri("lb://ACCOUNTS"))
        .route(p -> p
            .path("/easybank/loans/**")
            .filters(f -> f.rewritePath(
                "/easybank/loans/(?<segment>.*)", 
                "/${segment}"))
            .uri("lb://LOANS"))
        .route(p -> p
            .path("/easybank/cards/**")
            .filters(f -> f.rewritePath(
                "/easybank/cards/(?<segment>.*)", 
                "/${segment}"))
            .uri("lb://CARDS"))
        .build();
}
```

### 2. Hiểu Về Cấu Hình

**Các thành phần chính:**

- **`@Bean`**: Đăng ký RouteLocator như một Spring bean
- **`RouteLocatorBuilder`**: Builder để tạo các cấu hình route
- **`.routes()`**: Bắt đầu chuỗi định nghĩa route
- **`.route()`**: Định nghĩa cấu hình route riêng lẻ
- **`.path()`**: Chỉ định mẫu đường dẫn request đến
- **`.filters()`**: Áp dụng các filter để chuyển đổi request
- **`.rewritePath()`**: Viết lại đường dẫn trước khi chuyển tiếp đến microservice
- **`.uri()`**: Chỉ định URI microservice đích

**Viết lại đường dẫn:**
- Mẫu `/easybank/accounts/(?<segment>.*)` bắt mọi thứ sau `/easybank/accounts/` như một biến có tên `segment`
- Thay thế `/${segment}` chỉ chuyển tiếp đường dẫn đã bắt đến microservice
- Ví dụ: `/easybank/accounts/api/create` → `/api/create`

**Cân bằng tải:**
- `lb://ACCOUNTS` chỉ định routing có cân bằng tải
- Sử dụng Spring Cloud LoadBalancer cho cân bằng tải phía client
- Tên service phải khớp với tên ứng dụng đã đăng ký trong Eureka (phân biệt chữ hoa/thường)

### 3. Vô Hiệu Hóa Routing Mặc Định

Để tránh nhầm lẫn với nhiều cấu hình routing, vô hiệu hóa hành vi mặc định trong `application.yml`:

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: false  # Thay đổi từ true
```

Điều này đảm bảo chỉ các route tùy chỉnh của bạn được kích hoạt.

### 4. Build và Kiểm Tra

1. Lưu các thay đổi
2. Build dự án với Maven
3. Kiểm tra bằng Postman hoặc bất kỳ REST client nào

**Ví dụ request:**
```
POST http://localhost:8072/easybank/accounts/api/create
```

**Xác minh các route:**
```
GET http://localhost:8072/actuator/gateway/routes
```

Bạn sẽ chỉ thấy các route tùy chỉnh với tiền tố `easybank`.

## Các Kịch Bản Kiểm Tra

### Kiểm Tra Tích Cực
- Endpoint: `POST /easybank/accounts/api/create`
- Kỳ vọng: Response thành công từ ACCOUNTS microservice
- Request được định tuyến đúng và đường dẫn được viết lại

### Kiểm Tra Tiêu Cực
- Endpoint: `POST /accounts/api/create` (không có tiền tố)
- Kỳ vọng: 404 Not Found
- Routing mặc định đã bị vô hiệu hóa, nên đường dẫn này không còn hoạt động

## Những Điểm Quan Trọng Cần Lưu Ý

### Phân Biệt Chữ Hoa/Thường Của Tên Service
Luôn sử dụng tên ứng dụng chính xác như đã đăng ký trong Eureka:
- ✅ `lb://ACCOUNTS` (nếu đăng ký là ACCOUNTS)
- ❌ `lb://accounts` (sẽ thất bại nếu không khớp chữ hoa/thường)

### Định Dạng URI
Đảm bảo định dạng URI đúng với hai dấu gạch chéo:
- ✅ `uri("lb://ACCOUNTS")`
- ❌ `uri("lb:ACCOUNTS")` (thiếu dấu gạch chéo)

## Cấu Hình Thay Thế: Dựa Trên YAML

Spring Cloud Gateway cũng hỗ trợ cấu hình routing dựa trên YAML:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: accounts-route
          uri: lb://ACCOUNTS
          predicates:
            - Path=/easybank/accounts/**
          filters:
            - RewritePath=/easybank/accounts/(?<segment>.*), /$\{segment}
```

## Khuyến Nghị: Cấu Hình Java vs YAML

**Nên dùng cấu hình dựa trên Java** cho:
- Logic routing phức tạp
- Nhiều filter
- Cấu hình động
- Hỗ trợ IDE tốt hơn và type safety

**Hạn chế của cấu hình YAML:**
- Kém linh hoạt cho các tình huống phức tạp
- Khả năng chuỗi filter hạn chế
- Khó bảo trì hơn cho cấu hình lớn

## Kết Luận

Routing tùy chỉnh với Spring Cloud Gateway cung cấp cấu trúc API chuyên nghiệp và có tổ chức. Bằng cách sử dụng cấu hình dựa trên Java với `RouteLocator`, bạn có được sự linh hoạt và kiểm soát tối đa đối với logic routing của mình trong khi duy trì code sạch và dễ bảo trì.

Mô hình sử dụng tiền tố tổ chức (`/easybank/`) theo sau là tên service tạo ra một hệ thống phân cấp rõ ràng giúp cải thiện khả năng phát hiện API và trải nghiệm của developer.