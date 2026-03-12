# Triển Khai Pattern RateLimiter Trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách triển khai pattern RateLimiter trong microservices Spring Boot sử dụng Resilience4j. Khác với việc triển khai RateLimiter trong gateway server, cách tiếp cận này áp dụng giới hạn tốc độ trực tiếp trong từng microservice riêng lẻ.

## Yêu Cầu Trước

- Microservice Spring Boot (ví dụ: Accounts microservice)
- Thư viện Resilience4j
- Hiểu biết cơ bản về annotations trong Spring Boot

## Các Bước Triển Khai

### 1. Thêm Annotation RateLimiter

Đầu tiên, đánh dấu method cần giới hạn tốc độ với `@RateLimiter`:

```java
@RateLimiter(name = "getJavaVersion")
public String getJavaVersion() {
    // Phần thực thi method
}
```

Tham số `name` xác định cấu hình rate limiter cụ thể sẽ được sử dụng.

### 2. Cấu Hình Thuộc Tính RateLimiter

Thêm cấu hình sau vào file `application.yml`:

```yaml
resilience4j:
  ratelimiter:
    configs:
      default:
        limitRefreshPeriod: 5000  # 5 giây
        limitForPeriod: 1         # 1 request mỗi chu kỳ
        timeoutDuration: 1000     # Thời gian chờ 1 giây
```

### Giải Thích Các Thuộc Tính Cấu Hình

- **limitRefreshPeriod**: Chu kỳ sau đó rate limiter làm mới quota của nó (5000ms = 5 giây)
- **limitForPeriod**: Số lượng request được phép trong mỗi chu kỳ làm mới (1 request trong 5 giây trong ví dụ này)
- **timeoutDuration**: Thời gian tối đa một thread sẽ đợi để được phép thực thi (1000ms = 1 giây)

## Cách Hoạt Động

1. Khi một request đến, RateLimiter kiểm tra xem quota cho chu kỳ hiện tại có sẵn không
2. Nếu quota đã hết, thread sẽ đợi tối đa `timeoutDuration` cho chu kỳ làm mới tiếp theo
3. Nếu không được cấp phép trong khoảng timeout, một exception sẽ được throw ra
4. Mỗi `limitRefreshPeriod`, quota sẽ được làm mới

## Kiểm Tra Triển Khai

1. Khởi động ứng dụng microservice của bạn
2. Thực hiện nhiều request liên tiếp đến endpoint có rate limit
3. Sau khi vượt quá giới hạn, bạn sẽ nhận được lỗi: "RateLimiter does not permit further calls"

## Triển Khai Cơ Chế Fallback

### Thêm Method Fallback

Để xử lý exceptions về giới hạn tốc độ một cách mượt mà, thêm method fallback:

```java
@RateLimiter(name = "getJavaVersion", fallbackMethod = "getJavaVersionFallback")
public String getJavaVersion() {
    // Phần thực thi method gốc
}

public String getJavaVersionFallback(Throwable throwable) {
    return "Java 17"; // Phản hồi dự phòng
}
```

### Yêu Cầu Cho Method Fallback

- Phải có cùng signature với method gốc
- Phải bao gồm thêm tham số `Throwable`
- Có thể trả về dữ liệu từ cache, giá trị mặc định, hoặc thông báo thân thiện với người dùng

## Các Trường Hợp Sử Dụng

### Bảo Vệ Năng Lực Hạ Tầng
Nếu hạ tầng của bạn chỉ có thể xử lý 10,000 requests mỗi giây, sử dụng RateLimiter để ngăn quá tải.

### Phân Bổ Tài Nguyên Dựa Trên Độ Ưu Tiên
Áp dụng giới hạn tốc độ nghiêm ngặt hơn cho các API ưu tiên thấp, đảm bảo các API ưu tiên cao có đủ tài nguyên.

### Quản Lý Quota Tùy Chỉnh
Triển khai các giới hạn tốc độ khác nhau cho các method khác nhau dựa trên yêu cầu nghiệp vụ.

## So Sánh Với Rate Limiting Ở Tầng Gateway

### Cách Tiếp Cận Gateway Server
- Sử dụng Redis và KeyResolver
- Có thể áp dụng quota dựa trên user, địa chỉ IP, hoặc các tiêu chí khác
- Rate limiting tập trung

### Cách Tiếp Cận Tầng Microservice
- Áp dụng trực tiếp trong microservice
- Rate limiting đồng nhất cho tất cả requests đến
- Cấu hình đơn giản hơn, không cần dependencies bên ngoài (như Redis)

## Cân Nhắc Cho Môi Trường Production

- Trong production, `limitForPeriod` thường sẽ ở mức hàng nghìn
- Chọn các giá trị phù hợp dựa trên năng lực hạ tầng của bạn
- Giám sát các metrics về rate limiting để điều chỉnh cấu hình
- Cân nhắc triển khai các chiến lược fallback toàn diện

## Tổng Kết

Pattern RateLimiter trong microservices cung cấp khả năng kiểm soát chi tiết việc xử lý request:
- Bảo vệ hạ tầng khỏi quá tải
- Cho phép phân bổ tài nguyên dựa trên độ ưu tiên
- Hoạt động độc lập không cần gateway server
- Hỗ trợ cơ chế fallback cho việc giảm tải một cách mượt mà

Bây giờ bạn có hai cách tiếp cận để triển khai rate limiting:
1. **Gateway Server**: Sử dụng Spring Cloud Gateway với Redis
2. **Tầng Microservice**: Sử dụng annotations của Resilience4j

Chọn cách tiếp cận phù hợp nhất với yêu cầu nghiệp vụ và kiến trúc của bạn.