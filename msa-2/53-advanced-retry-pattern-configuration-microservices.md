# Cấu Hình Nâng Cao Retry Pattern Trong Microservices

## Tổng Quan

Hướng dẫn này trình bày các tùy chọn cấu hình nâng cao để triển khai retry pattern trong microservices Spring Boot, bao gồm xử lý ngoại lệ, tích hợp với Spring Cloud Gateway và các phương pháp tốt nhất cho triển khai production.

## Bỏ Qua Các Ngoại Lệ Cụ Thể

### Yêu Cầu Nghiệp Vụ

Trong một số trường hợp, việc retry một số ngoại lệ nhất định là không có ý nghĩa. Ví dụ, nếu `NullPointerException` xảy ra do dữ liệu đầu vào không hợp lệ, việc retry cùng một thao tác sẽ luôn dẫn đến cùng một ngoại lệ.

### Cấu Hình

Để cấu hình các ngoại lệ không nên kích hoạt retry, thêm thuộc tính `ignoreExceptions` vào file `application.yml`:

```yaml
resilience4j:
  retry:
    instances:
      your-retry-name:
        ignoreExceptions:
          - java.lang.NullPointerException
          - java.lang.IllegalArgumentException
```

**Lưu ý:** Bạn có thể thêm nhiều ngoại lệ bằng cách liệt kê chúng với dấu gạch ngang trong định dạng YAML.

### Ví Dụ Triển Khai

```java
@GetMapping("/build-info")
@Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
public ResponseEntity<String> getBuildInfo() throws TimeoutException {
    // Triển khai method
    throw new NullPointerException("Ngoại lệ mẫu");
}
```

Khi `NullPointerException` nằm trong danh sách bỏ qua, cơ chế retry sẽ bỏ qua các lần thử lại và ngay lập tức gọi phương thức fallback.

## Chỉ Retry Các Ngoại Lệ Cụ Thể

### Cấu Hình

Thay vì bỏ qua ngoại lệ, bạn có thể định nghĩa rõ ràng những ngoại lệ nào nên kích hoạt retry:

```yaml
resilience4j:
  retry:
    instances:
      your-retry-name:
        retryExceptions:
          - java.util.concurrent.TimeoutException
          - java.io.IOException
```

**Quan trọng:** Khi sử dụng `retryExceptions`, bạn không cần định nghĩa `ignoreExceptions`. Tất cả các ngoại lệ không được liệt kê trong `retryExceptions` sẽ tự động bị bỏ qua bởi Resilience4j.

### Ví Dụ Với TimeoutException

```java
@GetMapping("/build-info")
@Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
public ResponseEntity<String> getBuildInfo() throws TimeoutException {
    throw new TimeoutException("Thao tác hết thời gian chờ");
}
```

Vì `TimeoutException` là checked exception, nó phải được khai báo trong method signature với từ khóa `throws`.

## Retry Pattern Trong Spring Cloud Gateway

### Các Tùy Chọn Cấu Hình

Spring Cloud Gateway cung cấp khả năng cấu hình retry tương tự:

```java
// Trong cấu hình Gateway
.setExceptions(TimeoutException.class, IOException.class)
.setStatuses(HttpStatus.INTERNAL_SERVER_ERROR, HttpStatus.SERVICE_UNAVAILABLE)
```

### Sự Khác Biệt Chính

- **Không có tùy chọn bỏ qua ngoại lệ:** Gateway tập trung vào việc chỉ định cụ thể (retry cái gì)
- **Retry dựa trên HTTP status:** Bạn có thể cấu hình retry dựa trên mã trạng thái HTTP
- **Cấu hình dựa trên method:** Sử dụng các phương thức setter thay vì cấu hình YAML

## Sửa Lỗi Header Trùng Lặp Trong Gateway

### Vấn Đề

Khi triển khai retry pattern trong Gateway Server với custom filters, correlation ID header có thể xuất hiện nhiều lần trong response do response filter được thực thi ở mỗi lần retry.

### Giải Pháp

Sửa đổi `ResponseTraceFilter` để kiểm tra xem header đã tồn tại chưa:

```java
@Component
public class ResponseTraceFilter implements GlobalFilter, Ordered {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        return chain.filter(exchange).then(Mono.fromRunnable(() -> {
            ServerHttpResponse response = exchange.getResponse();
            
            // Kiểm tra header đã tồn tại trước khi thêm
            if (!response.getHeaders().containsKey(CORRELATION_ID_HEADER)) {
                String correlationId = exchange.getRequest()
                    .getHeaders()
                    .getFirst(CORRELATION_ID_HEADER);
                    
                response.getHeaders().add(CORRELATION_ID_HEADER, correlationId);
            }
        }));
    }
}
```

### Giải Thích Logic

- **Nếu header tồn tại:** `containsKey()` trả về `true`, phép phủ định làm nó thành `false`, khối if không thực thi
- **Nếu header không tồn tại:** `containsKey()` trả về `false`, phép phủ định làm nó thành `true`, header được thêm vào

## Các Bước Cấu Hình Hoàn Chỉnh

### 1. Thêm Retry Annotation

```java
@Retry(name = "retryPatternName", fallbackMethod = "fallbackMethodName")
```

### 2. Tạo Fallback Method

```java
public ResponseEntity<String> fallbackMethodName(Exception ex) {
    return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
        .body("Phản hồi dự phòng do: " + ex.getMessage());
}
```

### 3. Cấu Hình application.yml

```yaml
resilience4j:
  retry:
    instances:
      retryPatternName:
        maxAttempts: 3
        waitDuration: 500ms
        retryExceptions:
          - java.util.concurrent.TimeoutException
        ignoreExceptions:
          - java.lang.NullPointerException
```

## Kiểm Thử Và Xác Minh

### Xác Minh Đầu Ra Console

Sau khi cấu hình thành công, bạn sẽ thấy các log statements cho biết:

1. Lần gọi method ban đầu
2. Các lần thử retry (nếu có)
3. Lần gọi fallback method (nếu tất cả retry đều thất bại)

### Ví Dụ Đầu Ra Console

```
getBuildInfo() method invoked - Attempt 1
getBuildInfo() method invoked - Attempt 2
getBuildInfo() method invoked - Attempt 3
getBuildInfoFallback() method invoked
```

## Các Phương Pháp Tốt Nhất

1. **Chọn ngoại lệ một cách khôn ngoan:** Chỉ retry các lỗi tạm thời (timeout, lỗi mạng)
2. **Tránh retry các ngoại lệ nghiệp vụ:** Lỗi logic sẽ không được giải quyết bằng retry
3. **Sử dụng thời gian chờ phù hợp:** Cân bằng giữa khả năng phản hồi và tải hệ thống
4. **Triển khai cơ chế fallback phù hợp:** Luôn cung cấp sự suy giảm graceful
5. **Giám sát các metrics retry:** Theo dõi số lần retry và tỷ lệ thành công

## Tóm Tắt

Retry pattern trong microservices nên được cấu hình cẩn thận để xử lý các lỗi tạm thời trong khi tránh các lần retry không cần thiết. Bằng cách cấu hình đúng `retryExceptions` và `ignoreExceptions`, bạn có thể tạo ra các microservices có khả năng phục hồi cao, xử lý lỗi một cách graceful và hiệu quả.

---

**Các Chủ Đề Liên Quan:**
- Circuit Breaker Pattern
- Cơ Chế Fallback
- Cấu Hình Resilience4j
- Spring Cloud Gateway Filters