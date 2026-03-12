# Triển Khai Retry Pattern với Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách triển khai retry pattern (mẫu thử lại) trong kiến trúc microservices sử dụng Spring Cloud Gateway. Retry pattern giúp các microservices có khả năng chịu lỗi tốt hơn bằng cách tự động thử lại các request thất bại, đặc biệt hữu ích khi xử lý các vấn đề mạng tạm thời hoặc sự cố dịch vụ.

## Yêu Cầu Trước

- Spring Cloud Gateway đã được cấu hình
- Kiến trúc microservices với Eureka service discovery
- Hiểu biết cơ bản về circuit breaker pattern

## Các Bước Triển Khai

### 1. Cấu Hình Retry Filter trong Gateway Server

Thêm cấu hình retry filter vào ứng dụng Gateway Server sau các response header filters:

```java
.filter(f -> f
    .addResponseHeader(/* các header hiện có */)
    .retry(retryConfig -> retryConfig
        .setRetries(3)
        .setMethods(HttpMethod.GET)
        .setBackoff(100, 1000, 2, true)
    )
)
```

#### Các Tham Số Cấu Hình Chính

**setRetries(3)**
- Xác định số lần thử lại
- Trong ví dụ này: 3 lần thử lại (tổng cộng 4 requests bao gồm request ban đầu)

**setMethods(HttpMethod.GET)**
- Định nghĩa các phương thức HTTP nào được hỗ trợ retry
- **Quan trọng**: Chỉ sử dụng retry cho các thao tác idempotent (GET, DELETE)
- Tránh POST, PATCH, PUT để ngăn các tác động phụ

**setBackoff(firstBackoff, maxBackoff, factor, basedOnPreviousValue)**
- `firstBackoff` (100ms): Thời gian chờ ban đầu trước lần thử lại đầu tiên
- `maxBackoff` (1000ms): Thời gian chờ tối đa giữa các lần thử lại
- `factor` (2): Hệ số nhân áp dụng cho thời gian backoff
- `basedOnPreviousValue` (true): Áp dụng hệ số cho backoff trước đó (exponential backoff)

### 2. Hiểu Về Chiến Lược Backoff

Cấu hình backoff triển khai exponential backoff:

- **Lần thử lại 1**: Chờ 100ms
- **Lần thử lại 2**: Chờ 200ms (100ms × 2)
- **Lần thử lại 3**: Chờ 400ms (200ms × 2)
- **Chờ tối đa**: Giới hạn ở 1000ms bất kể phép tính

Điều này ngăn thời gian chờ quá lớn khi cấu hình số lần thử lại cao hơn.

### 3. Kiểm Tra Triển Khai

#### Thêm Logging vào Microservice

Trong `LoansController` hoặc microservice đích:

```java
@GetMapping("/contact-info")
public ResponseEntity<ContactInfoDto> getContactInfo() {
    logger.debug("Invoked loans contact-info API");
    // Logic nghiệp vụ của bạn
    return ResponseEntity.ok(contactInfo);
}
```

#### Kịch Bản Kiểm Tra 1: Timeout Exception

1. Đặt breakpoint trong endpoint của microservice
2. Gửi request qua Gateway
3. Giữ breakpoint để mô phỏng timeout
4. Quan sát Gateway timeout sau ~9 giây (4 requests × ~2 giây timeout)

#### Kịch Bản Kiểm Tra 2: Runtime Exception

Tạm thời throw exception để kiểm tra hành vi retry:

```java
@GetMapping("/contact-info")
public ResponseEntity<ContactInfoDto> getContactInfo() {
    logger.debug("Invoked loans contact-info API");
    throw new RuntimeException("Lỗi mô phỏng");
    // return ResponseEntity.ok(contactInfo);
}
```

Kết quả mong đợi:
- Console hiển thị 4 log entries (1 lần đầu + 3 lần thử lại)
- Gateway trả về 500 Internal Server Error sau khi hết lần thử lại

### 4. Các Bước Triển Khai

Sau khi thay đổi cấu hình:

