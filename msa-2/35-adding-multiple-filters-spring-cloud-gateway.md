# Thêm Nhiều Filter trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình nhiều filter trong Spring Cloud Gateway, bao gồm các filter có sẵn và chuẩn bị cho việc triển khai filter tùy chỉnh.

## Cấu Hình Gateway Hiện Tại

Hiện tại, Gateway server có các cấu hình routing bao gồm:
- **Path Predicate**: Xác thực xem đường dẫn request có khớp với giá trị predicate không
- **Rewrite Path Filter**: Viết lại đường dẫn trước khi chuyển tiếp đến microservice thực tế
- **Request Forwarding**: Định tuyến request đến microservice đích

## Hiểu về Cấu Hình Spring Cloud Gateway

### Cách Tiếp Cận Tài Liệu

Khi làm việc với Spring Cloud Gateway hoặc bất kỳ framework nào, hãy làm theo các bước sau:

1. **Đọc Tài Liệu Chính Thức**: Tài liệu đầy đủ chứa tất cả các chi tiết cần thiết
2. **Xem Xét Ví Dụ**: Các ví dụ chính thức minh họa các mẫu triển khai đúng
3. **Điều Chỉnh Theo Yêu Cầu**: Sửa đổi ví dụ dựa trên nhu cầu kinh doanh

### Các Phương Pháp Cấu Hình

#### 1. Fluent Java Routes API (Được Khuyến Nghị)

Sử dụng cấu hình dựa trên Java với annotation `@Bean` trả về `RouteLocator`:
- Cung cấp tính linh hoạt tối đa
- Cho phép triển khai các yêu cầu phức tạp
- Cho phép định nghĩa route theo cách lập trình

#### 2. Cấu Hình YAML

Định nghĩa routes sử dụng application properties:
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: route-id
          uri: target-uri
          predicates:
            - Path=/path/**
```

**Khuyến Nghị**: Ưu tiên cấu hình kiểu Java để có tính linh hoạt tốt hơn và xử lý các yêu cầu phức tạp.

## Thêm Response Header Filter

### Mục Tiêu

Thêm filter để bao gồm các header tùy chỉnh trong response gửi đến ứng dụng client.

### Các Bước Triển Khai

#### 1. Tìm Tài Liệu Filter

Từ tài liệu chính thức:
- Điều hướng đến **Gateway Filter Factories**
- Tìm **AddResponseHeader GatewayFilter Factory**

#### 2. Thêm Filter vào Cấu Hình Java

```java
.filter(f -> f.addResponseHeader("X-Response-Time", LocalDateTime.now().toString()))
```

### Chi Tiết Filter

**Tên Header**: `X-Response-Time`

**Mục Đích**:
- Cung cấp timestamp của thời điểm tạo response
- Giúp client tính toán thời gian khứ hồi request-response
- Hữu ích cho việc giám sát hiệu suất

**Giá Trị**: Ngày và giờ hiện tại sử dụng `LocalDateTime.now().toString()`

### Áp Dụng cho Tất Cả Microservices

Thêm cùng cấu hình filter cho:
- Route của Accounts microservice
- Route của Loans microservice
- Route của Cards microservice

## Kiểm Tra Triển Khai

### Sử Dụng Postman

1. Gửi request đến Gateway server
2. Kiểm tra response headers
3. Xác minh header `X-Response-Time` có mặt
4. Quan sát giá trị ngày và giờ hiện tại

### Trước và Sau

**Trước**: Ba header mặc định trong response

**Sau**: Thêm header tùy chỉnh `X-Response-Time` với timestamp

## Các Gateway Filter Có Sẵn

Spring Cloud Gateway cung cấp nhiều filter có sẵn:

- **Request Filters**:
  - AddRequestHeader
  - AddRequestParameter
  - ModifyRequestBody
  - MapRequestHeader

- **Response Filters**:
  - AddResponseHeader
  - ModifyResponseBody
  - LocalResponseCache

- **Path Filters**:
  - RewritePath
  - PrefixPath
  - StripPrefix

- **Advanced Filters**:
  - CircuitBreaker
  - FallbackHeaders
  - JsonToGrpc
  - Redirect

## Thực Hành Tốt Nhất

1. **Tận Dụng Filter Có Sẵn**: Sử dụng các filter được định nghĩa sẵn để đáp ứng yêu cầu kinh doanh
2. **Xem Xét Tài Liệu**: Khám phá các filter có sẵn trong tài liệu chính thức
3. **Thêm Nhiều Filter**: Chuỗi các filter sử dụng method chaining trong cấu hình Java
4. **Giám Sát Hiệu Suất**: Sử dụng response headers để theo dõi và debug

## Khi Filter Có Sẵn Không Đủ

Nếu không có filter được định nghĩa sẵn nào phù hợp với logic kinh doanh của bạn:
- Định nghĩa filter tùy chỉnh
- Triển khai logic filter tùy chỉnh
- Đăng ký filter tùy chỉnh trong cấu hình Gateway

## Các Bước Tiếp Theo

Chủ đề tiếp theo bao gồm việc tạo và triển khai filter tùy chỉnh trong Spring Cloud Gateway khi các filter có sẵn không đáp ứng các yêu cầu kinh doanh cụ thể.

## Tóm Tắt

- Spring Cloud Gateway hỗ trợ nhiều filter cho mỗi route
- Sử dụng filter `addResponseHeader` để bao gồm header tùy chỉnh
- Chuỗi nhiều filter sử dụng fluent API
- Filter có sẵn bao phủ hầu hết các trường hợp sử dụng phổ biến
- Filter tùy chỉnh có sẵn cho logic kinh doanh cụ thể

---

**Chủ Đề Liên Quan**:
- Triển Khai Filter Tùy Chỉnh
- Gateway Filter Factories
- Cấu Hình Routing
- Giám Sát Hiệu Suất