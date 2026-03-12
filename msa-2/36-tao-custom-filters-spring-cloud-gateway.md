# Tạo Custom Filters trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách tạo các custom filter trong Spring Cloud Gateway để triển khai tính năng truy vết request sử dụng correlation ID xuyên suốt các microservices.

## Kịch Bản Nghiệp Vụ

Khi Gateway server nhận các request từ bên ngoài, chúng ta muốn:
1. Tạo một correlation ID duy nhất cho mỗi request
2. Truyền cùng một correlation ID đến tất cả các microservices phía sau (accounts, loans, cards, v.v.)
3. Thêm các câu lệnh logger trong microservices sử dụng correlation ID
4. Bao gồm correlation ID trong response header để client có thể khắc phục sự cố

Cách tiếp cận này cho phép các developer truy vết request qua nhiều microservices và nhanh chóng xác định vị trí xảy ra vấn đề.

## Các Bước Triển Khai

### 1. Tạo Package Filter

Tạo cấu trúc package mới:
```
com.eazybytes.gatewayserver.filters
```

### 2. Tạo Ba Class Filter

#### RequestTraceFilter
Chịu trách nhiệm tạo và thiết lập correlation ID khi một request mới đến Gateway server.

**Tính Năng Chính:**
- Sử dụng annotation `@Component` để đăng ký làm Spring bean
- Sử dụng `@Order(1)` để đảm bảo thứ tự ưu tiên thực thi
- Implement interface `GlobalFilter` để xử lý tất cả traffic đến
- Tạo correlation ID sử dụng `UUID.randomUUID()`
- Kiểm tra xem correlation ID đã tồn tại chưa (tránh ghi đè trong trường hợp redirect)

**Cấu Trúc Code:**
```java
@Component
@Order(1)
public class RequestTraceFilter implements GlobalFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        HttpHeaders requestHeaders = exchange.getRequest().getHeaders();
        
        if (isCorrelationIdPresent(requestHeaders)) {
            logger.debug("eazybank-correlation-id found in RequestTraceFilter");
        } else {
            String correlationId = generateCorrelationId();
            exchange = setCorrelationId(exchange, correlationId);
            logger.debug("eazybank-correlation-id generated in RequestTraceFilter");
        }
        
        return chain.filter(exchange);
    }
}
```

#### ResponseTraceFilter
Thêm correlation ID vào response headers trước khi gửi lại cho client.

**Tính Năng Chính:**
- Sử dụng annotation `@Configuration`
- Tạo bean `GlobalFilter` thông qua cấu hình method
- Hoạt động như một post-filter sử dụng method `.then()`
- Trích xuất correlation ID từ request headers
- Thêm correlation ID vào response headers

**Cấu Trúc Code:**
```java
@Configuration
public class ResponseTraceFilter {
    
    @Bean
    public GlobalFilter postGlobalFilter() {
        return (exchange, chain) -> {
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                String correlationId = getCorrelationId(exchange.getRequest().getHeaders());
                exchange.getResponse().getHeaders().add(CORRELATION_ID, correlationId);
                logger.debug("Updated the correlation id to the outbound headers");
            }));
        };
    }
}
```

#### FilterUtility
Chứa các phương thức tiện ích chung được chia sẻ giữa request và response filters.

**Các Phương Thức:**
- `getCorrelationId()` - Lấy correlation ID từ request headers
- `setCorrelationId()` - Thiết lập correlation ID trong request headers
- `isCorrelationIdPresent()` - Kiểm tra xem correlation ID có tồn tại không

**Tên Header:**
```
eazybank-correlation-id
```

### 3. Hiểu Về Kiến Trúc Spring Cloud Gateway

**Lưu Ý Quan Trọng:**
- Spring Cloud Gateway được xây dựng trên **Spring Reactive** (không phải Servlet API truyền thống)
- Sử dụng `ServerWebExchange` thay vì HttpServletRequest/Response
- Sử dụng `Mono` và `Flux` cho lập trình reactive
  - `Mono<Void>` - Đại diện cho một response trống duy nhất
  - `Mono` - Đối tượng đơn
  - `Flux` - Tập hợp các đối tượng

### 4. Thực Thi Filter Chain

Các filter trong Gateway thực thi theo chuỗi:
1. Custom filters thực thi theo thứ tự (sử dụng annotation `@Order`)
2. Mỗi filter phải gọi `chain.filter(exchange)` để tiếp tục đến filter tiếp theo
3. Post-filters sử dụng method `.then()` để thực thi sau khi nhận được response

### 5. Kích Hoạt Debug Logging

Thêm cấu hình vào `application.yml`:

```yaml
logging:
  level:
    com.easybytes.gatewayserver: DEBUG
```

Cấu hình này kích hoạt tất cả các câu lệnh logger debug trong package gateway server.

## Các Bước Tiếp Theo

Sau khi triển khai Gateway filters, bạn cần:
1. Cập nhật các microservices riêng lẻ để chấp nhận correlation ID header
2. Đọc giá trị correlation ID trong microservices
3. Thêm các câu lệnh logger trong business logic sử dụng correlation ID

## Luồng Correlation ID

```
Request Bên Ngoài → Gateway Server (Tạo Correlation ID)
                        ↓
                Thêm vào Request Header
                        ↓
            Chuyển tiếp đến Microservice (Accounts)
                        ↓
        Chuyển tiếp đến Microservice (Loans/Cards)
                        ↓
                  Xử Lý Request
                        ↓
            Trả Response về Gateway
                        ↓
        Thêm Correlation ID vào Response Header
                        ↓
            Trả về Client Bên Ngoài
```

## Lợi Ích

1. **Truy Vết Request** - Theo dõi requests qua nhiều microservices
2. **Gỡ Lỗi** - Nhanh chóng xác định nơi xảy ra vấn đề sử dụng correlation ID
3. **Phân Tích Log** - Tìm kiếm logs xuyên suốt các services sử dụng một correlation ID duy nhất
4. **Hỗ Trợ Client** - Client có thể cung cấp correlation ID để khắc phục sự cố

## Điểm Chính Cần Nhớ

- Sử dụng `GlobalFilter` cho các filter áp dụng cho tất cả traffic
- Sử dụng `@Order` để kiểm soát thứ tự thực thi filter
- Spring Cloud Gateway sử dụng mô hình lập trình reactive
- Correlation IDs cho phép distributed tracing
- Cả request và response đều có thể mang correlation ID
- Ngăn chặn việc tạo correlation ID trùng lặp trong quá trình redirections