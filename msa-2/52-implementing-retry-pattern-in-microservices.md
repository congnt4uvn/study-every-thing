# Triển Khai Retry Pattern Trong Microservices Với Resilience4j

## Tổng Quan

Hướng dẫn này trình bày cách triển khai retry pattern (mẫu thử lại) trong từng microservice riêng lẻ sử dụng Resilience4j và Spring Boot, thay vì triển khai logic retry tại tầng Gateway Server. Retry pattern giúp cải thiện khả năng phục hồi của microservices bằng cách tự động thử lại các thao tác thất bại trước khi từ bỏ.

## So Sánh: Retry Tại Gateway vs Microservice

| Khía Cạnh | Retry Tại Gateway Server | Retry Tại Microservice |
|-----------|--------------------------|------------------------|
| **Số Lần Thử Lại** | 4 lần thử (bao gồm request ban đầu) | 3 lần thử (có thể cấu hình, không tính request ban đầu) |
| **Hỗ Trợ Fallback** | Hạn chế/Không có | Hỗ trợ đầy đủ cơ chế fallback |
| **Phạm Vi Cấu Hình** | Áp dụng ở tầng gateway | Áp dụng ở từng service riêng lẻ |
| **Độ Chi Tiết** | Kiểm soát ít đối với các endpoint cụ thể | Kiểm soát chi tiết từng phương thức |

## Các Bước Triển Khai

### 1. Thêm Annotation @Retry

Để triển khai retry pattern trong microservice, thêm annotation `@Retry` vào phương thức mục tiêu:

```java
@Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
public ResponseEntity<String> getBuildInfo() {
    // Nội dung phương thức
}
```

**Tham Số Quan Trọng:**
- `name`: Định danh duy nhất cho cấu hình retry này (ví dụ: tên phương thức)
- `fallbackMethod`: Tên phương thức fallback sẽ thực thi sau khi tất cả retry thất bại

### 2. Tạo Phương Thức Fallback

Phương thức fallback phải tuân theo các quy tắc cụ thể:

#### Quy Tắc 1: Khớp Signature Của Phương Thức
Signature của phương thức fallback phải khớp chính xác với phương thức gốc (cùng kiểu trả về).

#### Quy Tắc 2: Thêm Tham Số Throwable
Phương thức fallback phải chấp nhận thêm một tham số kiểu `Throwable` ở cuối.

**Ví Dụ:**
```java
// Phương thức gốc (không có tham số)
public ResponseEntity<String> getBuildInfo() {
    logger.debug("getBuildInfo method invoked");
    throw new NullPointerException(); // Mô phỏng lỗi
    // return ResponseEntity.ok(buildVersion);
}

// Phương thức fallback
public ResponseEntity<String> getBuildInfoFallback(Throwable throwable) {
    logger.debug("getBuildInfoFallback method invoked");
    return ResponseEntity.ok("0.9"); // Giá trị trả về mặc định
}
```

**Lưu Ý:** Nếu phương thức gốc có 2 tham số, phương thức fallback sẽ có 3 tham số (2 từ gốc + 1 Throwable).

### 3. Cấu Hình Properties Cho Retry

Thêm cấu hình retry trong file `application.yml`:

```yaml
resilience4j:
  retry:
    configs:
      default:
        maxAttempts: 3
        waitDuration: 100ms
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2
```

**Các Thuộc Tính Cấu Hình:**
- `maxAttempts`: Số lần thử lại tối đa (mặc định: 3)
- `waitDuration`: Thời gian chờ ban đầu giữa các lần thử (100ms)
- `enableExponentialBackoff`: Bật chiến lược exponential backoff
- `exponentialBackoffMultiplier`: Hệ số nhân backoff (2x)

#### Cấu Hình Cụ Thể Cho Từng Instance

Để có hành vi retry khác nhau cho từng phương thức:

```yaml
resilience4j:
  retry:
    configs:
      default:
        maxAttempts: 3
        waitDuration: 100ms
    instances:
      getBuildInfo:
        maxAttempts: 5
        waitDuration: 200ms
      backendA:
        maxAttempts: 4
        waitDuration: 150ms
      backendB:
        maxAttempts: 3
        waitDuration: 100ms
```

### 4. Thêm Logger Statements

Để theo dõi các lần thử lại, thêm logging:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AccountsController {
    private static final Logger logger = LoggerFactory.getLogger(AccountsController.class);
    
    @Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
    public ResponseEntity<String> getBuildInfo() {
        logger.debug("getBuildInfo method invoked");
        throw new NullPointerException(); // Mô phỏng lỗi
    }
    
    public ResponseEntity<String> getBuildInfoFallback(Throwable throwable) {
        logger.debug("getBuildInfoFallback method invoked");
        return ResponseEntity.ok("0.9");
    }
}
```

### 5. Kiểm Tra Triển Khai

**Kết Quả Console Mong Đợi:**
```
getBuildInfo method invoked
getBuildInfo method invoked
getBuildInfo method invoked
getBuildInfoFallback method invoked
```

Điều này xác nhận có 3 lần thử lại tiếp theo là thực thi fallback.

## Tương Tác Giữa Circuit Breaker và Retry

### Cấu Hình Time Limiter

Khi sử dụng cả Circuit Breaker và Retry pattern, bạn cần xem xét cấu hình Time Limiter:

**Vấn Đề:** Timeout mặc định của Circuit Breaker (1 giây) có thể nhỏ hơn tổng thời gian retry, khiến fallback của Circuit Breaker kích hoạt thay vì fallback của Retry.

**Giải Pháp:** Cấu hình Time Limiter của Circuit Breaker để phù hợp với thao tác retry.

### Cấu Hình Time Limiter Trong Gateway Server

```java
@Configuration
public class GatewayConfig {
    
