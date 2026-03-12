# Triển Khai Mẫu Thiết Kế Circuit Breaker trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách triển khai mẫu thiết kế Circuit Breaker trong kiến trúc microservices sử dụng Spring Cloud Gateway và Resilience4j. Mẫu Circuit Breaker giúp các microservices trở nên chịu lỗi và đàn hồi bằng cách ngăn chặn các lỗi lan truyền.

## Yêu Cầu Tiên Quyết

- Kiến trúc microservices Spring Boot
- Spring Cloud Gateway làm edge server
- Netflix Eureka Server cho service discovery
- Maven để quản lý dependencies
- IntelliJ IDEA (hoặc bất kỳ Java IDE nào)

## Vị Trí Triển Khai

Mẫu Circuit Breaker sẽ được triển khai ở hai cấp độ khác nhau:
1. **Gateway Server** - Đóng vai trò là edge server
2. **Các Microservices Riêng Lẻ** - Như Accounts microservice

## Bước 1: Thiết Lập Dự Án

### Tạo Thư Mục Section Mới

1. Sao chép code từ `section_9`
2. Đổi tên thư mục thành `section_10` cho các thay đổi liên quan đến resiliency
3. Xóa thư mục `.idea`
4. Mở `section_10` trong IntelliJ IDEA
5. Thực hiện clean build và bật annotation processing cho Lombok Library

## Bước 2: Thêm Dependencies

### Maven Dependency cho Gateway Server

Thêm dependency sau vào `pom.xml` của Gateway Server (sau dependency Netflix Eureka Client):

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-circuitbreaker-reactor-resilience4j</artifactId>
</dependency>
```

**Lưu ý:** Vì Gateway Server được xây dựng trên mô hình reactive Spring WebFlux, chúng ta sử dụng phiên bản `reactor-resilience4j`.

## Bước 3: Cấu Hình Circuit Breaker Filter

### Cấu Hình Gateway Server Application

Trong class main Spring Boot của Gateway Server, thêm Circuit Breaker filter vào cấu hình routing:

```java
// Trong cấu hình routing
.route(r -> r.path("/easybank/accounts/**")
    .filters(f -> f
        .rewritePath("/easybank/accounts/(?<segment>.*)", "/${segment}")
        .addResponseHeader("X-Response-Time", LocalDateTime.now().toString())
        .circuitBreaker(config -> config
            .setName("accountCircuitBreaker")
        )
    )
    .uri("lb://ACCOUNTS")
)
```

Filter `circuitBreaker` chấp nhận cấu hình lambda, nơi bạn gán tên cho instance circuit breaker.

## Bước 4: Cấu Hình Application Properties

### Thuộc Tính Circuit Breaker trong application.yml

Thêm cấu hình sau vào `application.yml`:

```yaml
resilience4j:
  circuitbreaker:
    configs:
      default:
        slidingWindowSize: 10
        permittedNumberOfCallsInHalfOpenState: 2
        failureRateThreshold: 50
        waitDurationInOpenState: 10000