1. Dừng Loans microservice
2. Dừng Gateway Server
3. Rebuild cả hai ứng dụng
4. Khởi động Loans microservice trước
5. Khởi động Gateway Server

## Best Practices (Thực Hành Tốt)

### Khi Nào Sử Dụng Retry Pattern

✅ **Nên dùng cho:**
- GET requests (thao tác đọc)
- Các thao tác idempotent
- Lỗi mạng tạm thời
- Dịch vụ tạm thời không khả dụng

❌ **Tránh dùng cho:**
- POST requests (tạo tài nguyên)
- PATCH/PUT requests (cập nhật)
- DELETE requests (nếu không chắc về điều kiện query)
- Các thao tác có tác động phụ

### Các Cân Nhắc Khi Cấu Hình

1. **Số Lần Thử Lại**: Cân bằng giữa khả năng phục hồi và thời gian phản hồi
2. **Cài Đặt Timeout**: Đảm bảo timeout toàn cục phù hợp với số lần thử lại
3. **Chiến Lược Backoff**: Ngăn việc quá tải các dịch vụ downstream
4. **Phương Thức HTTP**: Chỉ bật cho các thao tác idempotent

## Lợi Ích

- **Chịu Lỗi**: Tự động phục hồi từ các lỗi tạm thời
- **Không Cần Can Thiệp Thủ Công**: Gateway xử lý retry tự động
- **Khả Năng Phục Hồi Mạng**: Giảm thiểu các vấn đề mạng tạm thời
- **Trải Nghiệm Người Dùng Tốt Hơn**: Giảm các request thất bại do vấn đề tạm thời

## Ví Dụ Cấu Hình Hoàn Chỉnh

```java
@Bean
public RouteLocator routeConfig(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("loans_route", r -> r
            .path("/eazybank/loans/**")
            .filters(f -> f
                .rewritePath("/eazybank/loans/(?<segment>.*)", "/${segment}")
                .addResponseHeader("X-Response-Time", LocalDateTime.now().toString())
                .retry(retryConfig -> retryConfig
                    .setRetries(3)
                    .setMethods(HttpMethod.GET)
                    .setBackoff(100, 1000, 2, true)
                )
            )
            .uri("lb://LOANS")
        )
        .build();
}
```

## Xác Minh

Theo dõi logs ứng dụng để xác minh hành vi retry:

```
Invoked loans contact-info API
Invoked loans contact-info API
Invoked loans contact-info API
Invoked loans contact-info API
```

Bốn log entries xác nhận: 1 request ban đầu + 3 lần thử lại.

## Kết Luận

Retry pattern trong Spring Cloud Gateway cung cấp khả năng chịu lỗi tự động cho microservices. Bằng cách cấu hình số lần thử lại phù hợp, chiến lược backoff, và chỉ áp dụng cho các thao tác idempotent, bạn có thể cải thiện đáng kể độ tin cậy của dịch vụ mà không cần can thiệp thủ công.

## Điểm Chính Cần Nhớ

- Retry pattern giúp phục hồi từ các lỗi tạm thời
- Chỉ cấu hình retry cho các phương thức HTTP idempotent
- Sử dụng exponential backoff để tránh quá tải dịch vụ
- Gateway xử lý retry một cách minh bạch
- Kết hợp với circuit breaker để có khả năng phục hồi toàn diện

## Thuật Ngữ Kỹ Thuật

- **Retry Pattern**: Mẫu thử lại - chiến lược tự động thử lại các thao tác thất bại
- **Idempotent**: Tính idempotent - thao tác có thể thực hiện nhiều lần mà không gây tác động phụ
- **Backoff**: Thời gian chờ giữa các lần thử lại
- **Exponential Backoff**: Thời gian chờ tăng theo cấp số nhân
- **Transient Failure**: Lỗi tạm thời - lỗi ngắn hạn có thể tự phục hồi
- **Fault Tolerance**: Khả năng chịu lỗi - khả năng hoạt động khi có lỗi xảy ra