    @Bean
    public Customizer<ReactiveResilience4JCircuitBreakerFactory> defaultCustomizer() {
        return factory -> factory.configureDefault(id -> new Resilience4JConfigBuilder(id)
            .circuitBreakerConfig(CircuitBreakerConfig.ofDefaults())
            .timeLimiterConfig(TimeLimiterConfig.custom()
                .timeoutDuration(Duration.ofSeconds(4))
                .build())
            .build());
    }
}
```

**Điểm Quan Trọng:**
- Time Limiter xác định thời gian chờ tối đa cho một thao tác
- Timeout mặc định: ~1 giây
- Khuyến nghị cho retry: 4+ giây
- Ngăn Circuit Breaker kích hoạt sớm trong quá trình retry

### Điều Chỉnh Wait Duration Của Retry

**Kịch Bản 1:** Giảm thời gian chờ retry
```yaml
resilience4j:
  retry:
    configs:
      default:
        waitDuration: 100ms  # Retry nhanh hơn
```

**Kịch Bản 2:** Tăng timeout của Circuit Breaker
```java
.timeLimiterConfig(TimeLimiterConfig.custom()
    .timeoutDuration(Duration.ofSeconds(4))
    .build())
```

## Best Practices (Thực Hành Tốt Nhất)

### 1. Chọn Số Lần Retry Phù Hợp
- Bắt đầu với 3 lần thử cho hầu hết các trường hợp
- Điều chỉnh dựa trên yêu cầu SLA và đặc điểm của downstream service

### 2. Triển Khai Exponential Backoff
- Ngăn không làm quá tải downstream services
- Tăng thời gian chờ dần dần (100ms, 200ms, 400ms...)

### 3. Luôn Cung Cấp Fallback Methods
- Trả về giá trị mặc định/cached
- Trả về response lỗi nhã nhặn
- Log lỗi để theo dõi

### 4. Xem Xét Tổng Timeout
- Timeout Circuit Breaker > (số lần retry × thời gian chờ)
- Ví dụ: 4 giây > (3 × 500ms với backoff)

### 5. Giám Sát và Log
- Theo dõi số lần thử lại
- Log các lần gọi fallback
- Giám sát mẫu lỗi

### 6. Khởi Động Lại Services Sau Khi Thay Đổi Cấu Hình
- Khởi động lại microservice sau khi thay đổi config
- Khởi động lại Gateway Server để làm mới Eureka service registry
- Đảm bảo Gateway có thông tin instance service mới nhất

## Quy Trình Kiểm Tra

1. **Thực hiện thay đổi cấu hình** trong `application.yml`
2. **Build ứng dụng** (Maven/Gradle)
3. **Dừng AccountsApplication**
4. **Dừng Gateway Server**
5. **Khởi động AccountsApplication** ở chế độ debug
6. **Khởi động Gateway Server**
7. **Kiểm tra với Postman** hoặc REST client
8. **Xác minh console logs** cho các lần retry

## Tài Liệu Tham Khảo

Để biết thêm chi tiết về cấu hình Resilience4j:
- [Tài Liệu Chính Thức Resilience4j](https://resilience4j.readme.io/)
- Phần Getting Started > Configurations
- Cấu hình cụ thể cho Retry pattern
- Cấu hình Circuit Breaker

## Tóm Tắt

Triển khai retry pattern trong từng microservice riêng lẻ mang lại nhiều lợi ích:
- **Hỗ Trợ Fallback**: Khác với retry ở tầng Gateway, retry tại microservice hỗ trợ cơ chế fallback
- **Kiểm Soát Chi Tiết**: Cấu hình hành vi retry cho từng phương thức/endpoint
- **Khả Năng Phục Hồi Tốt Hơn**: Kết hợp với Circuit Breaker cho khả năng chịu lỗi toàn diện
- **Giám Sát**: Dễ dàng theo dõi và debug hành vi retry ở tầng service

Retry pattern, kết hợp với cấu hình Circuit Breaker và Time Limiter phù hợp, cải thiện đáng kể khả năng phục hồi của microservice và mang lại trải nghiệm người dùng tốt hơn trong các lỗi dịch vụ tạm thời.

---

## Chủ Đề Liên Quan
- Triển Khai Circuit Breaker Pattern
- Service Discovery Với Eureka
- Cấu Hình Spring Cloud Gateway
- Các Pattern Resilience4j Trong Microservices