```

### Giải Thích Các Thuộc Tính

| Thuộc Tính | Giá Trị | Mô Tả |
|------------|---------|-------|
| `slidingWindowSize` | 10 | Số lượng requests cần giám sát trước khi quyết định chuyển trạng thái từ CLOSED sang OPEN |
| `permittedNumberOfCallsInHalfOpenState` | 2 | Số lượng requests được phép ở trạng thái HALF_OPEN để kiểm tra xem service đã phục hồi chưa |
| `failureRateThreshold` | 50 | Phần trăm requests thất bại (50%) kích hoạt circuit breaker chuyển sang trạng thái open |
| `waitDurationInOpenState` | 10000 | Thời gian chờ tính bằng milliseconds (10 giây) trước khi chuyển sang trạng thái HALF_OPEN |

### Phạm Vi Cấu Hình

- Sử dụng `default` áp dụng các thuộc tính này cho tất cả circuit breakers trong ứng dụng
- Để cấu hình circuit breakers cụ thể, thay `default` bằng tên circuit breaker (ví dụ: `accountCircuitBreaker`)

## Bước 5: Khởi Động Các Microservices

Khởi động các services theo thứ tự sau:

1. **Config Server** - Tất cả microservices phụ thuộc vào service này
2. **Eureka Server** - Cho service discovery và registration
3. **Accounts Microservice** - Service chúng ta sẽ test
4. **Gateway Server** - Để định tuyến và áp dụng logic circuit breaker

**Lưu ý:** Không cần khởi động Cards và Loans microservices cho demo này.

## Bước 6: Testing và Monitoring

### Xác Minh Eureka Dashboard

1. Mở browser đến Eureka Dashboard
2. Xác minh Accounts và Gateway Server đã đăng ký thành công

### Actuator Endpoints để Monitoring

#### Xem Tất Cả Circuit Breakers
```
GET http://localhost:8072/actuator/circuitbreakers
```

Ban đầu trả về mảng rỗng cho đến khi các requests được xử lý.

#### Xem Circuit Breaker Events
```
GET http://localhost:8072/actuator/circuitbreakerevents?name=accountCircuitBreaker
```

Hiển thị tất cả các sự kiện chuyển trạng thái và kết quả requests.

#### Xem Trạng Thái Tổng Thể Circuit Breaker
```
GET http://localhost:8072/actuator/circuitbreakers
```

Trả về trạng thái hiện tại và thống kê:
- Trạng thái tổng thể (CLOSED, OPEN, HALF_OPEN)
- Tỷ lệ thất bại
- Tỷ lệ slow call
- Buffered calls
- Failed calls

## Bước 7: Demo Các Trạng Thái Circuit Breaker

### Testing Trạng Thái CLOSED (Hoạt Động Bình Thường)

1. Gửi request qua Postman:
   ```
   GET http://localhost:8072/easybank/accounts/api/contact-info
   ```

2. Response thành công cho biết trạng thái CLOSED:
   ```json
   {
     "message": "Contact details",
     "contactDetails": {...},
     "onCallSupport": {...}
   }
   ```

3. Kiểm tra actuator endpoint - trạng thái hiển thị là `CLOSED` với zero failed calls

### Mô Phỏng Lỗi (Kích Hoạt Trạng Thái OPEN)

Để minh họa hành vi circuit breaker:

1. Đặt breakpoint trong `AccountsController` tại endpoint contact-info
2. Gửi các requests sẽ timeout (Gateway timeout sau khi chờ)
3. Response chuyển sang `504 Gateway Timeout`
4. Tiếp tục gửi nhiều failed requests

### Chuyển Trạng Thái: CLOSED → OPEN

Sau nhiều lỗi (vượt quá 50% failure rate):

1. Response chuyển sang `503 Service Unavailable`
2. Thông báo lỗi: "Upstream service is temporarily unavailable"
3. Trạng thái circuit breaker chuyển sang `OPEN`
4. Kiểm tra actuator events để xem sự kiện chuyển trạng thái

### Lợi Ích của Trạng Thái OPEN

- Gateway Server không lãng phí tài nguyên gọi service đang lỗi
- Circuit breaker ngay lập tức trả về lỗi mà không chờ đợi
- Ngăn chặn cạn kiệt tài nguyên và blocking threads
- Bảo vệ các downstream services khỏi cascading failures

### Chuyển Trạng Thái: OPEN → HALF_OPEN

Sau khi chờ 10 giây (waitDurationInOpenState):

1. Circuit breaker tự động chuyển sang `HALF_OPEN`
2. Cho phép 2 test requests (permittedNumberOfCallsInHalfOpenState)
3. Dựa trên kết quả, quyết định trạng thái tiếp theo:
   - Nếu thành công → chuyển sang `CLOSED`
   - Nếu thất bại → quay lại `OPEN`

### Chuyển Trạng Thái: HALF_OPEN → CLOSED

Để khôi phục hoạt động bình thường:

1. Xóa breakpoint khỏi AccountsController
2. Gửi requests mới
3. Responses thành công chuyển trạng thái sang `CLOSED`
4. Kiểm tra actuator events để xác nhận: chuyển HALF_OPEN → CLOSED
5. Trạng thái tổng thể quay về `CLOSED` với thống kê bình thường

## Cách Circuit Breaker Bảo Vệ Hệ Thống

### Bảo Vệ Tài Nguyên

- **Không có Circuit Breaker:** Gateway tiếp tục cố gọi service đang lỗi, blocking threads và tiêu tốn tài nguyên
- **Có Circuit Breaker:** Ngay lập tức fail fast khi service không khả dụng, giải phóng tài nguyên

### Khả Năng Chịu Lỗi

- Ngăn chặn cascading failures giữa các microservices
- Tự động phát hiện và cô lập các services đang lỗi
- Khả năng tự phục hồi thông qua kiểm tra trạng thái HALF_OPEN

### Lợi Ích Về Hiệu Năng

- Giảm latency bằng cách fail fast thay vì chờ timeouts
- Sử dụng tài nguyên tốt hơn trong Gateway Server
- Cải thiện độ ổn định tổng thể của hệ thống

## Monitoring và Observability

### Monitoring Thời Gian Thực

Sử dụng Spring Boot Actuator endpoints để giám sát:

1. **Trạng Thái Hiện Tại:** Kiểm tra xem circuit đang CLOSED, OPEN hay HALF_OPEN
2. **Lịch Sử Events:** Xem tất cả chuyển trạng thái và kết quả requests
3. **Metrics:** Theo dõi failure rates, slow call rates và buffered calls

### Ví Dụ Actuator Response

```json
{
  "accountCircuitBreaker": {
    "state": "CLOSED",
    "failureRate": 0.0,
    "slowCallRate": -1.0,
    "bufferedCalls": 3,
    "failedCalls": 0,
    "slowCalls": 0
  }
}
```

## Best Practices (Thực Hành Tốt Nhất)

1. **Cấu Hình Phù Hợp:** Điều chỉnh ngưỡng dựa trên SLAs của service
2. **Nhiều Circuit Breakers:** Sử dụng cấu hình khác nhau cho các services khác nhau
3. **Giám Sát Tích Cực:** Thiết lập alerts cho thay đổi trạng thái circuit breaker
4. **Test Kỹ Lưỡng:** Mô phỏng các kịch bản lỗi khác nhau trong testing
5. **Tài Liệu Hóa Hành Vi:** Đảm bảo team hiểu hành vi của circuit breaker

## Kết Luận

Mẫu Circuit Breaker là thiết yếu để xây dựng microservices đàn hồi. Bằng cách triển khai nó ở cấp Gateway Server sử dụng Spring Cloud Gateway và Resilience4j, bạn có thể:

- Bảo vệ hệ thống khỏi cascading failures
- Tiết kiệm tài nguyên trong thời gian service gặp sự cố
- Cung cấp trải nghiệm người dùng tốt hơn với hành vi fail-fast
- Tự động phục hồi khi services trở lại khỏe mạnh

Triển khai này minh họa sức mạnh của mẫu circuit breaker trong việc làm cho microservices chịu lỗi và đàn hồi trong môi trường production.

## Các Bước Tiếp Theo

- Triển khai Circuit Breaker ở cấp độ individual microservice
- Khám phá các mẫu Resilience4j khác (Retry, Rate Limiter, Bulkhead)
- Cấu hình cơ chế fallback để xử lý lỗi tốt hơn
- Thiết lập monitoring và alerting cho circuit breaker events